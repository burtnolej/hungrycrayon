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

class TestSpotifyConnector(unittest.TestCase):

    def setUp(self):
        user='1165431378'
        scope = ''
        self.test_playlist_id_perm ='656pr766V8K4DRlHWQRXRU' # Mini Tracks
        self.test_playlist_name='MiniTracks' # Mini Tracks
        self.test_artist = 'Michael Jackson'
        self.test_artist_id = '3fMbdgg4jU18AjLCKBhRSm'
        self.test_related_artists = ['Whitney Houston','Prince','Diana Ross','Madonna',
                                     'Lionel Richie','Janet Jackson','Jermaine Jackson',
                                     'Tina Turner','The Pointer Sisters','George Michael',
                                     'Stevie Wonder','Donna Summer','Billy Ocean','Barry White',
                                     'Justin Timberlake','Philip Bailey','Terence Trent D\'Arby',
                                     'Bee Gees','Chaka Khan','Cyndi Lauper']
        
        self.test_artist_top_tracks = ['Billie Jean - Single Version','Love Never Felt so Good',
                                       'Beat It - Single Version','P.Y.T. (Pretty Young Thing)',
                                       'Don\'t Stop \'Til You Get Enough - Single Version',
                                       'Black or White - Single Version','The Way You Make Me Feel - 2012 Remaster',
                                       'Love Never Felt so Good','Man in the Mirror - 2012 Remaster',
                                       'Rock with You - Single Version']
        
        self.test_artist_top_n_tracks = [u'Billie Jean - Single Version',u'Love Never Felt so Good',
                                         u'Beat It - Single Version']
        
        self.test_album_tracks = [u'Wanna Be Startin\' Somethin\'',u'Baby Be Mine',
                                  u'The Girl Is Mine',
                                  u'Thriller',u'Beat It - Single Version',
                                  u'Billie Jean - Single Version',u'Human Nature',
                                  u'P.Y.T. (Pretty Young Thing)',u'The Lady in My Life']
        
        self.test_album = 'Thriller'
        
        self.test_album_id = '2ANVost0y2y52ema1E9xAZ'
        
        self.test_artist_albums = ['XSCAPE','XSCAPE - Track by Track Commentary',
                                   'Michael','Invincible',
                                   'BLOOD ON THE DANCE FLOOR/ HIStory In The Mix',
                                   'HIStory - PAST, PRESENT AND FUTURE - BOOK I',
                                   'Dangerous','Bad (Remastered)',
                                   'Bad 25th Anniversary','Thriller',
                                   'Thriller 25 Super Deluxe Edition',
                                   'Off the Wall','Forever, Michael',
                                   'Music and Me','Ben','Got To Be There']

     
        # ------------------------------------------------------------------------------
        # single track id and results created from it
        # ------------------------------------------------------------------------------
        self.test_artist_track_id = '5ChkMS8OtdzJeqyybCc9R5' #Billie Jean - Single Version

        self.test_track_info = [{'album': u'Thriller 25 Super Deluxe Edition', 
                                 'duration_ms': 293826,
                                 'name': u'Billie Jean - Single Version', 
                                 'artist': u'Michael Jackson'}]

        self.test_artist_track_popularity = 78 #Billie Jean - Single Version
        
        self.test_artist_track_name = 'Billie Jean - Single Version'
    
        # ------------------------------------------------------------------------------
        # list of track ids and various result sets created from them
        # ------------------------------------------------------------------------------
        self.test_track_ids = ['3S3dZXxNGghLtOqehzHtii', '5iOnSrG79MzrCaq0I8Lpv6']
        
        self.test_track_info_list = [{"album":"I Will Always Love You: The Best Of Whitney Houston",
                                      "duration_ms" : 285000,
                                      "name" : "One Moment in Time",
                                      "artist" : "Whitney Houston"},
                                     {"duration_ms" : 276653,
                                      "album" : "Sinatra: Best Of The Best",
                                      "artist" : "Frank Sinatra",
                                      "name" : "My Way"}]

        self.test_tracks_popularity = [51, 6]
        
        self.test_tracks_audio_features = [{"danceability":0.266,"energy":0.539,"loudness":-6.738,"tempo":155.484},
                                           {"danceability":0.277,"energy":0.464,"loudness":-7.643,"tempo":150.067}]
        
        # ------------------------------------------------------------------------------
        # create a random name for test playlist
        # ------------------------------------------------------------------------------
        self.test_create_playlist_name = hex(int(random.random()*pow(10,10))) 
        
        self.sc = SpotifyConnector(user,scope)

    def tearDown(self):
        del self.sc
        
