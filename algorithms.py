import time
import re
import os

def did_you_mean():
	print ("DID YOU MEAN XYZ")

def multiple_words(table, listofwords):
	try:
		x = time.time()
		intersect = set(table[listofwords[0].lower()])
		
		for i in range(1,len(listofwords)):
			intersect = intersect & set(table[listofwords[i].lower()])
		y = time.time()
		print (y-x)
		return intersect
	except KeyError:
		did_you_mean()

def search_keys(table,query):
	myre = re.compile("[\w]*" + query + "[\w-]*")
	result = []
	for key in table:
		if myre.match(key):
			result.append(key)
	return result
