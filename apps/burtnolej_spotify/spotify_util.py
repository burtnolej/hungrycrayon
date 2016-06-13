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
   
    def get_current_user_info(self):
        
        _user = self.sp.current_user()

        return({'display_name':_user['display_name'],
                'id':_user['id'],
                'followers':_user['followers']['total']})
    
    def get_user_playlists_info(self,playlist_id=None):
        
        if playlist_id==None:
            results = self.sp.user_playlists(self.user)['items']
        else:
            results = [self.sp.user_playlist(self.user,playlist_id)]
        
        _playlists = []
        for _playlist in results:
            

            _playlists.append({'collaborative':_playlist['collaborative'],
                               'public':_playlist['public'],
                               'owner':_playlist['owner']['id'],
                               'name':_playlist['name'],
                               'tracks':_playlist['tracks']['total'],
                               'id':_playlist['id']})
            
        return(_playlists)        
        
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
        
    def get_artist_related_artist(self,artist):
        _related_artists = self.sp.artist_related_artists(artist)
        
        _d ={}
        for _related_artist in _related_artists['artists']:
            _d[_related_artist['id']] = _related_artist['name']
            
        return(_d)
            
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
                

def get_track_info(sp):
    pass

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

def print_track_id_meta(sp,track_id_csv):
    
    l = track_id_csv.split(",")
    
    for track_id in l:
        track_urn = "spotify:track:"+track_id
        _track =  sp.track(track_urn)
        
        print track_id.ljust(10),_track['name'].ljust(20)[:15],str(_track['popularity']).ljust(10)
        
def get_popularity(sp,track_id):
    
    track_urn = "spotify:track:"+track_id
    return sp.track(track_urn)['popularity']
    
def get_artist_top_tracks(sp,artist):
    l=[]
    response = sp.artist_top_tracks(artist['uri'])
    
    for track in response['tracks']:
        l.append(track['id'])    
    return(l)





   




def show_album_tracks(album):
    tracks = []
    results = sp.album_tracks(album['id'])
    tracks.extend(results['items'])
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    for track in tracks:
        print(track['id'], track['name'])
        
def get_artist_albums(artist):
    albums = []
    results = sp.artist_albums(artist['id'], album_type='album')
    albums.extend(results['items'])
    while results['next']:
        results = sp.next(results)
        albums.extend(results['items'])
    print ('Total albums:', len(albums))
    seen = set() # to avoid dups
    #albums.sort(key=lambda album:album['name'].lower())
    for album in albums:
        name = album['name']
        if name not in seen:
            print(name)
            seen.add(name)
            show_album_tracks(album)

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
    

    