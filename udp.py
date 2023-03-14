import socket
import select
import time

SERVER_HOST, SERVER_PORT = ('<IP>', 8000)


def client():
    sock = socket.socket()
    print('Connecting to server...')
    sock.connect((SERVER_HOST, SERVER_PORT))
    print('Connected\nWaiting for peer info...')
    info = sock.recv(1024)
    sock.close()
    my_host, my_nat_port, peer_host, peer_port = info.decode().split()
    print('Got peer info\nstarting transmitting UDP packets...')

    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.bind(('', int(my_nat_port)))
    while True:
        udp_sock.sendto(b'Hello world!', (peer_host, int(peer_port)))
        # check if we got new message, if not continue
        if not select.select([udp_sock], [], [], 0):
            continue
        message, addr = udp_sock.recvfrom(1024)
        host, port = addr
        print(f'Received {message} from {host}:{port}')
        time.sleep(1)


if __name__ == '__main__':
    client()
