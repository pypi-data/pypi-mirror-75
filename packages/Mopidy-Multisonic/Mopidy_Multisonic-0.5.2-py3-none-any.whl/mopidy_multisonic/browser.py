from mopidy import models
from .backend import logger
from . import uri_parser
from . import httpclient
from . import cache
from . import lookup

top_root_dir = models.Ref.directory(
    name="Multisonic",
    uri=uri_parser.root_uri + ":" + uri_parser.build_top()
)

def log_subsonic_error(error):
    logger.error("Failed to browse : " + str(error["code"]) + " : " + error["message"])

def is_http_client_config_uri(http_client_config, uri):
    provider_name = uri_parser.get_provider_name(uri)
    return http_client_config.name == provider_name

def get_http_client_config(http_client_configs, uri):
    for http_client_config in http_client_configs:
        if is_http_client_config_uri(http_client_config, uri):
            return http_client_config

def browse_root_top(http_client_configs):
    return list(map(
        lambda http_client_config: models.Ref.directory(
            name=http_client_config.name,
            uri=uri_parser.build_top(http_client_config.name)
        ),
        http_client_configs
    ))

def browse_top(http_client_config):
    return [
        models.Ref.directory(
            name="Artists",
            uri=uri_parser.build_artists(http_client_config.name)
        ),
        models.Ref.directory(
            name="Albums",
            uri=uri_parser.build_albums(http_client_config.name)
        ),
        models.Ref.directory(
            name="Playlists",
            uri=uri_parser.build_playlists(http_client_config.name)
        ),
    ]

def browse_artists(http_client_config, uri):
    artists = []

    data = httpclient.get_artists(http_client_config).json()
    data = data["subsonic-response"]
    if 'failed' == data["status"]:
        log_subsonic_error(data["error"])
        return []

    for index in data["artists"]["index"]:
        for artist in index["artist"]:
            artists.append(
                models.Ref.artist(
                    name=artist["name"],
                    uri=uri_parser.build_artist(
                        str(artist["id"]),
                        http_client_config.name
                    ),
                )
            )
    return artists

def browse_albums(http_client_config, uri):
    albums = []

    data = httpclient.get_albums(http_client_config).json()
    data = data["subsonic-response"]
    if 'failed' == data["status"]:
        log_subsonic_error(data["error"])
        return []

    for album in data["albumList2"]["album"]:
        albums.append(
            models.Ref.album(
                name=album["name"],
                uri=uri_parser.build_album(
                    str(album["id"]),
                    http_client_config.name
                )
            )
        )

    return albums

def browse_playlists(http_client_config, uri):
    playlists = []

    data = httpclient.get_playlists(http_client_config).json()
    data = data["subsonic-response"]
    if 'failed' == data["status"]:
        log_subsonic_error(data["error"])
        return []

    for playlist in data["playlists"]["playlist"]:
        playlists.append(
            models.Ref.playlist(
                name=playlist["name"],
                uri=uri_parser.build_playlist(
                    str(playlist["id"]),
                    http_client_config.name
                )
            )
        )

    return playlists

def browse_artist(http_client_config, uri):
    albums = []
    id = uri_parser.get_id(uri)

    data = httpclient.get_artist(http_client_config, id).json()
    data = data["subsonic-response"]
    if 'failed' == data["status"]:
        log_subsonic_error(data["error"])
        return []

    for album in data["artist"]["album"]:
        albums.append(
            models.Ref.album(
                name=album["name"],
                uri=uri_parser.build_album(
                    str(album["id"]),
                    http_client_config.name
                )
            )
        )

    return albums

def build_track_ref(song, http_client_config):
    return models.Ref.track(
        name=song["title"],
        uri=uri_parser.build_track(
            str(song["id"]),
            http_client_config.name
        )
    )

def browse_album(http_client_config, uri):
    tracks = []
    id = uri_parser.get_id(uri)

    data = httpclient.get_album(http_client_config, id).json()
    data = data["subsonic-response"]
    if 'failed' == data["status"]:
        log_subsonic_error(data["error"])
        return []

    for song in data["album"]["song"]:
        tracks.append(build_track_ref(song, http_client_config))
        track = lookup.build_track_model(song, http_client_config)
        cache.hydrate_model(track.uri, [track])

    return tracks

def browse_playlist(http_client_config, uri):
    tracks = []
    id = uri_parser.get_id(uri)

    data = httpclient.get_playlist(http_client_config, id).json()
    data = data["subsonic-response"]
    if 'failed' == data["status"]:
        log_subsonic_error(data["error"])
        return []

    for song in data["playlist"]["entry"]:
        tracks.append(build_track_ref(song, http_client_config))
        track = lookup.build_track_model(song, http_client_config)
        cache.hydrate_model(track.uri, [track])

    return tracks

def browse(http_client_configs, uri):
    if uri_parser.is_root_top(uri):
        return browse_root_top(http_client_configs)

    http_client_config = get_http_client_config(http_client_configs, uri)

    if uri_parser.is_top(uri):
        return browse_top(http_client_config)
    if uri_parser.is_artists(uri):
        return browse_artists(http_client_config, uri)
    if uri_parser.is_albums(uri):
        return browse_albums(http_client_config, uri)
    if uri_parser.is_playlists(uri):
        return browse_playlists(http_client_config, uri)
    if uri_parser.is_artist(uri):
        return browse_artist(http_client_config, uri)
    if uri_parser.is_album(uri):
        return browse_album(http_client_config, uri)
    if uri_parser.is_playlist(uri):
        return browse_playlist(http_client_config, uri)
