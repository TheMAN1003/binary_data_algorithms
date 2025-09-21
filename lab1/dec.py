import sys

def dec(data: bytes) -> bytes:
    i = 0
    decoded_text = bytearray()

    while i < len(data):
        L = data[i]
        i += 1
        if L & 0x80: # same bytes
            if i >= len(data):
                raise ValueError("Недостатньо байтів у вхідному файлі")
            l = (L & 0x7F) + 2
            decoded_text.extend(data[i] for _ in range(l))
            i += 1
        else: # different bytes
            l = (L & 0x7F) + 1
            if i + l > len(data):
                raise ValueError("Недостатньо байтів у вхідному файлі")
            decoded_text.extend(data[i:i+l])
            i += l

    return bytes(decoded_text)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Некоректна кількість аргументів на вхід у декодер")
        sys.exit(1)

    input, output = sys.argv[1], sys.argv[2]

    with open(input, "rb") as input_f:
        data = input_f.read()

    decoded_text = dec(data)

    with open(output, "wb") as output_f:
        output_f.write(decoded_text)

    print(f"Успішно декодовано файл {input} у файл {output} використовуючи RLE!")