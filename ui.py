import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, Gdk, GObject
import os

s = Gdk.Screen.get_default()
screen_width = s.get_width()
screen_height = s.get_height()

builder = Gtk.Builder()
builder.add_from_file("verbose.glade")

prev_entry=""


class Handlers:
	def folder_chooser_clicked(self,button):
		dialog = Gtk.FileChooserDialog("Please choose a folder", None,
			Gtk.FileChooserAction.SELECT_FOLDER,
			(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
			 "Select", Gtk.ResponseType.OK))
		dialog.set_default_size(800, 400)

		response = dialog.run()
		if response == Gtk.ResponseType.OK:
			# input_dir = dialog.get_filename()
			print("Folder selected: " + dialog.get_filename())
		elif response == Gtk.ResponseType.CANCEL:
			print("Cancel clicked")

		dialog.destroy()

	def search_button_clicked(self,button):
		global prev_entry
		entry = builder.get_object("query_entry").get_text()
		if  prev_entry != entry:
			prev_entry = entry
			print (entry)


builder.connect_signals(Handlers())
window = builder.get_object("verbose")
window.connect("delete-event", Gtk.main_quit)
window.show_all()
Gtk.main()