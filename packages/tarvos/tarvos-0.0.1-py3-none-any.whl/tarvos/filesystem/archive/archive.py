from .. file import File, Path


class Archive(File):

	def pack(self, directory):
		raise NotImplementedError

	def unpack(self, directory):
		raise NotImplementedError