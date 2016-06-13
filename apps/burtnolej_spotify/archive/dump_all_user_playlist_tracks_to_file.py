import sys
import spotipy
import spotipy.util as util
from spotify_util import get_user_playlists, get_playlist_tracks
scope = 'playlist-modify-private'
user='1165431378'

token = util.prompt_for_user_token(user,scope)

if token:
    sp = spotipy.Spotify(auth=token)
    
    playlists = get_user_playlists(sp,user)
    
    for playlist in playlists:
        print get_playlist_tracks(sp,user,playlist)
    
else:
    print "ERROR: No Token"