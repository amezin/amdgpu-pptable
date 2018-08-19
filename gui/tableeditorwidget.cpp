#include "tableeditorwidget.h"

TableEditorWidget::TableEditorWidget(QWidget *parent)
    : QGroupBox(parent),
      fields_layout(new QFormLayout),
      tables_layout(new QVBoxLayout)
{
    auto layout = new QVBoxLayout(this);
    layout->addLayout(fields_layout);
    layout->addLayout(tables_layout);
    setLayout(layout);
}

TableEditorWidget::~TableEditorWidget()
{
}

void TableEditorWidget::setTable(Table *table)
{
    for (auto i = field_editors.begin(); i != field_editors.end();) {
        if (table->fields.find(i->first) == table->fields.end()) {
            fields_layout->removeRow(i->second);
            i = field_editors.erase(i);
        } else {
            i++;
        }
    }

    for (auto &p : table->fields) {
        auto editor = field_editors.find(p.first);
        if (editor == field_editors.end()) {
            auto widget = new FieldEditorWidget(this);
            auto name = QString::fromStdString(p.first);
            widget->setObjectName(name);
            fields_layout->addRow(name, widget);
            editor = field_editors.insert(std::make_pair(p.first, widget)).first;
        }
        editor->second->setField(p.second.get());
    }

    for (auto i = table_editors.begin(); i != table_editors.end();) {
        if (table->tables.find(i->first) == table->tables.end()) {
            tables_layout->removeWidget(i->second);
            delete i->second;
            i = table_editors.erase(i);
        } else {
            i++;
        }
    }

    for (auto &p : table->tables) {
        auto editor = table_editors.find(p.first);
        if (editor == table_editors.end()) {
            auto widget = new TableEditorWidget(this);
            auto name = QString::fromStdString(p.first);
            widget->setObjectName(name);
            widget->setTitle(name);
            tables_layout->addWidget(widget);
            editor = table_editors.insert(std::make_pair(p.first, widget)).first;
        }
        editor->second->setTable(p.second.get());
    }
}
