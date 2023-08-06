from .. node import Node, Path


class File(Node):

	def open(self, mode='r'):
		self.file = open(self.path, mode)

	def close(self):
		self.file.close()

	def read(self, *args, **kwargs):
		return self.file.read(*args, **kwargs)

	def write(self):
		return self.file.write(*args, **kwargs)

	def merge(self):
		raise NotImplementedError


class Temporary(File):
	pass