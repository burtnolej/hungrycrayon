import sys
import spotipy
import spotipy.util as util

#spotipy = spotipy.Spotify()

#scope = 'user-library-read'
#scope = 'user-library-modify'

#user='burtnolejusa'

DISPLAYNAME='display_name'
USERID='id'

PLAYLISTNAME='name'
PLAYLISTID='id'
PLAYLISTTRACKS='tracks'

TRACKNAME='name'
TRACKID='id'
TRACKARTISTS='artists'
TRACKITEMS='items'
TRACK='track'

ARTISTNAME='name'


class SpotifyConnector():
    
    def __init__(self,user,scope=None):
        if scope==None:
            scope = 'user-library-read'
        
        token = util.prompt_for_user_token(user,scope)
                
        if token:
            self.user = user
            self.scope = scope
            self.token = token
            self.playlists = {}
            self.sp = spotipy.Spotify(auth=self.token)
        else:
            raise Exception("connection failed")
   
    def extractor(*myargs):
        def _extractor(func):
            def wrapper(*args, **kwargs):
                _results = func(*args,**kwargs)
                return(SpotifyConnector.extract_fields(_results,myargs[0],myargs[1]))
            return wrapper
        return _extractor
    
    @staticmethod
    def extract_fields(records,fields,unique_key):
        
        ''' default action is to return a list of dicts but if fields is only
        1 attribute in length, returns a list of values. Also removes duplicates based
        on unique_key '''
        unique_records = set()
        
        _records = []
        for record in records:
            if record[unique_key].lower() not in unique_records:
                unique_records.add(record[unique_key].lower())
                d={}

                for field in fields:
                    if field=='artist':
                        d[field] = record['artists'][0]['name']
                    elif field=='album':
                        d[field] = record['album']['name']
                    elif field=='num_tracks':
                        d[field] = record['tracks']['total']
                    elif field=='owner':
                        d[field] = record['owner']['id']
                    else:
                        d[field] = record[field]
                _records.append(d)

        
        if len(fields)==1:
            return [_record[fields[0]] for _record in _records]
                    
        return(_records)

    def get_current_user_info(self):
        
        _user = self.sp.current_user()

        return({'display_name':_user['display_name'],
                'id':_user['id'],
                'followers':_user['followers']['total']})
    
    @extractor(['collaborative','public','name','id','num_tracks','owner'],'name')
    def get_user_playlists_info(self,playlist_id=None):
        return(self.sp.user_playlists(self.user)['items'])
    
        #f playlist_id==None:
        
        #else:
            #return([self.sp.user_playlist(self.user,playlist_id)])  
        
    def get_artist_info(self,name,match=False):
        
        results = self.sp.search(q='artist:' + name,type='artist')
        
        _artists=[]
        items = results['artists']['items']
        for item in items:
            if item['name'] == name and match==True:
                return({'name':item['name'],
                        'id':item['id']})
            else:
                _artists.append({'name':item['name'],
                            'id':item['id']})
                
        if match:
            return [] # no hits
        return _artists
    
        
    def create_private_playlist(self,playlist_name,public=False):
        playlists = self.sp.user_playlist_create(self.user, playlist_name, True)
        return(playlists['id'])
   
    def unfollow_playlist(self,playlist_id):
        self.sp.user_playlist_unfollow(self.user,playlist_id)
        
    def get_artist_related_artist(self,artist_id):
        related_artists = self.sp.artist_related_artists(artist_id)['artists']

        _related_artists = []
        for related_artist in related_artists:
            _related_artists.append({'id':related_artist['id'],
                                     'name':related_artist['name']})
            
        return(_related_artists)
            
    def get_playlist_tracks(self,playlist_id):
        results = self.sp.user_playlist(self.user, playlist_id, fields="tracks,next")
        tracks = results['tracks']
        
        _tracks = []
        for item in tracks['items']:
            _tracks.append({'id':item['track']['id'],
                            'name':item['track']['name'],
                            'artist':item['track']['artists'][0]['name']})
            
        return(_tracks)

    def add_track_to_playlist(self,playlist_id, track_ids):
        results = self.sp.user_playlist_add_tracks(self.user, playlist_id, track_ids)
                
    def get_artist_top_tracks(self,artist_id):
        _top_tracks=[]
        top_tracks = self.sp.artist_top_tracks(artist_id)
        
        for track in top_tracks['tracks']:
            _top_tracks.append({'id':track['id'],
                                'name':track['name']})    
        return(_top_tracks)
    
    def get_track_popularity(self,track_id):
        return self.sp.track(track_id)['popularity']

    def get_track_name(self,track_id):
        return(self.sp.track(track_id)['name'])
    
    def _sort_tracks_by_popularity(self,track_ids,num_tracks=3):
        
        track_by_popularity = {}
        for track in track_ids:
            track_by_popularity[self.get_track_popularity(track['id'])] = track['id']

        sorted_popularity = sorted(track_by_popularity,reverse=True)[:num_tracks]
        
        return([track_by_popularity[popularity] for popularity in sorted_popularity])
    
    def get_artist_top_n_tracks(self,artist_id,num_tracks):
        _top_tracks=[]
        top_tracks = self.get_artist_top_tracks(artist_id)
        
        return(self._sort_tracks_by_popularity(top_tracks,3))
    
    @extractor(['album','popularity','duration_ms','name','artist'],'name')
    def get_track_info(self,track_id):
        return([self.sp.track(track_id)])
        
    def get_audio_features(self,track_id):
        return(self.sp.audio_features(track_id))
    
    
    # complete using the extractor decorator
    # make search simple by track or by album - will always retreive a lot
    # use get_artist_albums() for more specific searches
    # search test should be simple (did we get stuff)
    
    @extractor(['id','name','artist'],'name')
    def search_spotify_tracks(self,track,artist=None):
        return(self.sp.search(q='track:'+track,type='track', limit=50)['tracks']['items'])
    
    @extractor(['id','name','artist'],'name')
    def search_spotify_tracks_by_artist(self,track,artist):
        return(self.sp.search(q='track:'+track+' artist:'+artist,type='track', limit=50)['tracks']['items'])
    
    @extractor(['id','name','artist'],'name')
    def search_spotify_tracks_by_album(self,track,album):
        return(self.sp.search(q='track:'+track+' album:'+album,type='track', limit=50)['tracks']['items'])
        
    def get_album_tracks(self,album_id):
        tracks = self.sp.album_tracks(album_id)['items']
        return(self._extract_fields(tracks,['id','name','artist'],'name'))
        
    def get_artist_albums(self,artist_id,fields):
        albums = self.sp.artist_albums(artist_id, album_type='album',country='US')['items']
        return(self._extract_fields(albums,fields,'name'))



