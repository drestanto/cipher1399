import random

class Cipher1399 :

	def __init__(self, key, filein):
		self.key = key
		self.filein = filein

	def read_block_by_block(self):
		file = open(self.filein, 'rb')
		block = file.read(8)
		while (block != ""):
			print(block)
			block = file.read(8)

	def process_block(block):
		# block harus berukuran 64 bit
		pass




ciph = Cipher1399("test","datatest.txt")
print(ciph.key)
ciph.read_block_by_block()