// A Bison parser, made by GNU Bison 3.6.3.

// Skeleton implementation for Bison LALR(1) parsers in C++

// Copyright (C) 2002-2015, 2018-2020 Free Software Foundation, Inc.

// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.

// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.

// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <http://www.gnu.org/licenses/>.

// As a special exception, you may create a larger work that contains
// part or all of the Bison parser skeleton and distribute that work
// under terms of your choice, so long as that work isn't itself a
// parser generator using the skeleton or a modified version thereof
// as a parser skeleton.  Alternatively, if you modify or redistribute
// the parser skeleton itself, you may (at your option) remove this
// special exception, which will cause the skeleton and the resulting
// Bison output files to be licensed under the GNU General Public
// License without this special exception.

// This special exception was added by the Free Software Foundation in
// version 2.2 of Bison.

// DO NOT RELY ON FEATURES THAT ARE NOT DOCUMENTED in the manual,
// especially those whose name start with YY_ or yy_.  They are
// private implementation details that can be changed or removed.


// Take the name prefix into account.
#define yylex   pytypelex



#include "parser.tab.hh"


// Unqualified %code blocks.
#line 34 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"

namespace {
PyObject* DOT_STRING = PyString_FromString(".");

/* Helper functions for building up lists. */
PyObject* StartList(PyObject* item);
PyObject* AppendList(PyObject* list, PyObject* item);
PyObject* ExtendList(PyObject* dst, PyObject* src);

}  // end namespace


// Check that a python value is not NULL.  This must be a macro because it
// calls YYERROR (which is a goto).
#define CHECK(x, loc) do { if (x == NULL) {\
    ctx->SetErrorLocation(loc); \
    YYERROR; \
  }} while(0)

// pytypelex is generated in lexer.lex.cc, but because it uses semantic_type and
// location, it must be declared here.
int pytypelex(pytype::parser::semantic_type* lvalp, pytype::location* llocp,
              void* scanner);


#line 74 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"


#ifndef YY_
# if defined YYENABLE_NLS && YYENABLE_NLS
#  if ENABLE_NLS
#   include <libintl.h> // FIXME: INFRINGES ON USER NAME SPACE.
#   define YY_(msgid) dgettext ("bison-runtime", msgid)
#  endif
# endif
# ifndef YY_
#  define YY_(msgid) msgid
# endif
#endif


// Whether we are compiled with exception support.
#ifndef YY_EXCEPTIONS
# if defined __GNUC__ && !defined __EXCEPTIONS
#  define YY_EXCEPTIONS 0
# else
#  define YY_EXCEPTIONS 1
# endif
#endif

#define YYRHSLOC(Rhs, K) ((Rhs)[K].location)
/* YYLLOC_DEFAULT -- Set CURRENT to span from RHS[1] to RHS[N].
   If N is 0, then set CURRENT to the empty location which ends
   the previous symbol: RHS[0] (always defined).  */

# ifndef YYLLOC_DEFAULT
#  define YYLLOC_DEFAULT(Current, Rhs, N)                               \
    do                                                                  \
      if (N)                                                            \
        {                                                               \
          (Current).begin  = YYRHSLOC (Rhs, 1).begin;                   \
          (Current).end    = YYRHSLOC (Rhs, N).end;                     \
        }                                                               \
      else                                                              \
        {                                                               \
          (Current).begin = (Current).end = YYRHSLOC (Rhs, 0).end;      \
        }                                                               \
    while (false)
# endif


// Enable debugging if requested.
#if PYTYPEDEBUG

// A pseudo ostream that takes yydebug_ into account.
# define YYCDEBUG if (yydebug_) (*yycdebug_)

# define YY_SYMBOL_PRINT(Title, Symbol)         \
  do {                                          \
    if (yydebug_)                               \
    {                                           \
      *yycdebug_ << Title << ' ';               \
      yy_print_ (*yycdebug_, Symbol);           \
      *yycdebug_ << '\n';                       \
    }                                           \
  } while (false)

# define YY_REDUCE_PRINT(Rule)          \
  do {                                  \
    if (yydebug_)                       \
      yy_reduce_print_ (Rule);          \
  } while (false)

# define YY_STACK_PRINT()               \
  do {                                  \
    if (yydebug_)                       \
      yy_stack_print_ ();                \
  } while (false)

#else // !PYTYPEDEBUG

# define YYCDEBUG if (false) std::cerr
# define YY_SYMBOL_PRINT(Title, Symbol)  YYUSE (Symbol)
# define YY_REDUCE_PRINT(Rule)           static_cast<void> (0)
# define YY_STACK_PRINT()                static_cast<void> (0)

#endif // !PYTYPEDEBUG

#define yyerrok         (yyerrstatus_ = 0)
#define yyclearin       (yyla.clear ())

#define YYACCEPT        goto yyacceptlab
#define YYABORT         goto yyabortlab
#define YYERROR         goto yyerrorlab
#define YYRECOVERING()  (!!yyerrstatus_)

#line 17 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
namespace pytype {
#line 167 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"

  /// Build a parser object.
  parser::parser (void* scanner_yyarg, pytype::Context* ctx_yyarg)
#if PYTYPEDEBUG
    : yydebug_ (false),
      yycdebug_ (&std::cerr),
#else
    :
#endif
      scanner (scanner_yyarg),
      ctx (ctx_yyarg)
  {}

  parser::~parser ()
  {}

  parser::syntax_error::~syntax_error () YY_NOEXCEPT YY_NOTHROW
  {}

  /*---------------.
  | symbol kinds.  |
  `---------------*/

  // basic_symbol.
  template <typename Base>
  parser::basic_symbol<Base>::basic_symbol (const basic_symbol& that)
    : Base (that)
    , value (that.value)
    , location (that.location)
  {}


  /// Constructor for valueless symbols.
  template <typename Base>
  parser::basic_symbol<Base>::basic_symbol (typename Base::kind_type t, YY_MOVE_REF (location_type) l)
    : Base (t)
    , value ()
    , location (l)
  {}

  template <typename Base>
  parser::basic_symbol<Base>::basic_symbol (typename Base::kind_type t, YY_RVREF (semantic_type) v, YY_RVREF (location_type) l)
    : Base (t)
    , value (YY_MOVE (v))
    , location (YY_MOVE (l))
  {}

  template <typename Base>
  parser::symbol_kind_type
  parser::basic_symbol<Base>::type_get () const YY_NOEXCEPT
  {
    return this->kind ();
  }

  template <typename Base>
  bool
  parser::basic_symbol<Base>::empty () const YY_NOEXCEPT
  {
    return this->kind () == symbol_kind::S_YYEMPTY;
  }

  template <typename Base>
  void
  parser::basic_symbol<Base>::move (basic_symbol& s)
  {
    super_type::move (s);
    value = YY_MOVE (s.value);
    location = YY_MOVE (s.location);
  }

  // by_kind.
  parser::by_kind::by_kind ()
    : kind_ (symbol_kind::S_YYEMPTY)
  {}

#if 201103L <= YY_CPLUSPLUS
  parser::by_kind::by_kind (by_kind&& that)
    : kind_ (that.kind_)
  {
    that.clear ();
  }
#endif

  parser::by_kind::by_kind (const by_kind& that)
    : kind_ (that.kind_)
  {}

  parser::by_kind::by_kind (token_kind_type t)
    : kind_ (yytranslate_ (t))
  {}

  void
  parser::by_kind::clear ()
  {
    kind_ = symbol_kind::S_YYEMPTY;
  }

  void
  parser::by_kind::move (by_kind& that)
  {
    kind_ = that.kind_;
    that.clear ();
  }

  parser::symbol_kind_type
  parser::by_kind::kind () const YY_NOEXCEPT
  {
    return kind_;
  }

  parser::symbol_kind_type
  parser::by_kind::type_get () const YY_NOEXCEPT
  {
    return this->kind ();
  }


  // by_state.
  parser::by_state::by_state () YY_NOEXCEPT
    : state (empty_state)
  {}

  parser::by_state::by_state (const by_state& that) YY_NOEXCEPT
    : state (that.state)
  {}

  void
  parser::by_state::clear () YY_NOEXCEPT
  {
    state = empty_state;
  }

  void
  parser::by_state::move (by_state& that)
  {
    state = that.state;
    that.clear ();
  }

  parser::by_state::by_state (state_type s) YY_NOEXCEPT
    : state (s)
  {}

  parser::symbol_kind_type
  parser::by_state::kind () const YY_NOEXCEPT
  {
    if (state == empty_state)
      return symbol_kind::S_YYEMPTY;
    else
      return YY_CAST (symbol_kind_type, yystos_[+state]);
  }

  parser::stack_symbol_type::stack_symbol_type ()
  {}

  parser::stack_symbol_type::stack_symbol_type (YY_RVREF (stack_symbol_type) that)
    : super_type (YY_MOVE (that.state), YY_MOVE (that.value), YY_MOVE (that.location))
  {
#if 201103L <= YY_CPLUSPLUS
    // that is emptied.
    that.state = empty_state;
#endif
  }

  parser::stack_symbol_type::stack_symbol_type (state_type s, YY_MOVE_REF (symbol_type) that)
    : super_type (s, YY_MOVE (that.value), YY_MOVE (that.location))
  {
    // that is emptied.
    that.kind_ = symbol_kind::S_YYEMPTY;
  }

#if YY_CPLUSPLUS < 201103L
  parser::stack_symbol_type&
  parser::stack_symbol_type::operator= (const stack_symbol_type& that)
  {
    state = that.state;
    value = that.value;
    location = that.location;
    return *this;
  }

  parser::stack_symbol_type&
  parser::stack_symbol_type::operator= (stack_symbol_type& that)
  {
    state = that.state;
    value = that.value;
    location = that.location;
    // that is emptied.
    that.state = empty_state;
    return *this;
  }
#endif

