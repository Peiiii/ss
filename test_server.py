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

if __name__=='__main__':

    S=ThreadingTCPServer(('0.0.0.0',8888),Socks5Server)
    S.serve_forever()

