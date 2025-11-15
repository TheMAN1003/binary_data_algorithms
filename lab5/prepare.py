import struct

def mtf(data):
    res = bytearray(b'')
    alphabet = list(range(256))
    for byte in data:
        if byte == 0:
            res.append(alphabet.index(byte))
        else:
            res.append(alphabet.index(byte))
            alphabet.remove(byte)
            alphabet.insert(0, byte)
    return bytes(res)

def bwt_encode(data: bytes) -> bytes:
    n = len(data)
    if n == 0:
        return struct.pack(">I", 0)

    sa = list(range(n))
    rank = [data[i % n] for i in range(n)]
    tmp = [0] * n

    k = 1
    while k < n:
        sa.sort(key=lambda i: (rank[i], rank[(i + k) % n]))

        tmp[sa[0]] = 0
        r = 0
        for i in range(1, n):
            prev, curr = sa[i-1], sa[i]
            if (rank[curr], rank[(curr + k) % n]) != (rank[prev], rank[(prev + k) % n]):
                r += 1
            tmp[curr] = r

        rank, tmp = tmp, rank
        if r == n - 1:
            break   # all ranks unique
        k <<= 1

    bwt = bytearray(n)
    orig_index = 0

    for idx, s in enumerate(sa):
        if s == 0:
            orig_index = idx
            bwt[idx] = data[n - 1]
        else:
            bwt[idx] = data[s - 1]

    return struct.pack(">I", orig_index) + bytes(bwt)

def bwt_decode(encoded: bytes) -> bytes:
    orig_index = struct.unpack(">I", encoded[:4])[0]
    bwt = encoded[4:]
    n = len(bwt)

    if n == 0:
        return b""

    counts = [0] * 256
    for b in bwt:
        counts[b] += 1

    starts = [0] * 256
    total = 0
    for i in range(256):
        starts[i] = total
        total += counts[i]

    occ = [0] * 256
    lf = [0] * n

    for i, b in enumerate(bwt):
        lf[i] = starts[b] + occ[b]
        occ[b] += 1

    out = bytearray(n)
    p = orig_index
    for i in range(n-1, -1, -1):
        out[i] = bwt[p]
        p = lf[p]

    return bytes(out)


text = b"ccccbdbdeee"

encoded = bwt_encode(text)
decoded = bwt_decode(encoded)
twice = mtf(encoded)

print(encoded)
print(decoded)
print(twice)