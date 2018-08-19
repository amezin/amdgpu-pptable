#include "mainwindow.h"

#include <QtDebug>
#include <QMenuBar>
#include <QMessageBox>
#include <QSaveFile>
#include <QScrollArea>

#include "vega10powerplaytable.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent),
      openDialog(new QFileDialog(this)),
      saveDialog(new QFileDialog(this)),
      editor(new TableEditorWidget(this))
{
    auto fileMenu = menuBar()->addMenu("&File");

    fileMenu->addAction("&Open", openDialog, &QFileDialog::exec, QKeySequence::Open);
    openDialog->setFileMode(QFileDialog::ExistingFile);
    connect(openDialog, &QFileDialog::fileSelected, this, &MainWindow::load);

    saveAction = fileMenu->addAction("&Save", saveDialog, &QFileDialog::exec, QKeySequence::Save);
    saveDialog->setAcceptMode(QFileDialog::AcceptSave);
    connect(saveDialog, &QFileDialog::fileSelected, this, &MainWindow::save);
    saveAction->setEnabled(false);

    auto scrollArea = new QScrollArea(this);
    scrollArea->setWidgetResizable(true);
    scrollArea->setWidget(editor);
    setCentralWidget(scrollArea);
}

MainWindow::~MainWindow()
{
}

void MainWindow::load(const QString &filePath)
{
    QFile file(filePath);
    if (!file.open(QFile::ReadOnly)) {
        QMessageBox::critical(this, "Can't open file for reading", file.errorString());
        return;
    }

    auto newData = file.readAll();
    if (newData.size() != file.size()) {
        QMessageBox::critical(this, "Can't read file", file.errorString());
        return;
    }

    setWindowFilePath(filePath);
    data = newData;
    pptable = parse_vega10_pptable(data.data());
    editor->setTable(pptable.get());

    saveDialog->selectFile(filePath);
    saveAction->setEnabled(true);

    qDebug() << "Loaded" << filePath;
}

void MainWindow::save(const QString &filePath)
{
    QSaveFile file(filePath);
    if (!file.open(QFile::WriteOnly | QFile::Truncate)) {
        QMessageBox::critical(this, "Can't open file for writing", file.errorString());
        return;
    }

    if (file.write(data) != data.size() || !file.commit()) {
        QMessageBox::critical(this, "Can't write file", file.errorString());
        return;
    }

    setWindowFilePath(filePath);
    openDialog->selectFile(filePath);

    qDebug() << "Saved" << filePath;
}
