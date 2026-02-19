#ifndef DOCUMENT_H
#define DOCUMENT_H

#include <QString>
#include <QMap>

struct Document {
    QString filePath;
    QString docID;
    int pageCount;
    int startBatesNumber;
    int endBatesNumber;
    QMap<QString, QString> metadata;  // Additional metadata from CSV
    QString volumeName;
    int volumeNumber;
    QString outputFileName;  // Final filename in volume folder
    
    Document() 
        : pageCount(0), startBatesNumber(0), endBatesNumber(0), volumeNumber(0) {}
};

#endif // DOCUMENT_H
