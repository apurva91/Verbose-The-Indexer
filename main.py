import re
import pdftotext
import os
import time
input_pdf="algo.pdf"

text_pdf = pdftotext.PDF(open(input_pdf,'rb'))

table={}
i = 0
for page in text_pdf:
	i = i+1
	x = list(filter(None,re.split("\n| |,|\.",page)))
	for word in x:
		wordl = word.lower()
		if wordl in table:
			table[wordl].append(i)
		else:
			table[wordl] = [i]


def multiple_words(table, listofwords):
	x = time.time()
	intersect = set(table[listofwords[0].lower()])

	for i in range(1,len(listofwords)):
		intersect = intersect & set(table[listofwords[i].lower()])
	y = time.time()
	print (y-x)
	return intersect

query = "in general practice"
result = multiple_words(table, query.split())
print (result)