  template <typename Base>
  void
  parser::yy_destroy_ (const char* yymsg, basic_symbol<Base>& yysym) const
  {
    if (yymsg)
      YY_SYMBOL_PRINT (yymsg, yysym);

    // User destructor.
    switch (yysym.kind ())
    {
      case 3: // NAME
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 374 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 4: // NUMBER
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 380 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 5: // STRING
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 386 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 6: // LEXERROR
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 392 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 48: // start
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 398 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 49: // unit
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 404 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 50: // alldefs
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 410 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 52: // classdef
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 416 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 53: // class_name
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 422 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 54: // parents
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 428 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 55: // parent_list
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 434 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 56: // parent
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 440 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 57: // maybe_class_funcs
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 446 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 58: // class_funcs
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 452 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 59: // funcdefs
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 458 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 60: // if_stmt
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 464 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 61: // if_and_elifs
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 470 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 62: // class_if_stmt
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 476 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 63: // class_if_and_elifs
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 482 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 64: // if_cond
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 488 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 65: // elif_cond
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 494 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 66: // else_cond
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 500 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 67: // condition
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 506 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 68: // version_tuple
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 512 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 69: // condition_op
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.str)); }
#line 518 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 70: // constantdef
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 524 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 71: // importdef
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 530 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 72: // import_items
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 536 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 73: // import_item
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 542 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 74: // import_name
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 548 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 75: // from_list
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 554 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 76: // from_items
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 560 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 77: // from_item
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 566 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 78: // alias_or_constant
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 572 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 79: // maybe_string_list
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 578 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 80: // string_list
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 584 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 81: // typevardef
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 590 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 82: // typevar_args
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 596 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 83: // typevar_kwargs
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 602 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 84: // typevar_kwarg
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 608 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 85: // funcdef
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 614 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 86: // funcname
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 620 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 87: // decorators
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 626 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 88: // decorator
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 632 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 89: // maybe_async
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 638 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 90: // params
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 644 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 91: // param_list
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 650 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 92: // param
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 656 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 93: // param_type
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 662 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 94: // param_default
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 668 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 95: // param_star_name
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 674 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 96: // return
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 680 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 98: // maybe_body
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 686 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 100: // body
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 692 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 101: // body_stmt
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 698 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 102: // type_parameters
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 704 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 103: // type_parameter
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 710 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 104: // maybe_type_list
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 716 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 105: // type_list
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 722 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 106: // type
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 728 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 107: // named_tuple_fields
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 734 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 108: // named_tuple_field_list
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 740 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 109: // named_tuple_field
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 746 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 111: // coll_named_tuple_fields
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 752 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 112: // coll_named_tuple_field_list
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 758 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 113: // coll_named_tuple_field
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 764 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 114: // type_tuple_elements
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 770 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 115: // type_tuple_literal
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 776 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 116: // dotted_name
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 782 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 117: // getitem_key
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 788 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 118: // maybe_number
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 794 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      default:
        break;
    }
  }

#if PYTYPEDEBUG
  template <typename Base>
  void
  parser::yy_print_ (std::ostream& yyo, const basic_symbol<Base>& yysym) const
  {
    std::ostream& yyoutput = yyo;
    YYUSE (yyoutput);
    if (yysym.empty ())
      yyo << "empty symbol";
    else
      {
        symbol_kind_type yykind = yysym.kind ();
        yyo << (yykind < YYNTOKENS ? "token" : "nterm")
            << ' ' << yysym.name () << " ("
            << yysym.location << ": ";
        YYUSE (yykind);
        yyo << ')';
      }
  }
#endif

  void
  parser::yypush_ (const char* m, YY_MOVE_REF (stack_symbol_type) sym)
  {
    if (m)
      YY_SYMBOL_PRINT (m, sym);
    yystack_.push (YY_MOVE (sym));
  }

  void
  parser::yypush_ (const char* m, state_type s, YY_MOVE_REF (symbol_type) sym)
  {
#if 201103L <= YY_CPLUSPLUS
    yypush_ (m, stack_symbol_type (s, std::move (sym)));
#else
    stack_symbol_type ss (s, sym);
    yypush_ (m, ss);
#endif
  }

  void
  parser::yypop_ (int n)
  {
    yystack_.pop (n);
  }

#if PYTYPEDEBUG
  std::ostream&
  parser::debug_stream () const
  {
    return *yycdebug_;
  }

  void
  parser::set_debug_stream (std::ostream& o)
  {
    yycdebug_ = &o;
  }


  parser::debug_level_type
  parser::debug_level () const
  {
    return yydebug_;
  }

  void
  parser::set_debug_level (debug_level_type l)
  {
    yydebug_ = l;
  }
#endif // PYTYPEDEBUG

  parser::state_type
  parser::yy_lr_goto_state_ (state_type yystate, int yysym)
  {
    int yyr = yypgoto_[yysym - YYNTOKENS] + yystate;
    if (0 <= yyr && yyr <= yylast_ && yycheck_[yyr] == yystate)
      return yytable_[yyr];
    else
      return yydefgoto_[yysym - YYNTOKENS];
  }

  bool
  parser::yy_pact_value_is_default_ (int yyvalue)
  {
    return yyvalue == yypact_ninf_;
  }

  bool
  parser::yy_table_value_is_error_ (int yyvalue)
  {
    return yyvalue == yytable_ninf_;
  }

  int
  parser::operator() ()
  {
    return parse ();
  }

  int
  parser::parse ()
  {
    int yyn;
    /// Length of the RHS of the rule being reduced.
    int yylen = 0;

    // Error handling.
    int yynerrs_ = 0;
    int yyerrstatus_ = 0;

    /// The lookahead symbol.
    symbol_type yyla;

    /// The locations where the error started and ended.
    stack_symbol_type yyerror_range[3];

    /// The return value of parse ().
    int yyresult;

#if YY_EXCEPTIONS
    try
#endif // YY_EXCEPTIONS
      {
    YYCDEBUG << "Starting parse\n";


    /* Initialize the stack.  The initial state will be set in
       yynewstate, since the latter expects the semantical and the
       location values to have been already stored, initialize these
       stacks with a primary value.  */
    yystack_.clear ();
    yypush_ (YY_NULLPTR, 0, YY_MOVE (yyla));

  /*-----------------------------------------------.
  | yynewstate -- push a new symbol on the stack.  |
  `-----------------------------------------------*/
  yynewstate:
    YYCDEBUG << "Entering state " << int (yystack_[0].state) << '\n';
    YY_STACK_PRINT ();

    // Accept?
    if (yystack_[0].state == yyfinal_)
      YYACCEPT;

    goto yybackup;


  /*-----------.
  | yybackup.  |
  `-----------*/
  yybackup:
    // Try to take a decision without lookahead.
    yyn = yypact_[+yystack_[0].state];
    if (yy_pact_value_is_default_ (yyn))
      goto yydefault;

    // Read a lookahead token.
    if (yyla.empty ())
      {
        YYCDEBUG << "Reading a token\n";
#if YY_EXCEPTIONS
        try
#endif // YY_EXCEPTIONS
          {
            yyla.kind_ = yytranslate_ (yylex (&yyla.value, &yyla.location, scanner));
          }
#if YY_EXCEPTIONS
        catch (const syntax_error& yyexc)
          {
            YYCDEBUG << "Caught exception: " << yyexc.what() << '\n';
            error (yyexc);
            goto yyerrlab1;
          }
#endif // YY_EXCEPTIONS
      }
    YY_SYMBOL_PRINT ("Next token is", yyla);

    if (yyla.kind () == symbol_kind::S_YYerror)
    {
      // The scanner already issued an error message, process directly
      // to error recovery.  But do not keep the error token as
      // lookahead, it is too special and may lead us to an endless
      // loop in error recovery. */
      yyla.kind_ = symbol_kind::S_YYUNDEF;
      goto yyerrlab1;
    }

    /* If the proper action on seeing token YYLA.TYPE is to reduce or
       to detect an error, take that action.  */
    yyn += yyla.kind ();
    if (yyn < 0 || yylast_ < yyn || yycheck_[yyn] != yyla.kind ())
      {
        goto yydefault;
      }

    // Reduce or error.
    yyn = yytable_[yyn];
    if (yyn <= 0)
      {
        if (yy_table_value_is_error_ (yyn))
          goto yyerrlab;
        yyn = -yyn;
        goto yyreduce;
      }

    // Count tokens shifted since error; after three, turn off error status.
    if (yyerrstatus_)
      --yyerrstatus_;

    // Shift the lookahead token.
    yypush_ ("Shifting", state_type (yyn), YY_MOVE (yyla));
    goto yynewstate;


  /*-----------------------------------------------------------.
  | yydefault -- do the default action for the current state.  |
  `-----------------------------------------------------------*/
  yydefault:
    yyn = yydefact_[+yystack_[0].state];
    if (yyn == 0)
      goto yyerrlab;
    goto yyreduce;


  /*-----------------------------.
  | yyreduce -- do a reduction.  |
  `-----------------------------*/
  yyreduce:
    yylen = yyr2_[yyn];
    {
      stack_symbol_type yylhs;
      yylhs.state = yy_lr_goto_state_ (yystack_[yylen].state, yyr1_[yyn]);
      /* If YYLEN is nonzero, implement the default value of the
         action: '$$ = $1'.  Otherwise, use the top of the stack.

         Otherwise, the following line sets YYLHS.VALUE to garbage.
         This behavior is undocumented and Bison users should not rely
         upon it.  */
      if (yylen)
        yylhs.value = yystack_[yylen - 1].value;
      else
        yylhs.value = yystack_[0].value;

      // Default location.
      {
        stack_type::slice range (yystack_, yylen);
        YYLLOC_DEFAULT (yylhs.location, range, yylen);
        yyerror_range[1].location = yylhs.location;
      }

      // Perform the reduction.
      YY_REDUCE_PRINT (yyn);
#if YY_EXCEPTIONS
      try
#endif // YY_EXCEPTIONS
        {
          switch (yyn)
            {
  case 2:
#line 134 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
             { ctx->SetAndDelResult((yystack_[1].value.obj)); (yylhs.value.obj) = NULL; }
#line 1065 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 3:
#line 135 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                          { ctx->SetAndDelResult((yystack_[1].value.obj)); (yylhs.value.obj) = NULL; }
#line 1071 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 4:
#line 139 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1077 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 5:
#line 143 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                        { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1083 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 6:
#line 144 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1089 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 7:
#line 145 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                      { (yylhs.value.obj) = (yystack_[1].value.obj); Py_DECREF((yystack_[0].value.obj)); }
#line 1095 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 8:
#line 146 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                              {
      (yylhs.value.obj) = (yystack_[1].value.obj);
      PyObject* tmp = ctx->Call(kAddAliasOrConstant, "(N)", (yystack_[0].value.obj));
      CHECK(tmp, yylhs.location);
      Py_DECREF(tmp);
    }
#line 1106 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 9:
#line 152 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                     { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1112 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 10:
#line 153 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                       { (yylhs.value.obj) = (yystack_[1].value.obj); Py_DECREF((yystack_[0].value.obj)); }
#line 1118 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 11:
#line 154 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    {
      PyObject* tmp = ctx->Call(kIfEnd, "(N)", (yystack_[0].value.obj));
      CHECK(tmp, yystack_[0].location);
      (yylhs.value.obj) = ExtendList((yystack_[1].value.obj), tmp);
    }
#line 1128 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 12:
#line 159 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = PyList_New(0); }
#line 1134 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 15:
#line 172 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    {
      (yylhs.value.obj) = ctx->Call(kNewClass, "(NNNN)", (yystack_[6].value.obj), (yystack_[4].value.obj), (yystack_[3].value.obj), (yystack_[0].value.obj));
      // Fix location tracking. See funcdef.
      yylhs.location.begin = yystack_[4].location.begin;
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1145 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 16:
#line 181 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
         {
      // Do not borrow the $1 reference since it is also returned later
      // in $$.  Use O instead of N in the format string.
      PyObject* tmp = ctx->Call(kRegisterClassName, "(O)", (yystack_[0].value.obj));
      CHECK(tmp, yylhs.location);
      Py_DECREF(tmp);
      (yylhs.value.obj) = (yystack_[0].value.obj);
    }
#line 1158 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 17:
#line 192 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                        { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1164 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 18:
#line 193 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
            { (yylhs.value.obj) = PyList_New(0); }
#line 1170 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 19:
#line 194 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                 { (yylhs.value.obj) = PyList_New(0); }
#line 1176 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 20:
#line 198 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                           { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1182 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 21:
#line 199 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
           { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 1188 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 22:
#line 203 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
         { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1194 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 23:
#line 204 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                  { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1200 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 24:
#line 205 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
               { (yylhs.value.obj) = PyString_FromString("NamedTuple"); }
#line 1206 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 25:
#line 209 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                       { (yylhs.value.obj) = PyList_New(0); }
#line 1212 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 26:
#line 210 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                              { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1218 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 27:
#line 211 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                           { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1224 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 28:
#line 215 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                     { (yylhs.value.obj) = PyList_New(0); }
#line 1230 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 29:
#line 216 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1236 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 30:
#line 220 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                         { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1242 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 31:
#line 221 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                               {
      PyObject* tmp = ctx->Call(kNewAliasOrConstant, "(N)", (yystack_[0].value.obj));
      CHECK(tmp, yylhs.location);
      (yylhs.value.obj) = AppendList((yystack_[1].value.obj), tmp);
    }
#line 1252 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 32:
#line 226 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                     { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1258 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 33:
#line 227 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                           {
      PyObject* tmp = ctx->Call(kIfEnd, "(N)", (yystack_[0].value.obj));
      CHECK(tmp, yystack_[0].location);
      (yylhs.value.obj) = ExtendList((yystack_[1].value.obj), tmp);
    }
#line 1268 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 34:
#line 232 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                      { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1274 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 35:
#line 233 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                { (yylhs.value.obj) = PyList_New(0); }
#line 1280 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 36:
#line 238 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                     {
      (yylhs.value.obj) = AppendList((yystack_[5].value.obj), Py_BuildValue("(NN)", (yystack_[4].value.obj), (yystack_[1].value.obj)));
    }
#line 1288 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 37:
#line 241 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1294 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 38:
#line 246 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                      {
      (yylhs.value.obj) = Py_BuildValue("[(NN)]", (yystack_[4].value.obj), (yystack_[1].value.obj));
    }
#line 1302 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 39:
#line 250 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                     {
      (yylhs.value.obj) = AppendList((yystack_[5].value.obj), Py_BuildValue("(NN)", (yystack_[4].value.obj), (yystack_[1].value.obj)));
    }
