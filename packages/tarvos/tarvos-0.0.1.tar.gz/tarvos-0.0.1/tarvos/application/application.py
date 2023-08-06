from . launcher import Launcher
from . console import Console


class Author:

	def __init__(self, name, email, website):
		pass


class Application:

	class Metadata:

		def __init__(self, name, version, author):
			self.name = name
			self.version = version
			self.author = author


	def __init__(self, metadata):
		self.metadata = metadata

	def version(self):
		pass

	def help(self):
		pass

	def __call__(self):
		pass