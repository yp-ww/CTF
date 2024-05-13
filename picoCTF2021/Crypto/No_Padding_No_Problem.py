from pwn import *

host = "mercury.picoctf.net"
port = 30048

r = remote(host, port)

r.recvuntil(b'!\n')
r.recvuntil(b'\n')
r.recvuntil(b'\n')

n = int(r.recvuntil(b'\n')[3:])
e = int(r.recvuntil(b'\n')[3:])
c = int(r.recvuntil(b'\n')[12:])

print("n:", n)
print("e:", e)
print("c:", c)

r.recvuntil(b'decrypt: ')

c2 = c + n
r.sendline(str(c2).encode())

r.recvuntil(b'go: ')
m = int(r.recvuntil(b'\n'))

print("m:", m)
from Crypto.Util.number import long_to_bytes
print(long_to_bytes(m))

r.close()





