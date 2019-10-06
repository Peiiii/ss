import socket

def demo():
    sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect(('45.77.124.235',8888))
    sock.sendall('hello sever')
    recv=sock.recv(1024)
    print(recv)