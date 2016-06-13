import sys
import spotipy
import spotipy.util as util
#spotipy = spotipy.Spotify()

#scope = 'user-library-read'
#scope = 'user-library-modify'
scope = 'playlist-modify-private'
user='burtnolejusa'
#user='Jon Butler'



def get_track(track_name,artist):
    tracks = sp.search(q='track:'+track_name,type='track')['tracks']['items']
    
    _most_popular_id=-1
    _most_popular_value=-1
    
    for track in tracks:
        _artist = track['artists'][0]['name']
        _popularity = track['popularity']
        _track_name=track['album']['name']
        _id = track['id']
        if _artist==artist:
            if _popularity>_most_popular_value:
                print _artist, _popularity
                _most_popular_id=_id
                _most_popular_value=_popularity
    return (_most_popular_id)

def create_playlist(playlist_name):
    playlists = sp.user_playlist_create(user, playlist_name, False)
    return(playlists)

def add_track_to_playlist(playlist_id, track_ids):
    results = sp.user_playlist_add_tracks(user, playlist_id, track_ids)
    
def get_artist_top_tracks(artist):
    l=[]
    response = sp.artist_top_tracks(artist['uri'])
    
    for track in response['tracks']:
        l.append(track['id'])    
    return(l)
    
def get_user_playlists():
    playlists = sp.user_playlists(user)
    for playlist in playlists['items']:
        if playlist['owner']['id'] == user:
            print()
            print(playlist['name'])                    

def get_artist(name):
    results = sp.search(q='artist:' + name,type='artist')
    items = results['artists']['items']
    for item in items:
        if item['name'] == name:
            return(item)

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

token = util.prompt_for_user_token(user,scope)

if token:
    sp = spotipy.Spotify(auth=token)
    print get_track("Two Tribes","Frankie Goes To Hollywood")
        
    #print "logged in as user:", sp.current_user()['id']
    exit()
    artist = get_artist('The Beatles')
    #get_artist_albums(artist)
    #playlists = get_user_playlists()
    playlist = create_playlist("foobar2")
    top_tracks = get_artist_top_tracks(artist)
    add_track_to_playlist(playlist['id'],top_tracks)