#line 1310 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 40:
#line 263 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                            {
      (yylhs.value.obj) = AppendList((yystack_[5].value.obj), Py_BuildValue("(NN)", (yystack_[4].value.obj), (yystack_[1].value.obj)));
    }
#line 1318 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 41:
#line 266 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1324 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 42:
#line 271 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                       {
      (yylhs.value.obj) = Py_BuildValue("[(NN)]", (yystack_[4].value.obj), (yystack_[1].value.obj));
    }
#line 1332 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 43:
#line 275 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                            {
      (yylhs.value.obj) = AppendList((yystack_[5].value.obj), Py_BuildValue("(NN)", (yystack_[4].value.obj), (yystack_[1].value.obj)));
    }
#line 1340 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 44:
#line 287 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                 { (yylhs.value.obj) = ctx->Call(kIfBegin, "(N)", (yystack_[0].value.obj)); CHECK((yylhs.value.obj), yylhs.location); }
#line 1346 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 45:
#line 291 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                   { (yylhs.value.obj) = ctx->Call(kIfElif, "(N)", (yystack_[0].value.obj)); CHECK((yylhs.value.obj), yylhs.location); }
#line 1352 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 46:
#line 295 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
         { (yylhs.value.obj) = ctx->Call(kIfElse, "()"); CHECK((yylhs.value.obj), yylhs.location); }
#line 1358 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 47:
#line 299 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                    {
      (yylhs.value.obj) = Py_BuildValue("((NO)sN)", (yystack_[2].value.obj), Py_None, (yystack_[1].value.str), (yystack_[0].value.obj));
    }
#line 1366 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 48:
#line 302 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                           {
      (yylhs.value.obj) = Py_BuildValue("((NO)sN)", (yystack_[2].value.obj), Py_None, (yystack_[1].value.str), (yystack_[0].value.obj));
    }
#line 1374 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 49:
#line 305 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                        {
      (yylhs.value.obj) = Py_BuildValue("((NN)sN)", (yystack_[5].value.obj), (yystack_[3].value.obj), (yystack_[1].value.str), (yystack_[0].value.obj));
    }
#line 1382 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 50:
#line 308 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                               {
      (yylhs.value.obj) = Py_BuildValue("((NN)sN)", (yystack_[5].value.obj), (yystack_[3].value.obj), (yystack_[1].value.str), (yystack_[0].value.obj));
    }
#line 1390 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 51:
#line 311 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                            { (yylhs.value.obj) = Py_BuildValue("(NsN)", (yystack_[2].value.obj), "and", (yystack_[0].value.obj)); }
#line 1396 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 52:
#line 312 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                           { (yylhs.value.obj) = Py_BuildValue("(NsN)", (yystack_[2].value.obj), "or", (yystack_[0].value.obj)); }
#line 1402 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 53:
#line 313 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                      { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1408 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 54:
#line 317 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                       { (yylhs.value.obj) = Py_BuildValue("(N)", (yystack_[2].value.obj)); }
#line 1414 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 55:
#line 318 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                              { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[3].value.obj), (yystack_[1].value.obj)); }
#line 1420 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 56:
#line 319 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                         {
      (yylhs.value.obj) = Py_BuildValue("(NNN)", (yystack_[5].value.obj), (yystack_[3].value.obj), (yystack_[1].value.obj));
    }
