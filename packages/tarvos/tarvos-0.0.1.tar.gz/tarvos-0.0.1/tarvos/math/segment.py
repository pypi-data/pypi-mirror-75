class Segment:

	def __init__(self, start, end):
		self.start = start
		self.end = end

	def overlaps(self, other):
		if other.start >= self.start and other.start <= self.end:
			return True

		if other.end >= self.start and other.end <= self.end:
			return True

		return False