from api.controllers.logging import log_debug, log_info, log_error
from api.services.esdb import EsClient


class Generator(object):

    es_client = EsClient()

    @classmethod
    def get_object(cls):
        result = {}
        cti_objects = cls.es_client.get_docs(index="stix21")
        result["status"] = 'success'
        result["payload"] = cti_objects
        return result

    @classmethod
    def find_object(cls, object_id):
        result = {}
        try:
            cti_object = cls.es_client.get_doc(index="stix21", doc_id=object_id)
            result["status"] = 'success'
            result["payload"] = {
                "data": {
                    "id": object_id,
                    "content": cti_object.get('data')
                }
            }
            return result
        except Exception as e:
            log_error(e)
            result["status"] = 'fail'
            result["payload"] = {
                "message": "Error (E:2) Object not found .."
            }
            return result

    @classmethod
    def post_objects(cls, cti_objects):
        result = {}
        print (cti_objects.dict().get('objects'))
        try:
            entry = cls.es_client.store_docs(index="stix21", data=cti_objects.dict().get('objects'))
            result["status"] = 'success'
            result["payload"] = entry
            return result
        except Exception as e:
            log_error(e)
            result["status"] = 'fail'
            result["payload"] = {
                "message": "Error (E:4) while posting the object .."
            }
            return result

    @classmethod
    def delete_object(cls, object_id):
        result = {}
        res = cls.es_client.delete_doc(index="stix21", doc_id=object_id)
        if res:
            result["status"] = 'success'
            result["payload"] = res
            return result
        else:
            result["status"] = 'fail'
            result["payload"] = {
                "message": "Error (E:5) Object not found .."
            }
            return result
