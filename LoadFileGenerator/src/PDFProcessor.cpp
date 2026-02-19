#include "PDFProcessor.h"
#include <QRunnable>
#include <QMutex>
#include <QThread>
#include <QFileInfo>
#include <podofo/podofo.h>

class PDFPageCountTask : public QRunnable {
public:
    PDFPageCountTask(Document *doc, QMutex *mutex, int *processed, int total, PDFProcessor *processor)
        : document(doc), mutex(mutex), processedCount(processed), totalCount(total), pdfProcessor(processor)
    {}
    
    void run() override {
        try {
            // Use PoDoFo 1.x API to count pages
            PoDoFo::PdfMemDocument pdf;
            pdf.Load(document->filePath.toStdString());
            document->pageCount = pdf.GetPages().GetCount();
            
            QMutexLocker locker(mutex);
            (*processedCount)++;
            emit pdfProcessor->logMessage(QString("Processed: %1 (%2 pages)")
                .arg(QFileInfo(document->filePath).fileName())
                .arg(document->pageCount));
            emit pdfProcessor->progressUpdated(*processedCount, totalCount);
            
        } catch (const PoDoFo::PdfError &error) {
            QMutexLocker locker(mutex);
            emit pdfProcessor->logMessage(QString("Error processing %1: %2")
                .arg(document->filePath)
                .arg(error.what()));
            document->pageCount = 0;
        }
    }
    
private:
    Document *document;
    QMutex *mutex;
    int *processedCount;
    int totalCount;
    PDFProcessor *pdfProcessor;
};

PDFProcessor::PDFProcessor(QObject *parent)
    : QObject(parent)
    , threadPool(new QThreadPool(this))
{
    // Use optimal thread count for system
    threadPool->setMaxThreadCount(QThread::idealThreadCount());
}

PDFProcessor::~PDFProcessor() {
    threadPool->waitForDone();
}

void PDFProcessor::processDocuments(QVector<Document> &documents) {
    if (documents.isEmpty()) {
        emit processingComplete();
        return;
    }
    
    QMutex mutex;
    int processedCount = 0;
    int totalCount = documents.size();
    
    emit logMessage(QString("Using %1 threads for PDF processing...").arg(threadPool->maxThreadCount()));
    
    // Create tasks for each document
    for (int i = 0; i < documents.size(); ++i) {
        PDFPageCountTask *task = new PDFPageCountTask(&documents[i], &mutex, &processedCount, totalCount, this);
        task->setAutoDelete(true);
        threadPool->start(task);
    }
    
    // Wait for all tasks to complete
    threadPool->waitForDone();
    
    emit logMessage(QString("PDF processing complete. %1 documents processed.").arg(totalCount));
    emit processingComplete();
}

int PDFProcessor::getPageCount(const QString &pdfPath) {
    return countPDFPages(pdfPath);
}

int PDFProcessor::countPDFPages(const QString &filePath) {
    try {
        PoDoFo::PdfMemDocument pdf;
        pdf.Load(filePath.toStdString());
        return pdf.GetPages().GetCount();
    } catch (const PoDoFo::PdfError &error) {
        emit logMessage(QString("Error reading PDF %1: %2").arg(filePath).arg(error.what()));
        return 0;
    }
}
