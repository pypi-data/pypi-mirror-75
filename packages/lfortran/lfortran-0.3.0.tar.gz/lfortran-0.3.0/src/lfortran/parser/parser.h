#ifndef LFORTRAN_PARSER_PARSER_H
#define LFORTRAN_PARSER_PARSER_H

#include <fstream>
#include <algorithm>
#include <memory>

#include <lfortran/containers.h>
#include <lfortran/parser/tokenizer.h>

namespace LFortran
{

class Parser
{
    std::string inp;

public:
    Allocator &m_a;
    Tokenizer m_tokenizer;
    Vec<AST::ast_t*> result;

    Parser(Allocator &al) : m_a{al} {
        result.reserve(al, 32);
    }

    void parse(const std::string &input);
    int parse();


private:
};

// Parses Fortran code to AST
AST::TranslationUnit_t* parse(Allocator &al, const std::string &s);

// Just like `parse`, but prints a nice error message to std::cout if a
// syntax error happens:
AST::TranslationUnit_t* parse2(Allocator &al, const std::string &s);

// Prints a nice error message to std::cout
void show_syntax_error(const std::string &filename, const std::string &input,
        const Location &loc, const int token, const std::string *tstr=nullptr);

// Tokenizes the `input` and return a list of tokens
std::vector<int> tokens(const std::string &input,
        std::vector<LFortran::YYSTYPE> *stypes=nullptr);

// Converts token number to text
std::string token2text(const int token);


} // namespace LFortran

#endif
