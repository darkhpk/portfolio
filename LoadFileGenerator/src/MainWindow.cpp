#include "MainWindow.h"
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QGroupBox>
#include <QFileDialog>
#include <QMessageBox>
#include <QMenuBar>
#include <QStatusBar>
#include <QFileInfo>
#include <QHeaderView>
#include <QBrush>
#include <QColor>
#include <QDialog>

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , pdfProcessor(new PDFProcessor(this))
    , csvParser(new CSVParser(this))
    , datGenerator(new DATGenerator(this))
    , optGenerator(new OPTGenerator(this))
    , volumeManager(new VolumeManager(this))
{
    setupUI();
    
    // Connect signals
    connect(pdfProcessor, &PDFProcessor::progressUpdated, this, &MainWindow::updateProgress);
    connect(pdfProcessor, &PDFProcessor::logMessage, this, &MainWindow::appendLog);
    connect(csvParser, &CSVParser::logMessage, this, &MainWindow::appendLog);
    connect(datGenerator, &DATGenerator::logMessage, this, &MainWindow::appendLog);
    connect(optGenerator, &OPTGenerator::logMessage, this, &MainWindow::appendLog);
    connect(volumeManager, &VolumeManager::logMessage, this, &MainWindow::appendLog);
}

MainWindow::~MainWindow() {
}

void MainWindow::setupUI() {
    setWindowTitle("Load File Generator - Professional Edition");
    resize(1000, 700);
    
    createMenuBar();
    createCentralWidget();
    
    statusLabel = new QLabel("Ready");
    statusBar()->addWidget(statusLabel);
}

