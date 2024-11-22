import pytest
from ply.lex import LexToken
from server.lexer import Lexer
from server.language import (
    IntegerValue,
    StringValue,
)


def test_init() -> None:
    lexer = Lexer()
    assert lexer.lexer is not None


def test_input() -> None:
    lexer = Lexer()
    lexer.input(data="hello world")
    assert lexer.lexer.lexdata == "hello world"


def test_tokens() -> None:
    lexer = Lexer()
    lexer.input(
        data="need procedure input output let branch when default integer string + - * / % = < >"
    )
    tokens: list[LexToken] = []
    while True:
        token: LexToken = lexer.token()
        if token is None:
            break
        tokens.append(token)
    assert lexer.token() is None

    assert [token.type for token in tokens] == [
        "NEED",
        "PROCEDURE",
        "INPUT",
        "OUTPUT",
        "LET",
        "BRANCH",
        "WHEN",
        "DEFAULT",
        "INTEGER",
        "STRING",
        "PLUS",
        "MINUS",
        "MUL",
        "DIV",
        "MOD",
        "ASSIGN",
        "COMPARATOR",
        "COMPARATOR",
    ]


def test_ignore_whitespace() -> None:
    lexer = Lexer()
    lexer.input(data="   hello   world   ")
    token: LexToken = lexer.token()
    assert token is not None
    assert token.type == "PROC_NAME"
    assert token.value == "hello"


def test_keywords() -> None:
    lexer = Lexer()
    keywords: list[str] = "need procedure input output let branch when default".split()
    for keyword in keywords:
        lexer.input(data=keyword)
        token: LexToken = lexer.token()
        assert token is not None
        assert token.type == keyword.upper()
        assert token.value == keyword

    assert lexer.token() is None


def test_type() -> None:
    lexer = Lexer()
    lexer.input(data="integer string")

    token: LexToken = lexer.token()
    assert token is not None
    assert token.type == "INTEGER"
    assert token.value == "integer"

    token: LexToken = lexer.token()
    assert token is not None
    assert token.type == "STRING"
    assert token.value == "string"

    assert lexer.token() is None


def test_var_id() -> None:
    lexer = Lexer()
    lexer.input(data="${hello}")

    token: LexToken = lexer.token()
    assert token is not None
    assert token.type == "VAR_ID"
    assert token.value == "${hello}"

    assert lexer.token() is None


def test_proc_name() -> None:
    lexer = Lexer()
    lexer.input(data="hello")

    token: LexToken = lexer.token()
    assert token is not None
    assert token.type == "PROC_NAME"
    assert token.value == "hello"

    assert lexer.token() is None


def test_operator() -> None:
    lexer = Lexer()
    operators = "+-*/%="
    expected_types = ["PLUS", "MINUS", "MUL", "DIV", "MOD", "ASSIGN"]
    for operator, expected_type in zip(operators, expected_types):
        lexer.input(data=operator)
        token: LexToken = lexer.token()
        assert token is not None
        assert token.type == expected_type
        assert token.value == operator
    assert lexer.token() is None


def test_comparator() -> None:
    lexer = Lexer()
    comparators: list[str] = "< <= == >= > != like".split()
    for comparator in comparators:
        lexer.input(data=comparator)
        token: LexToken = lexer.token()
        assert token is not None
        assert token.type == "COMPARATOR"
        assert token.value == comparator
    assert lexer.token() is None


def test_cast() -> None:
    lexer = Lexer()
    lexer.input(data="cast ${var} to integer")

    token: LexToken = lexer.token()
    assert token is not None
    assert token.type == "CAST"
    assert token.value == "cast"

    token = lexer.token()
    assert token is not None
    assert token.type == "VAR_ID"
    assert token.value == "${var}"

    token = lexer.token()
    assert token is not None
    assert token.type == "TO"
    assert token.value == "to"

    token = lexer.token()
    assert token is not None
    assert token.type == "INTEGER"
    assert token.value == "integer"

    assert lexer.token() is None


def test_to() -> None:
    lexer = Lexer()
    lexer.input(data="to")

    token: LexToken = lexer.token()
    assert token is not None
    assert token.type == "TO"
    assert token.value == "to"

    assert lexer.token() is None


