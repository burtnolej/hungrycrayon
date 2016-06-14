
from spotify_util import SpotifyConnector
import unittest
import random

def _display_dict(d,orient=1):
    
    if orient==1:
        for key,value in d.iteritems():            
            print key.rjust(25),
            print " : ", 
            print str(value).ljust(25)
    elif orient==2:
        
        for key,value in d.iteritems(): 
            try:
                print str(value)[:25].ljust(25),
            except Exception,e:
                print str(e)[:25].ljust(25),

    
class TestSpotifyConnectorRead(unittest.TestCase):

    def setUp(self):
        user='1165431378'
        scope = ''
        self.test_playlist_id='656pr766V8K4DRlHWQRXRU' # Mini Tracks
        self.test_artist = 'Michael Jackson'
        self.test_artist_id = '3fMbdgg4jU18AjLCKBhRSm'
        self.test_related_artists = ['Whitney Houston','Prince','Diana Ross','Madonna',
                                     'Lionel Richie','Janet Jackson','Jermaine Jackson',
                                     'Tina Turner','The Pointer Sisters','George Michael',
                                     'Stevie Wonder','Donna Summer','Billy Ocean','Barry White',
                                     'Justin Timberlake','Philip Bailey','Terence Trent D\'Arby',
                                     'Bee Gees','Chaka Khan','Cyndi Lauper']
        
        self.test_artist_top_tracks = ['Billie Jean - Single Version',
                                       'Love Never Felt so Good',
                                       'Beat It - Single Version',
                                       'P.Y.T. (Pretty Young Thing)',
                                       'Don\'t Stop \'Til You Get Enough - Single Version',
                                       'Black or White - Single Version',
                                       'The Way You Make Me Feel - 2012 Remaster',
                                       'Love Never Felt so Good',
                                       'Man in the Mirror - 2012 Remaster',
                                       'Rock with You - Single Version']
        
        
        self.test_artist_top_n_tracks = ['Billie Jean - Single Version',
                                         'Beat It - Single Version',
                                         'Man in the Mirror - 2012 Remaster']
        
        self.test_artist_track_id = '5ChkMS8OtdzJeqyybCc9R5' #Billie Jean - Single Version
        self.test_artist_track_popularity = 78 #Billie Jean - Single Version
           
        self.test_track_info = {'album': u'Thriller 25 Super Deluxe Edition', 
                                'duration_ms': 293826, 
                                'popularity': 78, 
                                'name': u'Billie Jean - Single Version', 
                                'artist': u'Michael Jackson'}
     
        self.sc = SpotifyConnector(user,scope)

    def tearDown(self):
        del self.sc
        
    def test_get_user_info(self):   
        _user_info = self.sc.get_current_user_info()
        self.assertEqual(_user_info['display_name'],'Jon Butler')
        self.assertEqual(_user_info['id'],'1165431378')
        self.assertIsInstance(_user_info['followers'],int)
       
    def test_get_artist_info(self):
        
        _artist_info = self.sc.get_artist_info(self.test_artist,True)
        self.assertEqual(_artist_info['name'],self.test_artist)
        self.assertEqual(_artist_info['id'], self.test_artist_id)
        
    def test_get_user_playlists_info(self):
        results = self.sc.get_user_playlists_info()
        
        for result in results:
            _display_dict(result,2)
            print
            
    def test_get_playlist_tracks(self):
        results = self.sc.get_playlist_tracks(self.test_playlist_id)
        
        for result in results:
            _display_dict(result,2)
            print
            
    def test_get_related_artists(self):
        related_artists = self.sc.get_artist_related_artist(self.test_artist_id)
        _related_artists = [related_artist['name'] for related_artist in related_artists]
        
        self.assertListEqual(_related_artists, self.test_related_artists)
        
    def test_get_artist_top_tracks(self):
        top_tracks = self.sc.get_artist_top_tracks(self.test_artist_id)
        _top_tracks = [top_track['name'] for top_track in top_tracks]
        
        self.assertListEqual(self.test_artist_top_tracks,_top_tracks)
        
    def test_get_artist_top_n_tracks(self):
        top_tracks = self.sc.get_artist_top_n_tracks(self.test_artist_id,3)
        print top_tracks 
        
    def test_get_track_info(self):
        
        track_info = self.sc.get_track_info(self.test_artist_track_id)
        self.assertDictEqual(self.test_track_info,track_info)
            
    def test_get_audio_features(self):
        audio_features = self.sc.get_audio_features([self.test_artist_track_id])
        
        for audio_feature in audio_features:
            _display_dict(audio_feature,1)
            print
        
    def test_search_spotify_tracks(self):
        tracks = self.sc.search_spotify_tracks("Easy to Love")
        
        for track in tracks:
            _display_dict(track,2)
            print
        
    def test_get_track_popularity(self):
        self.assertEqual(self.sc.get_track_popularity(self.test_artist_track_id),
                         self.test_artist_track_popularity)
        
            
