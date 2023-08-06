def passthru_return(resp):
	if resp.ok:
		return resp.data, None
	else:
		return None, resp


def boolean_return(resp):
	if resp.ok:
		return True, None
	else:
		return False, resp


class AbstractResponse():
	def as_exception(self):
		return Exception(self.data)


class LocalResponse(AbstractResponse):
	def __init__(self, data, ok=True):
		self.ok = ok
		self.resp = None
		self.data = data


class RawResponse(AbstractResponse):
	def __init__(self, resp):
		self.ok = False
		self.resp = resp
		self.data = resp.text
		if resp.status_code == 200:
			self.ok = True


class JSONResponse(AbstractResponse):
	def __init__(self, resp):
		self.ok = False
		self.resp = resp
		self.data = None
		if resp.status_code == 200:
			data = resp.json()
			if data.get("success"):
				self.ok = True
				self.data = data.get("response")
			else:
				self.data = data.get("error")
		else:
			self.data = resp.content

	def __repr__(self):
		return "<Response {}>".format(self.resp.status_code)


class CacheJSONResponse(AbstractResponse):
	def __init__(self, data):
		self.ok = True
		self.data = data
		self.resp = None
