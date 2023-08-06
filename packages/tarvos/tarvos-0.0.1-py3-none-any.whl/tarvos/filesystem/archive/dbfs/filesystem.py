from . schema import Schema, Path
import sqlite3

from . node import Node
from . file import File
from . directory import Directory


class Filesystem:

	__instance__ = None


	TYPES = (Node, File, Directory)


	@staticmethod
	def setup():
		for t in Filesystem.TYPES:
			t.filesystem = Filesystem.__instance__


	@staticmethod
	def instance():
		if Filesystem.__instance__ is None:
			Filesystem.__instance__ = Filesystem()

		Filesystem.schema = Schema()
		Filesystem.setup()

		return Filesystem.__instance__


	def __init__(self):
		self.ready = False


	def open(self, path):
		# Raise runtime error if
		# open is called twice
		# on the same instance
		if self.ready:
			raise RuntimeError

		self.path = Path(path)
		
		try:
			self.connection = sqlite3.connect(self.path)
		except:
			# @TODO: Handle exceptions
			print("Database open failed")

		self.ready = True


	def close(self, commit=True):

		if commit:
			try:
				self.connection.commit()

			except:
				# @TODO: Handle exceptions
				print("Database commit failed")

		try:
			self.connection.close()
			self.ready = False

		except:
			# @TODO: Handle exceptions
			# @TODO: Issue warning if connection
			#        attribute is not available
			print("Database close failed")


	def cursor(self):
		return self.connection.cursor()


	def initialize(self):
		cursor = self.cursor()
		cursor.execute(Filesystem.schema['node']['create'])
		cursor.execute(Filesystem.schema['file']['create'])
		cursor.execute(Filesystem.schema['directory']['create'])
		cursor.close()


	def __lshift__(self, item):
		# insert item into filesystem
		raise NotImplementedError

	def __rshift__(self, item):
		# fetch item from the database
		raise NotImplementedError

	def __delitem__(self, item):
		# delete item from the database
		raise NotImplementedError


'''
class Filesystem:

	def insert(self, item):
		params = item.insert(self.database.schema)
		cursor = self.database.cursor()
		cursor.execute(*params)
'''