def test_integer_constant() -> None:
    lexer = Lexer()
    lexer.input(data="123")

    token: LexToken = lexer.token()
    assert token is not None
    assert token.type == "INTEGER_CONSTANT"
    assert token.value == IntegerValue(123)

    assert lexer.token() is None


def test_string_literal() -> None:
    lexer = Lexer()
    lexer.input(data='"hello"')

    token: LexToken = lexer.token()
    assert token is not None
    assert token.type == "STRING_LITERAL"
    assert token.value == StringValue("hello")

    assert lexer.token() is None


def test_newline() -> None:
    lexer = Lexer()
    lexer.input(data="\n")
    token: LexToken = lexer.token()
    assert token is None
    assert lexer.lexer.lineno == 2


def test_comment() -> None:
    lexer = Lexer()
    lexer.input(data="# comment\n")

    token: LexToken = lexer.token()
    assert token is None

    lexer.input(data="hello # comment\n")

    token = lexer.token()
    assert token is not None
    assert token.type == "PROC_NAME"
    assert token.value == "hello"

    assert lexer.token() is None


def test_chinese_procedure() -> None:
    lexer = Lexer()
    lexer.input(data="沙黑然木斯德克")
    token: LexToken = lexer.token()
    assert token.type == "PROC_NAME"
    assert token.value == "沙黑然木斯德克"


def test_chinese_variable() -> None:
    lexer = Lexer()
    lexer.input(data="${变量一}")
    token: LexToken = lexer.token()
    assert token.type == "VAR_ID"
    assert token.value == "${变量一}"


def test_complex_input() -> None:
    code = """
    need ${姓名}
    need ${电话号码}

    procedure 问候
        let ${问候语后缀} = "同志您好，请问您有什么需要的吗？"
        let ${问候语} = ${姓名} + ${问候语后缀}
        output ${问候语}
        input ${答复}
        let ${话费查询模式} = "话费"
        let ${举报模式} = "举报"

        branch 话费查询 when ${答复} like ${话费查询模式}
        branch 举报 when ${答复} like ${举报模式}
        default 重新问一遍
    """
    lexer = Lexer()
    lexer.input(data=code)
    expected_results = [
        ("NEED", "need"),
        ("VAR_ID", "${姓名}"),
        ("NEED", "need"),
        ("VAR_ID", "${电话号码}"),
        ("PROCEDURE", "procedure"),
        ("PROC_NAME", "问候"),
        ("LET", "let"),
        ("VAR_ID", "${问候语后缀}"),
        ("ASSIGN", "="),
        ("STRING_LITERAL", StringValue("同志您好，请问您有什么需要的吗？")),
        ("LET", "let"),
        ("VAR_ID", "${问候语}"),
        ("ASSIGN", "="),
        ("VAR_ID", "${姓名}"),
        ("PLUS", "+"),
        ("VAR_ID", "${问候语后缀}"),
        ("OUTPUT", "output"),
        ("VAR_ID", "${问候语}"),
        ("INPUT", "input"),
        ("VAR_ID", "${答复}"),
        ("LET", "let"),
        ("VAR_ID", "${话费查询模式}"),
        ("ASSIGN", "="),
        ("STRING_LITERAL", StringValue("话费")),
        ("LET", "let"),
        ("VAR_ID", "${举报模式}"),
        ("ASSIGN", "="),
        ("STRING_LITERAL", StringValue("举报")),
        ("BRANCH", "branch"),
        ("PROC_NAME", "话费查询"),
        ("WHEN", "when"),
        ("VAR_ID", "${答复}"),
        ("COMPARATOR", "like"),
        ("VAR_ID", "${话费查询模式}"),
        ("BRANCH", "branch"),
        ("PROC_NAME", "举报"),
        ("WHEN", "when"),
        ("VAR_ID", "${答复}"),
        ("COMPARATOR", "like"),
        ("VAR_ID", "${举报模式}"),
        ("DEFAULT", "default"),
        ("PROC_NAME", "重新问一遍"),
    ]

    for expected_result in expected_results:
        token: LexToken = lexer.token()
        assert token.type == expected_result[0]
        assert token.value == expected_result[1]

    token: LexToken = lexer.token()
    assert token is None
