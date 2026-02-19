#include "CSVParser.h"
#include <QFile>
#include <QTextStream>
#include <QFileInfo>

CSVParser::CSVParser(QObject *parent)
    : QObject(parent)
{
}

CSVParser::~CSVParser() {
}

bool CSVParser::parseCSV(const QString &filePath) {
    QFile file(filePath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text)) {
        emit logMessage(QString("Failed to open CSV file: %1").arg(filePath));
        return false;
    }
    
    QTextStream in(&file);
    in.setCodec("UTF-8");  // Qt5 compatible
    headers.clear();
    metadataRecords.clear();
    
    bool isFirstLine = true;
    int lineNumber = 0;
    
    while (!in.atEnd()) {
        QString line = in.readLine().trimmed();
        lineNumber++;
        
        if (line.isEmpty()) {
            continue;
        }
        
        QVector<QString> fields = parseLine(line);
        
        if (isFirstLine) {
            headers = fields;
            isFirstLine = false;
            emit logMessage(QString("CSV Headers: %1").arg(QStringList::fromVector(headers).join(", ")));
        } else {
            if (fields.size() != headers.size()) {
                emit logMessage(QString("Warning: Line %1 has %2 fields, expected %3")
                    .arg(lineNumber).arg(fields.size()).arg(headers.size()));
                continue;
            }
            
            QMap<QString, QString> record;
            for (int i = 0; i < headers.size(); ++i) {
                record[headers[i]] = fields[i];
            }
            metadataRecords.append(record);
        }
    }
    
    file.close();
    emit logMessage(QString("Parsed %1 metadata records from CSV").arg(metadataRecords.size()));
    return true;
}

QMap<QString, QString> CSVParser::getMetadataForFile(const QString &fileName) {
    // Try to match by filename field in CSV
    for (const auto &record : metadataRecords) {
        if (record.contains("FileName") || record.contains("Filename") || record.contains("filename")) {
            QString csvFileName = record.value("FileName", record.value("Filename", record.value("filename")));
            if (csvFileName == fileName) {
                return record;
            }
        }
    }
    
    // If no match found, return first record or empty
    if (!metadataRecords.isEmpty()) {
        static int recordIndex = 0;
        if (recordIndex < metadataRecords.size()) {
            return metadataRecords[recordIndex++];
        }
    }
    
    return QMap<QString, QString>();
}

QVector<QString> CSVParser::parseLine(const QString &line) {
    QVector<QString> fields;
    QString currentField;
    bool inQuotes = false;
    
    for (int i = 0; i < line.length(); ++i) {
        QChar c = line[i];
        
        if (c == '"') {
            // Handle escaped quotes
            if (inQuotes && i + 1 < line.length() && line[i + 1] == '"') {
                currentField += '"';
                i++; // Skip next quote
            } else {
                inQuotes = !inQuotes;
            }
        } else if (c == ',' && !inQuotes) {
            fields.append(currentField.trimmed());
            currentField.clear();
        } else {
            currentField += c;
        }
    }
    
    // Add last field
    fields.append(currentField.trimmed());
    
    return fields;
}
