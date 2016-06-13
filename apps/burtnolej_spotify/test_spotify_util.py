
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
        
        self.sc = SpotifyConnector(user,scope)

    def tearDown(self):
        del self.sc
        
    def test_get_user_info(self):   
        _user_info = self.sc.get_current_user_info()
        self.assertEqual(_user_info['display_name'],'Jon Butler')
        self.assertEqual(_user_info['id'],'1165431378')
        self.assertIsInstance(_user_info['followers'],int)
       
    def test_get_artist_info(self):
        
        _artist_info = self.sc.get_artist_info('Michael Jackson',True)
        self.assertEqual(_artist_info['name'],'Michael Jackson')
        self.assertEqual(_artist_info['id'],'3fMbdgg4jU18AjLCKBhRSm')
        
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
    suite.addTest(TestSpotifyConnectorRead("test_get_playlist_tracks")) 
    suite.addTest(TestSpotifyConnectorRead("test_get_user_info")) 
    suite.addTest(TestSpotifyConnectorRead("test_get_artist_info")) 
    suite.addTest(TestSpotifyConnectorWrite("test_create_public_playlist")) 
    suite.addTest(TestSpotifyConnectorWrite("test_add_tracks_to_playlist")) 

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)    