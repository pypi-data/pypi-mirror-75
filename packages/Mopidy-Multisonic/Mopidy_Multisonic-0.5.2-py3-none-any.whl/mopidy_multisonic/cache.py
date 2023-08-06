from .backend import logger

cache = {}

def fetch_model(uri, default=None):
    return cache.get(uri, default)

def hydrate_model(uri, model, override=False):
    if override or not fetch_model(str(uri)):
        logger.debug("Hydrate model: " + str(uri))
        cache[uri] = model
    return model

