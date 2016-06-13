import sys
#import spotipy
#import spotipy.util as util
#from spotify_util import get_track
#spotipy = spotipy.Spotify()
import time

from spotify_util import spotipy
from spotify_util import util
from spotify_util import get_track

scope = 'playlist-modify-private'
user='burtnolejusa'
buffer_size=20
next_buffer_start=0

def get_tracks_from_file(filename):
    ''' parses format 00. Metallica - "Enter Sandman" (1991, #16 US)'''
    fh = open(filename,'r+')
    _tracks=[]  
    for line in fh:
        line = line[4:].strip("\n")
        try:
            (artist,_line) = line.split(" - ")
        except:
            print "failed - split:",line
            
        try:
            name,_ = _line.split(" (")
        except:
            print "failed ( split:",line
            
        name = name.replace('"',"")
        _tracks.append((artist,name))
        
    return _tracks


def get_tracks_from_file2(filename):
    ''' parses format "Burning Down the House" by Talking Heads (1983)'''
    fh = open(filename,'r+')
    _tracks=[]  
    for line in fh:
        line = line.strip("\n")
        track="_error"
        artist="_artist"
        try:
            track,_line = line.split(" by ")
        except:
            print "failed - split:",line
            
        try:
            new_len = len(_line)-7
            artist = _line[0:new_len]
        except:
            print "failed ( cut:",_line
            
        track = track.replace('"',"")
        _tracks.append((artist,track))
        
    return _tracks

#tracks = get_tracks_from_file("vh1-90s.txt")
tracks = get_tracks_from_file2("vh1-80s.txt")

print tracks
exit()

token = util.prompt_for_user_token(user,scope)
if token:
        
    num_tracks = len(tracks)
    #num_tracks = 20
    buffer_size=5
    
    fh = open("vh1-90s-ids.txt",'w+')
    fh_log = open("vh1-90s.log",'w+')
    
    for _buffer in range(0,num_tracks,buffer_size):
        log_str = "buffer"+","
        log_str = log_str + str(_buffer)+","
        log_str = log_str + str(num_tracks)+","
        log_str = log_str + str(buffer_size)+ "\n"
        
        fh_log.write(log_str)
        sp = util.spotipy.Spotify(auth=token)
        for i in range(_buffer,_buffer+buffer_size):
            _artist,_track = tracks[i]
            _found_track, _found_artist,_id =  get_track(sp,_track,_artist)
                
            try:
                if (_artist==str(_found_artist)) and (_track==str(_found_track)):
                    fh_log.write("100% match" + "," + _artist +","+_track + "\n")
                else:
                    log_str =  "imperfect match"
                    log_str += _artist + "="
                    log_str += str(_found_artist) +","
                    log_str += _track+"="
                    log_str += str(_found_track) + "\n"
                    fh_log.write(log_str)

                fh.write(_id + "\n")
                
            except:
                fh_log.write("error" + ","+_artist+","+_track + "\n")

        fh_log.flush()
        fh.flush()
        #time.sleep(5)
        del sp
    
    

    
    