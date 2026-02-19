#include "OPTGenerator.h"
#include <QFile>
#include <QTextStream>
#include <QFileInfo>
#include <QDir>

OPTGenerator::OPTGenerator(QObject *parent)
    : QObject(parent)
{
}

OPTGenerator::~OPTGenerator() {
}

bool OPTGenerator::generateOPT(const QString &outputPath, const QVector<Document> &documents) {
    QFile file(outputPath);
    if (!file.open(QIODevice::WriteOnly | QIODevice::Text)) {
        emit logMessage(QString("Failed to create OPT file: %1").arg(outputPath));
        return false;
    }
    
    QTextStream out(&file);
    out.setCodec("UTF-8");
    
    QDir outputDir = QFileInfo(outputPath).dir();
    
    // Generate OPT entries - one row per document
    for (const Document &doc : documents) {
        if (doc.pageCount == 0) {
            continue;
        }
        
        // Use outputFileName if set, otherwise use original filename
        QString fileName = doc.outputFileName.isEmpty() ? QFileInfo(doc.filePath).fileName() : doc.outputFileName;
        
        // Format: DOCID,Volume1,Volume1\filename.pdf,Y,,,PageCount
        QString pdfPath = QString("%1\\%2")
            .arg(doc.volumeName)
            .arg(fileName);
        
        out << doc.docID << ","
            << doc.volumeName << ","
            << pdfPath << ","
            << "Y,,,"
            << doc.pageCount << "\n";
    }
    
    file.close();
    emit logMessage(QString("OPT file created: %1 (%2 documents)").arg(outputPath).arg(documents.size()));
    return true;
}
