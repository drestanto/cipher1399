import random
import sys

class Cipher1399 :

    def __init__(self, key, filein):
        self.key = key
        self.filein = filein
        # self.round_key = "" # kayaknya ga bakal kepake
        # self.s_box = [] # kayaknya ga bakal kepake
        self.number_of_iter = Cipher1399.get_number_of_iter(self.key)
        self.list_of_round_key = Cipher1399.get_list_of_key(self.key)

    def read_file_as_string(self):
        # https://prefetch.net/blog/2012/01/30/reading-a-file-into-a-python-string/
        f = open(self.filein, "r")
        data = f.read()
        # end of code
        return data

    @staticmethod
    def get_number_of_iter(key):
        tot = 0
        for c in key:
            tot += ord(c)

        num_iter = tot % len(key) + 1
        return num_iter

    @staticmethod
    def get_round_key(key, length):
        random.seed(key)
        round_key = ""
        for i in range(0,length):
            round_key += str(chr(random.randint(0,255)))
        return round_key

    @staticmethod
    def get_list_of_key(key):
        length = Cipher1399.get_number_of_iter(key)
        round_keys = []
        key = Cipher1399.get_round_key(key,3)
        round_keys.append(key)
        idx = 0
        while (idx < length):
            key = Cipher1399.get_round_key(key,3)
            round_keys.append(key)
            idx += 1

        return round_keys

    # def get_first_round_key(self):
    #     self.round_key = Cipher1399.get_round_key(self.key,3)

    # def get_next_round_key(self):
    #     self.round_key = Cipher1399.get_round_key(self.round_key,3)

    def make_s_box(self, key):
        # initiate s-box
        s_box_size = 16
        for i in range(0,s_box_size):
            arr_baris = []
            for j in range(0,s_box_size):
                arr_baris.append(-1)
            self.s_box.append(arr_baris)

        # make s-box from key
        random.seed(key)
        row = random.randint(0,15)
        col = random.randint(0,15)
        idx = 0
        while (self.s_box[row][col] == -1):
            self.s_box[row][col] = idx
            idx += 1
            row = random.randint(0,15)
            col = random.randint(0,15)

        # fill in other s_box
        for i in range(0,16):
            for j in range(0,16):
                if (self.s_box[i][j] == -1):
                    self.s_box[i][j] = idx
                    idx += 1

    def print_s_box(self):
        for arr in self.s_box:
            for elem in arr:
                sys.stdout.write(format(elem,'02x'))
                sys.stdout.write(' ')
            print("")

    @staticmethod
    def generate_s_box(key): # return an s-box
        # initiate s-box
        s_box_size = 16
        new_s_box = []
        for i in range(0,s_box_size):
            arr_baris = []
            for j in range(0,s_box_size):
                arr_baris.append(-1)
            new_s_box.append(arr_baris)

        random.seed(key)
        row = random.randint(0,15)
        col = random.randint(0,15)
        idx = 0
        while (new_s_box[row][col] == -1):
            new_s_box[row][col] = idx
            idx += 1
            row = random.randint(0,15)
            col = random.randint(0,15)

        # fill in other s_box
        for i in range(0,16):
            for j in range(0,16):
                if (new_s_box[i][j] == -1):
                    new_s_box[i][j] = idx
                    idx += 1

        return new_s_box

    @staticmethod
    def subs_block(s_box, block): # melakukan transposisi bit menggunakan self.s_box
        substituted = ""
        for c in block:
            c_int = ord(c)
            hex_row = c_int / 16
            hex_col = c_int % 16
            c_subs = s_box[hex_row][hex_col]
            substituted += chr(c_subs)
        return substituted

    @staticmethod
    def trans_block(block, width): # melakukan transposisi bit setiap block
        # string to int / bit
        n = 0
        for c in block:
            n = n*256 + ord(c)

        # https://stackoverflow.com/questions/12681945/reversing-bits-of-python-integer
        b = '{:0{width}b}'.format(n, width=width)
        reversed_bit = int(b[::-1], 2)
        # end of code

        # int / bit to string
        reversed_bit_string = ""
        while (reversed_bit != 0):
            c = chr(reversed_bit % 256)
            reversed_bit /= 256
            reversed_bit_string = c + reversed_bit_string

        return reversed_bit_string

    def process_block(self, block, round):
        # block harus berukuran 64 bit
        s_box = Cipher1399.generate_s_box(self.list_of_round_key[round])
        substituted = Cipher1399.subs_block(s_box, block)
        transposed = Cipher1399.trans_block(substituted,8*len(block))
        return transposed

    # ga kepake
    # def read_block_by_block(self):
    #     cipher = ""
    #     file = open(self.filein, 'rb')
    #     block = file.read(8)
    #     while (block != ""):
    #         cipher += self.process_block(block)
    #         block = file.read(8)
    #     return cipher

    def encrypt_string_ecb(self, text, round):
        # print(len(text))
        test = ""
        i = 0
        block = ""
        for c in text:
            if (i == 8):
                test += self.process_block(block, round)
                block = ""
                i = 0
            block += c
            i += 1
        test += self.process_block(block, round)
        # print(len(test))
        return test

    def encrypt_string_cbc(self, text, round):
        # print(len(text))
        test = ""
        i = 0
        prev_ciph = ""
        block = ""
        for c in text:
            if (i == 8):
                if (prev_ciph == ""):
                    test += self.process_block(block, round)
                    prev_ciph = self.process_block(block, round)
                else:
                    test += self.process_block(Cipher1399.sxor(block, prev_ciph), round)
                    prev_ciph = self.process_block(Cipher1399.sxor(block, prev_ciph), round)
                block = ""
                i = 0
            block += c
            i += 1
        test += self.process_block(block, round)
        # print(len(test))
        return test

    def encrypt_string_cfb(self, text, round):
        # print(len(text))
        test = ""
        i = 0
        block = ""
        for c in text:
            if (i == 8):
                # cfb 8 bit, sehingga diproses perbyte
                msb = 0 # most significant bit
                hasil_enkripsi = ""
                for sub_block in block:
                    hasil = self.process_block(Cipher1399.sxor(block, chr(msb)), round)
                    # calculate msb
                    if (hasil != ""): # debug aja nih, ngasal
                        if (ord(hasil) >= 128):
                            msb = 1
                        else:
                            msb = 0
                    hasil_enkripsi += hasil
                test += hasil_enkripsi
                block = ""
                i = 0
            block += c
            i += 1
        test += self.process_block(block, round)
        # print(len(test))
        return test

    def encrypt_string_ofb(self, text, round):
        # print(len(text))
        test = ""
        i = 0
        block = ""
        for c in text:
            if (i == 8):
                # cfb 8 bit, sehingga diproses perbyte
                msb = 0 # most significant bit
                hasil_sebelumnya = ""
                hasil_enkripsi = ""
                for sub_block in block:
                    hasil = self.process_block(Cipher1399.sxor(block, chr(msb)), round)
                    # calculate msb
                    if (hasil_sebelumnya != ""): # debug aja nih, ngasal
                        if (ord(hasil_sebelumnya) >= 128):
                            msb = 1
                        else:
                            msb = 0
                    hasil_sebelumnya = hasil
                    hasil_enkripsi += hasil
                test += hasil_enkripsi
                block = ""
                i = 0
            block += c
            i += 1
        test += self.process_block(block, round)
        # print(len(test))
        return test

    @staticmethod
    def get_left(text):
        # if it's odd, will get the left of the center excluding the center byte
        length = len(text) / 2
        return text[:length]

    @staticmethod
    def get_right(text):
        # if it's odd, will get the right of the center excluding the center
        length = len(text) / 2
        if (len(text) % 2 == 0):
            return text[length:]
        else:
            return text[length + 1:]

    @staticmethod
    def get_center(text):
        # if it's odd, will return the center, if it's even, will return empty string
        length = len(text) / 2
        if (len(text) % 2 == 0):
            return ""
        else:
            return text[length:-length]

    @staticmethod
    # https://stackoverflow.com/questions/2612720/how-to-do-bitwise-exclusive-or-of-two-strings-in-python
    def sxor(s1,s2): # string xor
        # convert strings to a list of character pair tuples
        # go through each tuple, converting them to ASCII code (ord)
        # perform exclusive or on the ASCII code
        # then convert the result back to ASCII (chr)
        # merge the resulting array of characters as a string
        return ''.join(chr(ord(a) ^ ord(b)) for a,b in zip(s1,s2))
    # end of code

    def feistel_encrypt_recursive(self, left, center, right, round, type):
        # initiate round by zero
        # source = https://en.wikipedia.org/wiki/Feistel_cipher
        if (round > self.number_of_iter):
            return left + center + right # basis
        else: # rekurens
            new_left = right
            if (type == "ecb"):
                new_right = Cipher1399.sxor(left, self.encrypt_string_ecb(right, round))
            elif type == "cbc":
            	new_right = Cipher1399.sxor(left, self.encrypt_string_cbc(right, round))
            elif type == "cfb":
                new_right = Cipher1399.sxor(left, self.encrypt_string_cfb(right, round))
            elif type == "ofb":
                new_right = Cipher1399.sxor(left, self.encrypt_string_ofb(right, round))
            return self.feistel_encrypt_recursive(right, center, new_right, round + 1, type)

    def feistel_encrypt(self, text, type):
        return self.feistel_encrypt_recursive(Cipher1399.get_left(text), Cipher1399.get_center(text), Cipher1399.get_right(text), 0, type)

    def feistel_decrypt_recursive(self, left, center, right, round, type):
        # initiate round by number_of_iter
        # source = https://en.wikipedia.org/wiki/Feistel_cipher
        if (round == -1):
            return left + center + right # basis
        else: # rekurens
            # new_right = left
            if (type == "ecb"):
                new_left = Cipher1399.sxor(right, self.encrypt_string_ecb(left, round))
            elif type == "cbc":
            	new_left = Cipher1399.sxor(right, self.encrypt_string_cbc(left, round))
            elif type == "cfb":
            	new_left = Cipher1399.sxor(right, self.encrypt_string_cfb(left, round))
            elif type == "ofb":
            	new_left = Cipher1399.sxor(right, self.encrypt_string_ofb(left, round))

            return self.feistel_decrypt_recursive(new_left, center, left, round - 1, type)

    def feistel_decrypt(self, text, type):
        return self.feistel_decrypt_recursive(Cipher1399.get_left(text), Cipher1399.get_center(text), Cipher1399.get_right(text), self.number_of_iter, type)

    @staticmethod
    def print_as_hex(text):
        for char in text:
            int_format = ord(char)
            sys.stdout.write(format(int_format,'02x'))
            sys.stdout.write(" ")



