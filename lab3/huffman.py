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
        code_table(node.left, prefix + "0", table)
        code_table(node.right, prefix + "1", table)

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

    def write_bit_sequence(self, data:bytes, table:dict, freq:bytes):
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

# data = b'a'*26+b'b'*25+b'c'*24+b'd'*23+b'e'*22+b'f'*21+b'g'*20+b'h'*19+b'i'*18+b'j'*17+b'k'*16+b'l'*15+b'm'*14+b'n'*13+b'o'*12+b'p'*11+b'q'*10+b'r'*9+b's'*8+b't'*7+b'u'*6+b'v'*5+b'w'*4+b'x'*3+b'y'*2+b'z'
data = b'aaaaaaaaabbbbcde' #replace with input file later
assert len(data) <= (1<<32), "input file is too big"
freq_bytes = count_frequencies(data)

root = huffman_tree(freq_bytes)
table = code_table(root)
print(table)
bs = BitStream("stream.bin")
bs.write_bit_sequence(data, table, freq_bytes)
del bs
file = open("stream.bin", "rb")
data = file.read()
print(data[1032:])
bit_string = ''.join(f'{byte:08b}' for byte in data[1032:])
print(bit_string)
