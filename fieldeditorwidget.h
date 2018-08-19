#pragma once

#include <QWidget>
#include <QLineEdit>

#include "field.h"

class FieldEditorWidget : public QLineEdit
{
    Q_OBJECT
public:
    explicit FieldEditorWidget(QWidget *parent = nullptr);
    ~FieldEditorWidget() override;

    FieldBase *field() const;
    void setField(FieldBase *);

private:
    void commit();

    FieldBase *m_field;
};
