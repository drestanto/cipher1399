import random
import sys

class Cipher1399 :

	def __init__(self, key, filein):
		self.key = key
		self.round_key = ""
		self.filein = filein
		self.s_box = []

	@staticmethod
	def get_round_key(key, length):
		random.seed(key)
		round_key = ""
		for i in range(0,length):
			round_key += str(chr(random.randint(0,255)))
		return round_key

	def get_first_round_key(self):
		self.round_key = Cipher1399.get_round_key(self.key,3)

	def get_next_round_key(self):
		self.round_key = Cipher1399.get_round_key(self.round_key,3)

	def read_block_by_block(self):
		file = open(self.filein, 'rb')
		block = file.read(8)
		while (block != ""):
			print(block)
			block = file.read(8)

	def process_block(block):
		# block harus berukuran 64 bit
		pass

	def make_s_box(self): # make sure the self.round_key is correct at this step
		# initiate s-box
		s_box_size = 16
		for i in range(0,s_box_size):
			arr_baris = []
			for j in range(0,s_box_size):
				arr_baris.append(-1)
			self.s_box.append(arr_baris)

		# make s-box from round_key
		print(self.s_box[0][15])



	def print_s_box(self):
		for arr in self.s_box:
			for elem in arr:
				sys.stdout.write(format(elem,'02x'))
				sys.stdout.write(' ')
			print("")


ciph = Cipher1399("test","datatest.txt")
print(ciph.key)
ciph.read_block_by_block()
ciph.get_first_round_key()
ciph.make_s_box()
# ciph.print_s_box()