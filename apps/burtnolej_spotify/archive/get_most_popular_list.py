import sys
import spotipy
import spotipy.util as util
from spotify_util import get_most_popular_list
scope = 'playlist-modify-private'
user='burtnolejusa'

token = util.prompt_for_user_token(user,scope)

if token:
    sp = spotipy.Spotify(auth=token)
    
    l = ['2EoOZnxNgtmZaD8uUmz2nD',
         '2EoOZnxNgtmZaD8uUmz2nD',
         '1dWimOlV5KUHDerWZVDv5l',
         '5DiXcVovI0FcY2s0icWWUu',
         '0Ph6L4l8dYUuXFmb71Ajnd',
         '3XVozq1aeqsJwpXrEZrDJ9',
         '594M0rqYMOo8BhMGEdoi5C',
         '6b2oQwSGFkzsMtQruIWm2p',
         '6MdqqkQ8sSC0WB4i8PyRuQ',
         '1Je1IMUlBXcx1Fz0WE7oPT']

    print get_most_popular_list(sp,l,3)
    
else:
    print "ERROR: No Token"
    
    
    