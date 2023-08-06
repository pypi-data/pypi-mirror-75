#include <string>

#include <lfortran/pickle.h>
#include <lfortran/pickle.h>
#include <lfortran/parser/parser.h>
#include <lfortran/parser/parser.tab.hh>

using LFortran::AST::ast_t;
using LFortran::AST::Declaration_t;
using LFortran::AST::expr_t;
using LFortran::AST::stmt_t;
using LFortran::AST::Name_t;
using LFortran::AST::Num_t;
using LFortran::AST::BinOp_t;
using LFortran::AST::UnaryOp_t;
using LFortran::AST::Compare_t;
using LFortran::AST::If_t;
using LFortran::AST::Assignment_t;
using LFortran::AST::WhileLoop_t;
using LFortran::AST::Exit_t;
using LFortran::AST::Return_t;
using LFortran::AST::Cycle_t;
using LFortran::AST::DoLoop_t;
using LFortran::AST::Subroutine_t;
using LFortran::AST::Function_t;
using LFortran::AST::Program_t;
using LFortran::AST::astType;
using LFortran::AST::exprType;
using LFortran::AST::stmtType;
using LFortran::AST::operatorType;
using LFortran::AST::unaryopType;
using LFortran::AST::cmpopType;
using LFortran::AST::TranslationUnit_t;
using LFortran::AST::PickleBaseVisitor;


namespace LFortran {

std::string pickle(int token, const LFortran::YYSTYPE &yystype,
        bool colors)
{
    std::string t;
    t += "(token \"";
    t += token2text(token);
    t += "\"";
    if (token == yytokentype::TK_NAME) {
        t += " " + yystype.string.str();
    } else if (token == yytokentype::TK_INTEGER) {
        t += " " + std::to_string(yystype.n);
    }
    t += ")";
    return t;
}

std::string op2str(const operatorType type)
{
    switch (type) {
        case (operatorType::Add) : return "+";
        case (operatorType::Sub) : return "-";
        case (operatorType::Mul) : return "*";
        case (operatorType::Div) : return "/";
        case (operatorType::Pow) : return "**";
    }
    throw std::runtime_error("Unknown type");
}

std::string unop2str(const unaryopType type)
{
    switch (type) {
        case (unaryopType::Invert) : return "inv";
        case (unaryopType::Not) : return "not";
        case (unaryopType::UAdd) : return "u+";
        case (unaryopType::USub) : return "u-";
    }
    throw std::runtime_error("Unknown type");
}

std::string compare2str(const cmpopType type)
{
    switch (type) {
        case (cmpopType::Eq) : return "==";
        case (cmpopType::NotEq) : return "/=";
        case (cmpopType::Lt) : return "<";
        case (cmpopType::LtE) : return "<=";
        case (cmpopType::Gt) : return ">";
        case (cmpopType::GtE) : return ">=";
    }
    throw std::runtime_error("Unknown type");
}

class PickleVisitor : public PickleBaseVisitor<PickleVisitor>
{
public:
    void visit_BinOp(const BinOp_t &x) {
        s.append("(");
        // We do not print BinOp +, but rather just +. It is still uniquely
        // determined that + means BinOp's +.
        /*
        s.append(expr2str(x.base.type));
        s.append(" ");
        */
        s.append(op2str(x.m_op));
        s.append(" ");
        this->visit_expr(*x.m_left);
        s.append(" ");
        this->visit_expr(*x.m_right);
        s.append(")");
    }
    void visit_UnaryOp(const UnaryOp_t &x) {
        s.append("(");
        s.append(unop2str(x.m_op));
        s.append(" ");
        this->visit_expr(*x.m_operand);
        s.append(")");
    }
    void visit_Compare(const Compare_t &x) {
        s.append("(");
        s.append(compare2str(x.m_op));
        s.append(" ");
        this->visit_expr(*x.m_left);
        s.append(" ");
        this->visit_expr(*x.m_right);
        s.append(")");
    }
    void visit_Name(const Name_t &x) {
        if (use_colors) {
            s.append(color(fg::yellow));
        }
        s.append(x.m_id);
        if (use_colors) {
            s.append(color(fg::reset));
        }
    }
    void visit_Num(const Num_t &x) {
        if (use_colors) {
            s.append(color(fg::cyan));
        }
        s.append(std::to_string(x.m_n));
        if (use_colors) {
            s.append(color(fg::reset));
        }
    }
    std::string get_str() {
        return s;
    }
};

std::string pickle(LFortran::AST::ast_t &ast, bool colors) {
    PickleVisitor v;
    v.use_colors = colors;
    v.visit_ast(ast);
    return v.get_str();
}

std::string pickle(AST::TranslationUnit_t &ast, bool colors) {
    PickleVisitor v;
    v.use_colors = colors;
    v.visit_ast((AST::ast_t&)(ast));
    return v.get_str();
}

/* -----------------------------------------------------------------------*/
// ASR

static inline ASR::Variable_t* VARIABLE(const ASR::asr_t *f)
{
    LFORTRAN_ASSERT(f->type == ASR::asrType::var);
    ASR::var_t *t = (ASR::var_t *)f;
    LFORTRAN_ASSERT(t->type == ASR::varType::Variable);
    return (ASR::Variable_t*)t;
}

class ASRPickleVisitor :
    public LFortran::ASR::PickleBaseVisitor<ASRPickleVisitor>
{
public:
    std::string get_str() {
        return s;
    }
    void visit_Var(const ASR::Var_t &x) {
        s.append("(");
        if (use_colors) {
            s.append(color(style::bold));
            s.append(color(fg::magenta));
        }
        s.append("Var");
        if (use_colors) {
            s.append(color(fg::reset));
            s.append(color(style::reset));
        }
        s.append(" ");
        s.append(x.m_symtab->get_hash());
        s.append(" ");
        s.append(VARIABLE((ASR::asr_t*)x.m_v)->m_name);
        s.append(")");
    }
    void visit_Num(const ASR::Num_t &x) {
        s.append("(");
        if (use_colors) {
            s.append(color(style::bold));
            s.append(color(fg::magenta));
        }
        s.append("Num");
        if (use_colors) {
            s.append(color(fg::reset));
            s.append(color(style::reset));
        }
        s.append(" ");
        s.append(std::to_string(x.m_n));
        s.append(" ");
        this->visit_ttype(*x.m_type);
        s.append(")");
    }
};

std::string pickle(LFortran::ASR::asr_t &asr, bool colors) {
    ASRPickleVisitor v;
    v.use_colors = colors;
    v.visit_asr(asr);
    return v.get_str();
}

}
