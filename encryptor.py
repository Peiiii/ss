
# coding: utf8
import chardet,gzip,zlib,zipfile
import os,shutil,math
from  des import des
import base64
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
# a=E.encrypt('123')
# print(bytes(a,'utf-8'))
def decode_try(data):
    r = chardet.detect(data)
    print('encoding: %s' % (r))
    en = r['encoding']
    conf = r['confidence']
    text = 'cannot identify content'
    if conf > 0.5:
        text = str(data, encoding=en)
        return text
    print('decode failed.')
    return data
def encrypt1(data):
    return data
def decrypt1(data):
    return data
def encrypt2(data):
    r=chardet.detect(data)
    if r['confidence']>0.9:
        print('originl length:',len(data))
        text=str(data,encoding=r['encoding'])
        print('decode length:',len(text))
        # text=E.encrypt(text)
        text=bytes(text,'utf-8')
        print('encrypt length:',len(text))
        text=gzip.compress(text)
        print('compress length:',len(text))
        text=b'\x11\x12\x13'
        data=text
    return data

def decrypt2(data):
    if data[:3]==b'\x11\x12\x13':
        text=data[3:]
        print('original length:',len(text))
        text=gzip.decompress(text)
        print('decompress length:',len(text))
        text=str(text,'utf-8')
        # text=E.decrypt(text)
        text=bytes(text,'utf-8')
        print('decrypt length:',len(text))
        data=text
    return data

def encrypt3(data):
    text=data
    text=b''
    per_len=30
    fillbyte=b'\x12'
    num=math.ceil(len(data)/per_len)-1
    for i in range(num):
        text+=data[i*per_len:(i+1)*per_len]+fillbyte
    text+=data[num*per_len:]
    data=text
    # data=b'\x11\x12\x13'+text
    return data

def decrypt3(data):
    text=data
    # text=data[3:]
    text=b''
    per_len=30
    num=math.ceil(len(data)/(per_len+1))-1
    for i in range(num):
        text+=data[(per_len+1)*i:((per_len+1)*(i+1)-1)]
    text+=data[num*(per_len+1):]
    data=text
    return data

CONFIRM_HEAD=b'\x11\x12\x13'
CONFIRM_HEAD=b''

def encrypt4(data):
    text=data
    if len(data)!=0:
        text=CONFIRM_HEAD+text
    data=text
    return data

def decrypt4(data):
    text=data
    if len(data)!=0:
        assert text[:len(CONFIRM_HEAD)]==CONFIRM_HEAD
        text=text[len(CONFIRM_HEAD):]
    data=text
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
    return data
def decrypt_head(data):
    # data=gzip.decompress(data)
    data=E.decrypt(data)
    return data
def show_info(data):
    r=chardet.detect(data)
    l=len(data)
    head=data[:3] if l>=3 else data
    print('*****Data， Length: %s, encoding: %s  head: %s'%(l,r,head))

def encrypt(data):
    # show_info(data)
    # data=encrypt3(data)
    # data=encrypt4(data)
    data=encrypt5(data)
    # data=encrypt1(data)
    return data

def decrypt(data):
    # show_info(data)
    # data=decrypt3(data)
    # data=decrypt4(data)
    data=decrypt5(data)
    # data=decrypt1(data)

    return data