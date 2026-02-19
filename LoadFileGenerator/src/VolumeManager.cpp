#include "VolumeManager.h"
#include <QDir>
#include <QFileInfo>
#include <QSet>

VolumeManager::VolumeManager(QObject *parent)
    : QObject(parent)
    , documentsPerVolume(1000)
    , startBatesNumber(1)
    , renameWithDocID(false)
    , useCSVField(false)
    , volumeCSVField("")
{
}

VolumeManager::~VolumeManager() {
}

void VolumeManager::organizeIntoVolumes(QVector<Document> &documents) {
    if (documents.isEmpty()) {
        return;
    }
    
    int currentBatesNumber = startBatesNumber;
    
    if (useCSVField && !volumeCSVField.isEmpty()) {
        // Use CSV field to determine volumes
        QMap<QString, int> volumeNumbers;
        int nextVolumeNum = 1;
        
        for (Document &doc : documents) {
            // Get volume name from metadata
            QString volumeValue = doc.metadata.value(volumeCSVField, "").trimmed();
            
            if (volumeValue.isEmpty()) {
                volumeValue = "VOL001";
            }
            
            // Track volume numbers for consistency
            if (!volumeNumbers.contains(volumeValue)) {
                volumeNumbers[volumeValue] = nextVolumeNum++;
            }
            
            doc.volumeName = volumeValue;
            doc.volumeNumber = volumeNumbers[volumeValue];
            
            // Assign Bates numbers
            doc.startBatesNumber = currentBatesNumber;
            doc.endBatesNumber = currentBatesNumber + doc.pageCount - 1;
            currentBatesNumber += doc.pageCount;
        }
        
        emit logMessage(QString("Documents organized into %1 volume(s) by CSV field '%2'")
            .arg(volumeNumbers.size()).arg(volumeCSVField));
        
    } else {
        // Use document count method
        int currentVolume = 1;
        int docsInCurrentVolume = 0;
        
        for (Document &doc : documents) {
            // Check if we need a new volume
            if (docsInCurrentVolume >= documentsPerVolume) {
                currentVolume++;
                docsInCurrentVolume = 0;
            }
            
            // Assign volume information
            doc.volumeNumber = currentVolume;
            doc.volumeName = QString("VOL%1").arg(currentVolume, 3, 10, QChar('0'));
            
            // Assign Bates numbers
            doc.startBatesNumber = currentBatesNumber;
            doc.endBatesNumber = currentBatesNumber + doc.pageCount - 1;
            
            currentBatesNumber += doc.pageCount;
            docsInCurrentVolume++;
        }
        
        emit logMessage(QString("Documents organized into %1 volume(s)").arg(currentVolume));
    }
    
    emit logMessage(QString("Bates range: %1 - %2")
        .arg(formatBatesNumber(startBatesNumber))
        .arg(formatBatesNumber(currentBatesNumber - 1)));
}

bool VolumeManager::createOutputStructure(const QString &outputPath, const QVector<Document> &documents) {
    QDir outputDir(outputPath);
    
    if (!outputDir.exists()) {
        emit logMessage(QString("Creating output directory: %1").arg(outputPath));
        if (!outputDir.mkpath(".")) {
            emit logMessage("Error: Failed to create output directory");
            return false;
        }
    }
    
    // Create volume folders and copy PDF files
    QSet<QString> processedVolumes;
    
    for (const Document &doc : documents) {
        // Create volume folder if not already created
        if (!processedVolumes.contains(doc.volumeName)) {
            QString volumePath = outputDir.filePath(doc.volumeName);
            QDir volDir;
            if (!volDir.mkpath(volumePath)) {
                emit logMessage(QString("Error: Failed to create volume folder: %1").arg(volumePath));
                return false;
            }
            emit logMessage(QString("Created volume folder: %1").arg(volumePath));
            processedVolumes.insert(doc.volumeName);
        }
        
        // Copy PDF file to volume folder
        QFileInfo sourceInfo(doc.filePath);
        QString destFileName = renameWithDocID ? doc.docID + ".pdf" : sourceInfo.fileName();
        QString destPath = outputDir.filePath(doc.volumeName + "/" + destFileName);
        
        // Store the output filename in the document (need to modify const cast for this)
        const_cast<Document&>(doc).outputFileName = destFileName;
        
        // Remove destination file if it already exists
        if (QFile::exists(destPath)) {
            QFile::remove(destPath);
        }
        
        if (!QFile::copy(doc.filePath, destPath)) {
            emit logMessage(QString("Error: Failed to copy %1 to %2")
                .arg(sourceInfo.fileName()).arg(doc.volumeName));
            return false;
        }
        
        if (renameWithDocID) {
            emit logMessage(QString("Copied and renamed %1 to %2 as %3")
                .arg(sourceInfo.fileName()).arg(doc.volumeName).arg(destFileName));
        } else {
            emit logMessage(QString("Copied %1 to %2")
                .arg(sourceInfo.fileName()).arg(doc.volumeName));
        }
    }
    
    emit logMessage(QString("Successfully created %1 volume(s) and copied all files")
        .arg(processedVolumes.size()));
    
    return true;
}

QString VolumeManager::formatBatesNumber(int number, int width) {
    return QString("%1").arg(number, width, 10, QChar('0'));
}
