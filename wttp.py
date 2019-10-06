# import socket

class Wttp:
    def __init__(self,sock):
        self.sock=sock
        self.max_len=4096
        self.start_bytes=b'\x11\x12\x13'
        self.confirm_bytes=b'\x00\x00\x00'
        self.end_bytes=b'\x13\x12\x11'
    def send(self,data):
        self.send_step(self.start_bytes)
        pieces=self.cut_data(data)
        for p in pieces:
            self.send_step(p)
        self.send_step(self.end_bytes)
    def send_step(self,data):
        self.sock.sendall(data)
        self.wait_util(self.confirm_bytes)
    def recv(self):
        self.wait_util(self.start_bytes)
        self.sock.sendall(self.confirm_bytes)
        data=b''
        while True:
            piece=self.sock.recv(self.max_len)
            self.sock.sendall(self.confirm_bytes)
            if piece==self.end_bytes:
                break
            else:
                data+=piece
        return data
    def wait_util(self,data):
        while True:
            r=self.sock.recv(len(data))
            if len(r)!=0:
                if r==data:
                    return data
                else:
                    raise Exception('Recieved {} but expected {}'.format(r,data))
    def cut_data(self,data):
        pieces = []
        while len(data) > self.max_len:
            pieces.append(data[:self.max_len])
            data = data[self.max_len:]
        pieces.append(data)
        return pieces