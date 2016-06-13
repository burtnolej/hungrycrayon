import sys
import spotipy
import spotipy.util as util
from spotify_util import create_playlist_from_artist_file, get_user_playlists
scope = 'playlist-modify-private'
user='burtnolejusa'

token = util.prompt_for_user_token(user,scope)

l = [("jons-easy-artists.txt","jons-easy-artists"),
     ("jons-rock-artists.txt","jons-rock-artists"),
     ("jons-newroms-artists.txt","jons-newroms-artists"),
     ("jons-party-artists.txt","jons-party-artists")] 
          

if token:
    sp = spotipy.Spotify(auth=token)
    
    for filename, playlist_name in l:    
        create_playlist_from_artist_file(sp,filename,playlist_name)
    
else:
    print "ERROR: No Token"