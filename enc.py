from secret import flag,key
from random import randint
from libnum import n2s,s2n
from Crypto.Util.number import getPrime
limit = lambda n: n & 0xffffffff
padding="\xe6\xe6\xe7\xe6\xe5\xe6\xe5\xe9\xe5"
ek='\xe6\x84\xbf'

def encode(key,data):
    pad  = randint(0x10000000,0xffffffff)
    Key  = [ord(i) for i in key]
    Data = [ord(i) for i in data]
    a = limit((Key[0] << 24) | (Key[1] << 16) | (Key[2] << 8) | Key[3])
    b = limit((Key[4] << 24) | (Key[5] << 16) | (Key[6] << 8) | Key[7])
    c = limit((Key[8] << 24) | (Key[9] << 16) | (Key[10] << 8) | Key[11])
    d = limit((Key[12] << 24) | (Key[13] << 16) | (Key[14] << 8) | Key[15])
    y = limit((Data[0] << 24) | (Data[1] << 16) | (Data[2] << 8) | Data[3])
    z = limit((Data[4] << 24) | (Data[5] << 16) | (Data[6] << 8) | Data[7])
    pads = 0
    for j in range(32):
        pads = limit(pads + pad)
        y = limit( y + ((z*16 + a) ^ (z + pads) ^ ((z>>5) + b)))
        z = limit( z + ((y*16 + c) ^ (y + pads) ^ ((y>>5) + d)))
    print hex((y << 52) ^ (pads << 20) ^ z)

#pow_check()
#token_check()

flag=flag.ljust(len(flag)+(-len(flag)&7),'\x00')
for i in range(0,len(flag)/8):
    encode(key,flag[8*i:8*i+8])

for i in range(9):
    ek+=padding[i] + key[2*i:2*i+2]

p=getPrime(2048)
e=0x10001

for i in range(2):
    q=getPrime(2048)
    n=p*q
    print n
    print pow(s2n(ek),e,n)