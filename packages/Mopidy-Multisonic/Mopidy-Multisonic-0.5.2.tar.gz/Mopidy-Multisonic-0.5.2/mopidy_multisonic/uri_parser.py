import re

root_uri = "multisonic"

#def is_global(uri):
#    return re.search(r'^:\*:', uri)

def is_tracks(uri):
    return re.search(r':tracks$', uri)

def is_track(uri):
    return re.search(r':track:(\d)+$', uri)

def build_track(id, provider_name):
    return root_uri + ":" + provider_name + ":track:" + id

def is_albums(uri):
    return re.search(r':albums$', uri)

def is_album(uri):
    return re.search(r':album:(\d)+$', uri)

def is_playlist(uri):
    return re.search(r':playlist:(\d)+$', uri)

def build_album(id, provider_name):
    return root_uri + ":" + provider_name + ":album:" + id

def build_playlist(id, provider_name):
    return root_uri + ":" + provider_name + ":playlist:" + id

def is_artists(uri):
    return re.search(r':artists$', uri)

def build_artists(provider_name):
    return root_uri + ":" + provider_name + ":artists"

def build_albums(provider_name):
    return root_uri + ":" + provider_name + ":albums"

def build_playlists(provider_name):
    return root_uri + ":" + provider_name + ":playlists"

def is_artist(uri):
    return re.search(r':artist:(\d)+$', uri)

def build_artist(id, provider_name):
    return root_uri + ":" + provider_name + ":artist:" + id

def is_playlists(uri):
    return re.search(r':playlists$', uri)

def is_playlist(uri):
    return re.search(r':playlist:(\d)+$', uri)

def is_root_top(uri):
    return re.search("^" + root_uri + ":top$", uri)

def is_top(uri):
    return re.search(root_uri + ":[^\/]+:top$", uri)

def build_top(provider_name=None):
    if not provider_name:
        return "top"
    return root_uri + ":" + provider_name + ":top"

def is_folder(uri):
    return re.search(r':folder:(\d)+', uri)

def get_id(uri):
    match = re.match(r'(.*:)+(\d+)', uri)
    if None == match:
        return None
    return int(match.group(2))

def get_provider_name(uri):
    match = re.match("^" + root_uri + ":([^:]+):(.*)", uri)
    if None == match:
        return None # throw
    return match.group(1)
