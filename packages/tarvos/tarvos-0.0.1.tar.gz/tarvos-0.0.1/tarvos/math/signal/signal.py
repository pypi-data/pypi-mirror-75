'''

domain:
	List of Domain() objects specifying the
	invervals for which signal is defined

 -- Sampling a signal outside its domain
	raises ValueError


Signal[parameters]:
	Return a sample for signal


Signal + Signal
Signal - Signal
Signal * Signal
Signal / Signal
Signal ** Signal



'''


class Signal:

	def __init__(self, domain, ):
		pass

	def __getitem__(self, parameters):
		raise NotImplementedError

	def __add__(self, signal):

		def fn():
			pass

		return Signal([], fn)

	def __radd__(self, signal):
		raise NotImplementedError

	def __mul__(self, signal):
		raise NotImplementedError

	def __rmul__(self, signal):
		raise NotImplementedError

	def __truediv__(self, signal):
		raise NotImplementedError

	def __rtruediv__(self, signal):
		raise NotImplementedError

	def __pow__(self, signal):
		raise NotImplementedError

	def __rpow__(self, signal):
		raise NotImplementedError