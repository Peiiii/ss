
# coding: utf8
import chardet
from .des import des


class Encryptor():
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


E=Encryptor('Wp@000001')

def encrypt1(data):
    return data
def decrypt1(data):
    return data

def encrypt5(data):
    data2=[]
    for b in data:
        data2.append((b+10)%256)
    data=bytes(data2)
    return data

def decrypt5(data):
    data2 = []
    for b in data:
        if b>=10:
            b-=10
        else:
            b=b+256-10
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
    # data=encrypt5(data)
    data=encrypt1(data)
    return data

def decrypt(data):
    # show_info(data)
    # data=decrypt5(data)
    data=decrypt1(data)

    return data