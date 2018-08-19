#include "fieldeditorwidget.h"

#include <QLabel>
#include <QGridLayout>

FieldEditorWidget::FieldEditorWidget(QWidget *parent)
    : QLineEdit(parent),
      m_field(nullptr)
{
    connect(this, &QLineEdit::editingFinished, this, &FieldEditorWidget::commit);
}

FieldEditorWidget::~FieldEditorWidget()
{
}

FieldBase *FieldEditorWidget::field() const
{
    return m_field;
}

void FieldEditorWidget::setField(FieldBase *f)
{
    m_field = f;
    if (m_field) {
        setText(QString::fromStdString(f->value()));
    }
}

void FieldEditorWidget::commit()
{
    if (m_field) {
        m_field->set_value(text().toStdString());
    }
    setField(m_field);
}
