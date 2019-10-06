import socket,time,json
import socketserver,select,struct

class ThreadingTCPServer(socketserver.ThreadingMixIn,socketserver.TCPServer):
    pass

class Socks5Server(socketserver.StreamRequestHandler):
    def handle(self):
        try:
            print('new connection :', self.request)
            sock = self.connection
            data=sock.recv(1024)
            print('recieving data:',data)
            self.wfile.write(b'success')
        except socket.error:
            print('socket error')
            raise

def clean_linux_port(port):
    import os
    try:
        os.system('cleanp '+str(port))
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

