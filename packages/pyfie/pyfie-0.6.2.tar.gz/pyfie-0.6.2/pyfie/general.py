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
	""" Tile is a class used to make instances that can be encrypted into files """
	__children = {}

	class __cont:
		""" Cont class is used to make private containers """
		def __init__(self, value, password):
			""" Creates a cont class instance """
			self._value = value
			self._password = password

	def __init__(self, value, password = None):
		""" Creates a tile class instance """
		self.id = len(tile.__children)
		tile.__children[self.id] = {
			"body": {
				"container": tile.__cont(value, password)
			}
		}

	def fetch(self, password = None):
		""" Tries to retrieve value of a tile class instance, if password is valid """
		if self.id in tile.__children:
			this = tile.__children[self.id]
			container = this["body"]["container"]
			if password == container._password:
				return container._value

def write(path: str, value: tile) -> bool:
	""" Tries to write an encrypted tile class instance into the file in path """
	try:
		file = open(path, "wb")
		pickle.dump(value, file, -1)
		file.close()
		return True
	except:
		return False
	
def read(path: str, password = None) -> tile:
	""" Tries to return a decrypted tile class instance from the file in path """
	try:
		file = open(path, "rb")
		value = pickle.load(file)
		file.close()
		return value
	except:
		return tile(False, None)