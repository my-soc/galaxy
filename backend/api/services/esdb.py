import time
import json
from elasticsearch import Elasticsearch, helpers
from controllers.logging import log_debug, log_info, log_error


class EsClient(Elasticsearch):

    # Class Attributes
    default_settings = json.load(open('config/settings.json'))
    es_host = default_settings.get('services')['elasticsearch']['host']
    connection = Elasticsearch(es_host)


    # Constructor
    def __init__(self, host=es_host):
        super().__init__(hosts=[host])

    # Methods
    def is_alive(self):
        return self.connection.ping()

    def es_prep(self):
        try:
            return self.connection.indices.create(
                index="stix21",
                body={
                    'mappings': {},
                    'settings': {},
                },
                ignore=400
            )

        except Exception as error:
            log_error(error.__class__.__name__)
            return None

    def get_docs(self, index: str):
        try:
            res = self.connection.search(index=index, size=10, sort='_id')
            results = []
            for result in res['hits']['hits']:
                response = {}
                response.update(result['_source'])
                response.update({
                    'id': result['_id']
                })
                results.append(response)
            return {
                "data": results,
                "total": res['hits']['total']['value'],
            }
        except Exception as e:
            log_error(e)
            raise

    def get_doc(self, index: str, doc_id: str):
        try:
            res = self.connection.get(index=index, id=doc_id)
            return {
                "data": res.get('_source'),
            }
        except Exception as e:
            log_error(e)
            raise

    def store_doc(self, index: str, data: object,  doc_id=int(round(time.time() * 1000))):
        try:
            res = self.connection.index(
                index=index,
                id=doc_id,
                body=data,
                refresh='wait_for'
            )
            return {
                "index": res['_index'],
                "id": res['_id'],
                "result": res['result']
            }
        except Exception as e:
            log_error(e)
            raise

    def store_docs(self, index: str, data: list):
        try:
            def yield_bulk_data(bulk_data):
                for doc in bulk_data:
                    yield {
                        "_index": index,
                        "_id": doc['id'],
                        "_source": doc
                    }
            res = helpers.bulk(
                self,
                yield_bulk_data(data)
            )
            return {
                "result": res
            }
        except Exception as e:
            log_error(e)
            raise

    def delete_doc(self, index: str, doc_id: str):
        try:
            res = self.connection.delete(index=index, id=doc_id)
            return {
                "index": res['_index'],
                "id": res['_id'],
                "result": res['result']
            }
        except Exception as e:
            log_error(e)
            raise

    def delete_doc_by_query(self, index: str, query: dict):
        try:
            res = self.connection.delete_by_query(index=index, body=query)
            return {
                "index": index,
                "result": res
            }
        except Exception as e:
            log_error(e)
            raise

    def update_doc(self, index: str, data: object,  doc_id: str):
        try:
            res = self.connection.update(
                index=index,
                id=doc_id,
                body={
                    "doc": data
                },
                refresh='wait_for'
            )
            return {
                "index": res['_index'],
                "id": res['_id'],
                "result": res
            }
        except Exception as e:
            log_error(e)
            raise
