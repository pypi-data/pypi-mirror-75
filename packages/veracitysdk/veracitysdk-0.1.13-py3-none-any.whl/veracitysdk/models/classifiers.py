from .base import (
	Item,
	Resource,
)
from .articles import BareArticle


class ClassifierHit(Item):
	def process_input(self, data):
		self.article = BareArticle(self.client, {"pk": data["article"]})
		return data

	def __repr__(self):
		return "<ClassifierHit {}>".format(self.data["article"])


class Classifier(Item):
	def process_input(self, data):
		return data

	def list_hits(self, domains=None, collection=None, start_date=None, end_date=None, limit=50, page=1):
		params = {
			"name": self.data["name"],
			"limit": limit,
			"page": page,
		}
		if domains and collection:
			raise Exception("Cannot define both domains and collections")
		if domains:
			params["domains"] = domains
		if collection:
			params["collection"] = collection
		if start_date and end_date:
			params["start_date"] = start_date.isoformat()
			params["end_date"] = end_date.isoformat()
		resp = self.client.perform_get("api/v1/classifier/hits/", params=params)
		if resp.ok:
			return [ClassifierHit(self.client, data) for data in resp.data], None
		else:
			return None, resp

	def __repr__(self):
		return "<Classifier {}>".format(self.data["name"])


class Classifiers(Resource):
	def get(self, name, fetch=True, **kwargs):
		if fetch == False:
			source_type = kwargs.get("source_type")
			return Classifier(self.client, {"name": name}), None
		params = {"name": name}
		resp = self.client.perform_get("api/v1/classifier/info/", params=params)
		if resp.ok:
			return Classifier(self.client, resp.data), None
		else:
			return None, resp
