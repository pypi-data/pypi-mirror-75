from . path import Path


class Node:

	class TYPE:
		DIRECTORY = Path.is_dir
		FILE = Path.is_file


	def __init__(self, path):
		self.path = Path(path)

	def exists(self):
		return self.path.exists()

	def type(self, check):
		return check(self.path)

	def name(self):
		return self.path.name

	def parent(self):
		return self.path.parent