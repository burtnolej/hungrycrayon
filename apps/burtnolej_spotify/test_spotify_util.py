from spotify_util import SpotifyConnector
from types import StringType, IntType, UnicodeType
import unittest
import sys
import random

def _display_dict(d,orient=1):
    

    if orient==1:
        for key,value in d.iteritems():            
            print key.rjust(35),
            print " : ", 
            print str(value).ljust(35)
    elif orient==2:
        for key,value in d.iteritems(): 
            if isinstance(value,UnicodeType):
                print value[:35].ljust(35),
            else:
                print str(value)[:8].ljust(8),

    
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
        
        self.test_artist_top_n_tracks = [u'Billie Jean - Single Version',
                                         u'Love Never Felt so Good',
                                         u'Beat It - Single Version']
        
        self.test_album_tracks = ['Wanna Be Startin\' Somethin\'',
                                  'Baby Be Mine',
                                  'The Girl is Mine - Paul McCartney',
                                  'Thriller',
                                  'Beat It - Single Version',
                                  'Billie Jean - Single Version',
                                  'Human Nature',
                                  'P.Y.T.(Pretty Young Thing)',
                                  'The Lady in My Life']
        
        self.test_album = 'Thriller'
        
        self.test_album_id = '1C2h7mLntPSeVYciMRTF4a'
        
        self.test_artist_albums = ['XSCAPE',
                                   'XSCAPE - Track by Track Commentary',
                                   'Michael',
                                   'Invincible',
                                   'BLOOD ON THE DANCE FLOOR/ HIStory In The Mix',
                                   'HIStory - PAST, PRESENT AND FUTURE - BOOK I',
                                   'Dangerous',
                                   'Bad (Remastered)',
                                   'Bad 25th Anniversary',
                                   'Thriller',
                                   'Thriller 25 Super Deluxe Edition',
                                   'Off the Wall',
                                   'Forever, Michael',
                                   'Music and Me',
                                   'Ben',
                                   'Got To Be There']
                                   
        self.test_artist_track_name = 'Billie Jean - Single Version'
        self.test_artist_track_id = '5ChkMS8OtdzJeqyybCc9R5' #Billie Jean - Single Version
        self.test_artist_track_popularity = 78 #Billie Jean - Single Version
           
        self.test_track_info = [{'album': u'Thriller 25 Super Deluxe Edition', 
                                'duration_ms': 293826, 
                                'popularity': 78, 
                                'name': u'Billie Jean - Single Version', 
                                'artist': u'Michael Jackson'}]
     
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
        
        # number of playlists will so just check that a large number was returned
        self.assertGreater(len(results),20)
        
        # check some specifics of 1 record
        self.assertTrue(results[0].has_key('collaborative'))
        self.assertTrue(results[0].has_key('num_tracks'))   
        self.assertIsInstance(results[0]['num_tracks'],IntType)   

            
    def test_get_playlist_tracks(self):
        results = self.sc.get_playlist_tracks(self.test_playlist_id)
        
        for result in results:
            _display_dict(result,2)
            print
            
    def test_get_related_artists(self):
        related_artists = self.sc.get_artist_related_artist(self.test_artist_id)
        _related_artists = [related_artist['name'] for related_artist in related_artists]
        
        print sorted(_related_artists), sorted(self.test_related_artists)
        
        self.assertListEqual(sorted(_related_artists), 
                             sorted(self.test_related_artists))
        
    def test_get_artist_top_tracks(self):
        top_tracks = self.sc.get_artist_top_tracks(self.test_artist_id)
        _top_tracks = [top_track['name'] for top_track in top_tracks]
        
        self.assertListEqual(self.test_artist_top_tracks,_top_tracks)
        
    def test_get_artist_top_n_tracks(self):
        top_tracks = self.sc.get_artist_top_n_tracks(self.test_artist_id,3)
        self.assertListEqual(self.test_artist_top_n_tracks, 
                             [self.sc.get_track_name(track_id) for track_id in top_tracks ])
        
    def test_get_track_info(self):
        
        track_info = self.sc.get_track_info(self.test_artist_track_id)
        self.assertListEqual(self.test_track_info,track_info)
            
    def test_get_audio_features(self):
        audio_features = self.sc.get_audio_features([self.test_artist_track_id])
        
        for audio_feature in audio_features:
            _display_dict(audio_feature,1)
            print
        
    def test_search_spotify_tracks(self):     
        print self.sc.search_spotify_tracks(self.test_artist_track_name)

    def test_search_spotify_tracks_by_artist(self):
        print self.sc.search_spotify_tracks(self.test_artist_track_name,self.test_artist)
          
    def test_search_spotify_tracks_by_album(self):
        print self.sc.search_spotify_tracks(self.test_artist_track_name,self.test_album)
        
    def test_get_track_popularity(self):
        self.assertEqual(self.sc.get_track_popularity(self.test_artist_track_id),
                         self.test_artist_track_popularity)
        
    def test_get_artist_albums(self):
        albums =  self.sc.get_artist_albums('3fMbdgg4jU18AjLCKBhRSm',['name'])
        print self.test_artist_albums, albums
        self.assertListEqual( self.test_artist_albums, albums)
            
    def test_get_album_tracks(self):
        print self.sc.get_album_tracks('1C2h7mLntPSeVYciMRTF4a')
        
            
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

    suite.addTest(TestSpotifyConnectorRead("test_get_user_playlists_info")) 
    #suite.addTest(TestSpotifyConnectorRead("test_get_playlist_tracks")) 
    #suite.addTest(TestSpotifyConnectorRead("test_get_user_info")) 
    #suite.addTest(TestSpotifyConnectorRead("test_get_artist_info")) 
    #suite.addTest(TestSpotifyConnectorRead("test_get_related_artists")) 
    #suite.addTest(TestSpotifyConnectorRead("test_get_artist_top_tracks"))
    #suite.addTest(TestSpotifyConnectorRead("test_get_track_info"))
    #suite.addTest(TestSpotifyConnectorRead("test_get_audio_features"))
    #suite.addTest(TestSpotifyConnectorRead("test_search_spotify_tracks"))
    #suite.addTest(TestSpotifyConnectorRead("test_search_spotify_artist"))
    #suite.addTest(TestSpotifyConnectorRead("test_search_spotify_album"))
    #suite.addTest(TestSpotifyConnectorRead("test_get_track_popularity"))
    #suite.addTest(TestSpotifyConnectorRead("test_get_artist_top_n_tracks"))
    #suite.addTest(TestSpotifyConnectorRead("test_get_artist_albums"))
    #uite.addTest(TestSpotifyConnectorRead("test_get_album_tracks"))
    
    
    #suite.addTest(TestSpotifyConnectorWrite("test_create_public_playlist")) 
    #suite.addTest(TestSpotifyConnectorWrite("test_add_tracks_to_playlist")) 

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)    