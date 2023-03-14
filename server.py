import socket

BIND_ADDR = ('', 8000)


def server():
    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(BIND_ADDR)
    sock.listen(2)
    print('Waiting for connection...')
    while True:
        conn1, addr1 = sock.accept()
        print(f'Got connection from {addr1[0]}:{addr1[1]}')
        conn2, addr2 = sock.accept()
        print(f'Got connection from {addr2[0]}:{addr2[1]}')
        print('Sending each one NAT host port')
        # We got two clients
        # your_ip, your_port, peer_ip, peer_port ( peer NAT port! )
        conn1.sendall(f'{addr1[0]} {addr1[1]} {addr2[0]} {addr2[1]}'.encode())
        conn2.sendall(f'{addr2[0]} {addr2[1]} {addr1[0]} {addr1[1]}'.encode())
        conn1.close()
        conn2.close()


if __name__ == '__main__':
    server()
