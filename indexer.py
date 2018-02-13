import pdftotext
import time
import re
import os
from filedump import *
regex_query="(?<!\d(?=\.\d))\.|\s|,|˚|\)|\(|-|\?|\"|:|—|”|;|\\|\'"

'''
Take the common portion make into one pdf and text part
Something like this
def main_search(tableold,input_file):
	table={}
	if check_dump(input_file):
		table = load_dump(input_file)
	else:
		table = search_PDF() or search_text()

	tableold = merge_dump(tableold,table,input_file)
	return tableold
'''

def search_PDF(tableold, input_file):
	table={}
	if check_dump(input_file):
		table = load_dump(input_file)
	else:
		text_pdf = pdftotext.PDF(open(input_file,'rb'))
		i = 0
		for page in text_pdf:
			i = i+1
			x = list(filter(None,re.split('(?:'+regex_query+')+',page)))
			for word in x:
				wordl = word.lower()
				if wordl in table:
					table[wordl].append(str(i))
				else:
					table[wordl] = [str(i)]
		save_dump(table,input_file)

	tableold = merge_dump(tableold,table,input_file)
	return tableold


def search_text(tableold, input_file):
	table={}
	if check_dump(input_file):
		table = load_dump(input_file)
	else:
		text = open(input_file,'r')
		text = re.split("\\n|\\r|\\t", str(text.read()))
		i = 0
		for line in text:
			i = i+1
			x = list(filter(None,re.split('(?:'+regex_query+')+',line)))
			for word in x:
				wordl = word.lower()
				if wordl in table:
					table[wordl].append(str(i))
				else:
					table[wordl] = [str(i)]
		save_dump(table,input_file)

	tableold = merge_dump(tableold,table,input_file)
	return tableold

def list_files(folder):
	list_folder = os.listdir(folder)
	text = [os.path.realpath(folder + "/" + x) for x in os.listdir(folder) if x.lower().endswith(('.txt','.log'))]
	pdfs = [os.path.realpath(folder + "/" + x) for x in os.listdir(folder) if x.lower().endswith(('.pdf'))]
	dirs = [os.path.realpath(folder + "/" + x) for x in os.listdir(folder) if os.path.isdir(x) and not x.endswith("__")]
	return [text,pdfs]
