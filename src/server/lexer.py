"""
A module for tokenizing a source string into a sequence of tokens.
"""

__all__: list[str] = [
    "Lexer",
]

from ply import lex
from ply.lex import LexToken
from server.language import (
    IntegerValue,
    StringValue,
)


class Lexer:
    """
    A class for tokenizing a source string into a sequence of tokens.
    """

    def __init__(self, **kwargs) -> None:
        """
        Initializes a Lexer instance by creating a PLY lexer.

        Args:
            **kwargs: Arbitrary keyword arguments to configure the PLY lexer.
        """
        self.lexer: lex.Lexer = lex.lex(module=self, **kwargs)

    def input(self, data) -> None:
        """
        Sends input data to the lexer for tokenization.

        Args:
            data: The input data string to be tokenized by the lexer.
        """
        self.lexer.input(s=data)

    def token(self) -> LexToken | None:
        """
        Retrieves the next token from the lexer.

        Returns:
            LexToken | None: The next token from the lexer, or None if there are no more tokens.
        """
        token: LexToken | None = self.lexer.token()
        return token

    keywords: dict[str, str] = {
        "need": "NEED",
        "procedure": "PROCEDURE",
        "input": "INPUT",
        "output": "OUTPUT",
        "let": "LET",
        "branch": "BRANCH",
        "when": "WHEN",
        "default": "DEFAULT",
        "integer": "INTEGER",
        "string": "STRING",
        "like": "COMPARATOR",
        "and": "AND",
        "or": "OR",
        "not": "NOT",
        "cast": "CAST",
        "to": "TO",
    }

    tokens: tuple[str] = (
        "NEED",
        "PROCEDURE",
        "INPUT",
        "OUTPUT",
        "LET",
        "BRANCH",
        "WHEN",
        "DEFAULT",
        "COMPARATOR",
        "ASSIGN",
        "INTEGER",
        "STRING",
        "PLUS",
        "MINUS",
        "MUL",
        "DIV",
        "MOD",
        "AND",
        "OR",
        "NOT",
        "CAST",
        "TO",
        "LPAREN",
        "RPAREN",
        "INTEGER_CONSTANT",
        "STRING_LITERAL",
        "VAR_ID",
        "PROC_NAME",
    )

    t_ignore: str = " \t\r\f\v"

    def t_comment(self, _) -> None:
        r"[#].*"

    def t_comparator(self, token) -> LexToken:
        r"<=|>=|==|!=|<|>"
        token.type = "COMPARATOR"
        return token

    t_ASSIGN = r"="
    t_PLUS = r"\+"
    t_MINUS = r"\-"
    t_MUL = r"\*"
    t_DIV = r"\/"
    t_MOD = r"%"
    t_LPAREN = r"\("
    t_RPAREN = r"\)"

    def t_integer_constant(self, token) -> LexToken:
        r"\d+"
        token.type = "INTEGER_CONSTANT"
        token.value = IntegerValue(int(token.value))
        return token

    def t_string_literal(self, token) -> LexToken:
        r'"[^"]*"'
        token.type = "STRING_LITERAL"
        token.value = StringValue(str(token.value[1:-1]))
        return token

    t_VAR_ID = r"\$\{\w+\}"

    def t_proc_name(self, token) -> LexToken:
        r"\w+"
        word: str = token.value
        if word in self.keywords:
            token.type = self.keywords[word]
        else:
            token.type = "PROC_NAME"
        return token

    def t_newline(self, token) -> None:
        r"\n+"
        token.lexer.lineno += len(token.value)

    def t_error(self, token) -> None:
        """
        Handles a syntax error in the source program.

        This function is called when a syntax error is encountered by the lexer.
        It raises a SyntaxError exception with a message indicating the invalid
        token.

        :param token: The invalid token.
        :type token: LexToken
        :raises SyntaxError: A syntax error occurred.
        """

        raise SyntaxError(f"invalid token: {token.value!r}")