class TestSpotifyConnectorWrite(unittest.TestCase):

    def setUp(self):
        user='1165431378'
        scope = 'playlist-modify-public'
        
        # create a random name for test playlist
        self.test_playlist_name = hex(int(random.random()*pow(10,10))) 
       
        # real track id to play with "Whitney, One Moment in time;Sinatra, My Way"
        self.test_track_ids = ['3S3dZXxNGghLtOqehzHtii', '5iOnSrG79MzrCaq0I8Lpv6']
        
        # create connection object
        self.sc = SpotifyConnector(user,scope)
        
        # create the test playlist
        self.test_playlist_id = self.sc.create_private_playlist(self.test_playlist_name) 

    def tearDown(self):
        
        # "delete" the test playlist
        self.sc.unfollow_playlist(self.test_playlist_id)        

        del self.sc    
        
    def test_create_public_playlist(self):
        
        # fetch info from spotify for that playlist
        results = self.sc.get_user_playlists_info(self.test_playlist_id)
        
        # assert correctness
        self.assertEqual(results[0]['name'],self.test_playlist_name)
        
    def test_add_tracks_to_playlist(self):
    
        # add test tracks to playlist
        self.sc.add_track_to_playlist(self.test_playlist_id,
                                      self.test_track_ids)
    
        # get from spotify the tracks associated with the test playlist
        results = self.sc.get_playlist_tracks(self.test_playlist_id)

        # extract the track id's to compare with test tracks
        _result_ids = [result['id'] for result in results]
        
        self.assertListEqual(_result_ids,self.test_track_ids)

            
    def test_unfollow_playlist(self):
    
        print self.sc.unfollow_playlist("0lxfj5ZUmPMtAF43PmI4QY")
            
if __name__ == '__main__':

    suite = unittest.TestSuite()

    #suite.addTest(TestSpotifyConnectorRead("test_get_user_playlists_info")) 
    #suite.addTest(TestSpotifyConnectorRead("test_get_playlist_tracks")) 
    #suite.addTest(TestSpotifyConnectorRead("test_get_user_info")) 
    #suite.addTest(TestSpotifyConnectorRead("test_get_artist_info")) 
    suite.addTest(TestSpotifyConnectorRead("test_get_related_artists")) 
    suite.addTest(TestSpotifyConnectorRead("test_get_artist_top_tracks"))
    suite.addTest(TestSpotifyConnectorRead("test_get_track_info"))
    suite.addTest(TestSpotifyConnectorRead("test_get_audio_features"))
    suite.addTest(TestSpotifyConnectorRead("test_search_spotify_tracks"))
    suite.addTest(TestSpotifyConnectorRead("test_get_track_popularity"))
    suite.addTest(TestSpotifyConnectorRead("test_get_artist_top_n_tracks"))
    
    
    #suite.addTest(TestSpotifyConnectorWrite("test_create_public_playlist")) 
    #suite.addTest(TestSpotifyConnectorWrite("test_add_tracks_to_playlist")) 

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)    