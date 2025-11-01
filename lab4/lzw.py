class LZW:
    def __init__(self, length):
        self.dictionary = {(i, None): i for i in range(256)}
        self.S = (-1, -1)
        self.I = -1

    def encode(self, data:bytes):
        for byte in data:
            if (byte, self.S[1]) in self.dictionary:
                self.I = self.dictionary[(byte, self.I)]
                self.S = (byte, self.I)
            else:
                write(self.I, current_bit_length)
                self.dictionary[(byte, self.I)] = len(self.dictionary)
                # записати у S номер байта, який у c, у I індекс, який позначає позицію c у словнику
                self.S = (byte, self.S[1])
                self.I = self.dictionary[(byte, self.I)]
        write(self.I, current_bit_length)
    
    def decode(self, data:bytes):
        result = b""
        read(self.I, current_bit_length)
        self.S = next((key for key, value in self.dictionary.items() if value == self.I), None)
        result += bytes(self.S[0])
        old_I = self.I
        old_S = self.S
        while true:
            read(self.I, current_bit_length)
            if self.I in self.dictionary.keys():
                self.S = next((key for key, value in self.dictionary.items() if value == self.I), None)
                result += bytes(self.S)
                self.dictionary[]
        return
