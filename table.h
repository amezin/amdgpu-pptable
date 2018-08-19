#pragma once

#include <string>
#include <memory>
#include <vector>
#include <map>

#include "field.h"

class Table
{
public:
    Table();
    virtual ~Table();

    std::ostream &dump(std::ostream &s) const;

    std::map<std::string, std::unique_ptr<FieldBase>> fields;
    std::map<std::string, std::unique_ptr<Table>> tables;

    template<typename T>
    void add_field(const std::string &name, T &ref)
    {
        fields[name] = std::unique_ptr<FieldBase>(new Field<T>(ref));
    }
};

std::ostream &operator <<(std::ostream &, const Table &);
