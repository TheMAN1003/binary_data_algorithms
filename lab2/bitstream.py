class bitStream:
    
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

    def WriteBitSequence(self, data:bytes, length:int):
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

    def ReadBitSequence(self, data:list, length:int):
        current_byte = 0
        bit_shift = 0

        for _ in range(length):
            if self.readTail == 0:
                byte = self.file.read(1)
                if not byte:
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
bs = bitStream("stream.bin")
bs.WriteBitSequence(a1, 9)
bs.WriteBitSequence(a2, 9)
del bs

bs = bitStream("stream.bin", "rb")
out1 = []
out2 = []
bs.ReadBitSequence(out1, 11)
bs.ReadBitSequence(out2, 7)

print("Перші 11 біт:", out1)
print("Наступні 7 біт:", out2)
del bs