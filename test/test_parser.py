import pytest
from server.parser import Parser
from server.lexer import Lexer
from server.language import *


@pytest.fixture
def parser() -> Parser:
    lexer = Lexer()
    return Parser(lexer)


def test_parse_program(parser) -> None:
    source = """need ${x}
    procedure p1
    """
    program = parser.parse(source)
    assert isinstance(program, Program)
    assert program.needs[0].var_id == "${x}"
    assert program.procedures[0].name == "p1"


def test_parse_need(parser) -> None:
    source = """need ${需要}
    procedure p1"""
    program = parser.parse(source)
    assert isinstance(program, Program)
    assert len(program.needs) == 1
    assert program.needs[0].var_id == "${需要}"


def test_parse_procedure(parser) -> None:
    source = "procedure p1"
    program = parser.parse(source)
    assert isinstance(program, Program)
    assert program.procedures[0].name == "p1"


def test_parse_let_statement(parser):
    source = """
    need ${六六六}
    procedure 初始
        input ${六}
        let ${六六} = ${六}
        output ${六六六}
    """
    program = parser.parse(source)
    assert isinstance(program, Program)
    assert program.procedures[0].statements[1].var_id == "${六六}"


def test_parse_input_statement(parser):
    source = """
    need ${六六六}
    procedure 初始
        input ${六}
        output ${六六六}
    """
    program = parser.parse(source)
    assert isinstance(program, Program)
    assert program.procedures[0].statements[0].var_id == "${六}"


def test_parse_output_statement(parser):
    source = """
    need ${六六六}
    procedure 初始
        input ${六}
        output ${六六六}
    """
    program = parser.parse(source)
    assert isinstance(program, Program)
    assert program.procedures[0].statements[1].expr.name == "${六六六}"


def test_parse_syntax_error(parser):
    source = " invalid syntax ;"
    with pytest.raises(SyntaxError):
        parser.parse(source)
