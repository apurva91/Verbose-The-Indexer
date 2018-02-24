import os
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