def search_tracks(sp,track_name,artist):
    
    
    try:
        tracks = sp.search(q='track:'+track_name,type='track', limit=20)['tracks']['items']
    except:
        return(("_error","_error","_error"))
        
    _d = {}
    _most_popular_id=-1
    _most_popular_value=-1
    
    for track in tracks:
        _artist = track['artists'][0]['name']
        _popularity = track['popularity']
        _album_name=track['album']['name']
        _track_name=track['name']
        _id = track['id']
        _d[_popularity] = (_track_name,_artist,_id)
        #print artist, _artist,_popularity
        #if _artist.lower()==artist.lower():
        #    if _popularity>_most_popular_value:
        #        _most_popular_id=_id
        #        _most_popular_value=_popularity
        
    _d_sorted= sorted(_d.keys())
    _most_popular_value = _d_sorted[len(_d_sorted)-1]
     
    #_artist,_track_name,_id = _d[_most_popular_value]

        
    return _d[_most_popular_value]




def get_most_popular_list(sp,track_ids,num_tracks=10):
    d={}
    for track_id in track_ids:
        popularity = get_popularity(sp,track_id)
        d[popularity] = track_id
        
    d_sorted= sorted(d.keys(),reverse=True)
    top_d_sorted = d_sorted[:num_tracks]
        
    top_d = []
    for _popularity in top_d_sorted:
        top_d.append(d[_popularity])
    return(top_d)


    






   





        


def create_playlist_from_file(sp,filename,playlist_name):
    l=[]
    fh = open(filename,'r+')
    playlist = create_playlist(sp,playlist_name)
    for line in fh:
        if line.rstrip() <> "_error":
            l.append(line.rstrip())
            
    add_track_to_playlist(sp,playlist['id'],l.join(","))

def create_playlist_from_artist_file(sp,filename,playlist_name):
    
    l=[]
    
    fh = open(filename,'r+')
    playlist = create_playlist(sp,playlist_name)
    
    for line in fh:
        artist,num_tracks = line.rstrip().split(",")
        
        
        _artist = get_artist(sp,artist)
        
        try:
            print "for",artist,_artist['id']
            top_tracks = get_artist_top_tracks(sp,_artist)
        
            top_tracks = get_most_popular_list(sp,top_tracks,int(num_tracks))
            
            print "adding",len(top_tracks)
            add_track_to_playlist(sp,playlist['id'],top_tracks)
        except:
            print "error",artist

if __name__ == '__main__':
    
    user='1165431378'
    #scope = 'playlist-modify-private'
    scope = 'playlist-modify-public'
    
    scope = 'playlist-read-collaborative'
    
    
    sc = SpotifyConnector(user,scope)
    
    #sc.get_playlist_tracks('43YCKjl65PD2MiiuwgUzk7')
    #sc.show_user_playlists()
    
    #print sc.get_artist('Michael Jackson',True)
    
    #print sc.get_artist_related_artist('3fMbdgg4jU18AjLCKBhRSm')
    #sc.unfollow_playlist('30KDF9AxgfV4Zs64FBy1Cv')
    #sc.create_playlist("foobar_public",True)
    

    