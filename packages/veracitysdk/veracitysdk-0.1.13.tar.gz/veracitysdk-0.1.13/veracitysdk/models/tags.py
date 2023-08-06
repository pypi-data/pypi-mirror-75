from .articles import BareArticle
from .domains import BareDomain
from .base import (
	Item,
	Resource,
)
from ..responses import (
	boolean_return,
	passthru_return,
)


datatype_to_itemcls = {
	"domain": BareDomain,
	"article": BareArticle,
}

class Tag(Item):
	def process_input(self, data):
		return data

	def get(self, obj):
		return self.get_by_pk(obj.data["pk"])

	def update(self, description):
		params = {
			"namespace": self.data["namespace"],
		}
		data = {
			"description": description,
		}
		resp = self.client.perform_post("api/v1/tag/update/", params=params, data=data)
		if resp.ok:
			return Tag(self.client, resp.data), None
		else:
			return None, resp

	def get_by_pk(self, pk):
		params = {
			"namespace": self.data["public_namespace"],
			"source": pk,
		}
		resp = self.client.perform_get("api/v1/tag/get/", params=params)
		return passthru_return(resp)

	def set(self, obj, value=None, values=None):
		return self.set_by_pk(obj.data["pk"], value, values)

	def set_by_pk(self, pk, value=None, values=None):
		params = {
			"namespace": self.data["namespace"],
			"source": pk,
		}
		if values is not None:
			data = {
				"values": values,
			}
		else:
			data = {
				"value": value,
			}
		resp = self.client.perform_post("api/v1/tag/set/", params=params, data=data)
		return boolean_return(resp)

	def _get_pk(self):
		# return self.data.get("public_namespace", self.data["namespace"])
		namespace = self.data.get("public_namespace")
		if not namespace:
			namespace = self.data.get("namespace")
		return namespace


	def search_by_value(self, value, limit=100, page=1):
		namespace = self._get_pk()
		params = {
			"namespace": namespace,
			"value": value,
			"limit": limit,
			"page": page,
		}
		resp = self.client.perform_get("api/v1/tag/tagged/", params=params)
		cls = datatype_to_itemcls.get(self.data["source_type"])
		if resp.ok:
			return [cls(self.client, data) for data in resp.data], None
		else:
			return None, resp


class TagModel:
	Domain = "domain"
	Article = "article"
	Content = "content"


class TagType:
	String = "String"
	Integer = "Integer"
	Boolean = "Boolean"
	Array = "Array"


class Tags(Resource):
	@staticmethod
	def check_types(source_type, datatype):
		if source_type not in {"domain", "article", "content"}:
			raise Exception("unsupported model")
		if datatype not in {"String", "Integer", "Boolean", "Array"}:
			raise Exception("unsupported tagtype")

	def get(self, namespace, fetch=True, **kwargs):
		if fetch == False:
			source_type = kwargs.get("source_type")
			datatype = kwargs.get("datatype")
			try:
				Tags.check_types(source_type, datatype)
			except Exception as e:
				return None, e
			return Tag(self.client, {"namespace": namespace, "datatype": datatype, "source_type": source_type}), None
		params = {"namespace": namespace}
		resp = self.client.perform_get("api/v1/tag/", params=params)
		if resp.ok:
			return Tag(self.client, resp.data), None
		else:
			return None, resp

	def create(self, namespace, model, tagtype, description=None):
		try:
			Tags.check_types(model, tagtype)
		except Exception as e:
			return None, e
		data = {
			"namespace": namespace,
			"model": model,
			"type": tagtype,
			"description": description,
		}
		resp = self.client.perform_post("api/v1/tag/create/", data=data)
		if resp.ok:
			return Tag(self.client, resp.data), None
		else:
			return None, resp
