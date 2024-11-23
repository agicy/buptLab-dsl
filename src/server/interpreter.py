"""
Interpreter for the language.
"""

__all__: list[str] = [
    "Interpreter",
]

from config import delimiter
from config import exit_signal
from server.language import (
    StringValue,
    Value,
    Expression,
    BooleanExpression,
    Need,
    InputStatement,
    OutputStatement,
    LetStatement,
    Procedure,
    Branch,
    Default,
    Program,
)
from server.interface import (
    process_natrual_language,
    generate_multimedia_response,
)


class Interpreter:
    """
    Interpreter for the language.
    """

    def __init__(self, program: Program, conn, addr) -> None:
        """
        Initializes an Interpreter instance.

        Args:
            program: The Program object representing the program to run.
            conn: The socket object representing the connection to the client.
            addr: The address of the client.
        """
        self._program: Program = program
        self._conn = conn
        self._addr = addr
        self._excess_data: bytes = b""
        self._vartable: dict[str, Value] = {}

    def run(self) -> None:
        """
        Runs the program.

        This method executes the procedures in the program from top to bottom. For each
        procedure, it executes the statements in the procedure from top to bottom. If a
        branch statement is encountered, it branches to the specified procedure. If a
        default statement is encountered, it branches to the specified procedure. If the
        end of the program is reached, it sends a special exit signal to the client and
        terminates the connection.

        :return: None
        """
        for need in self._program.needs:
            self._execute_need(need)

        current_procedure = self._program.procedures[0]

        while current_procedure is not None:
            next_proc_name = self._execute_procedure(current_procedure)
            current_procedure = None
            for proc in self._program.procedures:
                if proc.name == next_proc_name:
                    current_procedure = proc
                    break

        self._conn.sendall(exit_signal)

    def get_vartable(self) -> dict[str, Value]:
        """
        Returns a dictionary mapping variable ids to their values.

        :return: A dictionary mapping variable ids to their values.
        """
        return self._vartable

    def _calculate(self, expression: Expression) -> Value:
        """
        Calculates the value of the given expression.

        Args:
            expression: The expression to be calculated.

        Returns:
            Value: The value of the expression.
        """
        return expression.get_value(self._vartable)

    def _check_condition(self, bexpr: BooleanExpression) -> bool:
        """
        Checks the condition of the given boolean expression.

        Args:
            bexpr: The boolean expression to be checked.

        Returns:
            bool: The result of the condition check.
        """
        return bexpr.get_value(self._vartable)

    def _execute_need(self, need: Need) -> None:
        """
        Executes a need statement by prompting the client for input for a required variable.

        Args:
            need: The Need instance containing the variable id to be prompted for input.

        This method outputs a message indicating the required variable, reads the input
        from the client, and stores the input as a StringValue in the variable table.
        """
        var_id: str = need.var_id
        self._output(output=f"{var_id} required: ")
        result: str = self._input()
        self._vartable[var_id] = StringValue(result)

    def _execute_let(self, var_id: str, expr: Expression) -> None:
        """
        Executes a let statement by calculating the given expression and
        storing the result in the given variable id.

        Args:
            var_id: The variable id to store the result of the expression in.
            expr: The expression to be evaluated and stored in the variable.
        """
        self._vartable[var_id] = self._calculate(expr)

    def _execute_input(self, var_id: str) -> None:
        """
        Executes an input statement by reading a line of input from the
        connection and storing the result in the given variable id.

        Args:
            var_id: The variable id to store the result of the input in.
        """
        text: str = self._input()
        result: str = process_natrual_language(text)
        self._vartable[var_id] = StringValue(result)

    def _execute_output(self, expr: Expression) -> None:
        """
        Executes an output statement by evaluating the given expression and
        sending the result to the client.

        Args:
            expr: The expression to be evaluated and sent to the client.
        """
        value = self._calculate(expr)
        self._output(output=value.value)

    def _execute_statement(self, statement) -> None:
        """
        Executes a statement by delegating to the appropriate method.

        Args:
            statement: The statement to be executed.

        Raises:
            RuntimeError: If the statement is unknown.
        """
        if isinstance(statement, LetStatement):
            self._execute_let(statement.var_id, statement.expr)
        elif isinstance(statement, InputStatement):
            self._execute_input(statement.var_id)
        elif isinstance(statement, OutputStatement):
            self._execute_output(statement.expr)
        else:
            raise RuntimeError(f"unknown statement type: {statement}")

    def _execute_procedure(self, procedure: Procedure) -> str | None:
        """
        Executes a procedure by executing its statements and evaluating its branches.

        Args:
            procedure: The Procedure instance to be executed.

        Returns:
            str | None: The id of the procedure to call next if a branch evaluates to
                True, or None if no branch evaluates to True.
        """
        for statement in procedure.statements:
            self._execute_statement(statement)
        for branch in procedure.branches:
            if isinstance(branch, Branch):
                if self._check_condition(branch.bexpr):
                    return branch.proc_name
            elif isinstance(branch, Default):
                return branch.proc_name
        return None

    def _input(self) -> str:
        """
        Reads input from the connection until a delimiter is encountered.

        Sends a delimiter to the client to signal readiness to receive data.
        Continuously receives data in chunks and appends it until the delimiter
        is found. Splits the data at the delimiter, stores excess data for future
        reads, and returns the decoded string of the data up to the delimiter.

        Returns:
            str: The input data received from the client up to the delimiter.
        """
        self._conn.sendall(delimiter)
        data = self._excess_data
        while True:
            chunk = self._conn.recv(1024)
            data += chunk
            if delimiter in data:
                break
        excess_data: bytes = data.split(delimiter, 1)[1]
        data: bytes = data.split(delimiter, 1)[0]
        self._excess_data: bytes = excess_data
        return data.decode()

    def _output(self, output: str) -> None:
        """
        Sends the given output string to the client, followed by a newline.

        Args:
            output: The string to be sent to the client.
        """
        response = generate_multimedia_response(output)
        self._conn.sendall((response + "\n").encode())
