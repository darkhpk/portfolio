#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QPushButton>
#include <QTextEdit>
#include <QProgressBar>
#include <QLineEdit>
#include <QSpinBox>
#include <QTableWidget>
#include <QLabel>
#include <QTabWidget>
#include <QTableWidget>
#include <QCheckBox>
#include <QRadioButton>
#include <QButtonGroup>
#include "PDFProcessor.h"
#include "CSVParser.h"
#include "DATGenerator.h"
#include "OPTGenerator.h"
#include "VolumeManager.h"

class MainWindow : public QMainWindow {
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private slots:
    void onBrowsePDFs();
    void onBrowseCSV();
    void onBrowseOutputFolder();
    void onGenerate();
    void onClearLog();
    void updateProgress(int current, int total);
    void appendLog(const QString &message);
    void updatePreviewTables();
    void onVolumeMethodChanged();

private:
    void setupUI();
    void createMenuBar();
    void createCentralWidget();
    
    // UI Components
    QPushButton *btnBrowsePDFs;
    QPushButton *btnBrowseCSV;
    QPushButton *btnBrowseOutput;
    QPushButton *btnGenerate;
    QPushButton *btnClearLog;
    
    QLineEdit *editCSVPath;
    QLineEdit *editOutputPath;
    QSpinBox *spinStartBates;
    QSpinBox *spinDocsPerVolume;
    QCheckBox *chkRenameWithDocID;
    QCheckBox *chkUseFilenameAsDocID;
    QCheckBox *chkUseCustomPrefix;
    QLineEdit *editCustomPrefix;
    
    QRadioButton *radioDocCount;
    QRadioButton *radioCSVField;
    QButtonGroup *volumeMethodGroup;
    QLineEdit *editVolumeField;
    QLabel *lblVolumeField;
    
    QTableWidget *listPDFs;
    QTextEdit *logOutput;
    QProgressBar *progressBar;
    QLabel *statusLabel;
    
    QTabWidget *previewTabs;
    QTableWidget *datPreviewTable;
    QTableWidget *optPreviewTable;
    
    // Data
    QStringList pdfFiles;
    QString csvFilePath;
    QString outputFolderPath;
    
    // Processing modules
    PDFProcessor *pdfProcessor;
    CSVParser *csvParser;
    DATGenerator *datGenerator;
    OPTGenerator *optGenerator;
    VolumeManager *volumeManager;
};

#endif // MAINWINDOW_H
