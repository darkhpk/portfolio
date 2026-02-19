#ifndef CSVPARSER_H
#define CSVPARSER_H

#include <QObject>
#include <QString>
#include <QVector>
#include <QMap>
#include "Document.h"

class CSVParser : public QObject {
    Q_OBJECT

public:
    explicit CSVParser(QObject *parent = nullptr);
    ~CSVParser();
    
    bool parseCSV(const QString &filePath);
    QVector<QString> getHeaders() const { return headers; }
    QVector<QMap<QString, QString>> getMetadata() const { return metadataRecords; }
    QMap<QString, QString> getMetadataForFile(const QString &fileName);
    
signals:
    void logMessage(const QString &message);
    
private:
    QVector<QString> headers;
    QVector<QMap<QString, QString>> metadataRecords;
    QVector<QString> parseLine(const QString &line);
};

#endif // CSVPARSER_H
