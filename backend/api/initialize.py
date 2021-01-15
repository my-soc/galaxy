import json
from api.services.esdb import EsClient

from api.controllers.logging import log_info, log_error

SETTINGS = json.load(open('config/settings.json'))


class BackInit(object):

    es_client = EsClient()

    @classmethod
    def is_es_alive(cls):
        log_info("Checking if ElasticSearch is Up!")
        status = cls.es_client.is_alive()
        if status:
            log_info("ElasticSearch is Up!")
        else:
            log_error("ElasticSearch is Down!")
        return status

    @classmethod
    def es_prep(cls):
        log_info("Creating Wave Elasticsearch Indices")
        status = cls.es_client.es_prep()
        if status.get('index') or status.get('error')['index']:
            log_info("Wave Elasticsearch Indices Created")
        else:
            log_error("Failed to create Elasticsearch Indices")
        return status

    @classmethod
    def ping_services(cls):
        es_pong = cls.is_es_alive()
        return es_pong

    @classmethod
    def services_prep(cls):
        cls.es_prep()
