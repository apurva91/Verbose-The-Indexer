import time
import re
import os
# from stopwords import *
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

def did_you_mean(table,query,listofwords):
	if len(listofwords) is 1:
		answer = {}
		if exact_check(query[0]) and exact_check(query[-1]):
			answer =  intersect_file(table,'"' + correction(stemmer.stem(listofwords[0])) + '"')
		else:
			answer =  intersect_file(table,correction(stemmer.stem(listofwords[0])))
		global dym
		dym = 1
		return answer
	else:
		return 0

def rank_result(answer,query):
	f_list = []
	global fiof, glof, wfof

	for k in sorted(answer, key=lambda k: calc_glfi_for_phrase(k,fiof,glof,query,wfof), reverse=True):
		f_list.append(k)
	return f_list


dym = 0

def result(table,query):
	x = time.time()
	recent_search_write(query)
	answer = intersect_file(table,query)
	y = time.time()
	if answer is 0:
		return ["No result Found",{},{}]
	else:
		if dym is 1:
			ny = correction(stemmer.stem(list(filter(None,re.split("\'|\"",query)))[0]))
			return ["Searched in " + str(y-x) + " seconds.\nShowing Results For Did You Mean " + ny ,answer,rank_result(answer,ny)]
		else:	
			return ["Searched in " + str(y-x) + " seconds.",answer,rank_result(answer,query)]

def exact_check(c):
	if c == "\"" or c =="\'":
		return 1
	else:
		return 0

def intersect_file(table,query):
	exact = 0
	if exact_check(query[0]) and exact_check(query[-1]):
		exact = 1 
	listofwords = list(filter(None,re.split('(?:'+regex_query+')+',query)))
	
	stemmer = PorterStemmer()
	# listofwords = [x for x in listofwords if x not in stopwords]
	listofwords = [stemmer.stem(x) for x in listofwords]
	global dym
	dym = 0
	try:
		books = set(table[listofwords[0].lower()].keys())		
		for i in range(1,len(listofwords)):
			books = books & set(table[listofwords[i].lower()].keys())
		return multiple_words(table,list(books),listofwords,exact)
	except KeyError:
		return did_you_mean(table,query,listofwords)


def multiple_words(table,list_books,listofwords,exact):
	answer = {}
	epage = exact_search(listofwords,table,list_books)
	try:
		for book in list_books:
			if exact is 0:
				intersect = set(table[listofwords[0].lower()][book].keys())		
				for i in range(1,len(listofwords)):
					intersect = intersect & set(table[listofwords[i].lower()][book].keys())
				if bool(epage):
					if book in epage:
						print(epage[book])
						answer[book] = [x for x in list(intersect) if str(x) not in epage[book]] + [x for x in epage[book]]
					else:
						answer[book] = list(intersect)
				else:
					answer[book] = list(intersect)
			else:
				answer[book] = [x for x in epage[book] if len(epage[book]) is not 0]
			if len(answer[book]) is 0:
				del answer[book]
		if len(answer) is 0:
			return 0
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

def words(text): return re.findall(r'\w+', text.lower())

def P(word): 
    "Probability of `word`."
    global glof
    return glof[word] / sum(glof.values())

def correction(word): 
    "Most probable spelling correction for word."
    return max(candidates(word), key=P)

def candidates(word): 
    "Generate possible spelling corrections for word."
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def known(words): 
    "The subset of `words` that appear in the dictionary of glof."
    global glof
    return set(w for w in words if w in glof)

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word): 
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))