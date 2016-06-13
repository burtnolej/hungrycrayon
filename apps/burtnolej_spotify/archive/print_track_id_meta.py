import sys
import spotipy
import spotipy.util as util
from spotify_util import print_track_id_meta
scope = 'playlist-modify-private'
user='burtnolejusa'

token = util.prompt_for_user_token(user,scope)

if token:
    sp = spotipy.Spotify(auth=token)
    
    print print_track_id_meta(sp,sys.argv[1])
    
else:
    print "ERROR: No Token"
    
    
    