class TestSpotifyConnectorPlaylists(TestSpotifyConnector):
    
    # user playlists
    # ------------------------------------------------------------------------------
    def test_get_user_playlist_ids(self):
        results = self.sc.get_user_playlist_ids()
        
        # number of playlists will so just check that a large number was returned
        self.assertGreater(len(results),20)
        
        # check that its returned an actual id
        self.assertEquals(len(results[0]),22)
        
    def test_get_user_playlist_info(self):
        results = self.sc.get_user_playlist_info(self.test_playlist_id_perm)
            
        # check some specifics of 1 record
        self.assertTrue(results[0].has_key('collaborative'))
        self.assertTrue(results[0].has_key('num_tracks'))   
        self.assertIsInstance(results[0]['num_tracks'],IntType) 

        self.assertEquals(self.test_playlist_name,results[0]['name'])
        
    def test_get_user_playlist_tracks(self):
        
        # create a dummy private playlist
        _playlist_id = self.sc.create_playlist(self.test_create_playlist_name)
        
        # add test tracks to playlist
        self.sc.add_track_to_playlist(_playlist_id, self.test_track_ids)
        
        self.assertEqual(self.sc.get_user_playlist_tracks(_playlist_id),self.test_track_ids)
        
        # unfollow the playlist
        self.sc.unfollow_playlist(_playlist_id)        

    def test_add_tracks_to_playlist(self):
    
        # create a dummy private playlist
        _playlist_id = self.sc.create_playlist(self.test_create_playlist_name)
        
        # add test tracks to playlist
        self.sc.add_track_to_playlist(_playlist_id, self.test_track_ids)
    
        # get from spotify the tracks associated with the test playlist
        _result_ids = self.sc.get_user_playlist_tracks(_playlist_id)
        
        self.assertListEqual(_result_ids,self.test_track_ids)
        
        # unfollow the playlist
        self.sc.unfollow_playlist(_playlist_id)
        
    def test_delete_playlist(self):
    
        # create a dummy private playlist
        _playlist_id = self.sc.create_playlist(self.test_create_playlist_name)
        
        # unfollow the playlist
        self.sc.unfollow_playlist(_playlist_id)
        
        # unfollow the playlist
        self.assertFalse(self.sc.playlist_exists('foobar_playlist_id'))
        
    def test_playlist_exists(self):
        # create a dummy private playlist
        
        _playlist_id = self.sc.create_playlist(self.test_create_playlist_name)
        
        self.assertTrue(self.sc.playlist_exists(_playlist_id))
                        
        # unfollow the playlist
        self.sc.unfollow_playlist(_playlist_id)
        
    def test_playlist_does_not_exists(self):
        self.assertFalse(self.sc.playlist_exists('foobar_playlist_id'))
    
    def test_create_playlist(self):
        
        # create a dummy private playlist
        _playlist_id = self.sc.create_playlist(self.test_create_playlist_name)
        
        # assert playlist exists by searching for it and comparing ids
        self.assertTrue(self.sc.playlist_exists(_playlist_id))
        
        # unfollow the playlist
        self.sc.unfollow_playlist(_playlist_id)
    
    # ------------------------------------------------------------------------------
    
