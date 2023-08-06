from mopidy import models
from .backend import logger
from . import uri_parser
from . import httpclient
from . import cache

def search_any(http_client_config, any_query):
    result = {
        "albums": [],
        "artists": [],
        "tracks": [],
    }

    data = httpclient.get_search(http_client_config, any_query).json()
    data = data["subsonic-response"]
    if 'failed' == data["status"]:
        log_subsonic_error(data["error"])
        return result

    data = data["searchResult3"]
    for artist in data["artist"]:
        result["artists"].append(
            models.Artist(
                uri = uri_parser.build_artist(
                    str(artist["id"]),
                    http_client_config.name
                ),
                name = artist["name"]
            )
        )

    for album in data["album"]:
        artists = [models.Artist(
            uri = uri_parser.build_artist(
                str(album["artistId"]),
                http_client_config.name
            ),
            name = album["artist"],
        )]
        result["albums"].append(
            models.Album(
                uri = uri_parser.build_album(
                    str(album["id"]),
                    http_client_config.name
                ),
                name = album["name"],
                artists = artists
            )
        )

    for song in data["song"]:
        artists = [models.Artist(
            uri = uri_parser.build_artist(
                str(song["artistId"]),
                http_client_config.name
            ),
            name = song["artist"],
        )]
        album = models.Album(
            uri = uri_parser.build_album(
                str(song["albumId"]),
                http_client_config.name
            ),
            name = song["album"],
        )
        result["tracks"].append(
            models.Track(
                uri = uri_parser.build_track(
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
        )

    return result

def search(http_client_configs, query):
    any_query = query.get("any", None)
    if not any_query:
        return None

    all_result = {
        "albums": [],
        "artists": [],
        "tracks": [],
    }
    for http_client_config in http_client_configs:
        result = search_any(http_client_config, any_query)
        all_result["albums"] += result["albums"]
        all_result["artists"] += result["artists"]
        all_result["tracks"] += result["tracks"]

    return models.SearchResult(
        albums = all_result["albums"],
        artists = all_result["artists"],
        tracks = all_result["tracks"],
    )
