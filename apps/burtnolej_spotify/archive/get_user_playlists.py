import sys
import spotipy
import spotipy.util as util
from spotify_util import show_user_playlists
scope = 'playlist-modify-private'
user=sys.argv[1]

token = util.prompt_for_user_token(user,scope)

if token:
    sp = spotipy.Spotify(auth=token)
    print show_user_playlists(sp)
    
else:
    print "ERROR: No Token"