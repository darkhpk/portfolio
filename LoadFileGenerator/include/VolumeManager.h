#ifndef VOLUMEMANAGER_H
#define VOLUMEMANAGER_H

#include <QObject>
#include <QString>
#include <QVector>
#include "Document.h"

class VolumeManager : public QObject {
    Q_OBJECT

public:
    explicit VolumeManager(QObject *parent = nullptr);
    ~VolumeManager();
    
    void setDocumentsPerVolume(int count) { documentsPerVolume = count; }
    void setStartBatesNumber(int start) { startBatesNumber = start; }
    void setRenameWithDocID(bool rename) { renameWithDocID = rename; }
    void setVolumeFromCSVField(const QString &fieldName) { volumeCSVField = fieldName; useCSVField = !fieldName.isEmpty(); }
    
    void organizeIntoVolumes(QVector<Document> &documents);
    bool createOutputStructure(const QString &outputPath, const QVector<Document> &documents);
    
signals:
    void logMessage(const QString &message);
    
private:
    int documentsPerVolume;
    int startBatesNumber;
    bool renameWithDocID;
    bool useCSVField;
    QString volumeCSVField;
    QString formatBatesNumber(int number, int width = 7);
};

#endif // VOLUMEMANAGER_H
