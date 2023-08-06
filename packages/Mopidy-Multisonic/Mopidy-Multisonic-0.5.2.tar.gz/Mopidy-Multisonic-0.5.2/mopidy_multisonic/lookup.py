from mopidy import models
from .backend import logger
from . import cache
from . import uri_parser
from . import httpclient
from . import browser

def log_subsonic_error(error):
    logger.error("Failed to lookup: " + str(error["code"]) + " : " + error["message"])

def build_track_model(song, http_client_config):
    artists = [models.Artist(
        name=song["artist"],
        uri=uri_parser.build_artist(
            str(song["artistId"]),
            http_client_config.name
        )
    )]
    album = models.Album(
        uri=uri_parser.build_album(
            str(song["albumId"]),
            http_client_config.name
        ),
        name=song["album"],
        date=str(song["year"]),
        artists=artists
    )

    track = models.Track(
        uri=uri_parser.build_track(
            str(song["id"]),
            http_client_config.name
        ),
        name=song["title"],
        date=str(song["year"]),
        length=song["duration"]*1000,
        disc_no=song["discNumber"],
        track_no=song["track"],
        artists=artists,
        album=album,
    )

    return track

def lookup_track(http_client_config, uri):
    id = uri_parser.get_id(uri)

    data = httpclient.get_track(http_client_config, id).json()
    data = data["subsonic-response"]
    if 'failed' == data["status"]:
        log_subsonic_error(data["error"])
        return []

    song = data["song"]
    track = build_track_model(song, http_client_config)

    return [track]

def lookup_album(http_client_config, uri):
    id = uri_parser.get_id(uri)

    data = httpclient.get_album(http_client_config, id).json()
    data = data["subsonic-response"]
    if 'failed' == data["status"]:
        log_subsonic_error(data["error"])
        return []

    data = data["album"]

    artists = [models.Artist(
        name=data["artist"],
        uri=uri_parser.build_artist(
            str(data["artistId"]),
            http_client_config.name
        )
    )]
    album = models.Album(
        uri=uri_parser.build_album(
            str(data["id"]),
            http_client_config.name
        ),
        name=data["name"],
        date=str(data["year"]),
        artists=artists
    )

    tracks = []
    for song in data["song"]:
        track = models.Track(
            uri=uri_parser.build_track(
                str(song["id"]),
                http_client_config.name
            ),
            name=song["title"],
            date=str(song["year"]),
            length=song["duration"]*1000,
            disc_no=song["discNumber"],
            track_no=song["track"],
            artists=artists,
            album=album,
        )
        tracks.append(track)

    return tracks

def lookup_artist(http_client_config, uri):
    id = uri_parser.get_id(uri)

    data = httpclient.get_artist(http_client_config, id).json()
    data = data["subsonic-response"]
    if 'failed' == data["status"]:
        log_subsonic_error(data["error"])
        return []

    data = data["artist"]

    artists = [models.Artist(
        name=data["name"],
        uri=uri_parser.build_artist(
            str(data["id"]),
            http_client_config.name
        )
    )]

    tracks = []
    for data in data["album"]:
        tracks += lookup_album(
            http_client_config,
            uri_parser.build_album(
                str(data["id"]),
                http_client_config.name
            )
        )

    return tracks

def lookup(http_client_configs, uri):
    http_client_config = browser.get_http_client_config(http_client_configs, uri)

    tracks = cache.fetch_model(uri)
    if tracks:
        return tracks

    if uri_parser.is_track(uri):
        return lookup_track(http_client_config, uri)
    if uri_parser.is_album(uri):
        return lookup_album(http_client_config, uri)
    if uri_parser.is_artist(uri):
        return lookup_artist(http_client_config, uri)

    logger.error("Can't lookup " + uri)
    return []