void MainWindow::createMenuBar() {
    QMenuBar *menuBar = new QMenuBar(this);
    
    QMenu *fileMenu = menuBar->addMenu("&File");
    fileMenu->addAction("E&xit", this, &QWidget::close);
    
    QMenu *helpMenu = menuBar->addMenu("&Help");
    helpMenu->addAction("&Instructions", [this]() {
        QDialog *instructionsDialog = new QDialog(this);
        instructionsDialog->setWindowTitle("Load File Generator - Instructions");
        instructionsDialog->resize(700, 600);
        
        QVBoxLayout *layout = new QVBoxLayout(instructionsDialog);
        
        QTextEdit *textEdit = new QTextEdit();
        textEdit->setReadOnly(true);
        textEdit->setHtml(
            "<html><body style='font-family: Arial; font-size: 11pt;'>"
            "<h2 style='color: #4682B4;'>Load File Generator - User Guide</h2>"
            
            "<h3 style='color: #2E8B57;'>Overview</h3>"
            "<p>This application generates industry-standard DAT and OPT load files from PDF documents with metadata for use in litigation support and document management systems.</p>"
            
            "<h3 style='color: #2E8B57;'>Step-by-Step Instructions</h3>"
            
            "<h4>1. Load PDF Documents</h4>"
            "<ul>"
            "<li>Click <b>Browse PDF Folder</b> button</li>"
            "<li>Select the folder containing your PDF files</li>"
            "<li>All PDF files will be listed in the document list</li>"
            "</ul>"
            
            "<h4>2. Import Metadata CSV</h4>"
            "<ul>"
            "<li>Click <b>Browse CSV</b> button</li>"
            "<li>Select your CSV file containing document metadata</li>"
            "<li>CSV should have headers in the first row</li>"
            "<li>Optional: Include 'FileName' column to match PDFs with metadata</li>"
            "</ul>"
            
            "<h4>3. Configure Output Settings</h4>"
            "<ul>"
            "<li><b>Output Folder:</b> Click Browse Output to select destination</li>"
            "<li><b>Start Bates Number:</b> Set the starting Bates number (default: 1)</li>"
            "</ul>"
            
            "<h4>4. Choose Volume Split Method</h4>"
            "<p><b>Option A - Document Count:</b></p>"
            "<ul>"
            "<li>Select 'Document Count' radio button</li>"
            "<li>Set how many documents per volume (default: 1000)</li>"
            "<li>Volumes will be named VOL001, VOL002, etc.</li>"
            "</ul>"
            "<p><b>Option B - CSV Field:</b></p>"
            "<ul>"
            "<li>Select 'CSV Field' radio button</li>"
            "<li>Enter the CSV column name to use for volume assignment</li>"
            "<li>Documents with the same value will be grouped in the same volume</li>"
            "<li>Example: Use 'Box' or 'Volume' column from your CSV</li>"
            "</ul>"
            
            "<h4>5. Optional Settings</h4>"
            "<ul>"
            "<li><b>Rename copied files with DocID:</b> Check this to rename files as DOC000001.pdf, DOC000002.pdf, etc.</li>"
            "<li>Uncheck to keep original filenames</li>"
            "</ul>"
            
            "<h4>6. Preview Your Data</h4>"
            "<ul>"
            "<li>Check the <b>DAT Preview</b> tab to see how the DAT file will look</li>"
            "<li>Check the <b>OPT Preview</b> tab to see volume assignments</li>"
            "<li>Preview shows ALL documents (not just samples)</li>"
            "</ul>"
            
            "<h4>7. Generate Load Files</h4>"
            "<ul>"
            "<li>Click <b>Generate Load Files</b> button</li>"
            "<li>Monitor progress in the log window</li>"
            "<li>Wait for completion message</li>"
            "</ul>"
            
            "<h3 style='color: #2E8B57;'>Output Files</h3>"
            "<p>The application creates:</p>"
            "<ul>"
            "<li><b>loadfile.dat</b> - Concordance format with metadata (delimiter: ASCII 20, qualifier: ASCII 254)</li>"
            "<li><b>loadfile.opt</b> - Image reference file with volume and page information</li>"
            "<li><b>VOL001/, VOL002/, etc.</b> - Volume folders containing copied PDF files</li>"
            "</ul>"
            
            "<h3 style='color: #2E8B57;'>DAT File Format</h3>"
            "<ul>"
            "<li>All fields enclosed in þ (ASCII 254)</li>"
            "<li>Fields separated by ¶ (ASCII 20)</li>"
            "<li>Contains DOCID + all CSV columns</li>"
            "<li>UTF-8 encoded</li>"
            "</ul>"
            
            "<h3 style='color: #2E8B57;'>OPT File Format</h3>"
            "<p>One row per document with format:</p>"
            "<p><code>DOCID,Volume,Volume\\filename.pdf,Y,,,PageCount</code></p>"
            
            "<h3 style='color: #2E8B57;'>Tips</h3>"
            "<ul>"
            "<li>Ensure PDF files are readable before processing</li>"
            "<li>CSV encoding should be UTF-8 for best compatibility</li>"
            "<li>Use Preview tabs to verify settings before generating</li>"
            "<li>Page counting is multi-threaded for fast processing</li>"
            "<li>Check the log for detailed processing information</li>"
            "</ul>"
            
            "<h3 style='color: #2E8B57;'>Troubleshooting</h3>"
            "<ul>"
            "<li><b>PDF processing errors:</b> Check if PDFs are corrupted or password-protected</li>"
            "<li><b>CSV parsing errors:</b> Verify CSV has proper formatting and UTF-8 encoding</li>"
            "<li><b>Missing metadata:</b> Ensure CSV has 'FileName' column or data is in correct order</li>"
            "</ul>"
            
            "</body></html>"
        );
        
        layout->addWidget(textEdit);
        
        QPushButton *closeButton = new QPushButton("Close");
        connect(closeButton, &QPushButton::clicked, instructionsDialog, &QDialog::accept);
        layout->addWidget(closeButton);
        
        instructionsDialog->exec();
    });
    
    helpMenu->addAction("&About", [this]() {
        QMessageBox::about(this, "About Load File Generator",
            "Load File Generator v1.0.0\n\n"
            "A professional tool for generating DAT and OPT load files "
            "from PDF documents with metadata.\n\n"
            "Built with Qt and optimized for high-performance processing.");
    });
    
    setMenuBar(menuBar);
}

