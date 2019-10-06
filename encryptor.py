
# coding: utf8
import chardet,gzip,zlib,zipfile
import os,shutil
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
    # a=str(data[:10],'utf-8')
    # print('data:',a)
    r=chardet.detect(data)
    print('encoding: %s'%(r))

    en=r['encoding']
    conf=r['confidence']
    text='cannot identify content'
    if conf>0.5:
        text=str(data,encoding=en)
    else:
        text=gzip.decompress(data)
        text = decode_try(text)
    print(text)
    input()
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
def encrypt_head(data):
    data=gzip.compress(data)
    return data
def decrypt_head(data):
    data=gzip.decompress(data)
    return data
def show_encode(data):
    r=chardet.detect(data)
    print('Detect result: ',r)

def encrypt(data):

    return data

def decrypt(data):

    return data