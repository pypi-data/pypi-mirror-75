from holger.elasticsearch.client import ElasticSearchClient
from .config import CURRENT_TIME_ZONE
from holger.command import Command
import uuid
import datetime


class ElasticSearchCommand(Command):
    def __init__(self, response, status_code, index, doc, params=None, headers=None):
        super(ElasticSearchCommand, self).__init__()
        if headers is None:
            headers = {}
        if params is None:
            params = {}
        self._response = response
        self._status_code = status_code
        self._index = index
        self._doc = doc
        self._params = params
        self._headers = headers

    def execute(self):
        response = self._response
        metadata = response.get('metadata')
        transaction = metadata.pop('transaction', {})
        created_at = datetime.datetime.now(tz=CURRENT_TIME_ZONE)
        index = self._index
        doc = self._doc
        params = self._params
        headers = self._headers
        client = ElasticSearchClient.get_client()
        elastic_id = metadata.get('id', F"{uuid.uuid4()}-{created_at.timestamp()}")
        client.index(
            index=index,
            body={
                **response,
                'transaction': transaction,
                'created_at': created_at
            },
            doc_type=doc,
            id=elastic_id,
            params=params,
            headers=headers
        )
        return {'elastic_id': elastic_id}
