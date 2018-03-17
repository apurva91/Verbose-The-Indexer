import os
import time
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

def time_calc_test(cmd):
	x = time.time()
	exec(cmd)
	y = time.time()
	print(str(x-y))


import re

def words(text): return re.findall(r'\w+', text.lower())

def P(word, N=sum(glof.values())): 
    "Probability of `word`."
    return glof[word] / N

def correction(word): 
    "Most probable spelling correction for word."
    return max(candidates(word), key=P)

def candidates(word): 
    "Generate possible spelling corrections for word."
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def known(words): 
    "The subset of `words` that appear in the dictionary of glof."
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