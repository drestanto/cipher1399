import random
import sys

class Cipher1399 :

	def __init__(self, key, filein):
		self.key = key
		self.filein = filein
		self.s_box = []

	def read_block_by_block(self):
		file = open(self.filein, 'rb')
		block = file.read(8)
		while (block != ""):
			print(block)
			block = file.read(8)

	def process_block(block):
		# block harus berukuran 64 bit
		pass

	def make_s_box(self):
		# initiate s-box
		for i in range(0,15):
			arr_baris = []
			for j in range(0,15):
				arr_baris.append(-1)
			self.s_box.append(arr_baris)

	def print_s_box(self):
		for arr in self.s_box:
			for elem in arr:
				sys.stdout.write(format(elem,'02x'))
				sys.stdout.write(' ')
			print("")


ciph = Cipher1399("test","datatest.txt")
print(ciph.key)
ciph.read_block_by_block()
ciph.make_s_box()
ciph.print_s_box()