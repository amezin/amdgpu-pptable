#include "table.h"

Table::Table()
{
}

Table::~Table()
{
}

std::ostream &Table::dump(std::ostream &s) const
{
    for (auto &p : fields) {
        s << p.first << " = " << p.second->value() << "\n";
    }
    for (auto &p : tables) {
        s << p.first << ":\n";
        p.second->dump(s);
    }
    return s;
}

std::ostream &operator <<(std::ostream &s, const Table &t)
{
    return t.dump(s);
}
