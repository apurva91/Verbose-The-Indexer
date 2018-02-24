import json
import os

def rename_file(filename):
	return os.path.realpath(".") + "/.DataDump/" + filename.replace("/","―") + ".dump"

def save_dump(table,filename):
	if not os.path.isdir(".DataDump"):
		os.mkdir(".DataDump")
	json.dump(table, open(rename_file(filename), 'w'))
	print("Saving Newly indexed File " + filename.split("/")[-1])

def load_dump(filename):
	print ("Using saved version of file " + filename.split("/")[-1])
	newtable = json.load(open(rename_file(filename)))
	return newtable

def check_dump(filename):
	if not os.path.isdir(".DataDump"):
		os.mkdir(".DataDump")
	if os.path.exists(rename_file(filename)):
		return True
	else:
		return False

def merge_dump(table,newtable,enc):
	for word in newtable.keys():
		if word in table:
			table[word][enc] = newtable[word]
		else:
			table[word] = {}
			table[word][enc] = newtable[word]
	return table
