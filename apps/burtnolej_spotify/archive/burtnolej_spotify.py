
import spotify
import logging

#session = spotify.Session()
#session.process_events()
#session.process_events()
#print session.user
#print session.connection.state
#print len(session.playlist_container)


def logged_in(session, error_type):
    if error_type is spotify.ErrorType.OK:
        print('Logged in as %s' % session.user)
    else:
        print('Login failed: %s' % error_type)

logging.basicConfig(level=logging.DEBUG)
session = spotify.Session()
#album = session.get_album('spotify:album:0XHpO9qTpqJJQwa2zFxAAE')
#print album
#session.on(spotify.SessionEvent.LOGGED_IN, logged_in)
session.login("burtnolejusa","G0ldm@n1")
session.process_events()
session.process_events()
print session.connection.state
