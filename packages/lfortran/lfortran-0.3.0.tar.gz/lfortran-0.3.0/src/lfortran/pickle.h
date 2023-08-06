#ifndef LFORTRAN_PICKLE_H
#define LFORTRAN_PICKLE_H

#include <lfortran/parser/parser_stype.h>
#include <lfortran/ast.h>
#include <lfortran/asr.h>

namespace LFortran {

    // Pickle a token
    std::string pickle(int token, const YYSTYPE &yystype, bool colors=false);

    // Pickle an AST node
    std::string pickle(AST::ast_t &ast, bool colors=false);
    std::string pickle(AST::TranslationUnit_t &ast, bool colors=false); 

    // Pickle an ASR node
    std::string pickle(ASR::asr_t &asr, bool colors=false);

}

#endif // LFORTRAN_PICKLE_H
