import sys
import spotipy
import spotipy.util as util
from spotify_util import get_playlist_tracks
scope = 'playlist-modify-private'
user='1165431378'

token = util.prompt_for_user_token(user,scope)

if token:
    sp = spotipy.Spotify(auth=token)
    print get_playlist_tracks(sp,user,sys.argv[1])
    
else:
    print "ERROR: No Token"