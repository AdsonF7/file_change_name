from file import File
from gui import GUI
from os import rename as os_rename
from os import path
class App:
	COMMANDS = {
		"new": lambda app, params: app.add_file(params.get("filepath")),
		"remove": lambda app, params: app.remove_file(params.get("index")),
		"exit": lambda app, params: app.exit(),
		"close": lambda app, params: app.close(),
		"save": lambda app, params: app.save(),
		"rename": lambda app, params: app.rename(params.get("index"), params.get("new_name"))
	}
	
	def __init__(self):
		self._files = []
		self._gui = GUI(self.receiver)
		self._gui.mainloop()
	
	def add_file(self, filepath: str):
		file = File(filepath)
		if len(list(filter(lambda x: x.old_filepath == file.old_filepath, self._files))) == 0:
			self._files.append(file)
			self._gui.receiver({"command": "add", "index": self.count_files, "old_name": file.old_name})
	
	def remove_file(self, index: int):
		self._files.pop(index)
		
	def receiver(self, params):
		App.COMMANDS.get(params.get("command"))(self, params)
	
	def close(self):
		self._files.clear()
		self._gui.receiver({"command": "close"})
	
	def rename(self, index, new_name):
		self._files[index].new_name = new_name

	def exit(self):
		self._gui.destroy()
	
	def save(self):
		for file in filter(lambda x: x.old_filepath != x.new_filepath, self._files):
			try:
				os_rename(file.old_filepath, file.new_filepath)
			except FileExistsError:
				counter = 2
				new_filepath = file.new_filepath.with_name(f"{file.filepath.stem} ({counter})")
				while path.exists(new_filepath):
					counter += 1
					new_filepath = file.new_filepath.with_name(f"{file.filepath.stem} ({counter})")
				os_rename(file.old_filepath, new_filepath)
   
	@property
	def count_files(self):
		return len(self._files)
	
	