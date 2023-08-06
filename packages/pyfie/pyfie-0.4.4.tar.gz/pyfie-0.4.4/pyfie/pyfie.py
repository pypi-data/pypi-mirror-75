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

__keys = {}

class __locker:
	def __init__(self, path, value):
		self.__value = value
		self.path = path

	def fetch(self, password):
		if self.path in globals()["__keys"] and globals()["__keys"][self.path] == password:
			return self.__value

def compose(path, value, password):
	""" Encrypts and writes given value to the file in path;
	if something will go wrong, nothing will happen """
	lock = __locker(path, value)
	__keys[path] = password
	file = open(path, "wb")
	pickle.dump(lock, file, -1)
	file.close()
	
def parse(path, password):
	""" Decrypts and returns a value from the file in path;
	if something will go wrong, nothing will happen """
	file = open(path, "rb")
	lock = pickle.load(file)
	file.close()
	return lock.fetch(password)