import time
import re
import os
from stopwords import *
from nltk import PorterStemmer

regex_query="(?<!\d(?=\.\d))\.|\s|,|˚|\)|\(|-|\?|\"|:|—|”|;|\\|\'"

def recent_search_write(query):
	with open("recent.dump", "a") as myfile:
		myfile.write("||"+query)

def recent_search_read():
	if os.path.isfile("recent.dump"):
		with open('recent.dump','r') as f:
			x = f.read()
		x = x.split("||")[::-1]
		x.pop()
		return list(set(x))
	else:
		return []

def did_you_mean():
	print ("DID YOU MEAN XYZ")

def rank_result(answer):
	f_list = []
	for k in sorted(answer, key=lambda k: len(answer[k]), reverse=True):
		f_list.append(k)
	return f_list


def result(table,query):
	x = time.time()
	recent_search_write(query)
	answer = intersect_file(table,query)
	y = time.time()
	
	return ["Searched in " + str(y-x) + " seconds.",answer,rank_result(answer)]

	for dkey in answer:
		print ("Filename: " + dkey.split("/")[-1])
		print (answer[dkey])

def intersect_file(table,query):
	listofwords = list(filter(None,re.split('(?:'+regex_query+')+',query)))
	stemmer = PorterStemmer()
	listofwords = [stemmer.stem(x) for x in listofwords]
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

def open_text(filename, linenumber):
	os.system("gedit "+filename+ " +"+linenumber)

def open_pdf(filename, pagenumber):
	os.system("okular +"+filename + " -p " + pagenumber)

'''
Now what about how will you index
inedxing is simple add occurence on 
'''
