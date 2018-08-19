#include "field.h"

FieldBase::FieldBase()
{
}

FieldBase::~FieldBase()
{
}

template<>
std::string FieldBase::to_string(char value)
{
    return to_string(int(value));
}

template<>
bool FieldBase::from_string(const std::string &s, char &value)
{
    int v;
    if (!from_string(s, v)) {
        return false;
    }
    value = char(v);
    return true;
}

template<>
std::string FieldBase::to_string(unsigned char value)
{
    return to_string(unsigned(value));
}

template<>
bool FieldBase::from_string(const std::string &s, unsigned char &value)
{
    unsigned v;
    if (!from_string(s, v)) {
        return false;
    }
    value = static_cast<unsigned char>(v);
    return true;
}
