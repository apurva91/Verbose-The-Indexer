import time
import re
import os

def did_you_mean():
	print ("DID YOU MEAN XYZ")

def result(table,query):
	x = time.time()
	answer = intersect_file(table,query)
	y = time.time()
	print ("These are the results found. Time Taken: " + str(y-x) + " seconds.")
	for dkey in answer:
		print ("Filename: " + dkey.split("/")[-1])
		print (answer[dkey])

def intersect_file(table,query):
	listofwords = query.split()
	try:
		books = set(table[listofwords[0].lower()].keys())		
		for i in range(1,len(listofwords)):
			books = books & set(table[listofwords[i].lower()].keys())
		return multiple_words(table,list(books),listofwords)
	except KeyError:
		did_you_mean()

def multiple_words(table,list_books,listofwords):
	answer = {}
	try:
		for book in list_books:
			intersect = set(table[listofwords[0].lower()][book])		
			for i in range(1,len(listofwords)):
				intersect = intersect & set(table[listofwords[i].lower()][book])
			answer[book] = list(intersect)
		return answer
	except KeyError:
		did_you_mean()

def search_keys(table,query):
	myre = re.compile("[\w]*" + query + "[\w-]*")
	result = []
	for key in table:
		if myre.match(key):
			result.append(key)
	return result

'''
Now what about how will you index
inedxing is simple add occurence on 
'''
