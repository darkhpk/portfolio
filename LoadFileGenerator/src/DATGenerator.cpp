#include "DATGenerator.h"
#include <QFile>
#include <QTextStream>
#include <QFileInfo>
#include <QDir>

DATGenerator::DATGenerator(QObject *parent)
    : QObject(parent)
    , delimiter(0x14)  // ASCII 20 (Concordance standard)
    , textQualifier(0xFE)  // ASCII 254
{
}

DATGenerator::~DATGenerator() {
}

bool DATGenerator::generateDAT(const QString &outputPath, const QVector<Document> &documents,
                                const QVector<QString> &headers) {
    QFile file(outputPath);
    if (!file.open(QIODevice::WriteOnly | QIODevice::Text)) {
        emit logMessage(QString("Failed to create DAT file: %1").arg(outputPath));
        return false;
    }
    
    QTextStream out(&file);
    out.setCodec("UTF-8");  // Qt5 compatible
    
    // Build headers: DOCID + CSV headers
    QVector<QString> datHeaders;
    datHeaders << "DOCID";
    
    // Add all headers from CSV
    for (const QString &header : headers) {
        datHeaders.append(header);
    }
    
    // Write header row - each field enclosed in þ (ASCII 254)
    QStringList headerLine;
    for (const QString &header : datHeaders) {
        headerLine << (textQualifier + header + textQualifier);
    }
    out << headerLine.join(delimiter) << "\n";
    
    // Write data rows
    for (const Document &doc : documents) {
        QStringList dataLine;
        
        // Add DOCID
        dataLine << (textQualifier + doc.docID + textQualifier);
        
        // Add metadata fields from CSV in same order as headers
        for (int i = 1; i < datHeaders.size(); ++i) {
            QString value = doc.metadata.value(datHeaders[i], "");
            dataLine << (textQualifier + value + textQualifier);
        }
        
        out << dataLine.join(delimiter) << "\n";
    }
    
    file.close();
    emit logMessage(QString("DAT file created: %1 (%2 records)").arg(outputPath).arg(documents.size()));
    return true;
}

QString DATGenerator::escapeField(const QString &field) {
    // Always wrap field in text qualifiers (þ)
    // If field contains text qualifier, escape it by doubling
    QString escaped = field;
    escaped.replace(textQualifier, QString(textQualifier) + QString(textQualifier));
    return textQualifier + escaped + textQualifier;
}