#line 1428 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 57:
#line 325 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { (yylhs.value.str) = "<"; }
#line 1434 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 58:
#line 326 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { (yylhs.value.str) = ">"; }
#line 1440 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 59:
#line 327 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { (yylhs.value.str) = "<="; }
#line 1446 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 60:
#line 328 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { (yylhs.value.str) = ">="; }
#line 1452 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 61:
#line 329 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { (yylhs.value.str) = "=="; }
#line 1458 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 62:
#line 330 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { (yylhs.value.str) = "!="; }
#line 1464 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 63:
#line 334 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1473 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 64:
#line 338 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1482 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 65:
#line 342 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1491 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 66:
#line 346 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                      {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", (yystack_[2].value.obj), ctx->Value(kAnything));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1500 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 67:
#line 350 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                         {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", (yystack_[5].value.obj), (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1509 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 68:
#line 354 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                    {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", (yystack_[3].value.obj), (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1518 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 69:
#line 358 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                 {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", (yystack_[5].value.obj), (yystack_[3].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1527 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 70:
#line 365 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                          {
      (yylhs.value.obj) = ctx->Call(kAddImport, "(ON)", Py_None, (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1536 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 71:
#line 369 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                        {
      (yylhs.value.obj) = ctx->Call(kAddImport, "(NN)", (yystack_[3].value.obj), (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1545 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 72:
#line 373 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                {
      // Special-case "from . import" and pass in a __PACKAGE__ token that
      // the Python parser code will rewrite to the current package name.
      (yylhs.value.obj) = ctx->Call(kAddImport, "(sN)", "__PACKAGE__", (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1556 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 73:
#line 379 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                    {
      // Special-case "from .. import" and pass in a __PARENT__ token that
      // the Python parser code will rewrite to the parent package name.
      (yylhs.value.obj) = ctx->Call(kAddImport, "(sN)", "__PARENT__", (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1567 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 74:
#line 388 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                 { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1573 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 75:
#line 389 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 1579 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 76:
#line 393 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1585 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 77:
#line 394 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                        { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1591 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 78:
#line 399 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1597 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 79:
#line 400 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    {
      (yylhs.value.obj) = PyString_FromFormat(".%s", PyString_AsString((yystack_[0].value.obj)));
      Py_DECREF((yystack_[0].value.obj));
    }
#line 1606 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 80:
#line 407 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1612 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 81:
#line 408 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                       { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1618 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 82:
#line 409 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                           { (yylhs.value.obj) = (yystack_[2].value.obj); }
#line 1624 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 83:
#line 413 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                             { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1630 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 84:
#line 414 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
              { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 1636 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 85:
#line 418 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1642 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 86:
#line 419 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
               {
      (yylhs.value.obj) = PyString_FromString("NamedTuple");
    }
#line 1650 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 87:
#line 422 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    {
      (yylhs.value.obj) = PyString_FromString("namedtuple");
    }
#line 1658 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 88:
#line 425 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
            {
      (yylhs.value.obj) = PyString_FromString("TypeVar");
    }
#line 1666 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 89:
#line 428 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        {
      (yylhs.value.obj) = PyString_FromString("*");
    }
#line 1674 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 90:
#line 431 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                 { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1680 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 91:
#line 435 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                  { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1686 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 92:
#line 436 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                       { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[4].value.obj), (yystack_[1].value.obj)); }
#line 1692 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 93:
#line 440 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                            { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1698 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 94:
#line 441 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                { (yylhs.value.obj) = PyList_New(0); }
#line 1704 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 95:
#line 445 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                           { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1710 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 96:
#line 446 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
           { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 1716 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 97:
#line 450 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                 {
      (yylhs.value.obj) = ctx->Call(kAddTypeVar, "(NNN)", (yystack_[6].value.obj), (yystack_[2].value.obj), (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1725 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 98:
#line 457 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                { (yylhs.value.obj) = Py_BuildValue("(OO)", Py_None, Py_None); }
#line 1731 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 99:
#line 458 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                  { (yylhs.value.obj) = Py_BuildValue("(NO)", (yystack_[0].value.obj), Py_None); }
#line 1737 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 100:
#line 459 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                       { (yylhs.value.obj) = Py_BuildValue("(ON)", Py_None, (yystack_[0].value.obj)); }
#line 1743 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 101:
#line 460 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                     { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1749 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 102:
#line 464 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                     { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1755 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 103:
#line 465 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                  { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 1761 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 104:
#line 469 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                  { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1767 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 105:
#line 471 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1773 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 106:
#line 476 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
               {
      (yylhs.value.obj) = ctx->Call(kNewFunction, "(NONNNN)", (yystack_[9].value.obj), (yystack_[8].value.obj), (yystack_[6].value.obj), (yystack_[3].value.obj), (yystack_[1].value.obj), (yystack_[0].value.obj));
      // Decorators is nullable and messes up the location tracking by
      // using the previous symbol as the start location for this production,
      // which is very misleading.  It is better to ignore decorators and
      // pretend the production started with DEF.  Even when decorators are
      // present the error line will be close enough to be helpful.
      yylhs.location.begin = yystack_[7].location.begin;
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1788 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 107:
#line 489 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
         { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1794 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 108:
#line 490 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { (yylhs.value.obj) = PyString_FromString("namedtuple"); }
#line 1800 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 109:
#line 494 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                         { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1806 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 110:
#line 495 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                { (yylhs.value.obj) = PyList_New(0); }
#line 1812 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 111:
#line 499 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                      { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1818 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 112:
#line 503 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
          { (yylhs.value.obj) = Py_True; }
#line 1824 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 113:
#line 504 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                { (yylhs.value.obj) = Py_False; }
#line 1830 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 114:
#line 508 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                           { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1836 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 115:
#line 509 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                { (yylhs.value.obj) = PyList_New(0); }
#line 1842 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 116:
#line 521 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                           { (yylhs.value.obj) = AppendList((yystack_[3].value.obj), (yystack_[0].value.obj)); }
#line 1848 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 117:
#line 522 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
          { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 1854 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 118:
#line 526 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                  { (yylhs.value.obj) = Py_BuildValue("(NNN)", (yystack_[2].value.obj), (yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1860 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 119:
#line 527 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { (yylhs.value.obj) = Py_BuildValue("(sOO)", "*", Py_None, Py_None); }
#line 1866 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 120:
#line 528 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                               { (yylhs.value.obj) = Py_BuildValue("(NNO)", (yystack_[1].value.obj), (yystack_[0].value.obj), Py_None); }
#line 1872 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 121:
#line 529 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
             { (yylhs.value.obj) = ctx->Value(kEllipsis); }
#line 1878 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 122:
#line 533 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
             { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1884 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 123:
#line 534 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                { Py_INCREF(Py_None); (yylhs.value.obj) = Py_None; }
#line 1890 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 124:
#line 538 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
             { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1896 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 125:
#line 539 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
               { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1902 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 126:
#line 540 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                 { (yylhs.value.obj) = ctx->Value(kEllipsis); }
#line 1908 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 127:
#line 541 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { Py_INCREF(Py_None); (yylhs.value.obj) = Py_None; }
#line 1914 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 128:
#line 545 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
             { (yylhs.value.obj) = PyString_FromFormat("*%s", PyString_AsString((yystack_[0].value.obj))); }
#line 1920 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 129:
#line 546 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                 { (yylhs.value.obj) = PyString_FromFormat("**%s", PyString_AsString((yystack_[0].value.obj))); }
#line 1926 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 130:
#line 550 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
               { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1932 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 131:
#line 551 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                { (yylhs.value.obj) = ctx->Value(kAnything); }
#line 1938 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 132:
#line 555 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                     { Py_DecRef((yystack_[0].value.obj)); }
#line 1944 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 133:
#line 559 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                      { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1950 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 134:
#line 560 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                           { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1956 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 135:
#line 561 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
               { (yylhs.value.obj) = PyList_New(0); }
#line 1962 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 143:
#line 575 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                   { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1968 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 144:
#line 576 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
              { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 1974 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 145:
#line 580 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                  { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1980 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 146:
#line 581 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
               { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1986 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 147:
#line 582 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                       { (yylhs.value.obj) = (yystack_[2].value.obj); }
#line 1992 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 148:
#line 586 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                       { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1998 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 149:
#line 587 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                   { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 2004 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 150:
#line 591 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
         { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 2010 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 151:
#line 592 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
             { (yylhs.value.obj) = ctx->Value(kEllipsis); }
#line 2016 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 152:
#line 594 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
           { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 2022 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 153:
#line 595 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
           { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 2028 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 154:
#line 597 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                            {
      (yylhs.value.obj) = ctx->Call(kNewType, "(sN)", "tuple", (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 2037 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 155:
#line 604 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                          { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 2043 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 156:
#line 605 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                { (yylhs.value.obj) = PyList_New(0); }
#line 2049 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 157:
#line 609 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                       { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 2055 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 158:
#line 610 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
         { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 2061 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 159:
#line 614 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                {
      (yylhs.value.obj) = ctx->Call(kNewType, "(N)", (yystack_[0].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 2070 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 160:
#line 618 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                {
      (yylhs.value.obj) = ctx->Call(kNewType, "(NN)", (yystack_[4].value.obj), PyList_New(0));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 2079 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 161:
#line 622 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                    {
      (yylhs.value.obj) = ctx->Call(kNewType, "(NN)", (yystack_[4].value.obj), (yystack_[2].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 2088 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 162:
#line 626 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                                 {
      (yylhs.value.obj) = ctx->Call(kNewNamedTuple, "(NN)", (yystack_[4].value.obj), (yystack_[2].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 2097 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 163:
#line 630 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                                           {
      (yylhs.value.obj) = ctx->Call(kNewNamedTuple, "(NN)", (yystack_[4].value.obj), (yystack_[2].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 2106 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 164:
#line 634 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                 { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 2112 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 165:
#line 635 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                  { (yylhs.value.obj) = ctx->Call(kNewIntersectionType, "([NN])", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 2118 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 166:
#line 636 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                 { (yylhs.value.obj) = ctx->Call(kNewUnionType, "([NN])", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 2124 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 167:
#line 637 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { (yylhs.value.obj) = ctx->Value(kAnything); }
#line 2130 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 168:
#line 638 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
            { (yylhs.value.obj) = ctx->Value(kNothing); }
#line 2136 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 169:
#line 642 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                               { (yylhs.value.obj) = (yystack_[2].value.obj); }
#line 2142 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 170:
#line 643 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
            { (yylhs.value.obj) = PyList_New(0); }
#line 2148 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 171:
#line 647 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                 { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 2154 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 172:
#line 648 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                      { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 2160 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 173:
#line 652 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                         { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[4].value.obj), (yystack_[2].value.obj)); }
#line 2166 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 176:
#line 661 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                    { (yylhs.value.obj) = (yystack_[2].value.obj); }
#line 2172 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 177:
#line 662 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
            { (yylhs.value.obj) = PyList_New(0); }
#line 2178 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 178:
#line 666 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                           {
      (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj));
    }
#line 2186 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 179:
#line 669 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                           { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 2192 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 180:
#line 673 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
           { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[0].value.obj), ctx->Value(kAnything)); }
#line 2198 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 181:
#line 680 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                 { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 2204 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 182:
#line 681 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                  { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 2210 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 183:
#line 690 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                            {
      Py_DECREF((yystack_[2].value.obj));
      (yylhs.value.obj) = ctx->Value(kTuple);
    }
#line 2219 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 184:
#line 695 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                     {
      Py_DECREF((yystack_[2].value.obj));
      (yylhs.value.obj) = ctx->Value(kTuple);
    }
#line 2228 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 185:
#line 701 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
             {
      Py_DECREF((yystack_[1].value.obj));
      (yylhs.value.obj) = ctx->Value(kTuple);
    }
#line 2237 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 186:
#line 708 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
         { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 2243 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 187:
#line 709 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                         {
#if PY_MAJOR_VERSION >= 3
      (yystack_[2].value.obj) = PyUnicode_Concat((yystack_[2].value.obj), DOT_STRING);
      (yystack_[2].value.obj) = PyUnicode_Concat((yystack_[2].value.obj), (yystack_[0].value.obj));
      Py_DECREF((yystack_[0].value.obj));
#else
      PyString_Concat(&(yystack_[2].value.obj), DOT_STRING);
      PyString_ConcatAndDel(&(yystack_[2].value.obj), (yystack_[0].value.obj));
#endif
      (yylhs.value.obj) = (yystack_[2].value.obj);
    }
#line 2259 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 188:
#line 723 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
           { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 2265 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 189:
#line 724 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                  {
      PyObject* slice = PySlice_New((yystack_[2].value.obj), (yystack_[0].value.obj), NULL);
      CHECK(slice, yylhs.location);
      (yylhs.value.obj) = slice;
    }
#line 2275 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 190:
#line 729 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                   {
      PyObject* slice = PySlice_New((yystack_[4].value.obj), (yystack_[2].value.obj), (yystack_[0].value.obj));
      CHECK(slice, yylhs.location);
      (yylhs.value.obj) = slice;
    }
#line 2285 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 191:
#line 737 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
           { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 2291 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 192:
#line 738 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                { (yylhs.value.obj) = NULL; }
#line 2297 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;


#line 2301 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"

            default:
              break;
            }
        }
#if YY_EXCEPTIONS
      catch (const syntax_error& yyexc)
        {
          YYCDEBUG << "Caught exception: " << yyexc.what() << '\n';
          error (yyexc);
          YYERROR;
        }
#endif // YY_EXCEPTIONS
      YY_SYMBOL_PRINT ("-> $$ =", yylhs);
      yypop_ (yylen);
      yylen = 0;

      // Shift the result of the reduction.
      yypush_ (YY_NULLPTR, YY_MOVE (yylhs));
    }
    goto yynewstate;


  /*--------------------------------------.
  | yyerrlab -- here on detecting error.  |
  `--------------------------------------*/
  yyerrlab:
    // If not already recovering from an error, report this error.
    if (!yyerrstatus_)
      {
        ++yynerrs_;
        context yyctx (*this, yyla);
        std::string msg = yysyntax_error_ (yyctx);
        error (yyla.location, YY_MOVE (msg));
      }


    yyerror_range[1].location = yyla.location;
    if (yyerrstatus_ == 3)
      {
        /* If just tried and failed to reuse lookahead token after an
           error, discard it.  */

        // Return failure if at end of input.
        if (yyla.kind () == symbol_kind::S_YYEOF)
          YYABORT;
        else if (!yyla.empty ())
          {
            yy_destroy_ ("Error: discarding", yyla);
            yyla.clear ();
          }
      }

    // Else will try to reuse lookahead token after shifting the error token.
    goto yyerrlab1;


  /*---------------------------------------------------.
  | yyerrorlab -- error raised explicitly by YYERROR.  |
  `---------------------------------------------------*/
  yyerrorlab:
    /* Pacify compilers when the user code never invokes YYERROR and
       the label yyerrorlab therefore never appears in user code.  */
    if (false)
      YYERROR;

    /* Do not reclaim the symbols of the rule whose action triggered
       this YYERROR.  */
    yypop_ (yylen);
    yylen = 0;
    YY_STACK_PRINT ();
    goto yyerrlab1;


  /*-------------------------------------------------------------.
  | yyerrlab1 -- common code for both syntax error and YYERROR.  |
  `-------------------------------------------------------------*/
  yyerrlab1:
    yyerrstatus_ = 3;   // Each real token shifted decrements this.
    // Pop stack until we find a state that shifts the error token.
    for (;;)
      {
        yyn = yypact_[+yystack_[0].state];
        if (!yy_pact_value_is_default_ (yyn))
          {
            yyn += symbol_kind::S_YYerror;
            if (0 <= yyn && yyn <= yylast_
                && yycheck_[yyn] == symbol_kind::S_YYerror)
              {
                yyn = yytable_[yyn];
                if (0 < yyn)
                  break;
              }
          }

        // Pop the current state because it cannot handle the error token.
        if (yystack_.size () == 1)
          YYABORT;

        yyerror_range[1].location = yystack_[0].location;
        yy_destroy_ ("Error: popping", yystack_[0]);
        yypop_ ();
        YY_STACK_PRINT ();
      }
    {
      stack_symbol_type error_token;

      yyerror_range[2].location = yyla.location;
      YYLLOC_DEFAULT (error_token.location, yyerror_range, 2);

      // Shift the error token.
      error_token.state = state_type (yyn);
      yypush_ ("Shifting", YY_MOVE (error_token));
    }
    goto yynewstate;


  /*-------------------------------------.
  | yyacceptlab -- YYACCEPT comes here.  |
  `-------------------------------------*/
  yyacceptlab:
    yyresult = 0;
    goto yyreturn;


  /*-----------------------------------.
  | yyabortlab -- YYABORT comes here.  |
  `-----------------------------------*/
  yyabortlab:
    yyresult = 1;
    goto yyreturn;


  /*-----------------------------------------------------.
  | yyreturn -- parsing is finished, return the result.  |
  `-----------------------------------------------------*/
  yyreturn:
    if (!yyla.empty ())
      yy_destroy_ ("Cleanup: discarding lookahead", yyla);

    /* Do not reclaim the symbols of the rule whose action triggered
       this YYABORT or YYACCEPT.  */
    yypop_ (yylen);
    YY_STACK_PRINT ();
    while (1 < yystack_.size ())
      {
        yy_destroy_ ("Cleanup: popping", yystack_[0]);
        yypop_ ();
      }

    return yyresult;
  }
#if YY_EXCEPTIONS
    catch (...)
      {
        YYCDEBUG << "Exception caught: cleaning lookahead and stack\n";
        // Do not try to display the values of the reclaimed symbols,
        // as their printers might throw an exception.
        if (!yyla.empty ())
          yy_destroy_ (YY_NULLPTR, yyla);

        while (1 < yystack_.size ())
          {
            yy_destroy_ (YY_NULLPTR, yystack_[0]);
            yypop_ ();
          }
        throw;
      }
#endif // YY_EXCEPTIONS
  }

  void
  parser::error (const syntax_error& yyexc)
  {
    error (yyexc.location, yyexc.what ());
  }

  /* Return YYSTR after stripping away unnecessary quotes and
     backslashes, so that it's suitable for yyerror.  The heuristic is
     that double-quoting is unnecessary unless the string contains an
     apostrophe, a comma, or backslash (other than backslash-backslash).
     YYSTR is taken from yytname.  */
  std::string
  parser::yytnamerr_ (const char *yystr)
  {
    if (*yystr == '"')
      {
        std::string yyr;
        char const *yyp = yystr;

        for (;;)
          switch (*++yyp)
            {
            case '\'':
            case ',':
              goto do_not_strip_quotes;

            case '\\':
              if (*++yyp != '\\')
                goto do_not_strip_quotes;
              else
                goto append;

            append:
            default:
              yyr += *yyp;
              break;

            case '"':
              return yyr;
            }
      do_not_strip_quotes: ;
      }

    return yystr;
  }

  std::string
  parser::symbol_name (symbol_kind_type yysymbol)
  {
    return yytnamerr_ (yytname_[yysymbol]);
  }



  // parser::context.
  parser::context::context (const parser& yyparser, const symbol_type& yyla)
    : yyparser_ (yyparser)
    , yyla_ (yyla)
  {}

  int
  parser::context::expected_tokens (symbol_kind_type yyarg[], int yyargn) const
  {
    // Actual number of expected tokens
    int yycount = 0;

    int yyn = yypact_[+yyparser_.yystack_[0].state];
    if (!yy_pact_value_is_default_ (yyn))
      {
        /* Start YYX at -YYN if negative to avoid negative indexes in
           YYCHECK.  In other words, skip the first -YYN actions for
           this state because they are default actions.  */
        int yyxbegin = yyn < 0 ? -yyn : 0;
        // Stay within bounds of both yycheck and yytname.
        int yychecklim = yylast_ - yyn + 1;
        int yyxend = yychecklim < YYNTOKENS ? yychecklim : YYNTOKENS;
        for (int yyx = yyxbegin; yyx < yyxend; ++yyx)
          if (yycheck_[yyx + yyn] == yyx && yyx != symbol_kind::S_YYerror
              && !yy_table_value_is_error_ (yytable_[yyx + yyn]))
            {
              if (!yyarg)
                ++yycount;
              else if (yycount == yyargn)
                return 0;
              else
                yyarg[yycount++] = YY_CAST (symbol_kind_type, yyx);
            }
      }

    if (yyarg && yycount == 0 && 0 < yyargn)
      yyarg[0] = symbol_kind::S_YYEMPTY;
    return yycount;
  }



  int
  parser::yy_syntax_error_arguments_ (const context& yyctx,
                                                 symbol_kind_type yyarg[], int yyargn) const
  {
    /* There are many possibilities here to consider:
       - If this state is a consistent state with a default action, then
         the only way this function was invoked is if the default action
         is an error action.  In that case, don't check for expected
         tokens because there are none.
       - The only way there can be no lookahead present (in yyla) is
         if this state is a consistent state with a default action.
         Thus, detecting the absence of a lookahead is sufficient to
         determine that there is no unexpected or expected token to
         report.  In that case, just report a simple "syntax error".
       - Don't assume there isn't a lookahead just because this state is
         a consistent state with a default action.  There might have
         been a previous inconsistent state, consistent state with a
         non-default action, or user semantic action that manipulated
         yyla.  (However, yyla is currently not documented for users.)
       - Of course, the expected token list depends on states to have
         correct lookahead information, and it depends on the parser not
         to perform extra reductions after fetching a lookahead from the
         scanner and before detecting a syntax error.  Thus, state merging
         (from LALR or IELR) and default reductions corrupt the expected
         token list.  However, the list is correct for canonical LR with
         one exception: it will still contain any token that will not be
         accepted due to an error action in a later state.
    */

    if (!yyctx.lookahead ().empty ())
      {
        if (yyarg)
          yyarg[0] = yyctx.token ();
        int yyn = yyctx.expected_tokens (yyarg ? yyarg + 1 : yyarg, yyargn - 1);
        return yyn + 1;
      }
    return 0;
  }

  // Generate an error message.
  std::string
  parser::yysyntax_error_ (const context& yyctx) const
  {
    // Its maximum.
    enum { YYARGS_MAX = 5 };
    // Arguments of yyformat.
    symbol_kind_type yyarg[YYARGS_MAX];
    int yycount = yy_syntax_error_arguments_ (yyctx, yyarg, YYARGS_MAX);

    char const* yyformat = YY_NULLPTR;
    switch (yycount)
      {
#define YYCASE_(N, S)                         \
        case N:                               \
          yyformat = S;                       \
        break
      default: // Avoid compiler warnings.
        YYCASE_ (0, YY_("syntax error"));
        YYCASE_ (1, YY_("syntax error, unexpected %s"));
        YYCASE_ (2, YY_("syntax error, unexpected %s, expecting %s"));
        YYCASE_ (3, YY_("syntax error, unexpected %s, expecting %s or %s"));
        YYCASE_ (4, YY_("syntax error, unexpected %s, expecting %s or %s or %s"));
        YYCASE_ (5, YY_("syntax error, unexpected %s, expecting %s or %s or %s or %s"));
#undef YYCASE_
      }

    std::string yyres;
    // Argument number.
    std::ptrdiff_t yyi = 0;
    for (char const* yyp = yyformat; *yyp; ++yyp)
      if (yyp[0] == '%' && yyp[1] == 's' && yyi < yycount)
        {
          yyres += symbol_name (yyarg[yyi++]);
          ++yyp;
        }
      else
        yyres += *yyp;
    return yyres;
  }


  const short parser::yypact_ninf_ = -312;

  const short parser::yytable_ninf_ = -192;

  const short
  parser::yypact_[] =
  {
      -1,  -312,    40,   111,   348,   117,  -312,  -312,    62,    19,
     134,    20,  -312,  -312,   371,   130,  -312,  -312,  -312,  -312,
    -312,    59,  -312,   234,   138,  -312,    19,   291,   330,    75,
    -312,     1,    14,   160,   167,  -312,    19,   182,   193,   209,
    -312,   238,   134,  -312,   254,  -312,   244,   250,   234,  -312,
     295,   323,  -312,  -312,   263,   237,   234,   306,    93,  -312,
     158,    19,    19,  -312,  -312,  -312,  -312,   325,  -312,  -312,
     340,    89,   347,   134,  -312,  -312,   358,   271,    31,  -312,
     271,   291,   337,   344,  -312,  -312,   350,    25,   171,   381,
     389,   239,   234,   234,   370,  -312,   178,   391,   234,   308,
     360,  -312,   359,   361,  -312,  -312,   386,  -312,   367,   362,
     369,  -312,  -312,   400,  -312,  -312,  -312,  -312,   387,  -312,
    -312,  -312,    15,  -312,   373,   372,  -312,   271,    50,   373,
    -312,  -312,   283,   133,   374,  -312,  -312,  -312,   375,   376,
     377,  -312,   393,  -312,   373,  -312,  -312,  -312,   199,   234,
     378,  -312,   321,   379,   313,   222,   234,   382,  -312,   406,
    -312,   349,   408,   380,   416,   304,  -312,    15,   373,  -312,
     300,   307,  -312,   383,   244,  -312,   352,  -312,   321,   373,
     373,   384,   385,  -312,   388,   390,   392,   321,   187,   394,
     256,   395,  -312,  -312,   321,   321,  -312,  -312,    83,  -312,
     398,    42,  -312,  -312,   126,  -312,  -312,  -312,  -312,   234,
    -312,   261,   324,    18,   140,   396,    55,   396,  -312,  -312,
     234,  -312,  -312,  -312,   397,   399,  -312,   401,  -312,  -312,
    -312,   408,   356,  -312,  -312,   321,  -312,  -312,  -312,    90,
    -312,   373,   403,  -312,    12,   404,   402,  -312,   403,   415,
    -312,   405,  -312,  -312,   407,  -312,  -312,   409,  -312,   411,
     321,     6,   419,   256,  -312,  -312,   421,   235,   410,   154,
    -312,  -312,   234,   412,  -312,   423,   420,   351,  -312,  -312,
     414,   413,   417,  -312,   422,   418,  -312,  -312,   321,   397,
    -312,   399,   424,   425,  -312,   345,  -312,  -312,   371,   427,
    -312,  -312,  -312,   321,   211,  -312,  -312,   234,   428,    18,
     234,  -312,  -312,  -312,  -312,  -312,  -312,   226,   429,   430,
     435,  -312,  -312,  -312,   321,   322,  -312,  -312,  -312,   107,
     436,   437,  -312,   186,   338,   373,   432,  -312,  -312,   175,
     431,   234,   439,   270,  -312,   440,   317,  -312,  -312,  -312,
     192,   259,  -312,   234,   253,  -312,  -312,  -312,  -312,   294,
     441,  -312,  -312,   321,   438,  -312,  -312,  -312
  };

  const unsigned char
  parser::yydefact_[] =
  {
      12,    12,     0,     0,   110,     0,     1,     2,     0,     0,
       0,     0,     9,    11,    37,     0,     5,     7,     8,    10,
       6,   113,     3,     0,     0,   186,     0,    44,     0,    14,
      75,    76,     0,     0,    78,    46,     0,     0,     0,     0,
     112,     0,     0,   109,     0,   168,     0,     0,     0,   167,
      14,   159,    63,    64,     0,    66,     0,    94,    91,    65,
       0,     0,     0,    61,    62,    59,    60,   192,    57,    58,
       0,     0,     0,     0,    70,    13,     0,     0,     0,    79,
       0,    45,     0,     0,    12,    16,    19,    14,     0,     0,
       0,     0,     0,     0,     0,    68,     0,     0,     0,     0,
     175,    96,     0,   175,   185,    53,    52,    51,   188,     0,
       0,   187,    47,     0,    48,   132,    74,    77,    85,    86,
      87,    88,     0,    89,    14,    80,    84,     0,     0,    14,
      12,    12,   110,     0,     0,   111,   107,   108,     0,     0,
       0,   164,   166,   165,    14,   152,   153,   151,     0,   156,
     175,   149,   150,    98,    14,     0,   174,     0,    92,   174,
      93,     0,   192,     0,     0,     0,    72,     0,    14,    71,
     110,   110,    38,   186,    24,    18,     0,    21,    22,    14,
      14,     0,     0,    69,     0,     0,   175,   158,   174,     0,
       0,     0,    67,   184,   182,   181,   183,    95,     0,   191,
     189,     0,    90,    81,     0,    83,    73,    39,    36,     0,
      17,     0,     0,   115,     0,   175,     0,   175,   160,   154,
     174,   155,   148,   161,   186,   100,   103,    99,    97,    49,
      50,   192,     0,    54,    82,    23,    20,   193,   194,    35,
      15,    14,   123,   121,   119,     0,   175,   117,   123,     0,
     170,   175,   172,   174,     0,   180,   177,   175,   179,     0,
     157,     0,     0,     0,   190,    55,     0,    35,     0,   110,
      28,    25,     0,   127,   128,     0,   131,    14,   114,   120,
       0,   174,     0,   162,   174,     0,   163,   105,   104,     0,
     102,   101,     0,     0,    26,     0,    34,    33,    41,     0,
      30,    31,    32,   122,     0,   118,   129,     0,   142,     0,
       0,   171,   169,   178,   176,    56,    27,     0,     0,     0,
       0,   124,   125,   126,   130,     0,   106,   135,   116,   175,
       0,     0,    35,     0,     0,   136,     0,    35,    35,   110,
       0,     0,     0,     0,   144,     0,     0,   138,   137,   173,
     110,   110,    42,     0,   146,   141,   134,   143,   140,     0,
       0,    43,    40,   145,     0,   133,   139,   147
  };

  const short
  parser::yypgoto_[] =
  {
    -312,  -312,   444,   -80,   -45,  -268,  -312,  -312,  -312,   241,
    -312,   188,  -186,  -312,  -312,  -312,  -312,  -262,   151,   155,
      77,   275,   293,  -259,  -312,  -312,   426,   448,   -72,   353,
    -143,  -253,  -312,  -312,  -312,  -312,   213,   215,  -249,  -312,
    -312,  -312,  -312,  -312,  -312,   169,   231,  -312,  -312,  -312,
      45,  -312,  -312,   135,  -311,  -312,   292,  -312,   296,   -23,
    -312,  -312,   201,  -101,  -312,  -312,   200,  -312,  -312,     3,
    -312,  -159,  -206
  };

  const short
  parser::yydefgoto_[] =
  {
      -1,     2,     3,     4,    74,    12,    86,   134,   176,   177,
     240,   268,   269,    13,    14,   297,   298,    15,    37,    38,
      27,   114,    71,    16,    17,    29,    30,    79,   124,   125,
     126,    18,   102,   103,    19,   191,   225,   226,    20,   138,
      21,    43,    44,   245,   246,   247,   273,   305,   248,   308,
      75,   326,   327,   343,   344,   150,   151,   185,   186,    58,
     215,   251,   252,   157,   217,   257,   258,   100,    59,    51,
     109,   110,   270
  };

  const short
  parser::yytable_[] =
  {
      50,   296,   160,   200,   132,    95,   241,   299,   129,    25,
     300,   287,    28,    31,    34,   274,   301,    25,   118,    76,
     302,   242,    25,    25,   205,    91,    45,    46,    47,    28,
      77,     1,   357,    99,    25,    34,   119,   120,   121,    28,
       6,    48,   135,   243,    70,    87,   232,   127,   357,   189,
     170,   171,    49,    25,    26,   168,   275,    78,    72,   123,
     255,   205,   244,    32,    28,    28,    40,    41,    70,   142,
     143,   296,   264,   152,   128,   154,    31,   299,   233,   166,
     300,    34,   296,   296,   169,   221,   301,   229,   299,   299,
     302,   300,   300,   128,   112,   256,    23,   301,   301,   183,
      24,   302,   302,    60,    42,   237,    92,    93,    72,   192,
     178,     7,    73,    81,   254,   238,   259,    22,   113,   335,
      92,    93,   267,   206,   113,    91,   187,   345,   347,   118,
     104,    34,   194,   195,   212,   213,   173,    25,   106,   107,
     360,    25,    52,    53,   253,   278,   339,   119,   120,   121,
     282,   350,   351,    45,   174,    47,   285,   295,    45,    46,
      47,    54,   234,    55,    39,   152,     9,   187,    48,   175,
     123,    61,    62,    56,   136,   249,    80,    57,   295,    49,
     250,    25,   145,   146,    49,   -29,   235,     9,   178,   340,
      25,   145,   146,   137,   105,   295,   271,   260,    45,    46,
      47,   237,    25,   147,     9,   341,   352,    45,    46,    47,
      70,   238,   147,   148,   321,   322,    82,   149,   342,    45,
      46,    47,    48,   361,    49,    25,   149,    83,   336,    25,
      52,    53,   309,    49,    48,   184,   323,    25,   288,    84,
     260,    85,    45,    46,    47,    49,    45,    46,    47,   303,
     237,    55,    92,    93,    45,    46,    47,    48,   193,   224,
     238,    56,   295,    88,   173,    57,    92,    93,    49,    48,
      98,     9,    49,   340,   118,   141,    45,    46,    47,    89,
      49,    45,   174,    47,   324,    90,     8,   329,   364,   341,
     362,    48,   119,   120,   121,     9,    48,   340,    97,    10,
      11,   356,    49,     8,    61,    62,   122,    49,    92,    93,
       8,   101,     9,   341,   172,   123,    10,    11,   354,     9,
     340,    92,    93,    10,    11,   365,    92,    93,    72,   108,
     363,   207,   237,    94,    92,    93,   341,   237,   208,   237,
     203,   204,   238,   111,   141,   155,    72,   238,    -4,   238,
     115,     8,   333,   237,   239,    72,    63,    64,    65,    66,
       9,   117,    96,   238,    10,    11,    70,   130,   346,    67,
     334,    68,    69,    70,   131,    63,    64,    65,    66,    23,
     348,    35,    36,   317,    72,   133,   139,  -174,   210,   211,
      68,    69,   265,   266,   140,   144,   153,   156,   159,   158,
      62,  -191,   161,   162,   163,   164,    72,    93,   179,   167,
     180,   197,   199,   181,   182,   188,   190,   201,   196,   202,
     280,   209,   289,   214,   216,   292,   306,   255,   218,   220,
     219,   228,   231,   253,   223,   261,   262,   272,   263,   277,
     276,   294,   281,   283,   307,     5,   284,   286,   249,   318,
     304,   310,   236,   319,   198,   293,   316,   312,   314,    33,
     315,   320,   325,   330,   331,   332,   337,   338,   349,   353,
     355,   358,   366,   230,   367,   165,   291,   290,   328,   279,
     222,   359,   311,     0,   313,     0,   227,     0,     0,     0,
       0,     0,     0,     0,     0,     0,     0,     0,     0,   116
  };

  const short
  parser::yycheck_[] =
  {
      23,   269,   103,   162,    84,    50,   212,   269,    80,     3,
     269,     5,     9,    10,    11,     3,   269,     3,     3,    18,
     269,     3,     3,     3,   167,    48,    20,    21,    22,    26,
      16,    32,   343,    56,     3,    32,    21,    22,    23,    36,
       0,    35,    87,    25,    43,    42,     4,    16,   359,   150,
     130,   131,    46,     3,    35,   127,    44,    43,    33,    44,
       5,   204,    44,    43,    61,    62,     7,     8,    43,    92,
      93,   339,   231,    96,    43,    98,    73,   339,    36,   124,
     339,    78,   350,   351,   129,   186,   339,     4,   350,   351,
     339,   350,   351,    43,     5,    40,    34,   350,   351,   144,
      38,   350,   351,    26,    45,    15,    13,    14,    33,   154,
     133,     0,    37,    36,   215,    25,   217,     0,    35,   325,
      13,    14,    32,   168,    35,   148,   149,   333,   334,     3,
      37,   128,   155,   156,   179,   180,     3,     3,    61,    62,
     346,     3,     4,     5,    37,   246,   332,    21,    22,    23,
     251,   337,   338,    20,    21,    22,   257,     3,    20,    21,
      22,    23,    36,    25,    34,   188,    12,   190,    35,    36,
      44,    13,    14,    35,     3,    35,    16,    39,     3,    46,
      40,     3,     4,     5,    46,    31,   209,    12,   211,     3,
       3,     4,     5,    22,    36,     3,   241,   220,    20,    21,
      22,    15,     3,    25,    12,    19,    31,    20,    21,    22,
      43,    25,    25,    35,     3,     4,    34,    39,    32,    20,
      21,    22,    35,    31,    46,     3,    39,    34,   329,     3,
       4,     5,   277,    46,    35,    36,    25,     3,   261,    30,
     263,     3,    20,    21,    22,    46,    20,    21,    22,   272,
      15,    25,    13,    14,    20,    21,    22,    35,    36,     3,
      25,    35,     3,     9,     3,    39,    13,    14,    46,    35,
      33,    12,    46,     3,     3,    36,    20,    21,    22,    35,
      46,    20,    21,    22,   307,    35,     3,   310,    35,    19,
      31,    35,    21,    22,    23,    12,    35,     3,    35,    16,
      17,    31,    46,     3,    13,    14,    35,    46,    13,    14,
       3,     5,    12,    19,    31,    44,    16,    17,   341,    12,
       3,    13,    14,    16,    17,    31,    13,    14,    33,     4,
     353,    31,    15,    38,    13,    14,    19,    15,    31,    15,
      36,    37,    25,     3,    36,    37,    33,    25,     0,    25,
       3,     3,    30,    15,    30,    33,    26,    27,    28,    29,
      12,     3,    39,    25,    16,    17,    43,    30,    30,    39,
     325,    41,    42,    43,    30,    26,    27,    28,    29,    34,
     335,    10,    11,    38,    33,    35,     5,    36,    36,    37,
      41,    42,    36,    37,     5,    25,     5,    37,    37,    40,
      14,    34,    40,    34,     4,    18,    33,    14,    34,    37,
      35,     5,     4,    37,    37,    37,    37,    37,    36,     3,
       5,    38,     3,    39,    39,     4,     3,     5,    40,    37,
      40,    36,    34,    37,    40,    38,    37,    34,    37,    37,
      36,    31,    37,    36,    24,     1,    37,    36,    35,   298,
      38,    37,   211,   298,   161,   267,    31,    40,    40,    11,
      36,    34,    34,    34,    34,    30,    30,    30,    36,    38,
      31,    31,    31,   198,    36,   122,   263,   262,   309,   248,
     188,   346,   281,    -1,   284,    -1,   190,    -1,    -1,    -1,
      -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    73
  };

  const signed char
  parser::yystos_[] =
  {
       0,    32,    48,    49,    50,    49,     0,     0,     3,    12,
      16,    17,    52,    60,    61,    64,    70,    71,    78,    81,
      85,    87,     0,    34,    38,     3,    35,    67,   116,    72,
      73,   116,    43,    74,   116,    10,    11,    65,    66,    34,
       7,     8,    45,    88,    89,    20,    21,    22,    35,    46,
     106,   116,     4,     5,    23,    25,    35,    39,   106,   115,
      67,    13,    14,    26,    27,    28,    29,    39,    41,    42,
      43,    69,    33,    37,    51,    97,    18,    16,    43,    74,
      16,    67,    34,    34,    30,     3,    53,   116,     9,    35,
      35,   106,    13,    14,    38,    51,    39,    35,    33,   106,
     114,     5,    79,    80,    37,    36,    67,    67,     4,   117,
     118,     3,     5,    35,    68,     3,    73,     3,     3,    21,
      22,    23,    35,    44,    75,    76,    77,    16,    43,    75,
      30,    30,    50,    35,    54,    51,     3,    22,    86,     5,
       5,    36,   106,   106,    25,     4,     5,    25,    35,    39,
     102,   103,   106,     5,   106,    37,    37,   110,    40,    37,
     110,    40,    34,     4,    18,    76,    51,    37,    75,    51,
      50,    50,    31,     3,    21,    36,    55,    56,   106,    34,
      35,    37,    37,    51,    36,   104,   105,   106,    37,   110,
      37,    82,    51,    36,   106,   106,    36,     5,    69,     4,
     118,    37,     3,    36,    37,    77,    51,    31,    31,    38,
      36,    37,    51,    51,    39,   107,    39,   111,    40,    40,
      37,   110,   103,    40,     3,    83,    84,   105,    36,     4,
      68,    34,     4,    36,    36,   106,    56,    15,    25,    30,
      57,   119,     3,    25,    44,    90,    91,    92,    95,    35,
      40,   108,   109,    37,   110,     5,    40,   112,   113,   110,
     106,    38,    37,    37,   118,    36,    37,    32,    58,    59,
     119,    51,    34,    93,     3,    44,    36,    37,   110,    93,
       5,    37,   110,    36,    37,   110,    36,     5,   106,     3,
      84,    83,     4,    58,    31,     3,    52,    62,    63,    64,
      70,    78,    85,   106,    38,    94,     3,    24,    96,    51,
      37,   109,    40,   113,    40,    36,    31,    38,    65,    66,
      34,     3,     4,    25,   106,    34,    98,    99,    92,   106,
      34,    34,    30,    30,    97,   119,   110,    30,    30,    59,
       3,    19,    32,   100,   101,   119,    30,   119,    97,    36,
      59,    59,    31,    38,   106,    31,    31,   101,    31,   100,
     119,    31,    31,   106,    35,    31,    31,    36
  };

  const signed char
  parser::yyr1_[] =
  {
       0,    47,    48,    48,    49,    50,    50,    50,    50,    50,
      50,    50,    50,    51,    51,    52,    53,    54,    54,    54,
      55,    55,    56,    56,    56,    57,    57,    57,    58,    58,
      59,    59,    59,    59,    59,    59,    60,    60,    61,    61,
      62,    62,    63,    63,    64,    65,    66,    67,    67,    67,
      67,    67,    67,    67,    68,    68,    68,    69,    69,    69,
      69,    69,    69,    70,    70,    70,    70,    70,    70,    70,
      71,    71,    71,    71,    72,    72,    73,    73,    74,    74,
      75,    75,    75,    76,    76,    77,    77,    77,    77,    77,
      77,    78,    78,    79,    79,    80,    80,    81,    82,    82,
      82,    82,    83,    83,    84,    84,    85,    86,    86,    87,
      87,    88,    89,    89,    90,    90,    91,    91,    92,    92,
      92,    92,    93,    93,    94,    94,    94,    94,    95,    95,
      96,    96,    97,    98,    98,    98,    99,    99,    99,    99,
      99,    99,    99,   100,   100,   101,   101,   101,   102,   102,
     103,   103,   103,   103,   103,   104,   104,   105,   105,   106,
     106,   106,   106,   106,   106,   106,   106,   106,   106,   107,
     107,   108,   108,   109,   110,   110,   111,   111,   112,   112,
     113,   114,   114,   115,   115,   115,   116,   116,   117,   117,
     117,   118,   118,   119,   119
  };

  const signed char
  parser::yyr2_[] =
  {
       0,     2,     2,     3,     1,     2,     2,     2,     2,     2,
       2,     2,     0,     1,     0,     7,     1,     3,     2,     0,
       3,     1,     1,     3,     1,     2,     3,     4,     1,     1,
       2,     2,     2,     2,     2,     0,     6,     1,     5,     6,
       6,     1,     5,     6,     2,     2,     1,     3,     3,     6,
       6,     3,     3,     3,     4,     5,     7,     1,     1,     1,
       1,     1,     1,     3,     3,     3,     3,     6,     4,     6,
       3,     5,     5,     6,     3,     1,     1,     3,     1,     2,
       1,     3,     4,     3,     1,     1,     1,     1,     1,     1,
       3,     3,     5,     2,     0,     3,     1,     7,     0,     2,
       2,     4,     3,     1,     3,     3,    10,     1,     1,     2,
       0,     3,     1,     0,     2,     0,     4,     1,     3,     1,
       2,     1,     2,     0,     2,     2,     2,     0,     2,     3,
       2,     0,     2,     5,     4,     1,     2,     3,     3,     5,
       4,     4,     0,     2,     1,     3,     2,     4,     3,     1,
       1,     1,     1,     1,     3,     2,     0,     3,     1,     1,
       5,     5,     7,     7,     3,     3,     3,     1,     1,     4,
       2,     3,     1,     6,     1,     0,     4,     2,     3,     1,
       1,     3,     3,     4,     4,     2,     1,     3,     1,     3,
       5,     1,     0,     1,     1
  };


#if PYTYPEDEBUG || 1
  // YYTNAME[SYMBOL-NUM] -- String name of the symbol SYMBOL-NUM.
  // First, the terminals, then, starting at \a YYNTOKENS, nonterminals.
  const char*
  const parser::yytname_[] =
  {
  "\"end of file\"", "error", "\"invalid token\"", "NAME", "NUMBER",
  "STRING", "LEXERROR", "ASYNC", "CLASS", "DEF", "ELSE", "ELIF", "IF",
  "OR", "AND", "PASS", "IMPORT", "FROM", "AS", "RAISE", "NOTHING",
  "NAMEDTUPLE", "COLL_NAMEDTUPLE", "TYPEVAR", "ARROW", "ELLIPSIS", "EQ",
  "NE", "LE", "GE", "INDENT", "DEDENT", "TRIPLEQUOTED", "TYPECOMMENT",
  "':'", "'('", "')'", "','", "'='", "'['", "']'", "'<'", "'>'", "'.'",
  "'*'", "'@'", "'?'", "$accept", "start", "unit", "alldefs",
  "maybe_type_ignore", "classdef", "class_name", "parents", "parent_list",
  "parent", "maybe_class_funcs", "class_funcs", "funcdefs", "if_stmt",
  "if_and_elifs", "class_if_stmt", "class_if_and_elifs", "if_cond",
  "elif_cond", "else_cond", "condition", "version_tuple", "condition_op",
  "constantdef", "importdef", "import_items", "import_item", "import_name",
  "from_list", "from_items", "from_item", "alias_or_constant",
  "maybe_string_list", "string_list", "typevardef", "typevar_args",
  "typevar_kwargs", "typevar_kwarg", "funcdef", "funcname", "decorators",
  "decorator", "maybe_async", "params", "param_list", "param",
  "param_type", "param_default", "param_star_name", "return", "typeignore",
  "maybe_body", "empty_body", "body", "body_stmt", "type_parameters",
  "type_parameter", "maybe_type_list", "type_list", "type",
  "named_tuple_fields", "named_tuple_field_list", "named_tuple_field",
  "maybe_comma", "coll_named_tuple_fields", "coll_named_tuple_field_list",
  "coll_named_tuple_field", "type_tuple_elements", "type_tuple_literal",
  "dotted_name", "getitem_key", "maybe_number", "pass_or_ellipsis", YY_NULLPTR
  };
#endif


#if PYTYPEDEBUG
  const short
  parser::yyrline_[] =
  {
       0,   134,   134,   135,   139,   143,   144,   145,   146,   152,
     153,   154,   159,   163,   164,   171,   181,   192,   193,   194,
     198,   199,   203,   204,   205,   209,   210,   211,   215,   216,
     220,   221,   226,   227,   232,   233,   238,   241,   246,   250,
     263,   266,   271,   275,   287,   291,   295,   299,   302,   305,
     308,   311,   312,   313,   317,   318,   319,   325,   326,   327,
     328,   329,   330,   334,   338,   342,   346,   350,   354,   358,
     365,   369,   373,   379,   388,   389,   393,   394,   399,   400,
     407,   408,   409,   413,   414,   418,   419,   422,   425,   428,
     431,   435,   436,   440,   441,   445,   446,   450,   457,   458,
     459,   460,   464,   465,   469,   471,   475,   489,   490,   494,
     495,   499,   503,   504,   508,   509,   521,   522,   526,   527,
     528,   529,   533,   534,   538,   539,   540,   541,   545,   546,
     550,   551,   555,   559,   560,   561,   565,   566,   567,   568,
     569,   570,   571,   575,   576,   580,   581,   582,   586,   587,
     591,   592,   594,   595,   597,   604,   605,   609,   610,   614,
     618,   622,   626,   630,   634,   635,   636,   637,   638,   642,
     643,   647,   648,   652,   656,   657,   661,   662,   666,   669,
     673,   680,   681,   690,   695,   701,   708,   709,   723,   724,
     729,   737,   738,   742,   743
  };

  void
  parser::yy_stack_print_ () const
  {
    *yycdebug_ << "Stack now";
    for (stack_type::const_iterator
           i = yystack_.begin (),
           i_end = yystack_.end ();
         i != i_end; ++i)
      *yycdebug_ << ' ' << int (i->state);
    *yycdebug_ << '\n';
  }

  void
  parser::yy_reduce_print_ (int yyrule) const
  {
    int yylno = yyrline_[yyrule];
    int yynrhs = yyr2_[yyrule];
    // Print the symbols being reduced, and their result.
    *yycdebug_ << "Reducing stack by rule " << yyrule - 1
               << " (line " << yylno << "):\n";
    // The symbols being reduced.
    for (int yyi = 0; yyi < yynrhs; yyi++)
      YY_SYMBOL_PRINT ("   $" << yyi + 1 << " =",
                       yystack_[(yynrhs) - (yyi + 1)]);
  }
#endif // PYTYPEDEBUG

  parser::symbol_kind_type
  parser::yytranslate_ (int t)
  {
    // YYTRANSLATE[TOKEN-NUM] -- Symbol number corresponding to
    // TOKEN-NUM as returned by yylex.
    static
    const signed char
    translate_table[] =
    {
       0,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
      35,    36,    44,     2,    37,     2,    43,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,    34,     2,
      41,    38,    42,    46,    45,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,    39,     2,    40,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     1,     2,     3,     4,
       5,     6,     7,     8,     9,    10,    11,    12,    13,    14,
      15,    16,    17,    18,    19,    20,    21,    22,    23,    24,
      25,    26,    27,    28,    29,    30,    31,    32,    33
    };
    const int user_token_number_max_ = 288;

    if (t <= 0)
      return symbol_kind::S_YYEOF;
    else if (t <= user_token_number_max_)
      return YY_CAST (symbol_kind_type, translate_table[t]);
    else
      return symbol_kind::S_YYUNDEF;
  }

#line 17 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
} // pytype
#line 3104 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"

#line 746 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"


void pytype::parser::error(const location& loc, const std::string& msg) {
  ctx->SetErrorLocation(loc);
  pytype::Lexer* lexer = pytypeget_extra(scanner);
  if (lexer->error_message_) {
    PyErr_SetObject(ctx->Value(pytype::kParseError), lexer->error_message_);
  } else {
    PyErr_SetString(ctx->Value(pytype::kParseError), msg.c_str());
  }
}

namespace {

PyObject* StartList(PyObject* item) {
  return Py_BuildValue("[N]", item);
}

PyObject* AppendList(PyObject* list, PyObject* item) {
  PyList_Append(list, item);
  Py_DECREF(item);
  return list;
}

PyObject* ExtendList(PyObject* dst, PyObject* src) {
  // Add items from src to dst (both of which must be lists) and return src.
  // Borrows the reference to src.
  Py_ssize_t count = PyList_Size(src);
  for (Py_ssize_t i=0; i < count; ++i) {
    PyList_Append(dst, PyList_GetItem(src, i));
  }
  Py_DECREF(src);
  return dst;
}

}  // end namespace
