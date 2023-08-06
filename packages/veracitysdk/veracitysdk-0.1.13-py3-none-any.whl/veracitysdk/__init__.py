"""Veracity api library."""
__version__ = "0.1.13"

import hashlib
import json
import os.path
import requests
import time

from .models.articles import Articles
from .models.articles import ArticleContent, ArticleContents, BareArticle, ArticleCollections, SearchObject
from .models.classifiers import Classifiers
from .models.classifiers import Classifier, ClassifierHit
from .models.domains import Domains
from .models.domains import ScreenshotUrl, MetadataType, Metadata, Domain, BareDomain, DomainCollections
from .models.tags import Tags
from .models.tags import Tag, TagModel, TagType
from .responses import (
	CacheJSONResponse,
	JSONResponse,
	LocalResponse,
	RawResponse,
)


DEFAULT_HOST = "https://dashboard.veracity.ai/"


class Client():
	def __init__(self, key, secret, host=DEFAULT_HOST, resolvers=None, cache=None):
		self._auth = (key, secret)
		self.host = host
		self.domains = Domains(self)
		self.articles = Articles(self)
		self.tags = Tags(self)
		self.classifiers = Classifiers(self)
		if resolvers is None:
			resolvers = {}
		if "raw" not in resolvers:
			resolvers["raw"] = ContentAPIResolver(self, "api/v1/article/raw/")
		if "text" not in resolvers:
			resolvers["text"] = ContentAPIResolver(self, "api/v1/article/text/")
		self.resolvers = resolvers
		self.cache = cache

	def _perform_request(self, method, endpoint, data, params, json=True):
		resp = method(
			self.host + endpoint,
			data = data,
			params = params,
			auth = self._auth,
		)
		if json:
			return JSONResponse(resp)
		else:
			return RawResponse(resp)

	# TODO: test caching
	def perform_get(self, endpoint, data=None, params=None, json=True):
		try_cache = (json == True) and (self.cache is not None)
		if try_cache:
			resp = self.cache.get(endpoint, data, params)
			if resp:
				return resp
		resp = self._perform_request(requests.get, endpoint, data, params, json)
		if try_cache and resp.ok:
			self.cache.set(endpoint, data, params, resp)
		return resp

	def perform_post(self, endpoint, data=None, params=None, json=True):
		return self._perform_request(requests.post, endpoint, data, params, json)

	def get_raw(self, articlecontent):
		return self.resolvers["raw"].get(articlecontent)

	def get_text(self, articlecontent):
		return self.resolvers["text"].get(articlecontent)


def paginated(f, *args, retry_time=None, **kwargs):
	p = 1
	while True:
		items, err = f(*args, **kwargs, page=p)
		if err:
			if err.resp.status_code == 200:
				if err.data == "Invalid page":
					return
			elif err.resp.status_code == 202:
				# result is not ready, try again
				if retry_time is not None:
					print("202 received, retrying in a bit")
					time.sleep(retry_time)
				continue
			raise Exception(err)
		l = len(items)
		if l == 0:
			break
		for item in items:
			yield item
		p = p + 1


class ContentFSResolver():
	def __init__(self, pathname):
		self.pathname = pathname

	def get(self, articlecontent):
		pk = articlecontent.data.get("pk")
		path = os.path.join(self.pathname, pk[0:2], pk[2:4], pk)
		try:
			with open(path, "r") as fh:
				content = fh.read()
		except Exception as e:
			return LocalResponse("error with {}".format(path), ok=False)
		else:
			return LocalResponse(content)


class ContentAPIResolver():
	def __init__(self, client, path):
		self.client = client
		self.path = path

	def get(self, articlecontent):
		params = {
			"pk": str(articlecontent.parent.data.get("pk")),
			"wrap": False,
		}
		resp = self.client.perform_get(self.path, params=params, json=False)
		return resp


class SimpleCache():
	def __init__(self, root, hasher=hashlib.md5):
		self.root = root
		self.hasher = hasher
		if not os.path.isdir(self.root):
			raise Exception("Cache directory does not exist")

	def make_hash(self, url, data, params):
		s = json.dumps([
			url,
			sorted(data.items()) if data else "",
			sorted(params.items()) if params else "",
		])
		h = self.hasher(s.encode("utf-8")).hexdigest()
		return os.path.join(self.root, h)

	def get(self, url, data, params):
		fn = self.make_hash(url, data, params)
		if os.path.exists(fn):
			with open(fn, "r") as fh:
				data = json.load(fh)
				return CacheJSONResponse(data)
		return None

	def set(self, url, data, params, resp):
		fn = self.make_hash(url, data, params)
		if not os.path.exists(fn):
			with open(fn, "w") as fh:
				json.dump(resp.data, fh)