void MainWindow::createCentralWidget() {
    QWidget *centralWidget = new QWidget(this);
    QHBoxLayout *mainLayout = new QHBoxLayout(centralWidget);
    
    // Left side - Preview Tables
    QGroupBox *previewGroup = new QGroupBox("Preview");
    QVBoxLayout *previewLayout = new QVBoxLayout(previewGroup);
    
    previewTabs = new QTabWidget();
    
    // DAT Preview Table
    datPreviewTable = new QTableWidget();
    datPreviewTable->setEditTriggers(QAbstractItemView::NoEditTriggers);
    datPreviewTable->setAlternatingRowColors(true);
    previewTabs->addTab(datPreviewTable, "DAT Preview");
    
    // OPT Preview Table
    optPreviewTable = new QTableWidget();
    optPreviewTable->setEditTriggers(QAbstractItemView::NoEditTriggers);
    optPreviewTable->setAlternatingRowColors(true);
    previewTabs->addTab(optPreviewTable, "OPT Preview");
    
    previewLayout->addWidget(previewTabs);
    previewGroup->setMinimumWidth(500);
    
    // Right side - Main controls
    QWidget *rightWidget = new QWidget();
    QVBoxLayout *rightLayout = new QVBoxLayout(rightWidget);
    
    // PDF Files Section
    QGroupBox *pdfGroup = new QGroupBox("PDF Documents");
    QVBoxLayout *pdfLayout = new QVBoxLayout(pdfGroup);
    
    QHBoxLayout *pdfButtonLayout = new QHBoxLayout();
    btnBrowsePDFs = new QPushButton("Browse PDF Folder");
    btnBrowsePDFs->setMinimumHeight(35);
    connect(btnBrowsePDFs, &QPushButton::clicked, this, &MainWindow::onBrowsePDFs);
    
    QPushButton *btnClearPDFs = new QPushButton("Clear List");
    btnClearPDFs->setMinimumHeight(35);
    btnClearPDFs->setMaximumWidth(100);
    connect(btnClearPDFs, &QPushButton::clicked, [this]() {
        pdfFiles.clear();
        listPDFs->clear();
        updatePreviewTables();
        appendLog("PDF list cleared");
    });
    
    pdfButtonLayout->addWidget(btnBrowsePDFs);
    pdfButtonLayout->addWidget(btnClearPDFs);
    
    listPDFs = new QTableWidget();
    listPDFs->setMaximumHeight(150);
    listPDFs->setColumnCount(2);
    listPDFs->setHorizontalHeaderLabels(QStringList() << "#" << "Filename");
    listPDFs->horizontalHeader()->setStretchLastSection(true);
    listPDFs->setColumnWidth(0, 50);
    listPDFs->setEditTriggers(QTableWidget::NoEditTriggers);
    listPDFs->setSelectionBehavior(QTableWidget::SelectRows);
    listPDFs->verticalHeader()->setVisible(false);
    
    pdfLayout->addLayout(pdfButtonLayout);
    pdfLayout->addWidget(listPDFs);
    
    // Metadata CSV Section
    QGroupBox *csvGroup = new QGroupBox("Metadata CSV");
    QHBoxLayout *csvLayout = new QHBoxLayout(csvGroup);
    
    editCSVPath = new QLineEdit();
    editCSVPath->setPlaceholderText("Select CSV file with metadata...");
    editCSVPath->setReadOnly(true);
    
    btnBrowseCSV = new QPushButton("Browse CSV");
    btnBrowseCSV->setMinimumWidth(120);
    connect(btnBrowseCSV, &QPushButton::clicked, this, &MainWindow::onBrowseCSV);
    
    csvLayout->addWidget(editCSVPath);
    csvLayout->addWidget(btnBrowseCSV);
    
    // Output Settings Section
    QGroupBox *settingsGroup = new QGroupBox("Output Settings");
    QVBoxLayout *settingsLayout = new QVBoxLayout(settingsGroup);
    
    QHBoxLayout *outputPathLayout = new QHBoxLayout();
    editOutputPath = new QLineEdit();
    editOutputPath->setPlaceholderText("Select output folder...");
    editOutputPath->setReadOnly(true);
    
    btnBrowseOutput = new QPushButton("Browse Output");
    btnBrowseOutput->setMinimumWidth(120);
    connect(btnBrowseOutput, &QPushButton::clicked, this, &MainWindow::onBrowseOutputFolder);
    
    outputPathLayout->addWidget(editOutputPath);
    outputPathLayout->addWidget(btnBrowseOutput);
    
    QHBoxLayout *batesLayout = new QHBoxLayout();
    QLabel *batesLabel = new QLabel("Start Bates Number:");
    spinStartBates = new QSpinBox();
    spinStartBates->setRange(1, 99999999);
    spinStartBates->setValue(1);
    spinStartBates->setMinimumWidth(150);
    
    batesLayout->addWidget(batesLabel);
    batesLayout->addWidget(spinStartBates);
    batesLayout->addStretch();
    
    // Volume splitting method
    QHBoxLayout *volumeMethodLayout = new QHBoxLayout();
    QLabel *volumeMethodLabel = new QLabel("Split Volumes By:");
    
    radioDocCount = new QRadioButton("Document Count:");
    radioDocCount->setChecked(true);
    
    spinDocsPerVolume = new QSpinBox();
    spinDocsPerVolume->setRange(1, 100000);
    spinDocsPerVolume->setValue(1000);
    spinDocsPerVolume->setMinimumWidth(120);
    
    radioCSVField = new QRadioButton("CSV Field:");
    
    editVolumeField = new QLineEdit();
    editVolumeField->setPlaceholderText("Enter CSV column name...");
    editVolumeField->setMinimumWidth(150);
    editVolumeField->setEnabled(false);
    
    lblVolumeField = new QLabel();
    
    volumeMethodGroup = new QButtonGroup(this);
    volumeMethodGroup->addButton(radioDocCount);
    volumeMethodGroup->addButton(radioCSVField);
    
    connect(radioDocCount, &QRadioButton::toggled, this, &MainWindow::onVolumeMethodChanged);
    connect(radioCSVField, &QRadioButton::toggled, this, &MainWindow::onVolumeMethodChanged);
    connect(spinDocsPerVolume, static_cast<void(QSpinBox::*)(int)>(&QSpinBox::valueChanged), this, &MainWindow::updatePreviewTables);
    connect(editVolumeField, &QLineEdit::textChanged, this, &MainWindow::updatePreviewTables);
    
    volumeMethodLayout->addWidget(volumeMethodLabel);
    volumeMethodLayout->addWidget(radioDocCount);
    volumeMethodLayout->addWidget(spinDocsPerVolume);
    volumeMethodLayout->addWidget(radioCSVField);
    volumeMethodLayout->addWidget(editVolumeField);
    volumeMethodLayout->addStretch();
    
    QHBoxLayout *optionsLayout = new QHBoxLayout();
    chkRenameWithDocID = new QCheckBox("Rename copied files with DocID");
    chkRenameWithDocID->setChecked(false);
    optionsLayout->addWidget(chkRenameWithDocID);
    
    chkUseFilenameAsDocID = new QCheckBox("Use filename (without extension) as DocID");
    chkUseFilenameAsDocID->setChecked(false);
    connect(chkUseFilenameAsDocID, &QCheckBox::toggled, this, &MainWindow::updatePreviewTables);
    optionsLayout->addWidget(chkUseFilenameAsDocID);
    optionsLayout->addStretch();
    
    QHBoxLayout *customPrefixLayout = new QHBoxLayout();
    chkUseCustomPrefix = new QCheckBox("Use custom DocID prefix:");
    chkUseCustomPrefix->setChecked(false);
    connect(chkUseCustomPrefix, &QCheckBox::toggled, this, &MainWindow::updatePreviewTables);
    
    editCustomPrefix = new QLineEdit();
    editCustomPrefix->setPlaceholderText("e.g., HGL");
    editCustomPrefix->setMaximumWidth(150);
    editCustomPrefix->setEnabled(false);
    connect(editCustomPrefix, &QLineEdit::textChanged, this, &MainWindow::updatePreviewTables);
    connect(chkUseCustomPrefix, &QCheckBox::toggled, [this](bool checked) {
        editCustomPrefix->setEnabled(checked);
    });
    
    customPrefixLayout->addWidget(chkUseCustomPrefix);
    customPrefixLayout->addWidget(editCustomPrefix);
    customPrefixLayout->addStretch();
    
    settingsLayout->addLayout(outputPathLayout);
    settingsLayout->addLayout(batesLayout);
    settingsLayout->addLayout(volumeMethodLayout);
    settingsLayout->addLayout(optionsLayout);
    settingsLayout->addLayout(customPrefixLayout);
    
    // Progress Section
    QGroupBox *progressGroup = new QGroupBox("Progress");
    QVBoxLayout *progressLayout = new QVBoxLayout(progressGroup);
    
    progressBar = new QProgressBar();
    progressBar->setMinimumHeight(25);
    
    logOutput = new QTextEdit();
    logOutput->setReadOnly(true);
    logOutput->setMaximumHeight(150);
    
    QHBoxLayout *logButtonLayout = new QHBoxLayout();
    btnClearLog = new QPushButton("Clear Log");
    connect(btnClearLog, &QPushButton::clicked, this, &MainWindow::onClearLog);
    logButtonLayout->addStretch();
    logButtonLayout->addWidget(btnClearLog);
    
    progressLayout->addWidget(progressBar);
    progressLayout->addWidget(logOutput);
    progressLayout->addLayout(logButtonLayout);
    
    // Generate Button
    btnGenerate = new QPushButton("Generate Load Files");
    btnGenerate->setMinimumHeight(45);
    btnGenerate->setStyleSheet("QPushButton { background-color: #4CAF50; color: white; font-size: 14px; font-weight: bold; }");
    connect(btnGenerate, &QPushButton::clicked, this, &MainWindow::onGenerate);
    
    // Add all to right layout
    rightLayout->addWidget(pdfGroup);
    rightLayout->addWidget(csvGroup);
    rightLayout->addWidget(settingsGroup);
    rightLayout->addWidget(progressGroup);
    rightLayout->addWidget(btnGenerate);
    
    // Add preview and controls to main layout
    mainLayout->addWidget(previewGroup, 1);
    mainLayout->addWidget(rightWidget, 1);
    
    setCentralWidget(centralWidget);
}

