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

    def write_bit_sequence(self, data:bytes, length:int):
        bit_length = 0
        for byte in data:
            for i in range(8):
                if bit_length >= length:
                    return
                bit = (byte >> i) & 1
                self.writeBuffer |= (bit << self.writeFill)
                self.writeFill += 1
                if self.writeFill == 8:
                    self.file.write(bytes([self.writeBuffer]))
                    self.writeBuffer = 0
                    self.writeFill = 0
                bit_length += 1
        print("Запис успішний")

    def read_bit_sequence(self, data:list, length:int):
        current_byte = 0
        bit_shift = 0

        for _ in range(length):
            if self.readTail == 0:
                byte = self.file.read(1)
                if not byte:
                    data.append(hex(self.readBuffer))
                    break
                self.readBuffer = byte[0]
                self.readTail = 8
            
            bit = self.readBuffer & 1
            self.readBuffer >>= 1
            self.readTail -= 1
            
            current_byte |= (bit << bit_shift)
            bit_shift += 1
            if bit_shift == 8:
                data.append(hex(current_byte))
                current_byte = 0
                bit_shift = 0
            
        if bit_shift > 0 :
            data.append(hex(current_byte))

a1 = bytes([0xE1, 0x01])
a2 = bytes([0xEE, 0x00])
bs = BitStream("stream.bin")
bs.write_bit_sequence(a1, 9)
bs.write_bit_sequence(a2, 9)
del bs

bs = BitStream("stream.bin", "rb")
out = []
bs.read_bit_sequence(out, 11)
print("Результат першого читання", out)
out.clear()
bs.read_bit_sequence(out, 7)
print("Результат другого читання", out)
out.clear()
del bs

bs = BitStream("stream.bin")
a3 = bytes([0xFF])
bs.write_bit_sequence(a3, 4)
del bs

bs = BitStream("stream.bin", "rb")
bs.read_bit_sequence(out, 8)
print("Результат третього читання", out)
out.clear()
del bs

a4 = bytes([0xA, 0x4F])
a5 = bytes([0x53, 0x5])
bs = BitStream("stream.bin")
bs.write_bit_sequence(a4, 10)
bs.write_bit_sequence(a5, 3)
del bs

bs = BitStream("stream.bin", "rb")
out = []
bs.read_bit_sequence(out, 3)
print("Результат четвертого читання", out)
out.clear()
bs.read_bit_sequence(out, 1)
print("Результат п'ятого читання", out)
out.clear()
bs.read_bit_sequence(out, 5)
print("Результат шостого читання", out)
out.clear()
bs.read_bit_sequence(out, 4)
print("Результат сьомого читання", out)
out.clear()
del bs