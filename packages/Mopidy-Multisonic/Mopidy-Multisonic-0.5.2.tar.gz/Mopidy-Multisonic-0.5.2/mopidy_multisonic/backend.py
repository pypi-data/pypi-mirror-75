import logging
import pykka
import re
from mopidy import backend

logger = logging.getLogger(__name__)

from . import library
from . import playback
from . import httpclient
from . import uri_parser

def parse_raw_options(raw_options):
    if not raw_options:
        return {}

    options = {}
    for raw_option in raw_options.split("&"):
        key, value = raw_option.split("=")
        options[key] = value

    return options

def load_http_client_config(provider):
    match = re.match(r'^([^:]+):(?: )?([^:]+)://([^:]+):([^@]+)@([^?]+)(\?(.+))?', provider)

    name=match.group(1)
    protocol=match.group(2)
    username=match.group(3)
    password=match.group(4)
    url=match.group(5)
    raw_options=match.group(7)

    options = parse_raw_options(raw_options)

    return httpclient.HttpClientConfig(
        name=name,
        url=protocol + "://" + url,
        username=username,
        password=password,
        max_bit_rate=options.get("max_bit_rate"),
        format=options.get("format")
    )

def load_http_client_configs(config):
    return list(map(
        lambda provider: load_http_client_config(provider),
        config["providers"]
    ))

class MultisonicBackend(pykka.ThreadingActor, backend.Backend):
    def __init__(self, config, audio):
        super(MultisonicBackend, self).__init__()
        self.config = config["multisonic"]
        self.audio = audio
        self.http_client_configs = load_http_client_configs(self.config)

        self.library = library.Library(self)
        self.playback = playback.Playback(audio, self)
        self.uri_schemes = [uri_parser.root_uri]
