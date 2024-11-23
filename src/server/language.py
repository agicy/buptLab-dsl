"""
A module for representing and evaluating a simple programming language.
"""

__all__: tuple[str] = (
    "IntegerValue",
    "StringValue",
    "Value",
    "Literal",
    "Variable",
    "Expression",
    "BooleanExpression",
    "Need",
    "InputStatement",
    "OutputStatement",
    "LetStatement",
    "Procedure",
    "Branch",
    "Default",
    "Program",
)

import re


class Value:
    """
    A base class representing a value.
    """

    def __init__(self, value: object) -> None:
        """
        Initializes a Value instance.

        Args:
            value: An object to be stored in the Value instance.
        """
        self._value: object = value

    def __repr__(self) -> str:
        """
        Returns a string representation of the Value instance.

        Returns:
            str: A string in the format 'Value(value=<value>)' where
            <value> is the object stored in the instance.
        """
        return f"Value(value={self.value})"

    @property
    def value(self) -> object:
        """
        Returns the value of the Value instance.

        Returns:
            object: The value stored in the instance.
        """
        return self._value

    def __eq__(self, other: object) -> bool:
        """
        Checks if this Value is equal to another object.

        Args:
            other: The object to compare with this Value.

        Returns:
            bool: True if the other object is a Value with the same value, False otherwise.
        """
        if isinstance(other, Value):
            return self.value == other.value
        return False


class IntegerValue(Value):
    """
    A class representing an integer value.
    """

    def __init__(self, value: int) -> None:
        """
        Initializes an IntegerValue instance.

        Args:
            value: An integer to be stored in the IntegerValue instance.
        """
        assert isinstance(value, int)
        super().__init__(value)

    def get_value(self, _) -> int:
        """
        Returns the integer value stored in the IntegerValue instance.

        Args:
            _: A placeholder argument (not used).

        Returns:
            int: The integer value stored in the instance.
        """
        return self.value


class StringValue(Value):
    """
    A class representing a string value.
    """

    def __init__(self, value: str) -> None:
        """
        Initializes a StringValue instance.

        Args:
            value: A string to be stored in the StringValue instance.
        """
        assert isinstance(value, str)
        super().__init__(value)

    def get_value(self, _) -> str:
        """
        Returns the string value stored in the StringValue instance.

        Args:
            _: A placeholder argument (not used).

        Returns:
            str: The string value stored in the instance.
        """
        return self.value


def positive(val: Value) -> Value:
    """
    Returns the positive value of the given IntegerValue.

    Args:
        val: A Value object, expected to be an IntegerValue.

    Returns:
        An IntegerValue representing the positive of the input integer.

    Raises:
        RuntimeError: If the input value is not an IntegerValue.
    """
    if isinstance(val, IntegerValue):
        return IntegerValue(+val.value)
    raise RuntimeError(f"Unable to calculate positive({val})")


def negative(val: Value) -> Value:
    """
    Returns the negative value of the given IntegerValue.

    Args:
        val: A Value object, expected to be an IntegerValue.

    Returns:
        An IntegerValue representing the negative of the input integer.

    Raises:
        RuntimeError: If the input value is not an IntegerValue.
    """
    if isinstance(val, IntegerValue):
        return IntegerValue(-val.value)
    raise RuntimeError(f"Unable to calculate negative({val})")


def add(lhs: Value, rhs: Value) -> Value:
    """
    Returns the sum of two Value objects.

    Args:
        lhs: A Value object to be added.
        rhs: A Value object to be added.

    Returns:
        A Value object representing the sum of the two input values.

    Raises:
        RuntimeError: If the input value is not an IntegerValue or a StringValue.
    """
    if isinstance(lhs, IntegerValue) and isinstance(rhs, IntegerValue):
        return IntegerValue(lhs.value + rhs.value)
    if isinstance(lhs, StringValue) and isinstance(rhs, StringValue):
        return StringValue(lhs.value + rhs.value)
    raise RuntimeError(f"Unable to calculate add({lhs}, {rhs})")


def sub(lhs: Value, rhs: Value) -> Value:
    """
    Returns the difference of two Value objects.

    Args:
        lhs: A Value object to be subtracted from.
        rhs: A Value object to be subtracted.

    Returns:
        A Value object representing the difference of the two input values.

    Raises:
        RuntimeError: If the input value is not an IntegerValue.
    """
    if isinstance(lhs, IntegerValue) and isinstance(rhs, IntegerValue):
        return IntegerValue(lhs.value - rhs.value)
    raise RuntimeError(f"Unable to calculate sub({lhs}, {rhs})")


