# All rights for this file are claimed by Kazafka/Kafajku.
# Copyright (C) PyFE by Kazafka/Kafajku -
# - All rights reserved.

# Python File Encrypter

# Licensed under MIT License
# MIT License implies:
# [O] Commercial use	[X] Liability	[!] License and copyright notice
# [O] Modification		[X] Warranty	
# [O] Distribution
# [O] Private use 

import pickle

class tile:
	__insts = {}

	def __init__(self, value, password):
		self.id = len(tile.__insts)
		tile.__insts[self.id] = {
			"value": value,
			"password": password
		}

	def fetch(self, password):
		if self.id in tile.__insts:
			value = tile.__insts[self.id]["value"]
			password_ = tile.__insts[self.id]["password"]
			if password == password_:
				return value

def write(path: str, value, password = None):
	file = open(path, "wb")
	pickle.dump(tile(value, password), file, -1)
	file.close()
	
def read(path: str, password = None):
	file = open(path, "rb")
	value = pickle.load(file)
	file.close()
	return value.fetch(password)