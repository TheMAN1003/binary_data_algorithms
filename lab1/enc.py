import sys
import os

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

if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Некоректна кількість аргументів на вхід у кодер")
        sys.exit(1)

    if len(sys.argv) == 3:
        input, output = sys.argv[1], sys.argv[2]
    else:
        input = sys.argv[1]
        name, _ = os.path.splitext(input)
        output = name + ".rle"

    with open(input, "rb") as input_f:
        data = input_f.read()

    encoded_text = enc(data)

    with open(output, "wb") as output_f:
        output_f.write(encoded_text)

    print(f"Успішно закодовано файл {input} у файл {output} використовуючи RLE!")