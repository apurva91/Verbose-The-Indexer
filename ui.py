import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, Gdk, GObject
import os
from indexer import *
from main import *
from algorithms import *
from filedump import *
s = Gdk.Screen.get_default()
screen_width = s.get_width()
screen_height = s.get_height()

builder = Gtk.Builder()
builder.add_from_file("verbose.glade")
prev_entry=""

def on_click_result_func(entry,data):
	global file_chart
	print(entry + " " + data)
	# return
	if(entry.endswith(".pdf")):
		os.system("okular " + entry + " -p " + data + " &")
	else:
		os.system("gedit " + entry + " +" + data + " &")

def generate_result_list(result_flist):
	list_box2 = builder.get_object("result_list")
	list_box2.unselect_all()
	for row in list_box2.get_children():
		list_box2.remove(row)
	global file_chart
	global last_result
	for data in result_flist:
		list_box2.insert(ListBoxRowWithData("File:" + file_chart[data].replace("/","->")),0)
	list_box2.connect('row-activated', lambda widget, row: get_particular_result(row.data))
	list_box2.show_all()

def generate_page_list(entry):
	list_box2 = builder.get_object("page_list")
	list_box2.unselect_all()
	for row in list_box2.get_children():
		list_box2.remove(row)
	global file_chart
	global rev_file_chart
	global last_result
	for data in last_result[1][rev_file_chart[entry]]:
		list_box2.insert(ListBoxRowWithDataMod("Line/Page Number: " + str(data),str(entry)) ,0)
	# list_box2.connect('key-release-event', on_key_enter(entry,row.data))
	# list_box2.connect('row-selected', lambda widget, row: print(entry + row.data.split("Number: ")[1]) )
	list_box2.show_all()

def search_it(entry):
	global table
	global last_result
	last_result = result(table,entry)
	print ("Searched for " + entry)
	builder.get_object("result_stats").set_text(last_result[0])
	generate_result_list(last_result[2])
	builder.get_object("main_notebook").set_current_page(1)

def get_particular_result(entry):
	dec_entry = entry.replace("->","/").split("File:")[-1]
	list_box2 = builder.get_object("page_list")
	builder.get_object("result_expand").set_text(dec_entry.split("/")[-1])
	generate_page_list(dec_entry)
	builder.get_object("main_notebook").set_current_page(2)


class ListBoxRowWithData(Gtk.ListBoxRow):

    def __init__(self, data):
        super(Gtk.ListBoxRow, self).__init__()
        self.data = data
        self.add(Gtk.Label(data))

class ListBoxRowWithDataMod(Gtk.ListBoxRow):

    def __init__(self, data,id):
        super(Gtk.ListBoxRow, self).__init__()
        self.data = data
        self.id = id

        box = Gtk.EventBox()
        label = Gtk.Label(data)
        box.add(label)
        # box.connect("enter-notify-event", self.on_mouse)
        box.connect("button-release-event",self.on_click)
        self.add(box)

    def on_click(self,widget,data=None):
    	on_click_result_func(self.id,self.data.split("Number: ")[1])

def list_insert(entry):
	list_box2 = builder.get_object("recent_list")
	list_box2.insert(ListBoxRowWithData(entry),0)
	list_box2.connect('row-activated', lambda widget, row: search_it(row.data))
	list_box2.show_all()

def list_insert_page(entry):
	list_box2 = builder.get_object("page_list")
	list_box2.insert(ListBoxRowWithData(entry),0)
	list_box2.connect('row-activated', lambda widget, row: search_it(row.data))
	list_box2.show_all()


class Handlers:

	def __init__(self):

		listbox_2 = builder.get_object("recent_list")
		items = recent_search_read()
		for item in items:
			listbox_2.add(ListBoxRowWithData(item))
		listbox_2.connect('row-activated', lambda widget, row: search_it(row.data))
		listbox_2.show_all()

	def folder_chooser_clicked(self,button):	
		
		dialog = Gtk.FileChooserDialog("Please choose a folder", None, Gtk.FileChooserAction.SELECT_FOLDER,(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,"Select", Gtk.ResponseType.OK))
		dialog.set_default_size(800, 400)
		response = dialog.run()
		if response == Gtk.ResponseType.OK:
			global input_dir
			input_dir = dialog.get_filename()
			print("Folder selected: " + input_dir)
		elif response == Gtk.ResponseType.CANCEL:
			print("Cancel clicked")
			dialog.destroy()
			return
		dialog.destroy()
		global table
		global file_chart
		global rev_file_chart
		p = index_folder(table,input_dir,file_chart,rev_file_chart)
		table = p[0]
		file_chart = p[1]
		rev_file_chart = p[2]

	def search_button_clicked(self,button):
		global prev_entry
		entry = builder.get_object("query_entry").get_text()
		if  prev_entry != entry:
			prev_entry = entry
			global table
			global last_result
			last_result = result(table,entry)
			builder.get_object("recent_list").add(ListBoxRowWithData(entry))
			generate_result_list(last_result[2])
			builder.get_object("result_stats").set_text(last_result[0])
			builder.get_object("main_notebook").set_current_page(1)
			list_insert(entry)

builder.connect_signals(Handlers())
window = builder.get_object("verbose")
window.connect("delete-event", Gtk.main_quit)
window.show_all()
Gtk.main()