from . node import Node, Path


class Temporary:

	@staticmethod
	def path():
		pass


class Directory(Node):

	def __init__(self, path, temporary=False):

		if temporary:
			path = Temporary.path() / path

		super().__init__(path)


	def exists(self):
		if super().exists():
			if self.type(Node.TYPE.DIRECTORY):
				return True
		return False

	def create(self):
		try:
			self.path.mkdir(exist_ok=True)
		except:
			print("Error: Directory.create")


	def __enter__(self):
		pass

	def __exit__(self):
		pass


	@staticmethod
	def HOME():
		return Path.home()