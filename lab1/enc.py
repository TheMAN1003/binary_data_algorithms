def enc(data: bytes) -> bytes:
    i = 0
    encoded_text = bytearray()
    while i < len(data):
        l = 1
        while i + l < len(data) and data[i] == data[i+l] and l < 129:
            l += 1
        if l >= 2: # same bytes
            L = 128 + l - 2
            encoded_text.append(L)
            encoded_text.append(data[i])
            i += l
        else: # different bytes
            j = i
            while (i < len(data) and (i+1 == len(data) or data[i] != data[i+1]) and i-j < 128):
                i += 1
            L = (i - j) - 1
            encoded_text.append(L)
            encoded_text.extend(data[j:i])
    return bytes(encoded_text)