class TestSpotifyConnectorTracks(TestSpotifyConnector):
    
    
    def test_get_track_info_all(self):
        # not checking popularity because it changes !!
        # pass in a list
        print self.sc.get_track_info_all(track_ids = self.test_track_ids)
    
    def test_get_track_info(self):
        # not checking popularity because it changes !!
        # pass in a list
        track_info = self.sc.get_track_info(track_ids = self.test_track_ids)
        self.assertListEqual(self.test_track_info_list ,track_info)
        
    def test_get_track_info_nonlist_arg(self):
        #not checking popularity because it changes !!
        # pass in a non list
        track_info = self.sc.get_track_info(track_ids = self.test_artist_track_id)
        self.assertListEqual(self.test_track_info,track_info)
        
    def test_get_track_popularity_nonlist_arg(self):
        #check popularity here not in get_track_info because we can usa assertAlmostEquals
        tpops = self.sc.get_track_popularity(track_ids =self.test_artist_track_id)
        
        for i in range(0,len(tpops)):
            self.assertAlmostEqual(tpops[i],self.test_artist_track_popularity,delta=2)    

    def test_get_track_popularity(self):
        #check popularity here not in get_track_info because we can usa assertAlmostEquals
        tpops = self.sc.get_track_popularity(track_ids =self.test_track_ids)
        
        for i in range(0,len(tpops)):
            self.assertAlmostEqual(tpops[i],self.test_tracks_popularity[i],delta=2)
        
    def test_get_key_track_audio_features(self):
        tracks = self.sc.get_key_track_audio_features(track_ids = self.test_track_ids)

        for i in range(len(tracks)):
            self.assertDictEqual(self.test_tracks_audio_features[i],tracks[i])    
        
    def test_get_album_track_names(self):
        self.assertListEqual(self.sc.get_album_track_names(self.test_album_id),
                             self.test_album_tracks)
    
    def test_get_artist_top_tracks(self):
        top_tracks = self.sc.get_artist_top_tracks(self.test_artist_id)
        _top_tracks = [top_track['name'] for top_track in top_tracks]
        
        self.assertListEqual(self.test_artist_top_tracks,_top_tracks)
        
    def test_get_artist_top_n_tracks(self):
        top_tracks = self.sc.get_artist_top_n_tracks(self.test_artist_id,3)
        self.assertListEqual(self.test_artist_top_n_tracks, 
                             [self.sc.get_track_name(track_id) for track_id in top_tracks ])
    
    def test_get_album_tracks(self):
        print self.sc.get_album_tracks('1C2h7mLntPSeVYciMRTF4a')
        
class TestSpotifyConnectorMisc(TestSpotifyConnector):
    
    def test_available_genre_seeds(self):
        
        genres = self.sc.get_available_genre_seeds()
        
        self.assertIsInstance(genres.index('dubstep'),IntType)
        self.assertIsInstance(genres.index('edm'),IntType)
        self.assertIsInstance(genres.index('electro'),IntType)                     
        self.assertIsInstance(genres.index('electronic'),IntType)

    def test_recommendations(self):

        tuneables={'energy':0.9,'tempo':120}
        print self.sc.get_recommendations(seed_genres=['dubstep'],
                                          seed_artists=["5he5w2lnU9x7JFhnwcekXX"],
                                          tuneables=tuneables)
        
    def test_get_user_info(self):   
        _user_info = self.sc.get_current_user_info()
        self.assertEqual(_user_info['display_name'],'Jon Butler')
        self.assertEqual(_user_info['id'],'1165431378')
        self.assertIsInstance(_user_info['followers'],int)
       
    def test_get_artist_info(self):
        _artist_info = self.sc.get_artist_info(self.test_artist,True)
        self.assertEqual(_artist_info['name'],self.test_artist)
        self.assertEqual(_artist_info['id'], self.test_artist_id)

    def test_get_related_artists(self):
        related_artists = self.sc.get_artist_related_artist(self.test_artist_id)
        _related_artists = [related_artist['name'] for related_artist in related_artists]
        
        print sorted(_related_artists), sorted(self.test_related_artists)
        
        self.assertListEqual(sorted(_related_artists), 
                             sorted(self.test_related_artists))
        
    def test_search_spotify_tracks(self):     
        print self.sc.search_spotify_tracks(self.test_artist_track_name)

    def test_search_spotify_tracks_by_artist(self):
        print self.sc.search_spotify_tracks(self.test_artist_track_name,self.test_artist)
          
    def test_search_spotify_tracks_by_album(self):
        print self.sc.search_spotify_tracks(self.test_artist_track_name,self.test_album)
        

        
    def test_get_artist_albums(self):
        albums =  self.sc.get_artist_albums('3fMbdgg4jU18AjLCKBhRSm',['name'])
        print self.test_artist_albums, albums
        self.assertListEqual( self.test_artist_albums, albums)
            

        
    def test_get_audio_features_for_playlist(self):
        self.sc.get_audio_features_for_playlist('0FiSiu1g2mL66GmKGozKsc')
            
            
