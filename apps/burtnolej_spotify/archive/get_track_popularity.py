import sys
import spotipy
import spotipy.util as util
from spotify_util import get_popularity
scope = 'playlist-modify-private'
user='burtnolejusa'

token = util.prompt_for_user_token(user,scope)

if token:
    sp = spotipy.Spotify(auth=token)
    print get_popularity(sp)
    
else:
    print "ERROR: No Token"