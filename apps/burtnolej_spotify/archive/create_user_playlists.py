import sys
import spotipy
import spotipy.util as util
from spotify_util import create_playlist
scope = 'playlist-modify-private'
user='burtnolejusa'

token = util.prompt_for_user_token(user,scope)

if token:
    sp = spotipy.Spotify(auth=token)
    print create_playlist(sp,sys.argv[1])
    
else:
    print "ERROR: No Token"