void MainWindow::onBrowsePDFs() {
    QString dir = QFileDialog::getExistingDirectory(this, "Select PDF Folder",
                                                     QString(),
                                                     QFileDialog::ShowDirsOnly);
    
    if (!dir.isEmpty()) {
        QDir pdfDir(dir);
        QStringList filters;
        filters << "*.pdf";
        QStringList newFiles = pdfDir.entryList(filters, QDir::Files);
        
        int addedCount = 0;
        // Convert to full paths and append only new files
        for (const QString &fileName : newFiles) {
            QString fullPath = pdfDir.absoluteFilePath(fileName);
            
            // Check if file already exists in the list
            if (!pdfFiles.contains(fullPath)) {
                pdfFiles.append(fullPath);
                
                int row = listPDFs->rowCount();
                listPDFs->insertRow(row);
                listPDFs->setItem(row, 0, new QTableWidgetItem(QString::number(row + 1)));
                listPDFs->setItem(row, 1, new QTableWidgetItem(QFileInfo(fullPath).fileName()));
                
                addedCount++;
            }
        }
        
        if (addedCount > 0) {
            appendLog(QString("Added %1 PDF file(s) from: %2 (Total: %3)")
                .arg(addedCount).arg(dir).arg(pdfFiles.size()));
            updatePreviewTables();
        } else {
            appendLog(QString("No new PDF files found in: %1").arg(dir));
        }
    }
}

