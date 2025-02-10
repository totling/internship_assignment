from elasticsearch import Elasticsearch
from doc_storage_service.config import settings


es_client = Elasticsearch(
    ['https://localhost:9200'],
    http_auth=(settings.ELASTIC_USER, settings.ELASTIC_PASSWORD),
    ssl_show_warn=False,
    verify_certs=False
)


def check_elasticsearch_health():
    return es_client.cluster.health(wait_for_status='yellow')
