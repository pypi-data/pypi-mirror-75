from ... file.YAML import YAML
from ... path import Path

# @TODO:
#
# Apparently this is not the perfect way
# to get the path to schema.yml
#
# The inspect module might be a better
# way forward 
PATH = __file__
NAME = 'schema.yml'


class Schema(YAML):

	def __init__(self):
		path = Path(PATH).with_name(NAME)
		super().__init__(path)
		self.open()
		self.data = self.read()

	def __getitem__(self, *args, **kwargs):
		return self.data.__getitem__(*args, **kwargs)

	def __setitem__(self, *args, **kwargs):
		return self.data.__setitem__(*args, **kwargs)