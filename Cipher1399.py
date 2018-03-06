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
        transposed = Cipher1399.trans_block(substituted,64)
        return transposed

    def read_block_by_block(self):
        cipher = ""
        file = open(self.filein, 'rb')
        block = file.read(8)
        while (block != ""):
            if (len(block) != 8):
                jumlah_tambahan_spasi = 8-len(block)
                for i in range(0,jumlah_tambahan_spasi):
                    block += " "
            cipher += self.process_block(block)
            block = file.read(8)
        return cipher

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


ciph = Cipher1399("test","datatest.txt")
# print(ciph.key)
# ciph.get_first_round_key()
ciph.make_s_box(Cipher1399.get_round_key(ciph.key,3))
# ciph.print_s_box()
# print(ciph.read_block_by_block())
print(Cipher1399.get_number_of_iter("Drestanto Muhammad Dyasputro"))
print(Cipher1399.get_number_of_iter("pada suatu hari"))
print(Cipher1399.get_list_of_key("Drestanto Muhammad Dyasputro"))