import time
import re
import os
from stopwords import *
from nltk import PorterStemmer
from indexer import *
import math
regex_query="(?<!\d(?=\.\d))\.|\s|,|˚|\)|\(|_|-|\?|\"|:|—|”|;|\\|\'"

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

def calc_glfi(fi,glt,gli):
	if gli is not 0:
		return math.log(glt/gli) * fi
	else:
		return 0

def calc_glfi_for_phrase(k,fiof,glof,query,wfof):
	listofwords = list(filter(None,re.split('(?:'+regex_query+')+',query)))
	stemmer = PorterStemmer()
	# listofwords = [x for x in listofwords if x not in stopwords]
	listofwords = [stemmer.stem(x) for x in listofwords]
	ans = 0
	for x in listofwords:
		ans = ans + calc_glfi(fiof[k][x],len(fiof),wfof[x])/len(fiof[k])/len(listofwords)
	print(ans)
	return ans

def did_you_mean():
	print ("DID YOU MEAN XYZ")

def rank_result(answer,query):
	f_list = []
	global fiof, glof, wfof

	for k in sorted(answer, key=lambda k: calc_glfi_for_phrase(k,fiof,glof,query,wfof), reverse=True):
		f_list.append(k)
	return f_list



def result(table,query):
	x = time.time()
	recent_search_write(query)
	answer = intersect_file(table,query)
	y = time.time()
	
	return ["Searched in " + str(y-x) + " seconds.",answer,rank_result(answer,query)]


def intersect_file(table,query):
	listofwords = list(filter(None,re.split('(?:'+regex_query+')+',query)))
	
	stemmer = PorterStemmer()
	# listofwords = [x for x in listofwords if x not in stopwords]
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
	epage = exact_search(listofwords,table,list_books)
	try:
		for book in list_books:

			intersect = set(table[listofwords[0].lower()][book].keys())		
			for i in range(1,len(listofwords)):
				intersect = intersect & set(table[listofwords[i].lower()][book].keys())

			if book in epage:
				print(epage[book])
				answer[book] = [x for x in list(intersect) if str(x) not in epage[book]] + [x for x in epage[book]]
			else:
				answer[book] = list(intersect)
	
		return answer
	except KeyError:
		did_you_mean()

def exact_search(listofwords, table, list_books):
	elist = {}
	epage = {}
	try:
		for book in list_books:
			a = []
			for i , word in enumerate(listofwords):
				a.append([ y - i for x in table[word][book].values() for y in x])
			elist[book] = set(a[0]).intersection(*a)


		for book in elist:
			epage[book] = []
			tof = elist[book]
			for key in table[listofwords[0].lower()][book]:
				for ind in list(tof):
					if ind in table[listofwords[0].lower()][book][str(key)]:
						epage[book].append(key)

		return epage
	except KeyError:
		"NO RESULTS"


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
