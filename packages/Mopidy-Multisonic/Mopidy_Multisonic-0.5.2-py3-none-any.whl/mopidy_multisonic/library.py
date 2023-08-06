from mopidy import backend
from .backend import logger
from . import browser
from . import lookup
from . import searcher

class Library(backend.LibraryProvider):
    def __init__(self, backend):
        self.backend = backend
        self.root_directory = browser.top_root_dir

    def get_http_client_configs(self):
        return self.backend.http_client_configs

    def browse(self, uri):
        logger.debug("Browse " + str(uri))
        return browser.browse(self.get_http_client_configs(), uri)

    def get_distinct(self, field, query=None):
        logger.debug("Get distinct")
        return set()

    def get_images(self, uris):
        logger.debug("Get images " + str(uris))
        return {}

    def lookup(self, uri):
        logger.debug("Lookup " + str(uri))
        return lookup.lookup(self.get_http_client_configs(), uri)

    def refresh(self, uri=None):
        logger.debug("Refresh " + str(uri))

    def search(self, query=None, uris=None, exact=False):
        logger.debug("Search")
        return searcher.search(self.get_http_client_configs(), query)