class TestSpotifyConnectorGenerator(unittest.TestCase):

    def setUp(self):
        user='1165431378'
        scope = ''
        
        # create a random name for test playlist
        self.test_playlist_name = hex(int(random.random()*pow(10,10))) 
        
        self.sc = SpotifyConnector(user,scope)
        
    def test_create_recommended_playlist(self):
        
        # create a dummy private playlist
        _playlist_id = self.sc.create_playlist(self.test_playlist_name)
        
        tuneables={'energy':0.9,'tempo':120}
        track_ids =  self.sc.get_recommendations(seed_genres=['dubstep'],
                                                    seed_artists=["5he5w2lnU9x7JFhnwcekXX"],
                                                    seed_tracks=['1LV5G400jD3Ytvyv6Dlkym'],
                                                    tuneables=tuneables)
        
        self.sc.add_track_to_playlist(_playlist_id, track_ids)
       
if __name__ == '__main__':

    suite = unittest.TestSuite()

    # playlist based tests
    #uite.addTest(TestSpotifyConnectorPlaylists("test_get_user_playlist_ids")) 
    #suite.addTest(TestSpotifyConnectorPlaylists("test_get_user_playlist_info")) 
    #suite.addTest(TestSpotifyConnectorPlaylists("test_get_user_playlist_tracks"))
    #suite.addTest(TestSpotifyConnectorPlaylists("test_add_tracks_to_playlist"))
    #suite.addTest(TestSpotifyConnectorPlaylists("test_playlist_exists"))
    #suite.addTest(TestSpotifyConnectorPlaylists("test_playlist_does_not_exists"))
    #suite.addTest(TestSpotifyConnectorPlaylists("test_delete_playlist"))
    #suite.addTest(TestSpotifyConnectorPlaylists("test_create_playlist")) 
    
    # track based tests
    
    #suite.addTest(TestSpotifyConnectorTracks("test_get_track_info_all"))
    suite.addTest(TestSpotifyConnectorTracks("test_get_track_info"))
    suite.addTest(TestSpotifyConnectorTracks("test_get_track_info_nonlist_arg"))
    suite.addTest(TestSpotifyConnectorTracks("test_get_track_popularity"))
    suite.addTest(TestSpotifyConnectorTracks("test_get_track_popularity_nonlist_arg"))
    suite.addTest(TestSpotifyConnectorTracks('test_get_key_track_audio_features'))
    suite.addTest(TestSpotifyConnectorTracks("test_get_album_track_names"))
    
    #suite.addTest(TestSpotifyConnectorTracks("test_get_artist_top_tracks"))
    #suite.addTest(TestSpotifyConnectorTracks("test_get_artist_top_n_tracks"))
    #suite.addTest(TestSpotifyConnector("test_get_user_info")) 
    #suite.addTest(TestSpotifyConnector("test_get_artist_info")) 
    #suite.addTest(TestSpotifyConnector("test_get_related_artists"))     
    #suite.addTest(TestSpotifyConnector("test_get_audio_features"))
    #suite.addTest(TestSpotifyConnector("test_get_artist_albums"))
    #suite.addTest(TestSpotifyConnector("test_available_genre_seeds")) 
    #suite.addTest(TestSpotifyConnectorGenerator('test_create_recommended_playlist'))
    #suite.addTest(TestSpotifyConnector("test_recommendations"))
    #suite.addTest(TestSpotifyConnector("test_search_spotify_tracks"))
    #suite.addTest(TestSpotifyConnector("test_search_spotify_artist"))
    #suite.addTest(TestSpotifyConnector("test_search_spotify_album"))

    
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)    