from pwn import *

host = "mercury.picoctf.net"
port = 31133

r = remote(host, port)
r.recvuntil(b'Welcome to my RSA challenge!\n')

e = int(r.recvuntil(b'\n')[3:])
n = int(r.recvuntil(b'\n')[3:])
c = int(r.recvuntil(b'\n')[3:])

r.close()

print("e:", e)
print("n:", n)
print("c:", c)

import gmpy2
def continued_fraction(x: int, y: int):
    # x/y の連分数展開
    a = []
    while y:
        a.append(x//y)
        x, y = y, x%y
    return a

def convergent(a):
    # 主近似分数
    # https://www.cits.ruhr-uni-bochum.de/imperia/md/content/may/krypto2ss08/shortsecretexponents.pdf
    if len(a) == 1:
        return [(a[0], 1)]
    res = []
    n0, d0 = a[0], 1
    n1, d1 = a[0]*a[1]+1, a[1]
    res.append((n0, d0))
    res.append((n1, d1))

    for ai in a[2:]:
        n0, n1 = n1, ai*n1 + n0
        d0, d1 = d1, ai*d1 + d0
        res.append((n1, d1))
    return res

# print(convergent(continued_fraction(17, 29)))

def wieners_attack(e, n):
    kd = convergent(continued_fraction(e, n))
    for k, d in kd:
        if k == 0: continue
        if (e*d-1)%k: continue
        # s = p + q
        s = n - (e*d-1)//k + 1
        D = s*s - 4*n
        if D<0: continue
        if not gmpy2.is_square(D): continue
        return d
    return -1

d = wieners_attack(e, n)

print("d:", d)

m = pow(c, d, n)
from Crypto.Util.number import long_to_bytes
print(long_to_bytes(m))
