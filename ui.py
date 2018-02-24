import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, Gdk, GObject
import os
from indexer import *
from main import *
from algorithms import *

s = Gdk.Screen.get_default()
screen_width = s.get_width()
screen_height = s.get_height()

builder = Gtk.Builder()
builder.add_from_file("verbose.glade")
prev_entry=""

def on_click_result_func(data):
	if(data[0].endswith(".pdf")):
		os.system("okular " + data[0] + " -p " + data[1] + " &")
	else:
		os.system("gedit " + data[0] + " +" + data[1] + " &")

def generate_result_list(result_flist):
	list_box2 = builder.get_object("result_list")
	for row in list_box2.get_children():
		list_box2.remove(row)

	for data in result_flist:
		list_box2.insert(ListBoxRowWithData(data[1]+ "-No.: " + data[0]),0)
	list_box2.connect('row-activated', lambda widget, row: on_click_result_func(row.data.split("-No.: ")))
	list_box2.show_all()

def search_it(entry):
	global table
	stats = result(table,entry)
	print ("searched for" + entry)
	builder.get_object("result_stats").set_text(stats[0])
	generate_result_list(stats[1])
	builder.get_object("main_notebook").set_current_page(1)

class ListBoxRowWithData(Gtk.ListBoxRow):

    def __init__(self, data):
        super(Gtk.ListBoxRow, self).__init__()
        self.data = data
        self.add(Gtk.Label(data))

def list_insert(entry):
	list_box2 = builder.get_object("recent_list")
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
		table = index_folder(table,input_dir)

	def search_button_clicked(self,button):
		global prev_entry
		entry = builder.get_object("query_entry").get_text()
		if  prev_entry != entry:
			prev_entry = entry
			global table
			stats = result(table,entry)
			builder.get_object("recent_list").add(ListBoxRowWithData(entry))
			generate_result_list(stats[1])
			builder.get_object("result_stats").set_text(stats[0])
			builder.get_object("main_notebook").set_current_page(1)
			list_insert(entry)

builder.connect_signals(Handlers())
window = builder.get_object("verbose")
window.connect("delete-event", Gtk.main_quit)
window.show_all()
Gtk.main()