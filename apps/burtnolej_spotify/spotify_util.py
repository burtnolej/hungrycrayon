import sys
import spotipy
import spotipy.util as util
from types import ListType



class SpotifyConnector():
    
    def __init__(self,user,scope=None):
        if scope==None:
            scope = 'user-library-read'
            #scope = 'user-library-read'
            #scope = 'user-library-modify'            
        
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
                return(SpotifyConnector.extract_fields(_results,*myargs))
            return wrapper
        return _extractor
    
    def enrich_kwargs(*myargs):
        ''' checks that the correct parameters are passed in and forces single items to lists of 1 item where appropriate
        
            parameters:
                 - dict of the form {arg_name:arg_value}
        '''
        def _extractor(func):
            def wrapper(*args, **kwargs):                    
                for arg_name in myargs[0].keys():
                    if not kwargs.has_key(arg_name): raise Exception('must pass arg',arg_name)
                    
                    if not isinstance(kwargs[arg_name],myargs[0][arg_name]):
                        if myargs[0][arg_name] == ListType:
                            kwargs[arg_name] = [kwargs[arg_name]]
            
                return func(*args,**kwargs)
            return wrapper
        return _extractor

    @staticmethod
    def extract_fields(records,fields,unique_key=None):
        
        ''' default action is to return a list of dicts but if fields is only
        1 attribute in length, returns a list of values. Also removes duplicates based
        on unique_key '''
        
        assert isinstance(fields,list)

        # if only one record is sent not as a list; create a list
        if not isinstance(records,list): records = [records]
        
        unique_records = set()
        
        _records = []
        for record in records:
            d={}
            if unique_key != None:
                # if there is more than 1 record in the return set
                if record[unique_key].lower() not in unique_records:
                    # add unique key if not seen before
                    unique_records.add(record[unique_key].lower())
                else: # otherwise exit
                    next  

            for field in fields:
                if field=='artist':
                    d[field] = record['artists'][0]['name']
                elif field=='album':
                    d[field] = record['album']['name']
                elif field=='num_tracks':
                    d[field] = record['tracks']['total']
                elif field=='owner':
                    d[field] = record['owner']['id']
                elif field=='tid':
                    d[field] = record['track']['id']
                else:
                    d[field] = record[field]
            _records.append(d)

        
        if len(fields)==1:
            return [_record[fields[0]] for _record in _records]
                 
        return(_records)
    
    # ------------------------------------------------------------------------------
    # user playlists: gets
    # ------------------------------------------------------------------------------
    @extractor(['id'],'name')
    def get_user_playlist_ids(self):
        ''' return a list of playlist id's '''
        return(self.sp.user_playlists(self.user)['items'])
        
    def get_user_playlist_count(self):
        ''' return the number of playlists a user has. remember max number that can be returned is 50 '''
        return(len(self.get_user_playlist_ids()))
    
    @extractor(['collaborative','public','name','num_tracks','owner','followers'])
    def get_user_playlist_info(self,playlist_id):
        ''' given a playlist id; return useful info '''
        return self.sp.user_playlist(self.user,playlist_id)
    
    @extractor(['tid'])
    def get_user_playlist_tracks(self,playlist_id):
        ''' given a playlist id; return track ids'''
        return(self.sp.user_playlist(self.user,playlist_id)['tracks']['items'])
    
    # user playlists: checks
    def playlist_exists(self,playlist_id):
        ''' given a playlist id; return useful info, check if the playlist id
        is a member of the list of returned playlist id's. This is to get around the issue
        where nothing is really deleted and "unfollowed" playlists are not visible
        on the spotify app but are still retreivable via the api'''
        try:
            self.get_user_playlist_ids().index(playlist_id)
            return True
        except:
            return False
        
    # user playlists: delete
    def unfollow_playlist(self,playlist_id):
        self.sp.user_playlist_unfollow(self.user,playlist_id)
        
    def delete_test_playlist(self):
        ''' get list of playlist id's, detect ones used for testing by checking if the
        string can be converted from hex to a base10 int'''
        
        playlists = SpotifyConnector.extract_fields(self.sp.user_playlists(self.user)['items'],
                                                    ['id','name'])
        
        test_playlist = []
        for playlist in playlists:
            try:
                int(playlist['name'],16)
                test_playlist.append(playlist['id'])
            except:
                print "cannot convert from hex",playlist['name'][2:]
        
        for pid in test_playlist:
            self.unfollow_playlist(pid) 
        
    # user playlists: create
    def create_playlist(self,playlist_name,public=False):
        playlists = self.sp.user_playlist_create(self.user, playlist_name, public)
        return(playlists['id'])
    
    # ------------------------------------------------------------------------------ 
    # tracks : read
    # ------------------------------------------------------------------------------
        
    # tracks : info
    def get_track_info_all(self,**kwargs):
        ''' given a single track_id or a list of track_id's, returns a list of dicts containing all available fields

            Parameters:
                - track_ids - the id of the tracks - can be either a list or single value
                            if a single value then the decorator will force it into a single item list
        '''
        return ([self.sp.track(track_id) for track_id in kwargs['track_ids']])
   
    @enrich_kwargs({'track_ids':ListType})
    @extractor(['album','duration_ms','name','artist'])
    def get_track_info(self,**kwargs):
        ''' given a single track_id or a list of track_id's, return the popularity field only
            this just uses the extractor to limit the returned fields
        '''
        return(self.get_track_info_all(**kwargs))
        
    @enrich_kwargs({'track_ids':ListType})
    @extractor(['popularity'])
    def get_track_popularity(self,**kwargs):
        ''' given a single track_id or a list of track_id's, return the popularity field only
            this just uses the extractor to limit the returned fields
        '''
        return(self.get_track_info_all(**kwargs))
    
    # tracks : audio features
    def get_track_audio_features_all(self,**kwargs):
        return(self.sp.audio_features(kwargs['track_ids']))

    @enrich_kwargs({'track_ids':ListType})
    @extractor(["danceability","energy","loudness","tempo"])
    def get_key_track_audio_features(self,**kwargs):
        return(self.get_track_audio_features_all(**kwargs))
          
    # tracks : albums
    def get_album_tracks(self,album_id):
        return(self.sp.album_tracks(album_id)['items'])
        
    @extractor(["name"])      
    def get_album_track_names(self,album_id):
        return(self.sp.album_tracks(album_id)['items'])

    @extractor(["id"])
    def get_artist_top_tracks(self,artist_id):
        return self.sp.artist_top_tracks(artist_id)['tracks']
    
    @enrich_kwargs({'track_ids':ListType})
    @extractor(["name"]) 
    def get_track_name(self,**kwargs):
        return self.sp.tracks(kwargs['track_ids'])['tracks']
    

    
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
        


    # ------------------------------------------------------------------------------ 
    # tracks : misc
    # ------------------------------------------------------------------------------      
    def get_current_user_info(self):
        
        _user = self.sp.current_user()

        return({'display_name':_user['display_name'],
                'id':_user['id'],
                'followers':_user['followers']['total']})
    
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
    
        
    def get_available_genre_seeds(self):
        return self.sp.available_genre_seeds()['genres']
    
    @extractor(['id'])
    def get_recommendations(self,**kwargs):
        return self.sp.recommendation(**kwargs)['tracks']
            
    def get_artist_related_artist(self,artist_id):
        related_artists = self.sp.artist_related_artists(artist_id)['artists']

        _related_artists = []
        for related_artist in related_artists:
            _related_artists.append({'id':related_artist['id'],
                                     'name':related_artist['name']})
            
        return(_related_artists)
    


    def add_track_to_playlist(self,playlist_id, track_ids):
        results = self.sp.user_playlist_add_tracks(self.user, playlist_id, track_ids)
                


    def get_artist_albums(self,artist_id,fields):
        albums = self.sp.artist_albums(artist_id, album_type='album',country='US')['items']
        return(self._extract_fields(albums,fields,'name'))


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
    

    
    # ------------------------------------------------------------------------------ 
    # tracks : search
    # ------------------------------------------------------------------------------ 
    
    @extractor(['id','name','artist'],'name')
    def search_spotify_tracks(self,track,artist=None):
        return(self.sp.search(q='track:'+track,type='track', limit=50)['tracks']['items'])
    
    @extractor(['id','name','artist'],'name')
    def search_spotify_tracks_by_artist(self,track,artist):
        return(self.sp.search(q='track:'+track+' artist:'+artist,type='track', limit=50)['tracks']['items'])
    
    @extractor(['id','name','artist'],'name')
    def search_spotify_tracks_by_album(self,track,album):
        return(self.sp.search(q='track:'+track+' album:'+album,type='track', limit=50)['tracks']['items'])
        

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
    scope = ''
    
    sc = SpotifyConnector(user,scope)
    
    sc.delete_test_playlist()
