import random
import sys

class Cipher1399 :

    def __init__(self, key, filein):
        self.key = key
        self.round_key = ""
        self.filein = filein
        self.s_box = []
        self.number_of_iter = Cipher1399.get_number_of_iter(self.key)
        self.list_of_round_key = Cipher1399.get_list_of_key(self.key)

    @staticmethod
    def get_number_of_iter(key):
        tot = 0
        for c in key:
            tot += ord(c)

        num_iter = tot % len(key) + 1
        return num_iter

    @staticmethod
    def get_list_of_key(key):
        length = Cipher1399.get_number_of_iter(key)
        round_keys = []
        key = Cipher1399.get_round_key(key,3)
        round_keys.append(key)
        idx = 1
        while (idx < length):
            key = Cipher1399.get_round_key(key,3)
            round_keys.append(key)
            idx += 1

        return round_keys

    @staticmethod
    def get_round_key(key, length):
        random.seed(key)
        round_key = ""
        for i in range(0,length):
            round_key += str(chr(random.randint(0,255)))
        return round_key

    # def get_first_round_key(self):
    #     self.round_key = Cipher1399.get_round_key(self.key,3)

    # def get_next_round_key(self):
    #     self.round_key = Cipher1399.get_round_key(self.round_key,3)

    def subs_block(self, block): # melakukan transposisi bit menggunakan self.s_box
        substituted = ""
        for c in block:
            c_int = ord(c)
            hex_row = c_int / 16
            hex_col = c_int % 16
            c_subs = self.s_box[hex_row][hex_col]
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

    def process_block(self, block):
        # block harus berukuran 64 bit
        substituted = self.subs_block(block)
        transposed = Cipher1399.trans_block(substituted,8*len(block))
        return transposed

    def read_block_by_block(self):
        cipher = ""
        file = open(self.filein, 'rb')
        block = file.read(8)
        while (block != ""):
            cipher += self.process_block(block)
            block = file.read(8)
        return cipher

    def read_file_as_string(self):
        # https://prefetch.net/blog/2012/01/30/reading-a-file-into-a-python-string/
        f = open(self.filein, "r")
        data = f.read()
        # end of code
        return data

    def encrypt_string(self, text):
        # print(len(text))
        test = ""
        i = 0
        block = ""
        for c in text:
            if (i == 8):
                test += self.process_block(block)
                block = ""
                i = 0
            block += c
            i += 1
        test += self.process_block(block)
        # print(len(test))
        return test

    def make_s_box(self, key): # make sure the self.round_key is correct at this step
        # initiate s-box
        s_box_size = 16
        for i in range(0,s_box_size):
            arr_baris = []
            for j in range(0,s_box_size):
                arr_baris.append(-1)
            self.s_box.append(arr_baris)

        # make s-box from round_key
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
    def get_left(text):
        length = len(text) / 2
        return text[:length]

    @staticmethod
    def get_right(text):
        length = len(text) / 2
        return text[length:]

    @staticmethod
    # https://stackoverflow.com/questions/2612720/how-to-do-bitwise-exclusive-or-of-two-strings-in-python
    def sxor(s1,s2):    
        # convert strings to a list of character pair tuples
        # go through each tuple, converting them to ASCII code (ord)
        # perform exclusive or on the ASCII code
        # then convert the result back to ASCII (chr)
        # merge the resulting array of characters as a string
        return ''.join(chr(ord(a) ^ ord(b)) for a,b in zip(s1,s2))
    # end of code

    def feistel_encrypt_recursive(self, left, right, round):
        # initiate round by zero
        # source = https://en.wikipedia.org/wiki/Feistel_cipher
        if (round > self.number_of_iter):
            return left + right # basis
        else: # rekurens
            new_left = right
            new_right = Cipher1399.sxor(left, self.encrypt_string(right))
            return self.feistel_encrypt_recursive(new_left, new_right, round + 1)

    def feistel_encrypt(self, text):
        return self.feistel_encrypt_recursive(Cipher1399.get_left(text), Cipher1399.get_right(text), 0)

    def feistel_decrypt_recursive(self, left, right, round):
        # initiate round by zero
        # source = https://en.wikipedia.org/wiki/Feistel_cipher
        if (round > self.number_of_iter):
            return left + right # basis
        else: # rekurens
            new_right = left
            new_left = Cipher1399.sxor(right, self.encrypt_string(left))
            return self.feistel_decrypt_recursive(new_left, new_right, round + 1)

    def feistel_decrypt(self, text):
        return self.feistel_decrypt_recursive(Cipher1399.get_left(text), Cipher1399.get_right(text), 0)


ciph = Cipher1399("testaaaaaaaaaaaaa","datatest.txt")
# print(ciph.key)
# ciph.get_first_round_key()
ciph.make_s_box(Cipher1399.get_round_key(ciph.key, 3))
# ciph.print_s_box()
# print(ciph.read_block_by_block())
# print(Cipher1399.get_number_of_iter("Drestanto Muhammad Dyasputro"))
# print(Cipher1399.get_number_of_iter("pada suatu hari"))
# print(Cipher1399.get_list_of_key("Drestanto Muhammad Dyasputro"))
print(ciph.number_of_iter)

# print(Cipher1399.get_left("qwertyuiopasdfghjklzxcvbnmmnbvcxzlkjhgfdsapoiuytrewq"))
# print(Cipher1399.get_right("qwertyuiopasdfghjklzxcvbnmmnbvcxzlkjhgfdsapoiuytrewq"))
print(ciph.feistel_encrypt("qwertyuiopasdfghjklzxcvbnmmnbvcxzlkjhgfdsapoiuytrewq"))
simpen = ciph.feistel_encrypt("qwertyuiopasdfghjklzxcvbnmmnbvcxzlkjhgfdsapoiuytrewq")
print(ciph.feistel_decrypt(simpen))
