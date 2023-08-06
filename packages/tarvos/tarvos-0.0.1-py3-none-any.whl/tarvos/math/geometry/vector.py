import math

class Vector:

	def __init__(self, x, y):
		self.x = x
		self.y = y

	def length(self):
		return math.sqrt((self.x ** 2) + (self.y ** 2))

	def __add__(self, vector):
		return Vector(self.x + vector.x, self.y + vector.y)

	def __sub__(self, vector):
		return Vector(self.x - vector.x, self.y - vector.y)

	def __radd__(self, vector):
		return Vector(self.x + vector.x, self.y + vector.y)

	def __rsub__(self, vector):
		return Vector(self.x - vector.x, self.y - vector.y)

	def __mul__(self, other):

		try:
			# Return cross product if other is a vector
			other.x
			other.y

		except:
			return Vector(self.x * other, self.y * other)

	def __rmul__(self, other):
		# same as __mul__
		pass



	def dotproduct(self, vector):
		pass