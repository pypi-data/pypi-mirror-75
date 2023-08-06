#ifndef LFORTRAN_SRC_PARSER_TOKENIZER_H
#define LFORTRAN_SRC_PARSER_TOKENIZER_H

#include <lfortran/exception.h>
#include <lfortran/parser/parser_stype.h>

namespace LFortran
{

class Tokenizer
{
public:
    unsigned char *cur;
    unsigned char *mar;
    unsigned char *ctxmar;
    unsigned char *tok;
    unsigned char *cur_line;
    unsigned int line_num;

public:
    // Set the string to tokenize. The caller must ensure `str` will stay valid
    // as long as `lex` is being called.
    void set_string(const std::string &str);

    // Get next token. Token ID is returned as function result, the semantic
    // value is put into `yylval`.
    int lex(YYSTYPE &yylval, Location &loc);

    // Return the current token as std::string
    std::string token() const
    {
        return std::string((char *)tok, cur - tok);
    }

    // Return the current token as YYSTYPE::Str
    void token(YYSTYPE::Str &s) const
    {
        s.p = (char*) tok;
        s.n = cur-tok;
    }

    // Return the current token's location
    void token_loc(Location &loc)
    {
        loc.first_line = line_num;
        loc.last_line = line_num;
        loc.first_column = tok-cur_line+1;
        loc.last_column = cur-cur_line;
    }
};

} // namespace LFortran

#endif
