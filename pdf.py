import pdftotext
import time
import re
import os
from indexer import *
from algorithms import *
import sys
input_dir="Files"
listed_files = list_files(input_dir)
table = {}

# for text,pdfs in listed_files:
# 	for x in text:
# 		z= time.time()
# 		y= time.time()
# 		print ("Indexed " + x.split("/")[-1] + "In " + str(y-z)[0:5] + "Seconds")
# 	for x in pdfs:
# 		z= time.time()
# 		y= time.time()
# 		print ("Indexed " + x.split("/")[-1] + "In " + str(y-z)[0:5] + "Seconds")
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
sizev = sys.getsizeof(table)
print (str(fin_time - ini_time)[0:5] + " seconds to index the directory \"" + input_dir + "\" . Used a total of " + str(sizev/1024/1024)[0:5] + " MB. ")
'''
query = "in general practice"
result = multiple_words(table, query.split())
print (result)
'''