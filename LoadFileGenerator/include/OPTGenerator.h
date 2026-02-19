#ifndef OPTGENERATOR_H
#define OPTGENERATOR_H

#include <QObject>
#include <QString>
#include <QVector>
#include "Document.h"

class OPTGenerator : public QObject {
    Q_OBJECT

public:
    explicit OPTGenerator(QObject *parent = nullptr);
    ~OPTGenerator();
    
    bool generateOPT(const QString &outputPath, const QVector<Document> &documents);
    
signals:
    void logMessage(const QString &message);
};

#endif // OPTGENERATOR_H
