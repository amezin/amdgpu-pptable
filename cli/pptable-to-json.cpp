#include <cstdlib>
#include <iostream>
#include <fstream>

#include "vega10powerplaytable.h"

enum ARG
{
    ARG_SELF,
    ARG_PPTABLE_FILE,
    ARG_OUTPUT_FILE,
    ARGC
};

void print_table(const Table &t, std::ostream &os, std::string &indent)
{
    os << "{\n";
    indent.push_back('\t');

    bool first = true;
    for (auto &p : t.fields) {
        if (first) {
            first = false;
        } else {
            os << ",\n";
        }

        os << indent << "\"" << p.first << "\": " << p.second->value();
    }

    for (auto &p : t.tables) {
        os << ",\n" << indent << "\"" << p.first << "\": ";
        print_table(*(p.second), os, indent);
    }

    indent.pop_back();
    os << "\n" << indent << "}";
}

int main(int argc, char *argv[])
{
    if (argc != ARGC) {
        std::cerr << "Usage: " << argv[ARG_SELF] << " pptable_file output.json" << std::endl;
        return EXIT_FAILURE;
    }

    char data[4096];
    std::streamsize data_size = 0;

    {
        std::ifstream input(argv[ARG_PPTABLE_FILE], std::ios::binary);
        input.read(data, sizeof(data));
        data_size = input.gcount();
    }

    auto pptable = parse_vega10_pptable(data);
    std::ofstream output(argv[ARG_OUTPUT_FILE]);
    std::string indent;
    print_table(*pptable, output, indent);

    return EXIT_SUCCESS;
}
