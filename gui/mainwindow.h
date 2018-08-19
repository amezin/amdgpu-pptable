#pragma once

#include <QMainWindow>
#include <QFileDialog>

#include "table.h"
#include "tableeditorwidget.h"

class MainWindow : public QMainWindow
{
    Q_OBJECT
public:
    explicit MainWindow(QWidget *parent = nullptr);
    ~MainWindow() override;

    void load(const QString &file);
    void save(const QString &file);

private:
    QFileDialog *const openDialog;
    QFileDialog *const saveDialog;
    QAction *saveAction;

    TableEditorWidget *const editor;

    QByteArray data;
    std::unique_ptr<Table> pptable;
};
