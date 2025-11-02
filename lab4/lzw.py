import os

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

class LZW:
    def __init__(self, length):
        self.max_length = length
        self.S = (-1, None)
        self.I = None
        self.reset()         

    def reset(self):
        self.dictionary = {(i, None): i for i in range(256)}
        self.dictionary[(256, None)] = 0
        self.dictionary_dec = {i : (i, None) for i in range(256)}
        self.dictionary_dec[256] = 0
        self.current_bit_length = 9

    @staticmethod
    def toByte(input:int):
        return bytes([input])

    def encode(self, data:bytes, filename):
        bs = BitStream(filename)
        for byte in data:
            if (byte, self.I) in self.dictionary:
                self.S = (byte, self.I)
                self.I = self.dictionary[(byte, self.I)]
            else:
                bs.write_bit_sequence(self.I.to_bytes(4, byteorder='little'), self.current_bit_length)
                if len(self.dictionary) == (1 << self.current_bit_length):
                    self.current_bit_length += 1
                if len(self.dictionary) >= self.max_length:
                    self.I = 256
                    bs.write_bit_sequence(self.I.to_bytes(4, byteorder='little'), self.current_bit_length)
                    self.reset()
                    self.I = byte
                    continue
                self.dictionary[(byte, self.I)] = len(self.dictionary)
                self.S = (byte, None)
                self.I = byte
        bs.write_bit_sequence(self.I.to_bytes(4, byteorder='little'), self.current_bit_length)
        del bs
        self.reset()

    def getString(self):
        result = b""
        reversed_string = b""
        S_temp = (self.S[0], self.S[1])
        while True:
            reversed_string += bytes([S_temp[0]])
            if S_temp[1] == None:
                break
            S_temp = self.dictionary_dec[S_temp[1]]
        result = reversed_string[::-1]
        return result
    
    @staticmethod
    def listToInt(l:list) -> int:
        bytelist = [int(s, 16) for s in l]
        res = 0
        i = 0
        for byte in bytelist:
            res |= byte << i * 8
            i += 1
        l.clear()
        return res
    
    def decode(self, filename):
        bs = BitStream(filename, "rb")
        file_size_bytes = os.path.getsize(filename)
        file_size_bits = file_size_bytes * 8
        result = b""
        bytelist = []
        bs.read_bit_sequence(bytelist, self.current_bit_length)
        file_size_bits -= self.current_bit_length
        self.I = self.listToInt(bytelist)
        self.S = self.dictionary_dec[self.I]
        result += self.getString()
        if len(self.dictionary_dec) == (1 << self.current_bit_length):
            self.current_bit_length += 1
        if len(self.dictionary_dec) == self.max_length:
            self.reset()
        old_I = self.I
        old_S = self.S
        while True:
            bs.read_bit_sequence(bytelist, self.current_bit_length)
            file_size_bits -= self.current_bit_length
            if file_size_bits <= 0:
                break
            if not bytelist:
                break
            self.I = self.listToInt(bytelist)
            if self.I in self.dictionary_dec:
                if self.I == 256:                    
                    self.reset()
                    continue
                self.S = self.dictionary_dec[self.I]
                result += self.getString()
                self.dictionary_dec[len(self.dictionary_dec)] = (self.S[0], old_I)
                if len(self.dictionary_dec) == (1 << self.current_bit_length):
                    self.current_bit_length += 1
                old_I = self.I
                old_S = self.S
            else:
                self.S = (self.dictionary_dec[old_S[1]][0], old_I)
                result += self.getString()
                self.dictionary_dec[len(self.dictionary_dec)] = (self.S[0], old_I)
                if len(self.dictionary_dec) == (1 << self.current_bit_length):
                    self.current_bit_length += 1
                if len(self.dictionary_dec) == self.max_length:
                    self.reset()
        del bs
        self.reset()
        return result
    
file = open("input.txt", "rb")
input = file.read()

lzw = LZW(1048576) # макс довжина 2^20

lzw.encode(input, "res.bin")

output = lzw.decode("res.bin")
file = open("decode.txt", "wb+")
file.write(output)