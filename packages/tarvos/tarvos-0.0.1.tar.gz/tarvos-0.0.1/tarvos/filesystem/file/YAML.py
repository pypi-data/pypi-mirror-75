from . file import File, Path
import yaml


class YAML(File):

	class LOAD:
		SAFE = yaml.CSafeLoader
		UNSAFE = yaml.CLoader

	class DUMP:
		SAFE = yaml.CSafeDumper
		UNSAFE = yaml.CDumper

	def read(self, safe=True):
		document = super().read()
		loader = YAML.LOAD.SAFE if safe else LOAD.UNSAFE
		self.data = yaml.load(document, Loader=loader)
		return self.data

	def write(self, data=None, safe=False):
		data = self.data if data is None else data
		dumper = YAML.DUMP.SAFE if safe else DUMP.UNSAFE
		return yaml.dump(data, self.file, Dumper=dumper, default_flow_style=False)

	def __getitem__(self, *args, **kwargs):
		return self.data.__getitem__(*args, **kwargs)

	def __setitem__(self, *args, **kwargs):
		return self.data.__setitem__(*args, **kwargs)