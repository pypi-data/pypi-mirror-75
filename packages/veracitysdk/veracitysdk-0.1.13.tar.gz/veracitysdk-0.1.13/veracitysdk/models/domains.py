import requests

from .base import (
	Item,
	Resource,
)


class ScreenshotUrl(Item):
	def process_input(self, data):
		return data

	def get_screenshot(self):
		resp = requests.get(self.data)
		if resp.status_code == 200:
			return resp.content, None
		else:
			return None, Exception(resp.text)


class MetadataType:
	Whois = "whois"
	Adstxt = "adstxt"
	ATSGlobal = "atsglobal"
	BuiltwithFree = "builtwithfree"
	BuiltwithDomain = "builtwithdomain"
	HTTPS = "https"
	Robotstxt = "robotstxt"
	HomepageScreenshot = "homepage_screenshot"
	HeaderBidding = "header_bidding"


class Metadata(Resource):
	def get(self, metadatatype):
		params = {
			"pk": self.parent.data["pk"],
			"metadata": metadatatype,
		}
		resp = self.client.perform_get("api/v1/domain/metadata/", params=params)
		if resp.ok:
			return resp.data, None
		else:
			return None, resp


class Domain(Item):
	def process_input(self, data):
		self.metadata = Metadata(self.client, self)
		return data

	def get_screenshoturl(self):
		pk = self.data.get("pk")
		params = {"pk": pk}
		resp = self.client.perform_get("api/v1/domain/screenshot/", params=params)
		if resp.ok:
			return ScreenshotUrl(self.client, resp.data), None
		else:
			return None, resp


class BareDomain(Domain):
	def resolve(self):
		pk = self.data.get("pk")
		params = {"pk": pk}
		resp = self.client.perform_get("api/v1/domain/info/", params=params)
		if resp.ok:
			return Domain(self.client, resp.data), None
		else:
			return None, resp


class DomainCollections(Resource):
	def get(self, namespace):
		params = {"namespace": namespace}
		resp = self.client.perform_get("api/v1/domain/collection/", params=params)
		if resp.ok:
			return [Domain(self.client, data) for data in resp.data], None
		else:
			return None, resp


class DomainSuggestionStatus(Item):
	def process_input(self, data):
		return data


class DomainSuggestion(Item):
	def process_input(self, data):
		return data

	def get_status(self):
		pk = self.data.get("suggestion")
		params = {"pk": pk}
		resp = self.client.perform_get("api/v1/domain/suggest/status/", params=params)
		if resp.ok:
			return DomainSuggestionStatus(self.client, resp.data), None
		else:
			return None, resp

	def requeue(self):
		pk = self.data.get("suggestion")
		data = {"pk": pk}
		resp = self.client.perform_post("api/v1/domain/suggest/requeue/", data=data)
		if resp.ok:
			return DomainSuggestionStatus(self.client, resp.data), None
		else:
			return None, resp


class Domains(Resource):
	def __init__(self, client, parent=None):
		super().__init__(client, parent)
		self.collections = DomainCollections(self.client, self)

	def get(self, pk, fetch=True):
		params = {"pk": pk}
		if fetch == False:
			return Domain(self.client, params), None
		resp = self.client.perform_get("api/v1/domain/info/", params=params)
		if resp.ok:
			return Domain(self.client, resp.data), None
		else:
			return None, resp

	def search(self, name):
		params = {"q": name}
		resp = self.client.perform_get("api/v1/domain/search/", params=params)
		if resp.ok:
			return [BareDomain(self.client, data) for data in resp.data], None
		else:
			return None, resp

	def suggest(self, url, source):
		data = {
			"url": url,
			"source": source,
		}
		resp = self.client.perform_post("api/v1/domain/suggest/", data=data)
		if resp.ok:
			return DomainSuggestion(self.client, resp.data), None
		else:
			return None, resp
