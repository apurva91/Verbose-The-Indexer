import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, Gdk
import os

s = Gdk.Screen.get_default()
screen_width = s.get_width()
screen_height = s.get_height()

class MainWindow(Gtk.Window):
	
	query_entry = Gtk.Entry()

	def __init__(self):
		Gtk.Window.__init__(self, title="Verbose")
		self.set_border_width(20)
		# self.set_default_size(700, 400)

		box_outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
		self.add(box_outer)

		box_search = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
		box_outer.pack_start(box_search,True,True,0)

		self.query_entry.set_text("Search Here")
		box_search.pack_start(self.query_entry, True, True, 0)

		search_button = Gtk.Button(label="Search")
		search_button.connect("clicked", self.on_search_button_clicked)
		box_search.pack_start(search_button, True, True, 0)

		list_result = Gtk.ListBox()
		

	def on_search_button_clicked(self,widget):
		value = self.query_entry.get_text()
		print (value)

win = MainWindow()

win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()