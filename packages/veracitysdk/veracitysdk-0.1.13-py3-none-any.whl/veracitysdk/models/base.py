class Item():
	def __init__(self, client, data=None, parent=None):
		self.client = client
		self.raw = data
		self.data = self.process_input(data)
		self.parent = parent

	def process_input(self):
		raise NotImplementedError()

	def _get_pk(self):
		return self.data.get("pk")

	def __repr__(self):
		return "<{} {}>".format(type(self).__name__, self._get_pk())


class Resource():
	def __init__(self, client, parent=None):
		self.client = client
		self.parent = parent
