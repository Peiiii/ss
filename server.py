import socket, json
import socketserver,select
from utils.encryptor import encrypt,decrypt
from utils import encryptor

TEST_MODE=0
def tprint(*args,**kwargs):
    if TEST_MODE:
        print(*args,**kwargs)

class ThreadingTCPServer(socketserver.ThreadingMixIn,socketserver.TCPServer):
    pass
def connect(head):
    addrtype=head['addrtype']
    addr=head['addr']
    port=head['port']
    if addrtype==1:
        sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    elif addrtype==3:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    elif addrtype==4:
        sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    try:
        sock.connect((addr,port))
    except:
        tprint(addr,port)
        raise

    return sock

class Socks5Server(socketserver.StreamRequestHandler):
    def handle(self):
        try:
            print('new connection :', self.request)
            sock = self.connection
            data=sock.recv(256)
            data=encryptor.decrypt_head(data)
            tprint('data:',data)
            head=json.loads(data)
            print('target info: ',head)
            self.wfile.write(b'success')
            remote = connect(head)
            self.handle_tcp(sock,remote)
        except socket.error:
            tprint('socket error')
            raise
    def handle_tcp(self,sock, remote):
        try:
            fdset = [sock, remote]
            while True:
                r, w, e = select.select(fdset, [], [])
                if remote in r:
                    data=remote.recv(4096)
                    tprint('from remote server:%s,%s' % (data, len(data)))
                    if len(data) <= 0: break
                    sock.send(encrypt(data))
                if sock in r:
                    data=decrypt(sock.recv(8192))
                    tprint('from client:%s,%s' % (data, len(data)))
                    if remote.send(data) <= 0:break
        finally:
            sock.close()
            remote.close()
            tprint('communication with remote has terminated.')
def clean_linux_port(port):
    return
    import os,time
    try:
        os.system('cleanp '+str(port))
        time.sleep(0.2)
    except:
        print('clean port failed.')
if __name__=='__main__':
    addr,port ='0.0.0.0',8888
    import platform
    sysstr=platform.system()
    print('system type: %s'%(sysstr))
    if str=='Linux':
        clean_linux_port(port)
    S=ThreadingTCPServer((addr,port),Socks5Server)
    print('waiting for connect...')
    S.serve_forever()
