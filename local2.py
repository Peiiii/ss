import socket, json
import socketserver,select,struct
from utils import encryptor

# proxy_addr,proxy_port='127.0.0.1',8888
# proxy_addr,proxy_port='45.77.124.235',8888



with open('config.json','r') as f:
    cfg=json.load(f)
proxy_addr,proxy_port=cfg['remote_server_address'],cfg['remote_server_port']
proxy_address_family=socket.AF_INET



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
    elif addrtype==4:
        sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    sock.connect((addr,port))
    return sock
def parse_socks5_head(sock):
    '''完成握手，并获取相关信息'''
    # 1. Version
    a = sock.recv(262)
    tprint('from browser recv(262):', a)
    sock.send(b"\x05\x00")
    # 2. Request
    data = sock.recv(4)
    tprint('from browser data:', data)
    mode = data[1]
    addrtype = data[3]
    if addrtype == 1:  # IPv4
        addr = socket.inet_ntoa(sock.recv(4))
    elif addrtype == 3:  # Domain name
        addr = str(sock.recv(sock.recv(1)[0]),'utf-8')
    elif addrtype == 4:  # IPv6
        addr = socket.inet_ntop(socket.AF_INET6, sock.recv(16))
    port = struct.unpack('>H', sock.recv(2))[0]
    return addrtype,addr,port

def connect_through_proxy(head):
    '''以远程代理服务器为中介与目标主机建立虚拟连接'''
    remote = socket.socket(proxy_address_family, socket.SOCK_STREAM)
    remote.connect((proxy_addr, proxy_port))
    print('Tcp connect to remote proxy server %s:%s' % (proxy_addr, proxy_port))
    head2 = json.dumps(head)
    remote.sendall(encryptor.encrypt_head(head2))
    # time.sleep(1)
    s=remote.recv(7)
    tprint('recv:',s)

    return remote


class Socks5Server(socketserver.StreamRequestHandler):
    def handle(self):
        try:
            print('new connection:',self.request)
            sock = self.connection

            addrtype,addr,port=parse_socks5_head(sock)
            head = {
                'addrtype': addrtype,
                'addr': addr,
                'port': port
            }
            print('destination info:',head)
            try:
                remote=connect_through_proxy(head)
                (addr, port) = remote.getsockname()
                status= b'\x05\x00\x00\x01' if remote.family==socket.AF_INET else b'\x05\x00\x00\x04'
                reply = status+ socket.inet_pton(remote.family, addr) + struct.pack(">H", port)
            except socket.error:
                reply = b'\x05\x05\x00\x01\x00\x00\x00\x00\x00\x00'
                raise
            self.wfile.write(reply)
            tprint('reply to browser:',reply)
            self.test_firewall(remote)
            self.handle_tcp(sock, remote)
        except socket.error:
            print('socket error')
            raise
    def test_firewall(self,sock):
        def confirm(sock):
            data=sock.recv(4096)
            if not isinstance(data,str):
                data=str(data)
                data='I(client) recieved :'+data
                print('**test_firewall_resv:',data)
                data=bytes(data,'utf-8')
                sock.sendall(data)
        confirm(sock)
        confirm(sock)
        confirm(sock)
        confirm(sock)
    def handle_tcp(self,sock, remote):
        print('local server start exchanging data between client and remote.')
        try:
            fdset = [sock, remote]
            while True:
                r, w, e = select.select(fdset, [], [])
                if remote in r:
                    data=encryptor.decrypt(remote.recv(8192))
                    tprint('from remote:%s,%s' % (data, len(data)))
                    if sock.send(data) <= 0: break
                if sock in r:
                    data=sock.recv(4096)
                    tprint('from brower:%s,%s' % (data, len(data)))
                    if len(data)==0:break
                    remote.send(encryptor.encrypt(data))
        finally:
            sock.close()
            remote.close()
            print('communication with remote has terminated.')

def run_local():
    S = ThreadingTCPServer(('localhost', 9999), Socks5Server)
    S.serve_forever()

if __name__=='__main__':
    proxy_addr,proxy_port='127.0.0.1',8888
    run_local()


