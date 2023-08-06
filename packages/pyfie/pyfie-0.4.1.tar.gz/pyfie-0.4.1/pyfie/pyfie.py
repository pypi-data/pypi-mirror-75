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

import base64
import random

def __cE(base, key):
	base += 'A'
	big = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
	small = 'abcdefghijklmnopqrstuvwxyz'
	llist = list(base)
	llist2 = list(big)
	llist3 = list(small)
	for k, v in enumerate(llist):
		if(v.isupper()):
			where = big.find(v)
		else:
			where = small.find(v)
		where += key
		while where > 25:
			where -= 26
		if(v.isupper() and v in big):
			llist[k] = llist2[where]
		elif(v.islower() and v in small):
			llist[k] = llist3[where]
		else:
			llist[k] = llist[k]
	base = ''.join(llist)
	return base

def __cD(base, key):
	mode = 1
	big = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
	small = 'abcdefghijklmnopqrstuvwxyz'
	llist = list(base)
	llist2 = list(big)
	llist3 = list(small)
	for k, v in enumerate(llist):
		if(v.isupper()):
			where = big.find(v)
		else:
			where = small.find(v)
		where -= key
		while where < 0:
			where += 26
		if(v.isupper() and v in big):
			llist[k] = llist2[where]
		elif(v.islower() and v in small):
			llist[k] = llist3[where]
		else:
			llist[k] = llist[k]
	if(mode == 1):
            llist[-1] = ''
	base = ''.join(llist)
	return base

def __bE(string):
	string = string.encode()
	string = base64.b64encode(string)
	return string.decode("ascii")

def __bD(bytesValue):
	normalValue = bytesValue.encode("ascii")
	normalValue = base64.b64decode(normalValue)
	return normalValue.decode("ascii")

def compose(path, value):
	""" Encrypts and writes given value to the file in path;
	if something will go wrong, nothing will happen """
	try:
		key = random.randint(3, 28)
		key_ = key + 5
		value = __cE(str(value), key)
		value = [
			value,
			key_
		]
		value = __bE(str(value))
		value = __cE(str(value), 5)
		file = open(path, "w")
		file.write(value)
		file.close()
	except:
		pass

def parse(path):
	""" Decrypts and returns a value from the file in path;
	if something will go wrong, nothing will happen """
	try:
		file = open(path)
		value = file.read()
		file.close()
		value = __cD(value, 5)
		value = __bD(value)
		value = eval(value)
		key = value[1] - 5
		value = value[0]
		value = __cD(value, key)
		return value
	except:
		pass