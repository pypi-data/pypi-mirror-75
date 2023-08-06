class Node:

	KEY = 'node'

	@staticmethod
	def initialize(self):
		pass

	def __init__(self, name=None, parent=None):
		self.id = None
		self.name = name
		self.parent = parent


	def get(self):
		schema = self.filesystem.schema

		if self.id is None:
			query = schema[self.KEY]['search']['unique']
			values = (self.parent, self.name)
		
		else:
			query = schema[self.KEY]['get']
			values = (self.id, )

		cursor = self.filesystem.cursor()
		cursor.execute(query, values)

		result = cursor.fetchone()
		self.id, self.parent, self.name = result

		cursor.close()


	def insert(self):
		schema = self.filesystem.schema

		query = schema[self.KEY]['insert']
		values = (self.parent, self.name)

		cursor = self.filesystem.cursor()
		cursor.execute(query, values)
		cursor.close()