"""
A module for parsing a source string into a Program object.
"""

__all__: tuple[str] = ("Parser",)

from ply import yacc
from server.lexer import Lexer
from server.language import (
    IntegerValue,
    StringValue,
    BooleanExpression,
    Literal,
    Variable,
    Expression,
    Need,
    InputStatement,
    OutputStatement,
    LetStatement,
    Procedure,
    Branch,
    Default,
    Program,
)


class Parser:
    """
    A class for parsing a source string into a Program object.
    """

    tokens: tuple[str] = Lexer.tokens

    def __init__(self, lexer: Lexer, **kwargs) -> None:
        """
        Initializes a Parser instance.

        Args:
            lexer: The Lexer instance to be used for lexical analysis.
            **kwargs: Arbitrary keyword arguments to configure the PLY parser.
        """
        self.lexer: Lexer = lexer
        self.parser: yacc.yacc = yacc.yacc(module=self, **kwargs)

    def parse(self, source: str) -> Program:
        """
        Parses a source string and returns a Program object.

        Args:
            source: The source string to be parsed.

        Returns:
            A Program object, which represents the parsed program.
        """
        return self.parser.parse(source, lexer=self.lexer)

    def p_error(self, p) -> None:
        """
        Handles a syntax error in the source program.

        This function is called when a syntax error is encountered by the parser.
        It prints the token that caused the error, and then raises a SyntaxError exception.
        """
        print(p)
        raise SyntaxError

    def p_program(self, p) -> None:
        "program : needs procedures"
        p[0] = Program(needs=p[1], procedures=p[2])

    def p_needs(self, p) -> None:
        """needs : need needs
        |"""
        if len(p) == 3:  # need needs
            p[0] = [p[1]] + p[2]
        else:  # EMPTY
            p[0] = []

    def p_need(self, p) -> None:
        """need : NEED VAR_ID"""
        p[0] = Need(var_id=p[2])

    def p_procedures(self, p) -> None:
        """procedures : procedure procedures
        | procedure"""
        if len(p) == 3:  # procedure procedures
            p[0] = [p[1]] + p[2]
        else:  # procedure
            p[0] = [p[1]]

    def p_procedure(self, p) -> None:
        """procedure : PROCEDURE PROC_NAME statements branches"""
        p[0] = Procedure(name=p[2], statements=p[3], branches=p[4])

    def p_statements(self, p) -> None:
        """statements : statement statements
        |"""
        if len(p) == 3:  # statement statements
            p[0] = [p[1]] + p[2]
        else:  # EMPTY
            p[0] = []

    def p_statement(self, p) -> None:
        """statement : let_statement
        | input_statement
        | output_statement"""
        p[0] = p[1]

    def p_branches(self, p) -> None:
        """branches : branch branches
        | default
        |"""
        if len(p) == 3:  # branch branches
            p[0] = [p[1]] + p[2]
        elif len(p) == 2:  # default
            p[0] = [p[1]]
        else:  # EMPTY
            p[0] = []

    def p_branch(self, p) -> None:
        """branch : BRANCH PROC_NAME WHEN bexpr"""
        p[0] = Branch(proc_name=p[2], bexpr=p[4])

    def p_default(self, p) -> None:
        """default : DEFAULT PROC_NAME"""
        p[0] = Default(proc_name=p[2])

    def p_let_statement(self, p) -> None:
        """let_statement : LET VAR_ID ASSIGN expr"""
        p[0] = LetStatement(var_id=p[2], expr=p[4])

    def p_input_statement(self, p) -> None:
        """input_statement : INPUT VAR_ID"""
        p[0] = InputStatement(var_id=p[2])

    def p_output_statement(self, p) -> None:
        """output_statement : OUTPUT expr"""
        p[0] = OutputStatement(expr=p[2])

    def p_bexpr(self, p) -> None:
        """bexpr : bterm
        | bexpr AND expr"""
        if len(p) == 2:
            # bterm
            p[0] = p[1]
        else:
            # bexpr AND expr
            p[0] = BooleanExpression((p[1], p[2], p[3]))

    def p_bterm(self, p) -> None:
        """bterm : bfactor
        | bterm OR bfactor"""
        if len(p) == 2:
            # bfactor
            p[0] = p[1]
        else:
            # bterm OR expr
            p[0] = BooleanExpression((p[1], p[2], p[3]))

    def p_bfactor(self, p) -> None:
        """bfactor : NOT bfactor
        | LPAREN bexpr RPAREN
        | expr COMPARATOR expr"""
        if len(p) == 3:
            # NOT bfactor
            p[0] = BooleanExpression(words=(p[1], p[2]))
        elif p[1] == "(" and p[3] == ")":
            # LPAREN bexpr RPAREN
            p[0] = p[2]
        else:
            # expr COMPARATOR expr
            p[0] = BooleanExpression(words=(p[1], p[2], p[3]))

    def p_expr(self, p) -> None:
        """expr : term
        | PLUS expr
        | MINUS expr
        | expr PLUS term
        | expr MINUS term
        | CAST expr TO INTEGER
        | CAST expr TO STRING"""
        if len(p) == 2:
            # term
            p[0] = p[1]
        elif len(p) == 3:
            # ? expr
            p[0] = Expression(words=(p[1], p[2]))
        else:
            if p[1] == "cast":
                # CAST expr TO INTEGER
                # CAST expr TO STRING
                p[0] = Expression(words=(p[2], p[3], p[4]))
            else:
                # expr ? term
                p[0] = Expression(words=(p[1], p[2], p[3]))

    def p_term(self, p) -> None:
        """term : factor
        | term MUL factor
        | term DIV factor
        | term MOD factor"""
        if len(p) == 2:
            # factor
            p[0] = p[1]
        else:
            # term ? factor
            p[0] = Expression((p[1], p[2], p[3]))

    def p_factor(self, p) -> None:
        """factor : INTEGER_CONSTANT
        | STRING_LITERAL
        | VAR_ID
        | LPAREN expr RPAREN"""
        if len(p) == 2:
            if isinstance(p[1], IntegerValue):
                # INTEGER_CONSTANT
                p[0] = Literal(IntegerValue(p[1].value))
            elif isinstance(p[1], StringValue):
                # STRING_LITERAL
                p[0] = Literal(StringValue(p[1].value))
            else:
                # VAR_ID
                p[0] = Variable(p[1])
        else:
            # LPAREN expr RPAREN
            p[0] = p[2]
