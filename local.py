import socket,time,json
import socketserver,select,struct
from encryptor import encrypt,decrypt
import encryptor
proxy_addr,proxy_port='127.0.0.1',8888
proxy_addr,proxy_port='45.77.124.235',8888
proxy_address_family=socket.AF_INET



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
    print('from browser recv(262):', a)
    sock.send(b"\x05\x00")
    # 2. Request
    data = sock.recv(4)
    print('from browser data:', data)
    mode = data[1]
    addrtype = data[3]
    if addrtype == 1:  # IPv4
        addr = socket.inet_ntoa(sock.recv(4))
    elif addrtype == 3:  # Domain name
        addr = sock.recv(ord(sock.recv(1)[0]))
    elif addrtype == 4:  # IPv6
        addr = socket.inet_ntop(socket.AF_INET6, sock.recv(16))
    port = struct.unpack('>H', sock.recv(2))[0]
    return addrtype,addr,port

def connect_through_proxy(head):
    '''以远程代理服务器为中介与目标主机建立虚拟连接'''
    remote = socket.socket(proxy_address_family, socket.SOCK_STREAM)
    remote.connect((proxy_addr, proxy_port))
    print('Tcp connect to remote proxy server %s:%s' % (proxy_addr, proxy_port))
    head2 = bytes(json.dumps(head).ljust(128,' '), 'utf-8')
    remote.sendall(encryptor.encrypt_head(head2))
    # time.sleep(1)
    s=remote.recv(7)
    print('recv:',s)

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
            print('reply to browser:',reply)
            # 3. Transfering
            self.handle_tcp(sock, remote)
        except socket.error:
            print('socket error')
            raise

    def handle_tcp(self,sock, remote):
        print('local server start exchanging data between client and remote.')
        try:
            fdset = [sock, remote]
            while True:
                r, w, e = select.select(fdset, [], [])
                if remote in r:
                    data = decrypt(remote.recv(4096))
                    print('from remote:%s,%s' % (data, len(data)))
                    if sock.send(data) <= 0: break
                if sock in r:
                    data=sock.recv(4096)
                    print('from brower:%s,%s' % (data, len(data)))
                    data = encrypt(data)
                    if remote.send(data) <= 0:break
        finally:
            sock.close()
            remote.close()
            print('communication with remote has terminated.')

if __name__=='__main__':

    S=ThreadingTCPServer(('localhost',9999),Socks5Server)
    S.serve_forever()

