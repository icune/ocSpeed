import sublime, sublime_plugin
import os
import sys

BASE_PATH = os.path.abspath(os.path.dirname(__file__))
globals()['BASE_PATH'] = BASE_PATH

if not BASE_PATH in sys.path:
	sys.path += [BASE_PATH]
	sys.path += [BASE_PATH + '\\airspeed']

from ocs_utils.filer import makeFiles

class WriteNewCommand(sublime_plugin.TextCommand):
	def run(self, edit, sam):
		self.view.insert(edit, 0, sam)

class WantPanelCommand(sublime_plugin.TextCommand):
	input_message         = "Make OpenCart modules"
	default_input         = "create * test/it"
	process_panel_input   = lambda s, i: i.title()
	window = None
	def is_enabled(self):
		return True

	def on_change(self, abbr):
		pass

	def undo(self):
		pass

	def on_done(self, txt):
		makeFiles(txt)

	def run(self, edit, panel_input=None, **kwargs):
		self.edit = edit
		self.window = self.view.window()
		panel = self.view.window().show_input_panel (
			self.input_message,
			self.default_input,
			self.on_done,              
			self.on_change,            
			self.undo)                       

