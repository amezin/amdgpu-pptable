#pragma once

#include <map>
#include <string>

#include <QGroupBox>
#include <QFormLayout>
#include <QVBoxLayout>

#include "table.h"
#include "fieldeditorwidget.h"

class TableEditorWidget : public QGroupBox
{
    Q_OBJECT
public:
    explicit TableEditorWidget(QWidget *parent = nullptr);
    ~TableEditorWidget() override;

    void setTable(Table *table);

private:
    std::map<std::string, FieldEditorWidget *> field_editors;
    std::map<std::string, TableEditorWidget *> table_editors;

    QFormLayout *const fields_layout;
    QVBoxLayout *const tables_layout;
};
