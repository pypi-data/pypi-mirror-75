#ifndef LFORTRAN_AST_TO_SRC_H
#define LFORTRAN_AST_TO_SRC_H

#include <lfortran/ast.h>

namespace LFortran {

    // Converts AST to Fortran source code
    std::string ast_to_src(LFortran::AST::ast_t &ast);

}

#endif // LFORTRAN_AST_TO_SRC_H
