/* A Bison parser, made by GNU Bison 3.3.2.  */

/* Skeleton interface for Bison GLR parsers in C

   Copyright (C) 2002-2015, 2018-2019 Free Software Foundation, Inc.

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.  */

/* As a special exception, you may create a larger work that contains
   part or all of the Bison parser skeleton and distribute that work
   under terms of your choice, so long as that work isn't itself a
   parser generator using the skeleton or a modified version thereof
   as a parser skeleton.  Alternatively, if you modify or redistribute
   the parser skeleton itself, you may (at your option) remove this
   special exception, which will cause the skeleton and the resulting
   Bison output files to be licensed under the GNU General Public
   License without this special exception.

   This special exception was added by the Free Software Foundation in
   version 2.2 of Bison.  */

#ifndef YY_YY_PARSER_TAB_HH_INCLUDED
# define YY_YY_PARSER_TAB_HH_INCLUDED
/* Debug traces.  */
#ifndef YYDEBUG
# define YYDEBUG 0
#endif
#if YYDEBUG
extern int yydebug;
#endif
/* "%code requires" blocks.  */
#line 25 "parser.yy" /* glr.c:197  */

#include <lfortran/parser/parser.h>

#line 48 "parser.tab.hh" /* glr.c:197  */

/* Token type.  */
#ifndef YYTOKENTYPE
# define YYTOKENTYPE
  enum yytokentype
  {
    END_OF_FILE = 0,
    TK_NEWLINE = 258,
    TK_NAME = 259,
    TK_DEF_OP = 260,
    TK_INTEGER = 261,
    TK_REAL = 262,
    TK_PLUS = 263,
    TK_MINUS = 264,
    TK_STAR = 265,
    TK_SLASH = 266,
    TK_COLON = 267,
    TK_SEMICOLON = 268,
    TK_COMMA = 269,
    TK_EQUAL = 270,
    TK_LPAREN = 271,
    TK_RPAREN = 272,
    TK_LBRACKET = 273,
    TK_RBRACKET = 274,
    TK_PERCENT = 275,
    TK_VBAR = 276,
    TK_STRING = 277,
    TK_DBL_DOT = 278,
    TK_DBL_COLON = 279,
    TK_POW = 280,
    TK_CONCAT = 281,
    TK_ARROW = 282,
    TK_EQ = 283,
    TK_NE = 284,
    TK_LT = 285,
    TK_LE = 286,
    TK_GT = 287,
    TK_GE = 288,
    TK_NOT = 289,
    TK_AND = 290,
    TK_OR = 291,
    TK_EQV = 292,
    TK_NEQV = 293,
    TK_TRUE = 294,
    TK_FALSE = 295,
    KW_ABSTRACT = 296,
    KW_ALL = 297,
    KW_ALLOCATABLE = 298,
    KW_ALLOCATE = 299,
    KW_ASSIGNMENT = 300,
    KW_ASSOCIATE = 301,
    KW_ASYNCHRONOUS = 302,
    KW_BACKSPACE = 303,
    KW_BIND = 304,
    KW_BLOCK = 305,
    KW_CALL = 306,
    KW_CASE = 307,
    KW_CHARACTER = 308,
    KW_CLASS = 309,
    KW_CLOSE = 310,
    KW_CODIMENSION = 311,
    KW_COMMON = 312,
    KW_COMPLEX = 313,
    KW_CONCURRENT = 314,
    KW_CONTAINS = 315,
    KW_CONTIGUOUS = 316,
    KW_CONTINUE = 317,
    KW_CRITICAL = 318,
    KW_CYCLE = 319,
    KW_DATA = 320,
    KW_DEALLOCATE = 321,
    KW_DEFAULT = 322,
    KW_DEFERRED = 323,
    KW_DIMENSION = 324,
    KW_DO = 325,
    KW_DOWHILE = 326,
    KW_DOUBLE = 327,
    KW_ELEMENTAL = 328,
    KW_ELSE = 329,
    KW_END = 330,
    KW_END_IF = 331,
    KW_ENDIF = 332,
    KW_END_DO = 333,
    KW_ENDDO = 334,
    KW_END_WHERE = 335,
    KW_ENDWHERE = 336,
    KW_ENTRY = 337,
    KW_ENUM = 338,
    KW_ENUMERATOR = 339,
    KW_EQUIVALENCE = 340,
    KW_ERRMSG = 341,
    KW_ERROR = 342,
    KW_EXIT = 343,
    KW_EXTENDS = 344,
    KW_EXTERNAL = 345,
    KW_FILE = 346,
    KW_FINAL = 347,
    KW_FLUSH = 348,
    KW_FORALL = 349,
    KW_FORMAT = 350,
    KW_FORMATTED = 351,
    KW_FUNCTION = 352,
    KW_GENERIC = 353,
    KW_GO = 354,
    KW_IF = 355,
    KW_IMPLICIT = 356,
    KW_IMPORT = 357,
    KW_IMPURE = 358,
    KW_IN = 359,
    KW_INCLUDE = 360,
    KW_INOUT = 361,
    KW_INQUIRE = 362,
    KW_INTEGER = 363,
    KW_INTENT = 364,
    KW_INTERFACE = 365,
    KW_INTRINSIC = 366,
    KW_IS = 367,
    KW_KIND = 368,
    KW_LEN = 369,
    KW_LOCAL = 370,
    KW_LOCAL_INIT = 371,
    KW_LOGICAL = 372,
    KW_MODULE = 373,
    KW_MOLD = 374,
    KW_NAME = 375,
    KW_NAMELIST = 376,
    KW_NOPASS = 377,
    KW_NON_INTRINSIC = 378,
    KW_NON_OVERRIDABLE = 379,
    KW_NON_RECURSIVE = 380,
    KW_NONE = 381,
    KW_NULLIFY = 382,
    KW_ONLY = 383,
    KW_OPEN = 384,
    KW_OPERATOR = 385,
    KW_OPTIONAL = 386,
    KW_OUT = 387,
    KW_PARAMETER = 388,
    KW_PASS = 389,
    KW_POINTER = 390,
    KW_PRECISION = 391,
    KW_PRINT = 392,
    KW_PRIVATE = 393,
    KW_PROCEDURE = 394,
    KW_PROGRAM = 395,
    KW_PROTECTED = 396,
    KW_PUBLIC = 397,
    KW_PURE = 398,
    KW_QUIET = 399,
    KW_RANK = 400,
    KW_READ = 401,
    KW_REAL = 402,
    KW_RECURSIVE = 403,
    KW_RESULT = 404,
    KW_RETURN = 405,
    KW_REWIND = 406,
    KW_SAVE = 407,
    KW_SELECT = 408,
    KW_SEQUENCE = 409,
    KW_SHARED = 410,
    KW_SOURCE = 411,
    KW_STAT = 412,
    KW_STOP = 413,
    KW_SUBMODULE = 414,
    KW_SUBROUTINE = 415,
    KW_TARGET = 416,
    KW_TEAM = 417,
    KW_TEAM_NUMBER = 418,
    KW_THEN = 419,
    KW_TO = 420,
    KW_TYPE = 421,
    KW_UNFORMATTED = 422,
    KW_USE = 423,
    KW_VALUE = 424,
    KW_VOLATILE = 425,
    KW_WHERE = 426,
    KW_WHILE = 427,
    KW_WRITE = 428,
    UMINUS = 429
  };
#endif

/* Value type.  */
#if ! defined YYSTYPE && ! defined YYSTYPE_IS_DECLARED
typedef LFortran::YYSTYPE YYSTYPE;
# define YYSTYPE_IS_TRIVIAL 1
# define YYSTYPE_IS_DECLARED 1
#endif

/* Location type.  */
#if ! defined YYLTYPE && ! defined YYLTYPE_IS_DECLARED
typedef struct YYLTYPE YYLTYPE;
struct YYLTYPE
{
  int first_line;
  int first_column;
  int last_line;
  int last_column;
};
# define YYLTYPE_IS_DECLARED 1
# define YYLTYPE_IS_TRIVIAL 1
#endif



int yyparse (LFortran::Parser &p);

#endif /* !YY_YY_PARSER_TAB_HH_INCLUDED  */
