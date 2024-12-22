from tkinter import *
from tkinter import filedialog as fd
#from posixpath import join, normpath, splitdrive, split, splitext
#from pathlib import Path

class GUI(Tk):
	
	COMMANDS = {
		"rename": lambda gui, params: gui._rename_command(params.get("index"), params.get("new_name")),
		"close": lambda gui, params: gui._close_command(),
		"add": lambda gui, params: gui._add_file_command(params.get("index"), params.get("old_name"), params.get("new_name"))
	}

	def __init__(self, fn_receiver):
		FILEMENU = [
    		{"label": "Open", "command": self._open_click},
			{"label": "Save", "command": self._save_click},
			{"label": "Close", "command": self._close_click},
			{},
			{"label": "Exit", "command": self._exit_click},
		]
  
		EDITMENU = [
      		{"label": "Replace", "command": self._replace_click},
			{"label": "Add Preffix", "command": self._add_prefix_click},
			{"label": "Add Suffix", "command": self._add_suffix_click},
   		]
  
		super().__init__()
		self._fn_receiver = fn_receiver
		self.replace_dialog = GUIReplaceDialog(self)
		menubar = Menu(self)
		filemenu = GUIMenuExpansion(self, FILEMENU, tearoff=0)
		editmenu = GUIMenuExpansion(self, EDITMENU, tearoff=0)
		menubar.add_cascade(label="File", menu=filemenu)
		menubar.add_cascade(label="Edit", menu=editmenu)
		self.config(menu=menubar)
		Grid.columnconfigure(self, 0, weight=1)
		self._frame = Frame(self)
		lb_select = Label(self._frame, text="Sel")
		lb_select.grid(column=0, row=0, sticky=NSEW)
		lb_old_name = Label(self._frame, text="Nome Antigo")
		lb_old_name.grid(column=1, row=0, sticky=NSEW)
		lb_new_name = Label(self._frame, text="Nome Novo")
		lb_new_name.grid(column=2, row=0, sticky=NSEW)
		Grid.columnconfigure(self._frame, 0, weight=1)
		Grid.columnconfigure(self._frame, 1, weight=1)
		self._frame.grid(column=0, row=0, sticky=NSEW)
		self._var_new_names = []
  
	def send(self, params):
		self._fn_receiver(params)
		
	def receiver(self, params):
		GUI.COMMANDS.get(params.get("command"))(self, params)

	def _add_file_command(self, index, old_name, new_name):
		var_check = IntVar()
		var_old = StringVar(self, old_name)
		var_new = StringVar(self, old_name)
		sel_check = Checkbutton(self._frame, variable=var_check)
		sel_check.grid(column=0, row=index)
		et_old_name = Entry(self._frame, textvariable=var_old)
		et_old_name.grid(column=1, row=index, sticky=NSEW)
		et_old_name.configure(state=DISABLED)
		et_new_name = Entry(self._frame, textvariable=var_new)
		et_new_name.grid(column=2, row=index, sticky=NSEW)
		self._var_new_names.append(var_new)
  
	def _rename_command(self, index, new_name):
		self._var_new_names[index].set(new_name)
	
	def _close_command(self):
		for widget in self._frame.winfo_children()[3:]:
			widget.destroy()
		self._var_new_names.clear()

	def _open_click(self):
		filepaths = fd.askopenfilenames()
		if filepaths != "":
			for filepath in filepaths:
				self.send({"command": "new", "filepath": filepath})

	def _save_click(self): 
		for index, var_name_name in enumerate(self._var_new_names):
			self.send({"command": "rename", "index": index, "new_name": var_name_name.get()})
		self.send({"command": "save"})
		self.send({"command": "close"})

	def _exit_click(self):   
		self.send({"command": "exit"})

	def _close_click(self):
		self.send({"command": "close"})
  
	def _replace_click(self):
		pass
				
	def _add_prefix_click(self):
		pass

	def _add_suffix_click(self):
		pass

class GUIReplaceDialog(Toplevel):

	def __init__(self, main, *args, **kwargs):
		super().__init__(main, *args, **kwargs)
		self.transient(main)
		lb_find = Label(self, text="Find")
		lb_find.grid()

		lb_replace_with = Label(self, text="Replace With")
		lb_replace_with.grid(row=1)

		et_find = Entry(self)
		et_find.grid(column=1)

		et_replace_with = Entry(self)
		et_replace_with.grid(column=1, row=1)
				
	def ok(self):
		self.destroy()

	
class GUIMenuExpansion(Menu):
	
	def __init__(self, root, commands, *args, **kwargs):
		super().__init__(root, *args, **kwargs)
		for command in commands:
			if command.get("label"):
				self.add_command(label=command.get("label"), command=command.get("command"))
			else:
				self.add_separator()
  
