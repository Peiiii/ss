import socket

def demo():
    sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect(('127.0.0.1',8888))

    a=sock.sendall(b'n'*7777)
    print(a)
    recv=sock.recv(1024)
    print(recv)

demo()