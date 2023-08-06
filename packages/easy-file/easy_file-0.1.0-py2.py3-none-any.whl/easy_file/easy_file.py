import json
import yaml
try:
	from yaml import CLoader as YLoader, CDumper as YDumper
except ImportError:
	from yaml import Loader as YLoader, Dumper as YDumper


class TextFile:
	def __init__(self, file_path):
		self.file_path = file_path
		
	def load(self):
		with open(self.file_path, encoding='utf8') as f:
			text = f.read()
		return text
		
	def save(self, text):
		with open(self.file_path, 'w', encoding='utf8') as f:
			f.write(text)

class JSONFile:
	def __init__(self, file_path, indent=4, ensure_ascii=False):
		self.file_path = file_path
		self.indent = indent
		self.ensure_ascii = ensure_ascii
		
	def load(self):
		with open(self.file_path, encoding='utf8') as f:
			data = json.load(f)
		return data
		
	def save(self, data):
		with open(self.file_path, 'w', encoding='utf8') as f:
			json.dump(data, f, indent=self.indent, ensure_ascii=self.ensure_ascii)

			
class YAMLFile:
	def __init__(self, file_path, indent=4):
		self.file_path = file_path
		self.indent = indent
		
	def load(self):
		with open(self.file_path, encoding='utf8') as f:
			data = yaml.load(f.read(), Loader=YLoader)
		return data
		
	def save(self, data):
		with open(self.file_path, 'w', encoding='utf8') as f:
			yaml.dump(data, stream=f, Dumper=YDumper)

			

if __name__	== '__main__':
	pass
