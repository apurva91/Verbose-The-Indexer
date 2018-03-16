import pdftotext, sys, time, re, os
from algorithms import *
from indexer import *
from filedump import *

input_dir="sdc"
table = {}
file_chart = {}
rev_file_chart = {}
last_result = []

from ui import *

'''
query = "in general practice"
result = multiple_words(table, query.split())
print (result)
'''