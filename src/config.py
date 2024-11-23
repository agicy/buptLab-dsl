__all__: list[str] = [
    "delimiter",
    "exit_signal",
    "default_port",
]

delimiter: bytes = b"hello;__2022212720__;world"
exit_signal: bytes = b"goodbye;__2022212720__;world"
default_port: int = 10001
