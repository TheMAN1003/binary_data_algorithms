from struct import pack, unpack
from heapq import heappush, heappop

class Node:
    def __init__(self, weight, symbol=None, left=None, right=None):
        self.weight = weight
        self.symbol = symbol
        self.left = left
        self.right = right
    
    def __lt__(self, other):
        return self.weight < other.weight

def count_frequencies(data: bytes) -> bytes:
    freqs = [0] * 256
    for byte in data:
        freqs[byte] += 1
    res = b''.join(pack('<I', c) for c in freqs)

    return res

def huffman_tree(freq_bytes: bytes) -> Node:
    assert len(freq_bytes) == 1024, "Розмір таблиці має бути 1024 байта"
    freqs = [unpack('<I', freq_bytes[i*4:(i+1)*4])[0] for i in range(256)]

    heap = []

    for symbol, freq in enumerate(freqs):
        if freq > 0:
            heappush(heap, (freq, Node(weight=freq, symbol=symbol)))

    if len(heap) == 0:
        return None

    while len(heap) > 1:
        w1, n1 = heappop(heap)
        w2, n2 = heappop(heap)
        parent = Node(weight=w1 + w2, left=n1, right=n2)
        heappush(heap, (parent.weight, parent))

    return heap[0][1]

def code_table(node, prefix="", table=None):
    if table is None:
        table = {}
    
    if node.symbol is not None:
        table[node.symbol] = prefix
    else:
        code_table(node.left, prefix + "1", table)
        code_table(node.right, prefix + "0", table)

    return table

#для реалізації потрібно трохи змінити код з лаб 2, щоб він працював як застосування кодової таблиці на вхідне слово
class BitStream:
    
    def __init__(self, filename, mode='wb+'):
        self.filename = filename
        self.file = None
        try:
            self.file = open(filename, mode)
        except FileNotFoundError:
            print(f"Потік {self.filename} не знайдено")
        except Exception as e:
            print(f"Сталася помилка під час відкриття: {e}")
        self.writeBuffer = 0
        self.writeFill = 0
        self.readBuffer = 0
        self.readTail = 0
        
    def __del__(self):
        if self.file:
            if self.writeFill > 0:
                self.file.write(bytes([self.writeBuffer]))
            self.file.close()

    def encode_bit_sequence(self, data:bytes, table:dict, freq:bytes):
        self.file.write(freq)
        self.file.write(pack('>Q', len(data)))
        for byte in data:
            bits = table[byte]
            for str_bit in bits:
                bit = int(str_bit)
                self.writeBuffer |= (bit << self.writeFill)
                self.writeFill += 1
                if self.writeFill == 8:
                    self.file.write(bytes([self.writeBuffer]))
                    self.writeBuffer = 0
                    self.writeFill = 0

    def decode_bit_sequence(self, data:bytes, table:dict, length:int):
        decode_table = {v: k for k, v in table.items()}
        current_length = length
        bit_string = ''.join(f'{byte:08b}'[::-1] for byte in data)
        current_string = ''
        for bit in bit_string:
            if current_length == 0:
                break
            current_string += bit
            if current_string in decode_table:
                self.file.write(decode_table[current_string].to_bytes(1, 'big'))
                current_length -= 1
                current_string = ''
                