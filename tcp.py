import socket
import select
import time

SERVER_HOST, SERVER_PORT = ('<IP>', 8000)


def on_connect(conn: 'socket.socket'):
    while True:
        if select.select([conn], [], [], 0)[0]:
            message = conn.recv(1024)
            print(f'Received {message} from {conn.getpeername()}')
        else:
            conn.send(b'Hello world!')
        time.sleep(1)


def client():
    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print('Connecting to server...')
    sock.connect((SERVER_HOST, SERVER_PORT))
    my_priv_addr = sock.getsockname()
    print('Connected to server\nWaiting for peer info...')
    info = sock.recv(1024)
    sock.close()
    my_host, my_nat_port, peer_host, peer_port = info.decode().split()

    accpet_sock = socket.socket()
    accpet_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    accpet_sock.bind(('', int(my_nat_port)))
    accpet_sock.listen(1)

    connect_sock = socket.socket()
    connect_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connect_sock.bind(my_priv_addr)
    connect_sock.settimeout(0.1)
    while True:
        if connect_sock.connect_ex((peer_host, int(peer_port))) == 0:
            print(f'Connected to {peer_host}:{peer_port} using connect()')
            on_connect(connect_sock)
        elif select.select([accpet_sock], [], [], 0)[0]:
            conn, addr = accpet_sock.accept()
            print(f'Connected to {peer_host}:{peer_port} using accept()')
            on_connect(conn)


if __name__ == '__main__':
    client()