def mul(lhs: Value, rhs: Value) -> Value:
    """
    Returns the product of two Value objects.

    Args:
        lhs: A Value object to be multiplied.
        rhs: A Value object to be multiplied.

    Returns:
        A Value object representing the product of the two input values.

    Raises:
        RuntimeError: If the input value is not an IntegerValue.
    """
    if isinstance(lhs, IntegerValue) and isinstance(rhs, IntegerValue):
        return IntegerValue(lhs.value * rhs.value)
    raise RuntimeError(f"Unable to calculate mul({lhs}, {rhs})")


def div(lhs: Value, rhs: Value) -> Value:
    """
    Returns the quotient of two Value objects.

    Args:
        lhs: A Value object to be divided.
        rhs: A Value object to be divided by.

    Returns:
        A Value object representing the quotient of the two input values.

    Raises:
        RuntimeError: If the input value is not an IntegerValue.
    """
    if isinstance(lhs, IntegerValue) and isinstance(rhs, IntegerValue):
        return IntegerValue(lhs.value // rhs.value)
    raise RuntimeError(f"Unable to calculate div({lhs}, {rhs})")


def mod(lhs: Value, rhs: Value) -> Value:
    """
    Returns the remainder of two Value objects.

    Args:
        lhs: A Value object to be divided.
        rhs: A Value object to be divided by.

    Returns:
        A Value object representing the remainder of the two input values.

    Raises:
        RuntimeError: If the input value is not an IntegerValue.
    """
    if isinstance(lhs, IntegerValue) and isinstance(rhs, IntegerValue):
        return IntegerValue(lhs.value % rhs.value)
    raise RuntimeError(f"Unable to calculate mod({lhs}, {rhs})")


def cast(val: Value, cast_type: str) -> Value:
    """
    Casts a Value to a given type.

    Args:
        val: A Value object to be casted.
        cast_type: A string indicating the type to cast to.

    Returns:
        A Value object representing the casted value.

    Raises:
        RuntimeError: If the input value is not an IntegerValue or a StringValue.
    """

    if cast_type == "integer":
        return IntegerValue(int(val.value))
    if cast_type == "string":
        return StringValue(str(val.value))
    raise RuntimeError(f"Unable to cast {val} to {cast_type}")


class Literal:
    """
    A class representing a literal value.
    """

    def __init__(self, value: object) -> None:
        """
        Initializes a Literal instance.

        Args:
            value: An object to be stored in the Literal instance.
        """
        self.value: object = value

    def __repr__(self) -> str:
        """
        Returns a string representation of the Literal instance.

        Returns:
            str: A string in the format 'Literal(value=<value>)' where
            <value> is the value stored in the instance.
        """
        return f"Value(value={self.value})"

    def get_value(self, _) -> Value:
        """
        Returns the value of the Literal instance.

        Returns:
            Value: The value stored in the Literal instance.
        """
        return self.value


class Variable:
    """
    A class representing a variable.
    """

    def __init__(self, name: str) -> None:
        """
        Initializes a Variable instance.

        Args:
            name: The name of the variable.
        """
        self.name: str = name

    def __repr__(self) -> str:
        """
        Returns a string representation of the Variable instance.

        Returns:
            str: A string in the format 'Variable(name=<name>)' where
            <name> is the name of the variable.
        """
        return f"Variable(name={self.name})"

    def get_value(self, table: dict[str, Value]) -> Value:
        """Retrieves the value of the variable from the given table.

        Args:
            table: The table of variables to lookup the value from.

        Returns:
            Value: The value of the variable.

        Raises:
            RuntimeError: If the variable is not found in the table.
        """
        if table.get(self.name) is None:
            raise RuntimeError("Variable {self.name} not found")
        return table[self.name]


class Expression:
    """
    A class representing an expression.
    """

    def __init__(self, words: tuple) -> None:
        """
        Initializes an Expression instance.

        Args:
            words: A tuple of words forming the expression.
        """
        self.words: tuple = words

    def __repr__(self) -> str:
        """
        Returns a string representation of the Expression instance.

        Returns:
            str: A string in the format 'Expression(words=<words>)' where
            <words> is the tuple of words forming the expression.
        """
        return f"Expression(words={self.words})"

    def get_value(self, table: dict[str, Value]) -> Value:
        """
        Evaluates the expression and returns the result.

        Args:
            table: The table of variables to lookup values from.

        Returns:
            Value: The result of the expression.

        Raises:
            RuntimeError: If the expression contains an unknown operator.
        """
        result: Value | None = None
        if len(self.words) == 1:
            result = self.words[0].get_value(table)
        elif len(self.words) == 2:
            operator: str = self.words[0]
            if operator == "+":
                result = positive(self.words[1].get_value(table))
            elif operator == "-":
                result = negative(self.words[1].get_value(table))
            else:
                raise RuntimeError(f"Unknown operator: {operator}")
        elif len(self.words) == 3:
            operator: str = self.words[1]
            if operator in ("+", "-", "*", "/", "%"):
                lef_oprand: Value = self.words[0].get_value(table)
                rig_oprand: Value = self.words[2].get_value(table)
                result = self._calc(lef_oprand, operator, rig_oprand)
            elif operator == "to":
                val = self.words[0].get_value(table)
                cast_type = self.words[2]
                result = cast(val, cast_type)
            else:
                raise RuntimeError(f"Unknown operator: {operator}")
        if result is None:
            raise RuntimeError("Unknown expression structure")
        return result

    def _calc(
        self, lef_oprand: Value, operator: str, rig_oprand: Value | None
    ) -> Value:
        """
        Evaluates a binary expression.

        Args:
            lef_oprand: The left operand.
            operator: The operator.
            rig_oprand: The right operand.

        Returns:
            Value: The result of the expression.

        Raises:
            RuntimeError: If the operator is unknown.
        """
        if operator == "+":
            return add(lef_oprand, rig_oprand)
        if operator == "-":
            return sub(lef_oprand, rig_oprand)
        if operator == "*":
            return mul(lef_oprand, rig_oprand)
        if operator == "/":
            return div(lef_oprand, rig_oprand)
        if operator == "%":
            return mod(lef_oprand, rig_oprand)
        raise RuntimeError(f"Unknown operator: {operator}")


def match(text: str, pattern: str) -> bool:
    """
    Checks if the given text matches the specified pattern using regular expressions.

    Args:
        text: The string to be searched.
        pattern: The regular expression pattern to search for.

    Returns:
        bool: True if the pattern is found in the text, False otherwise.
    """
    regex: re.Pattern[str] = re.compile(pattern=pattern)
    return regex.search(string=text) is not None


class BooleanExpression:
    """
    A class representing a boolean expression.
    """

    def __init__(self, words: tuple) -> None:
        """
        Initializes a BooleanExpression instance.

        Args:
            words: A tuple of words forming the boolean expression.
        """
        self.words: tuple = words

    def __repr__(self) -> str:
        """
        Returns a string representation of the BooleanExpression instance.

        Returns:
            str: A string in the format 'BooleanExpression(words=<words>)' where
            <words> is the tuple of words forming the boolean expression.
        """
        return f"BooleanExpression(words={self.words})"

    def get_value(self, table: dict[str, Value]) -> bool:
        """
        Evaluates the boolean expression and returns the result.

        Args:
            table: The table of variables to lookup values from.

        Returns:
            bool: The result of the boolean expression.

        Raises:
            RuntimeError: If the expression contains an unknown operator or
                if the operands are not of the correct type.
        """
        if len(self.words) == 2:
            operator = self.words[0]
            if operator == "not":
                return not self.words[1].get_value(table)
            raise RuntimeError(f"Unknown operator: {operator}")
        if len(self.words) == 3:
            operator = self.words[1]
            lef_oprand = self.words[0].get_value(table)
            rig_oprand = self.words[2].get_value(table)
            if isinstance(lef_oprand, bool) and isinstance(rig_oprand, bool):
                return self._bool_binop(lef_oprand, operator, rig_oprand)
            if isinstance(lef_oprand, Value) and isinstance(rig_oprand, Value):
                return self._value_binop(lef_oprand, operator, rig_oprand)
            raise RuntimeError(
                f"Invalid bool expression ({lef_oprand}, {operator}, {rig_oprand})"
            )
        raise RuntimeError("Unknown boolean expression structure")

    def _bool_binop(self, lef: bool, operator: str, rig: bool) -> bool:
        """
        Evaluates a binary boolean expression.

        Args:
            lef: The left boolean operand.
            operator: The boolean operator.
            rig: The right boolean operand.

        Returns:
            bool: The result of the boolean expression.
        """
        if operator == "and":
            return lef and rig
        if operator == "or":
            return lef or rig
        raise RuntimeError(f"Unknown boolean operator: {operator}")

    def _value_binop(self, lef: Value, operator: str, rig: Value) -> bool:
        """
        Evaluates a binary expression between two values.

        Args:
            lef: The left value operand.
            operator: The comparator.
            rig: The right value operand.

        Returns:
            bool: The result of the boolean expression.
        """
        result = False
        if operator == "==":
            result = lef.value == rig.value
        elif operator == "!=":
            result = lef.value != rig.value
        elif operator == "<":
            result = lef.value < rig.value
        elif operator == "<=":
            result = lef.value <= rig.value
        elif operator == ">":
            result = lef.value > rig.value
        elif operator == ">=":
            result = lef.value >= rig.value
        elif operator == "like":
            result = match(text=lef.value, pattern=rig.value)
        else:
            raise RuntimeError(f"Unknown comparator: {operator}")
        return result


class Need:
    """
    A class representing a need for a variable.
    """

    def __init__(self, var_id: str) -> None:
        """
        Initializes a Need instance.

        Args:
            var_id: The variable id of the variable to be needed.
        """
        self._var_id: str = var_id

    def __repr__(self) -> str:
        """
        Returns a string representation of the Need instance.

        Returns:
            str: A string in the format 'Need(var_id=<var_id>)' where
            <var_id> is the variable id of the variable to be needed.
        """
        return f"Need(var_id={self._var_id})"

    @property
    def var_id(self) -> str:
        """
        Returns the variable id of the variable to be needed.

        Returns:
            str: The variable id of the variable to be needed.
        """
        return self._var_id


class LetStatement:
    """
    A class representing a let statement.
    """

    def __init__(self, var_id: str, expr: Expression) -> None:
        """
        Initializes a LetStatement instance.

        Args:
            var_id: The variable id to be associated with the expression.
            expr: The expression to be evaluated and assigned to the variable.
        """
        self._var_id: str = var_id
        self._expr: Expression = expr

    def __repr__(self) -> str:
        """
        Returns a string representation of the LetStatement instance.

        Returns:
            str: A string in the format 'LetStatement(var_id=<var_id>, expr=<expr>)'
            where <var_id> is the variable id and <expr> is the expression.
        """
        return f"LetStatement(var_id={self.var_id}, expr={self.expr})"

    @property
    def var_id(self) -> str:
        """
        Returns the variable id associated with the expression.

        Returns:
            str: The variable id associated with the expression.
        """
        return self._var_id

    @property
    def expr(self) -> Expression:
        """
        Returns the expression to be evaluated and assigned to the variable.

        Returns:
            Expression: The expression to be evaluated and assigned to the variable.
        """
        return self._expr


class InputStatement:
    """
    A class representing an input statement.
    """

    def __init__(self, var_id: str) -> None:
        """
        Initializes an InputStatement instance.

        Args:
            var_id: The variable id to store the input value into.
        """
        self._var_id: str = var_id

    def __repr__(self) -> str:
        """
        Returns a string representation of the InputStatement instance.

        Returns:
            str: A string in the format 'InputStatement(var_id=<var_id>)' where
            <var_id> is the variable id to store the input value into.
        """
        return f"InputStatement(var_id={self.var_id})"

    @property
    def var_id(self) -> str:
        """
        Returns the variable id to store the input value into.

        Returns:
            str: The variable id to store the input value into.
        """
        return self._var_id


class OutputStatement:
    """
    A class representing an output statement.
    """

    def __init__(self, expr: Expression) -> None:
        """
        Initializes an OutputStatement instance.

        Args:
            expr: The expression to be evaluated and printed when the statement is executed.
        """
        self._expr: Expression = expr

    def __repr__(self) -> str:
        """
        Returns a string representation of the OutputStatement instance.

        Returns:
            str: A string in the format 'OutputStatement(expr=<expr>)' where
            <expr> is the expression to be evaluated and printed when the statement is executed.
        """
        return f"OutputStatement(expr={self.expr})"

    @property
    def expr(self) -> Expression:
        """
        Returns the expression to be evaluated and printed when the statement is executed.

        Returns:
            Expression: The expression to be evaluated and printed when the statement is executed.
        """
        return self._expr


Statement = LetStatement | InputStatement | OutputStatement


class Branch:
    """
    A class representing a branch statement.
    """

    def __init__(self, proc_name: str, bexpr: BooleanExpression) -> None:
        """
        Initializes a Branch instance.

        Args:
            proc_name: The id of the procedure to call if the boolean expression evaluates to True.
            bexpr: The boolean expression to evaluate when the statement is executed.
        """
        self._proc_name: str = proc_name
        self._bexpr: BooleanExpression = bexpr

    def __repr__(self) -> str:
        """
        Returns a string representation of the Branch instance.

        Returns:
            str: A string in the format 'Branch(proc_name=<proc_name>, bexpr=<bexpr>)' where
            <proc_name> is the id of the procedure to call if the boolean expression evaluates
            to True, and <bexpr> is the boolean expression to evaluate when the statement
            is executed.
        """
        return f"Branch(proc_name={self.proc_name}, bexpr={self.bexpr})"

    @property
    def proc_name(self) -> str:
        """
        Returns the id of the procedure to call if the boolean expression evaluates to True.

        Returns:
            str: The id of the procedure to call if the boolean expression evaluates to True.
        """
        return self._proc_name

    @property
    def bexpr(self) -> BooleanExpression:
        """
        Returns the boolean expression to evaluate when the statement is executed.

        Returns:
            BooleanExpression: The boolean expression to evaluate when the statement is executed.
        """
        return self._bexpr


class Default:
    """
    A class representing a default statement.
    """

    def __init__(self, proc_name: str) -> None:
        """
        Initializes a Default instance.

        Args:
            proc_name: The id of the procedure to call when no other branch evaluates to True.
        """
        self._proc_name = proc_name

    def __repr__(self) -> str:
        """
        Returns a string representation of the Default instance.

        Returns:
            str: A string in the format 'Default(proc_name=<proc_name>)' where
            <proc_name> is the id of the procedure to call when no other branch evaluates
            to True.
        """
        return f"Default(proc_name={self.proc_name})"

    @property
    def proc_name(self) -> str:
        """
        Returns the id of the procedure to call when no other branch evaluates to True.

        Returns:
            str: The id of the procedure to call when no other branch evaluates to True.
        """
        return self._proc_name


class Procedure:
    """
    A class representing a procedure.
    """

    def __init__(
        self, name: str, statements: list[Statement], branches: list[Branch | Default]
    ) -> None:
        """
        Initializes a Procedure instance.

        Args:
            name: The name of the procedure.
            statements: The list of statements to be executed in the procedure.
            branches: The list of branches or default statements associated with the procedure.
        """
        self._name: str = name
        self._statements: list[Statement] = statements
        self._branches: list[Branch | Default] = branches

    def __repr__(self) -> str:
        """
        Returns a string representation of the Procedure instance.

        Returns:
            str: A string in the format
            'Procedure(name=<name>, statements=<statements>, branches=<branches>)' where
            <name> is the name of the procedure, <statements> is the list of statements to be
            executed, and <branches> is the list of branches or default statements associated with
            the procedure.
        """
        return (
            f"Procedure(name={self.name}, statements={self.statements}, "
            f"branches={self.branches})"
        )

    @property
    def name(self) -> str:
        """
        Returns the name of the procedure.

        Returns:
            str: The name of the procedure.
        """
        return self._name

    @property
    def statements(self) -> list[Statement]:
        """
        Returns the list of statements to be executed in the procedure.

        Returns:
            list[Statement]: The list of statements to be executed in the procedure.
        """
        return self._statements

    @property
    def branches(self) -> list[Branch | Default]:
        """
        Returns the list of branches or default statements associated with the procedure.

        Returns:
            list[Branch | Default]: The list of branches or default statements associated with
            the procedure.
        """
        return self._branches


class Program:
    """
    A class representing a program.
    """

    def __init__(self, needs: list[Need], procedures: list[Procedure]) -> None:
        """
        Initializes a Program instance.

        Args:
            needs: A list of Need instances representing the required variables.
            procedures: A list of Procedure instances representing the procedures in the program.
        """
        self._needs: list[Need] = needs
        self._procedures: list[Procedure] = procedures

    def __repr__(self) -> str:
        """
        Returns a string representation of the Program instance.

        Returns:
            str: A string in the format 'Program(needs=<needs>, procedures=<procedures>)' where
            <needs> is the list of required variables and <procedures> is the list of procedures
            in the program.
        """
        return f"Program(needs={self._needs}, procedures={self._procedures})"

    @property
    def needs(self) -> list[Need]:
        """
        Returns the list of required variables.

        Returns:
            list[Need]: The list of required variables.
        """
        return self._needs

    @property
    def procedures(self) -> list[Procedure]:
        """
        Returns the list of procedures in the program.

        Returns:
            list[Procedure]: The list of procedures in the program.
        """
        return self._procedures
