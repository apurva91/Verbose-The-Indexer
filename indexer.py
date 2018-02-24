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

def index_folder(table,input_dir):
	listed_files = list_files(input_dir)
	ini_time = time.time()
	for text in listed_files[0]:
			z= time.time()
			table=search_text(table, text)
			y= time.time()
			print ("Indexed " + text.split("/")[-1] + " in " + str(y-z)[0:5] + " seconds.")
	for pdf in listed_files[1]:
			z= time.time()
			table=search_PDF(table, pdf)
			y= time.time()
			print ("Indexed " + pdf.split("/")[-1] + " in " + str(y-z)[0:5] + " seconds.")
	fin_time = time.time()
	return table

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

