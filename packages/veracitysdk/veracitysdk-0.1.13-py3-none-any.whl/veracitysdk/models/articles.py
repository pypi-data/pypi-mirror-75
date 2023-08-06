from .base import (
	Item,
	Resource,
)


class ArticleContent(Item):
	def process_input(self, data):
		return data

	def get_text(self):
		resp = self.client.get_text(self)
		if resp.ok:
			return resp, None
		else:
			return None, resp

	def get_raw(self):
		resp = self.client.get_raw(self)
		if resp.ok:
			return resp, None
		else:
			return None, resp


class ArticleContents(Resource):
	def get_latest(self):
		pk = self.parent.data.get("pk")
		params = {"pk": int(pk)}
		resp = self.client.perform_get("api/v1/article/latest_crawl/", params=params)
		if resp.ok:
			return ArticleContent(self.client, resp.data, self.parent), None
		else:
			return None, resp


class Article(Item):
	def process_input(self, data):
		self.contents = ArticleContents(self.client, self)
		return data


class BareArticle(Article):
	def resolve(self):
		articles = Articles(self.client)
		return articles.get(self.data["pk"])


class ArticleCollections(Resource):
	def get(self, namespace):
		params = {"namespace": namespace}
		resp = self.client.perform_get("api/v1/article/collection/", params=params)
		if resp.ok:
			return [Article(self.client, data) for data in resp.data], None
		else:
			return None, resp


class SearchObject(Item):
	def process_input(self, data):
		self.search_id = data
		return data

	def get_page(self, page=1, limit=50, debug=False):
		params = {
			"id": self.search_id,
			"limit": limit,
			"page": page,
		}
		resp = self.client.perform_get("api/v1/fts/result/", params=params)
		if resp.ok:
			return [BareArticle(self.client, data) for data in resp.data], None
		else:
			return None, resp


class Articles(Resource):
	def __init__(self, client, parent=None):
		super().__init__(client, parent)
		self.collections = ArticleCollections(self.client, self)

	def get(self, pk, fetch=True):
		params = {"pk": pk}
		if fetch == False:
			return Article(self.client, params), None
		resp = self.client.perform_get("api/v1/article/info/", params=params)
		if resp.ok:
			return Article(self.client, resp.data), None
		else:
			return None, resp

	def fulltext_search(self, query, domains=None, collection=None, start_date=None, end_date=None, limit=50, page=1, debug=False):
		params = {
			"q": query,
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
		resp = self.client.perform_get("api/v1/fts/", params=params)
		if resp.ok:
			return SearchObject(self.client, resp.data), None
		else:
			return None, resp
