
# coding: utf8
import chardet
from .des import des


class DesEncryptor():
    def __init__(self, key):
        self.key = key
        self.des=des()
    # 加密函数，如果text不是16的倍数【加密文本text必须为16的倍数！】，那就补足为16的倍数
    def encrypt(self, data):
        data=self.des.encrypt(self.key,data,padding=True)
        return data

    def decrypt(self, data):
        data=self.des.decrypt(self.key,data,padding=True)
        return data


E=DesEncryptor('Wp@000001')


def encrypt1(data):
    return data
def decrypt1(data):
    return data
def encrypt2(data):
    data=data[::-1]
    return data
def decrypt2(data):
    data=data[::-1]
    return data
N=57
M1,M2=57,80
def encrypt5(data):
    data2=[]
    for b in data:
        data2.append((b+N)%256)
    data=bytes(data2)
    return data

def decrypt5(data):
    data2 = []
    for b in data:
        if b>=N:
            b-=N
        else:
            b=b+256-N
        data2.append(b)
    data = bytes(data2)
    return data
def encrypt6(data):
    data2=[]
    N=M1
    for i,b in enumerate(data):
        data2.append((b+N)%256)
        N+=1
        if N>M2:
            N=M1
    data=bytes(data2)
    return data

def decrypt6(data):
    data2 = []
    N=M1
    for i,b in enumerate(data):
        if b>=N:
            b-=N
        else:
            b=b+256-N
        N += 1
        if N > M2:
            N = M1
        data2.append(b)
    data = bytes(data2)
    return data


def encrypt_head(data):
    # data=gzip.compress(data)
    data=E.encrypt(data)
    data=bytes(data,'utf-8')
    data=encrypt5(data)
    return data
def decrypt_head(data):
    data=decrypt5(data)
    data=str(data,'utf-8')
    data=E.decrypt(data)
    return data
def show_info(data):
    r=chardet.detect(data)
    l=len(data)
    head=data[:3] if l>=3 else data
    print('*****Data， Length: %s, encoding: %s  head: %s'%(l,r,head))

def encrypt(data):
    # show_info(data)
    data=encrypt1(data)
    # data=encrypt5(data)
    # data=encrypt6(data)
    # data=encrypt2(data)
    return data

def decrypt(data):
    # show_info(data)
    data=decrypt1(data)
    # data=decrypt5(data)
    # data=decrypt6(data)
    # data=decrypt2(data)
    return data

