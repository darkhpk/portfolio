#ifndef DATGENERATOR_H
#define DATGENERATOR_H

#include <QObject>
#include <QString>
#include <QVector>
#include "Document.h"

class DATGenerator : public QObject {
    Q_OBJECT

public:
    explicit DATGenerator(QObject *parent = nullptr);
    ~DATGenerator();
    
    bool generateDAT(const QString &outputPath, const QVector<Document> &documents,
                     const QVector<QString> &headers);
    
signals:
    void logMessage(const QString &message);
    
private:
    QString escapeField(const QString &field);
    QChar delimiter;
    QChar textQualifier;
};

#endif // DATGENERATOR_H
