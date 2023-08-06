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
import pyfie.src.klass as klass
import pyfie.src.vars as vars

def compose(path: str, value, password = None):
	""" Encrypts and writes given value to the file in path;
	if something will go wrong, nothing will happen """
	lock = klass.locker(path, value)
	vars.keys[path] = password
	file = open(path, "wb")
	pickle.dump(lock, file, -1)
	file.close()
	
def parse(path: str, password = None):
	""" Decrypts and returns a value from the file in path;
	if something will go wrong, nothing will happen """
	file = open(path, "rb")
	lock = pickle.load(file)
	file.close()
	return lock.fetch(password)