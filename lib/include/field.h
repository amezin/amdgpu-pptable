#pragma once

#include <string>
#include <sstream>

class FieldBase
{
public:
    FieldBase();
    virtual ~FieldBase();

    virtual std::string value() const = 0;
    virtual bool set_value(const std::string &) = 0;

    template<typename T>
    static std::string to_string(T value)
    {
        std::ostringstream ss;
        ss << value;
        return ss.str();
    }

    template<typename T>
    static bool from_string(const std::string &s, T &value)
    {
        return bool(std::istringstream(s) >> value);
    }
};

template<>
std::string FieldBase::to_string(char value);
template<>
bool FieldBase::from_string(const std::string &s, char &value);
template<>
std::string FieldBase::to_string(unsigned char value);
template<>
bool FieldBase::from_string(const std::string &s, unsigned char &value);

template<typename T>
class Field : public FieldBase
{
public:
    explicit Field(T &ref) : ref(ref) {}
    ~Field() override {}

    std::string value() const override
    {
        return to_string(ref);
    }

    bool set_value(const std::string &value) override
    {
        return from_string(value, ref);
    }

    T &ref;
};
