"""
Run the client.
"""

import socket
import argparse
import config


def main(host: str, port: int) -> None:
    """
    Runs the client.

    This function connects to the server and enters a loop of receiving and sending
    messages. The loop continues until the server sends the special exit signal.

    :param host: The host to connect to.
    :param port: The port to connect to.
    :return: None
    """

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    excess_data = b""
    while True:
        data = excess_data
        while True:
            chunk = client_socket.recv(1024)
            data += chunk
            if config.delimiter in data:
                break
            if config.exit_signal in data:
                output = data.split(config.exit_signal, maxsplit=1)[0]
                print(f"对方：{output.decode()}")
                print("对方已终止通信")
                client_socket.close()
                return
        output, excess_data = data.split(config.delimiter, 1)
        print("对方：")
        print(f"{output.decode()}")

        user_input = input("输入 > ")
        client_socket.sendall(user_input.encode())
        client_socket.sendall(config.delimiter)
        print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the client.")
    parser.add_argument("--host", default="localhost", help="The host to connect to.")
    parser.add_argument(
        "--port", type=int, default=config.default_port, help="The port to connect to."
    )
    args = parser.parse_args()
    main(host=args.host, port=args.port)

    print("客户端已退出")
