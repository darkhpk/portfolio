#include <QApplication>
#include "MainWindow.h"

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);
    
    app.setApplicationName("Load File Generator");
    app.setApplicationVersion("1.0.0");
    app.setOrganizationName("LFG");
    
    MainWindow mainWindow;
    mainWindow.show();
    
    return app.exec();
}
