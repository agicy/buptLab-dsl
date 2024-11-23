"""
Run the server.
"""

import argparse
import threading
import signal
import socket
import config
from server.lexer import Lexer
from server.parser import Parser
from server.interpreter import Interpreter
from server.language import Program


def start(filename: str, host: str, port: int) -> None:
    """
    Starts a server.

    Args:
        filename: The filename of the source code file for the server.
        host: The host to listen on.
        port: The port to listen on.
    """

    # open file and read its content
    with open(file=filename, mode="r", encoding="utf-8") as file:
        source_code = file.read()

    # create lexer and parser
    lexer: Lexer = Lexer()
    parser: Parser = Parser(lexer)

    # parse the source code
    program: Program = parser.parse(source_code)

    # create socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print(f"Server is listening on {host}:{port}")

    def handle_connection(conn, addr) -> None:
        print(f"Connected by {addr}")
        interpreter: Interpreter = Interpreter(program, conn, addr)
        interpreter.run()
        conn.close()
        print(f"Disconnected by {addr}")

    while True:
        conn, addr = server_socket.accept()
        thread = threading.Thread(target=handle_connection, args=(conn, addr))
        thread.start()


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    arg_parser = argparse.ArgumentParser(description="Run the server.")
    arg_parser.add_argument("filename", help="The path to the source file.")
    arg_parser.add_argument(
        "--host", default="localhost", help="The host to listen on."
    )
    arg_parser.add_argument(
        "--port", type=int, default=config.default_port, help="The port to listen on."
    )
    args = arg_parser.parse_args()

    start(filename=args.filename, host=args.host, port=args.port)