void MainWindow::onBrowseCSV() {
    QString file = QFileDialog::getOpenFileName(this, "Select Metadata CSV",
                                                QString(),
                                                "CSV Files (*.csv);;All Files (*)");
    
    if (!file.isEmpty()) {
        csvFilePath = file;
        editCSVPath->setText(file);
        appendLog(QString("CSV file selected: %1").arg(file));
        updatePreviewTables();
    }
}

void MainWindow::onBrowseOutputFolder() {
    QString dir = QFileDialog::getExistingDirectory(this, "Select Output Folder",
                                                     QString(),
                                                     QFileDialog::ShowDirsOnly);
    
    if (!dir.isEmpty()) {
        outputFolderPath = dir;
        editOutputPath->setText(dir);
        appendLog(QString("Output folder: %1").arg(dir));
    }
}

void MainWindow::onGenerate() {
    // Validate inputs
    if (pdfFiles.isEmpty()) {
        QMessageBox::warning(this, "Validation Error", "Please select PDF files.");
        return;
    }
    
    if (csvFilePath.isEmpty()) {
        QMessageBox::warning(this, "Validation Error", "Please select a metadata CSV file.");
        return;
    }
    
    if (outputFolderPath.isEmpty()) {
        QMessageBox::warning(this, "Validation Error", "Please select an output folder.");
        return;
    }
    
    btnGenerate->setEnabled(false);
    progressBar->setValue(0);
    appendLog("=== Starting Load File Generation ===");
    
    // Validation for CSV field method
    if (radioCSVField->isChecked() && editVolumeField->text().trimmed().isEmpty()) {
        QMessageBox::warning(this, "Validation Error", "Please enter a CSV column name for volume assignment.");
        btnGenerate->setEnabled(true);
        return;
    }
    
    // Step 1: Parse CSV metadata
    appendLog("Parsing CSV metadata...");
    if (!csvParser->parseCSV(csvFilePath)) {
        QMessageBox::critical(this, "Error", "Failed to parse CSV file.");
        btnGenerate->setEnabled(true);
        return;
    }
    
    // Step 2: Create document objects
    QVector<Document> documents;
    for (int i = 0; i < pdfFiles.size(); ++i) {
        Document doc;
        doc.filePath = pdfFiles[i];
        
        // Set DocID based on checkbox
        if (chkUseFilenameAsDocID->isChecked()) {
            QFileInfo fileInfo(pdfFiles[i]);
            doc.docID = fileInfo.baseName(); // Filename without extension
        } else if (chkUseCustomPrefix->isChecked() && !editCustomPrefix->text().trimmed().isEmpty()) {
            QString prefix = editCustomPrefix->text().trimmed();
            doc.docID = QString("%1_%2").arg(prefix).arg(i + 1, 6, 10, QChar('0'));
        } else {
            doc.docID = QString("DOC%1").arg(i + 1, 6, 10, QChar('0'));
        }
        
        // Get metadata from CSV
        QFileInfo fileInfo(pdfFiles[i]);
        doc.metadata = csvParser->getMetadataForFile(fileInfo.fileName());
        
        documents.append(doc);
    }
    
    // Step 3: Process PDFs (count pages)
    appendLog(QString("Processing %1 PDF documents...").arg(documents.size()));
    pdfProcessor->processDocuments(documents);
    
    // Step 4: Organize into volumes and assign Bates numbers
    volumeManager->setStartBatesNumber(spinStartBates->value());
    volumeManager->setRenameWithDocID(chkRenameWithDocID->isChecked());
    
    if (radioCSVField->isChecked()) {
        volumeManager->setVolumeFromCSVField(editVolumeField->text().trimmed());
    } else {
        volumeManager->setDocumentsPerVolume(spinDocsPerVolume->value());
        volumeManager->setVolumeFromCSVField("");  // Clear CSV field method
    }
    
    volumeManager->organizeIntoVolumes(documents);
    
    // Step 5: Create output folder structure
    appendLog("Creating output folder structure...");
    volumeManager->createOutputStructure(outputFolderPath, documents);
    
    // Step 6: Generate DAT file
    appendLog("Generating DAT file...");
    QString datPath = QDir(outputFolderPath).filePath("loadfile.dat");
    if (!datGenerator->generateDAT(datPath, documents, csvParser->getHeaders())) {
        QMessageBox::critical(this, "Error", "Failed to generate DAT file.");
        btnGenerate->setEnabled(true);
        return;
    }
    
    // Step 7: Generate OPT file
    appendLog("Generating OPT file...");
    QString optPath = QDir(outputFolderPath).filePath("loadfile.opt");
    if (!optGenerator->generateOPT(optPath, documents)) {
        QMessageBox::critical(this, "Error", "Failed to generate OPT file.");
        btnGenerate->setEnabled(true);
        return;
    }
    
    progressBar->setValue(100);
    appendLog("=== Load File Generation Complete ===");
    QMessageBox::information(this, "Success", 
        QString("Load files generated successfully!\n\nTotal Documents: %1\nOutput: %2")
        .arg(documents.size()).arg(outputFolderPath));
    
    btnGenerate->setEnabled(true);
}

