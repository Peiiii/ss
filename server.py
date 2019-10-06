import socket,time,json
import socketserver,select,struct
from encryptor import encrypt,decrypt
import encryptor

class ThreadingTCPServer(socketserver.ThreadingMixIn,socketserver.TCPServer):
    pass
def connect(head):
    addrtype=head['addrtype']
    addr=head['addr']
    port=head['port']
    if addrtype==1:
        sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    elif addrtype==4:
        sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    try:
        sock.connect((addr,port))
    except:
        print(addr,port)
        raise

    return sock

class Socks5Server(socketserver.StreamRequestHandler):
    def handle(self):
        try:
            print('new connection :', self.request)
            sock = self.connection
            data=encryptor.decrypt_head(sock.recv(128))
            print('data:',data)
            head=str(data,'utf-8').strip()
            head=json.loads(head)
            self.wfile.write(b'success')
            remote = connect(head)
            self.handle_tcp(sock,remote)
        except socket.error:
            print('socket error')
            raise
    def handle_tcp(self,sock, remote):
        try:
            fdset = [sock, remote]
            while True:
                r, w, e = select.select(fdset, [], [])
                if remote in r:
                    data=remote.recv(4096)
                    print('from remote server:%s,%s' % (data, len(data)))
                    data=encrypt(data)
                    if sock.send(data) <= 0: break
                if sock in r:
                    data = sock.recv(4096)
                    data=decrypt(data)
                    print('from client:%s,%s' % (data, len(data)))
                    if remote.send(data) <= 0:break
        finally:
            sock.close()
            remote.close()
            print('communication with remote has terminated.')
if __name__=='__main__':

    S=ThreadingTCPServer(('localhost',8888),Socks5Server)
    S.serve_forever()

