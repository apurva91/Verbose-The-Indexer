import pdftotext
import time
import re
import os
from filedump import *
regex_query="(?<!\d(?=\.\d))\.|\s|,|˚|\)|_|\(|-|\?|\"|:|—|”|;|\\|\'"
# from stopwords import *
from nltk import PorterStemmer
stemmer = PorterStemmer()
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

def search_PDF(tableold, input_file,enc):
	table={}
	if check_dump(input_file):
		table = load_dump(input_file)
	else:
		text_pdf = pdftotext.PDF(open(input_file,'rb'))
		i = 0
		j = 0
		for page in text_pdf:
			i = i+1
			x = list(filter(None,re.split('(?:'+regex_query+')+',page)))
			for word in x:
				if 1:
					wordl = stemmer.stem(word)
					j = j+1
					if wordl in table:
						if i in table[wordl]:
							table[wordl][i].append(j)
						else:
							table[wordl][i] = [j]
					else:
						table[wordl] = {i:[j]}
		save_dump(table,input_file)

	tableold = merge_dump(tableold,table,enc)
	return tableold

def search_text(tableold, input_file,enc):
	table={}
	if check_dump(input_file):
		table = load_dump(input_file)
	else:
		text = open(input_file,'rb')
		text = re.split("\r\n|\n", text.read().decode("utf-8",errors = "ignore"))
		i = 0
		j=0
		for line in text:
			i = i+1
			x = list(filter(None,re.split('(?:'+regex_query+')+',line)))
			for word in x:
				if 1:
					wordl = stemmer.stem(word)
					j = j+1
					if wordl in table:
						if i in table[wordl]:
							table[wordl][i].append(j)
						else:
							table[wordl][i] = [j]
					else:
						table[wordl] = {i:[j]}
		save_dump(table,input_file)

	tableold = merge_dump(tableold,table,enc)
	return tableold

file_number = 0

def index_folder(table,input_dir,file_chart,rev_file_chart):
	global file_number
	listed_files = list_files(input_dir)
	val = len(listed_files[0]) + len(listed_files[1])
	# progress_dialog_ini(val)
	ini_time = time.time()
	for text in listed_files[0]:
		file_chart[hex(file_number)] = text
		rev_file_chart[text] = hex(file_number)
		z= time.time()
		table=search_text(table, text, hex(file_number))
		y= time.time()
		print ("Indexed " + text.split("/")[-1] + " in " + str(y-z)[0:5] + " seconds.")
		file_number += 1
		# progress_dialog_update(i,val)
	for pdf in listed_files[1]:
		file_chart[hex(file_number)] = pdf
		rev_file_chart[pdf] = hex(file_number)
		z= time.time()
		table=search_PDF(table, pdf, hex(file_number))
		y= time.time()
		print ("Indexed " + pdf.split("/")[-1] + " in " + str(y-z)[0:5] + " seconds.")
		file_number += 1
		# progress_dialog_update(i,val)
	fin_time = time.time()	
	return [table,file_chart,rev_file_chart]

def list_files(folder):
	list_folder = os.listdir(folder)
	text = [os.path.realpath(folder + "/" + x) for x in os.listdir(folder) if x.lower().endswith(('.txt','.log'))]
	pdfs = [os.path.realpath(folder + "/" + x) for x in os.listdir(folder) if x.lower().endswith(('.pdf'))]
	dirs = [os.path.realpath(folder + "/" + x) for x in os.listdir(folder) if os.path.isdir(folder + "/" + x) and not x.endswith("__")]
	if len(dirs) > 0:
		for dir_cur in dirs:
			dir_list = list_files(dir_cur)
			text = text + dir_list[0]
			pdfs = pdfs + dir_list[1]
	return [text,pdfs,dirs]

