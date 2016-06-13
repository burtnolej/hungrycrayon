import sys
import spotipy
import spotipy.util as util
from spotify_util import create_playlist_from_artist_file, get_user_playlists
scope = 'playlist-modify-private'
user='burtnolejusa'

token = util.prompt_for_user_token(user,scope)

if token:
    sp = spotipy.Spotify(auth=token)
    create_playlist_from_artist_file(sp,sys.argv[1],sys.argv[2])
    
    get_user_playlists(sp)
    
else:
    print "ERROR: No Token"