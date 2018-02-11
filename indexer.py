import pdftotext
import time
import re
import os

def search_PDF(table, input_file):
	text_pdf = pdftotext.PDF(open(input_file,'rb'))
	i = 0
	for page in text_pdf:
		i = i+1
		x = list(filter(None,re.split('\n| |,|\.|˚|\)|\(|-|\?|\"|:|—|”|;',page)))
		for word in x:
			wordl = word.lower()
			if wordl in table:
				table[wordl].append(input_file+":"+str(i))
			else:
				table[wordl] = [input_file+":"+str(i)]

	return table

def search_text(table, input_file):
	text = open(input_file,'rb')
	text = re.split("\\n|\\r|\\t", str(text.read()))
	i = 0
	for line in text:
		i = i+1
		x = list(filter(None,re.split('\n| |\\|,|\.|˚|\)|\(|-|\?|\"|:|—|”|;|\'',line)))
		for word in x:
			wordl = word.lower()
			if wordl in table:
				table[wordl].append(input_file+":"+str(i))
			else:
				table[wordl] = [input_file+":"+str(i)]

	return table

def list_files(folder):
	list_folder = os.listdir(folder)
	text = [os.path.realpath(folder + "/" + x) for x in os.listdir(folder) if x.lower().endswith(('.txt','.log'))]
	pdfs = [os.path.realpath(folder + "/" + x) for x in os.listdir(folder) if x.lower().endswith(('.pdf'))]
	dirs = [os.path.realpath(folder + "/" + x) for x in os.listdir(folder) if os.path.isdir(x) and not x.endswith("__")]
	return [text,pdfs]
