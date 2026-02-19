#ifndef PDFPROCESSOR_H
#define PDFPROCESSOR_H

#include <QObject>
#include <QString>
#include <QVector>
#include <QThreadPool>
#include "Document.h"

class PDFProcessor : public QObject {
    Q_OBJECT

public:
    explicit PDFProcessor(QObject *parent = nullptr);
    ~PDFProcessor();
    
    void processDocuments(QVector<Document> &documents);
    int getPageCount(const QString &pdfPath);
    
signals:
    void progressUpdated(int current, int total);
    void logMessage(const QString &message);
    void processingComplete();
    
private:
    QThreadPool *threadPool;
    int countPDFPages(const QString &filePath);
};

#endif // PDFPROCESSOR_H
