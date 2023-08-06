import json

from stackifyapm.conf import setup_stackifyapm_logging
from stackifyapm.transport.base import BaseTransport


class DefaultTransport(BaseTransport):
    """
    Default Transport handles logging of transaction data into a log file
    """
    def __init__(self, client):
        self._client = client
        self.logging = setup_stackifyapm_logging(self._client)

    def send_all(self):
        # nothing to do in here since we do log transaction immediately once done
        pass

    def log_transaction(self, transaction):
        # log transaction immediately
        config = self._client and self._client.config or None
        self.logging and self.logging.debug(json.dumps(transaction.to_dict(config=config)))