void MainWindow::onClearLog() {
    logOutput->clear();
}

void MainWindow::updateProgress(int current, int total) {
    if (total > 0) {
        progressBar->setValue((current * 100) / total);
        statusLabel->setText(QString("Processing: %1 / %2").arg(current).arg(total));
    }
}

void MainWindow::appendLog(const QString &message) {
    logOutput->append(message);
    logOutput->ensureCursorVisible();
}

void MainWindow::onVolumeMethodChanged() {
    bool useCSVField = radioCSVField->isChecked();
    editVolumeField->setEnabled(useCSVField);
    spinDocsPerVolume->setEnabled(!useCSVField);
    updatePreviewTables();
}

void MainWindow::updatePreviewTables() {
    // Clear tables
    datPreviewTable->clear();
    optPreviewTable->clear();
    
    if (pdfFiles.isEmpty()) {
        datPreviewTable->setRowCount(0);
        datPreviewTable->setColumnCount(0);
        optPreviewTable->setRowCount(0);
        optPreviewTable->setColumnCount(0);
        return;
    }
    
    // Show all documents in preview
    int previewCount = pdfFiles.size();
    
    // Setup DAT Preview Table
    QVector<QString> datHeaders;
    datHeaders << "DOCID";
    
    // Get CSV headers if available
    if (!csvFilePath.isEmpty()) {
        CSVParser tempParser(this);
        if (tempParser.parseCSV(csvFilePath)) {
            QVector<QString> csvHeaders = tempParser.getHeaders();
            for (const QString &header : csvHeaders) {
                datHeaders.append(header);
            }
        }
    }
    
    datPreviewTable->setRowCount(previewCount + 1); // +1 for header
    datPreviewTable->setColumnCount(datHeaders.size());
    
    // Set DAT headers
    for (int col = 0; col < datHeaders.size(); ++col) {
        QTableWidgetItem *headerItem = new QTableWidgetItem(datHeaders[col]);
        headerItem->setBackground(QBrush(QColor(70, 130, 180)));
        headerItem->setForeground(QBrush(Qt::white));
        datPreviewTable->setItem(0, col, headerItem);
    }
    
    // Fill DAT preview data
    for (int row = 0; row < previewCount; ++row) {
        QString docID;
        if (chkUseFilenameAsDocID->isChecked()) {
            QFileInfo fileInfo(pdfFiles[row]);
            docID = fileInfo.baseName();
        } else if (chkUseCustomPrefix->isChecked() && !editCustomPrefix->text().trimmed().isEmpty()) {
            QString prefix = editCustomPrefix->text().trimmed();
            docID = QString("%1_%2").arg(prefix).arg(row + 1, 6, 10, QChar('0'));
        } else {
            docID = QString("DOC%1").arg(row + 1, 6, 10, QChar('0'));
        }
        datPreviewTable->setItem(row + 1, 0, new QTableWidgetItem(docID));
        
        // Add placeholder data for other columns
        for (int col = 1; col < datHeaders.size(); ++col) {
            datPreviewTable->setItem(row + 1, col, new QTableWidgetItem("..."));
        }
    }
    
    datPreviewTable->resizeColumnsToContents();
    
    // Setup OPT Preview Table
    QStringList optHeaders;
    optHeaders << "DOCID" << "Volume" << "File Path" << "Doc Break" << "Folder" << "Box" << "Page Count";
    
    optPreviewTable->setRowCount(previewCount + 1);
    optPreviewTable->setColumnCount(optHeaders.size());
    
    // Set OPT headers
    for (int col = 0; col < optHeaders.size(); ++col) {
        QTableWidgetItem *headerItem = new QTableWidgetItem(optHeaders[col]);
        headerItem->setBackground(QBrush(QColor(70, 130, 180)));
        headerItem->setForeground(QBrush(Qt::white));
        optPreviewTable->setItem(0, col, headerItem);
    }
    
    // Fill OPT preview data
    int docsPerVol = spinDocsPerVolume->value();
    QString volumeField = editVolumeField->text().trimmed();
    bool useCSVField = radioCSVField->isChecked() && !volumeField.isEmpty();
    
    // Parse CSV to get volume assignments if using CSV field method
    QMap<QString, QString> fileToVolume;
    if (useCSVField && !csvFilePath.isEmpty()) {
        CSVParser tempParser(this);
        if (tempParser.parseCSV(csvFilePath)) {
            QVector<QMap<QString, QString>> metadata = tempParser.getMetadata();
            for (int i = 0; i < qMin(metadata.size(), pdfFiles.size()); ++i) {
                QString volumeValue = metadata[i].value(volumeField, "VOL001");
                QFileInfo fileInfo(pdfFiles[i]);
                fileToVolume[fileInfo.fileName()] = volumeValue;
            }
        }
    }
    
    for (int row = 0; row < previewCount; ++row) {
        QString docID;
        if (chkUseFilenameAsDocID->isChecked()) {
            QFileInfo fileInfo(pdfFiles[row]);
            docID = fileInfo.baseName();
        } else if (chkUseCustomPrefix->isChecked() && !editCustomPrefix->text().trimmed().isEmpty()) {
            QString prefix = editCustomPrefix->text().trimmed();
            docID = QString("%1_%2").arg(prefix).arg(row + 1, 6, 10, QChar('0'));
        } else {
            docID = QString("DOC%1").arg(row + 1, 6, 10, QChar('0'));
        }
        QString volumeName;
        
        if (useCSVField) {
            QFileInfo fileInfo(pdfFiles[row]);
            volumeName = fileToVolume.value(fileInfo.fileName(), "VOL001");
        } else {
            int volumeNum = (row / docsPerVol) + 1;
            volumeName = QString("VOL%1").arg(volumeNum, 3, 10, QChar('0'));
        }
        
        QFileInfo fileInfo(pdfFiles[row]);
        QString filePath = QString("%1\\%2").arg(volumeName).arg(fileInfo.fileName());
        
        optPreviewTable->setItem(row + 1, 0, new QTableWidgetItem(docID));
        optPreviewTable->setItem(row + 1, 1, new QTableWidgetItem(volumeName));
        optPreviewTable->setItem(row + 1, 2, new QTableWidgetItem(filePath));
        optPreviewTable->setItem(row + 1, 3, new QTableWidgetItem("Y"));
        optPreviewTable->setItem(row + 1, 4, new QTableWidgetItem(""));
        optPreviewTable->setItem(row + 1, 5, new QTableWidgetItem(""));
        optPreviewTable->setItem(row + 1, 6, new QTableWidgetItem("..."));
    }
    
    optPreviewTable->resizeColumnsToContents();
}