key = "ITB = Institut Teknologi Bandung"
ciph = Cipher1399(key,"datatest.txt")
print(ciph.number_of_iter)
# print(ciph.list_of_round_key)

# print(Cipher1399.get_left("qwertyuiopasdfghjklzxcvbnmmnbvcxzlkjhgfdsapoiuytrew"))
# print(Cipher1399.get_right("qwertyuiopasdfghjklzxcvbnmmnbvcxzlkjhgfdsapoiuytrew"))
# print(Cipher1399.get_center("qwertyuiopasdfghjklzxcvbnmmnbvcxzlkjhgfdsapoiuytrew"))
plain = "Red: These walls are funny. First you hate 'em, then you get used to 'em. Enough time passes, you get so you depend on them. That's institutionalized.\nHeywood: Shit. I could never get like that.\nErnie: Oh yeah? Say that when you been here as long as Brooks has.\nRed: Goddamn right. They send you here for life, and that's exactly what they take. The part that counts, anyway."
plain1 = "qwertyuiopasdfghjklzxcvbnm qazwsxedcrfvtgbyhnujmikolp mnbvcxzlkjhgfdsapoiuytrewq abcdefghijklmnopqrstuvwxyz"
# print((len(plain)-3)/26)
print(plain)
# Cipher1399.print_as_hex(plain)
# print(ciph.feistel_encrypt(plain, "ecb"))
simpen = ciph.feistel_encrypt(plain, "ofb")
print("")
print("")
# Cipher1399.print_as_hex(simpen)
print(simpen)
print(ciph.feistel_decrypt(simpen, "ofb"))
