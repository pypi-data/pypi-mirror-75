from collections import namedtuple
import uuid
import requests
import hashlib

HttpClientConfig = namedtuple(
    'HttpClientConfig',
    [
        'name',
        'url',
        'username',
        'password',
        'max_bit_rate',
        'format',
    ]
)

def get_request(client_config, endpoint, params={}):
    return requests.get(
        client_config.url + endpoint,
        params=build_params(client_config, params)
    )

def build_login_params(client_config):
    salt = build_salt()
    return {
        "u": client_config.username,
        "t": build_token(client_config, salt),
        "s": salt
    }

def build_params(client_config, params):
    login_params = build_login_params(client_config)
    return {**params, **login_params}

def build_salt():
    return uuid.uuid4().hex

def build_token(client_config, salt):
    return hashlib.md5((client_config.password + salt).encode()).hexdigest()


def get_artists(client_config):
    params = {
        "f": "json",
    }
    return get_request(client_config, "/rest/getArtists", params)

def get_playlists(client_config):
    params = {
        "f": "json",
    }
    return get_request(client_config, "/rest/getPlaylists", params)

def get_albums(client_config):
    params = {
        "f": "json",
        "type": "alphabeticalByName",
    }
    return get_request(client_config, "/rest/getAlbumList2", params)


def get_artist(client_config, id):
    params = {
        "id": id,
        "f": "json",
    }
    return get_request(client_config, "/rest/getArtist", params)

def get_album(client_config, id):
    params = {
        "id": id,
        "f": "json",
    }
    return get_request(client_config, "/rest/getAlbum", params)

def get_playlist(client_config, id):
    params = {
        "id": id,
        "f": "json",
    }
    return get_request(client_config, "/rest/getPlaylist", params)

def get_song(client_config, id):
    params = {
        "id": id,
        "f": "json",
    }
    return get_request(client_config, "/rest/getSong", params)

def get_stream(client_config, id):
    params = {
        "id": id,
    }

    if client_config.max_bit_rate:
        params["maxBitRate"] = client_config.max_bit_rate,
    if client_config.format:
        params["format"] = client_config.format,

    return get_request(client_config, "/rest/stream", params)

def get_search(client_config, query):
    params = {
        "query": query,
        "f": "json"
    }
    return get_request(client_config, "/rest/search3", params)

def get_track(client_config, id):
    params = {
        "id": id,
        "f": "json"
    }
    return get_request(client_config, "/rest/getSong", params)
