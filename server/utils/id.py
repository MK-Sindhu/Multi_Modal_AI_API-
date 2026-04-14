import socket


def get_container_id() -> str:
    return socket.gethostname()
