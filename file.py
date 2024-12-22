from pathlib import PurePath
class File:
    
    def __init__(self, filepath):
        print(filepath)
        self._file = PurePath(filepath)
        self._filepath = filepath
        self.new_name = self.old_name
        
    @property
    def old_filepath(self):
        return self._file
        #return self._filepath
    
    @property
    def new_filepath(self):
        return self._file.with_stem(self._new_name)
    
    @property
    def extension(self):
        return self._file.suffix
    
    @property
    def old_name(self):
        return self._file.stem
    
    @property
    def full_old_name(self):
        return self._file.name
    
    @property
    def new_name(self):
        return self._new_name
        
    @new_name.setter
    def new_name(self, value):
        self._new_name = value