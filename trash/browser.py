import socket,requests,os,sys

def demo1():
    host, port = 'localhost', 9999
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    print('socket name :',sock.getsockname())
    sock.sendall(bytes('hello,i like english and ...' + '\n', 'utf-8'))
    recieved = str(sock.recv(1024))
    print(recieved)
def demo2():
    host, port = 'www.sina.com.cn',80
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    send_data='GET / HTTP/1.1\r\nHost:www.sina.com.cn\r\nConnection:close\r\n\r\n'
    sock.sendall(bytes(send_data, 'utf-8'))
    recieved = str(sock.recv(1024))
    print(recieved)

def demo3():
    # os.system('set http_proxy=http://localhost:9999')
    # os.system('set https_proxy=http://localhost:9999')
    import requests
    proxies={
        'http':'socks5://localhost:9999',
        'https':'scoks5://localhost:9999'
    }
    res=requests.get('http://www.sina.com.cn',proxies=proxies)
    print(res)

# demo1()
demo3()

