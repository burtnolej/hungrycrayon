#!/usr/bin/env python

import cmd
import locale
import os
import pprint
import shlex
import sys

from dropbox import client, rest, session

APP_KEY="0h9v6zkbl1td5ga"
APP_SECRET="3nks9h0tx37qihp"

class DropboxTerm(cmd.Cmd):
    TOKEN_FILE = "token_store.txt"

    def __init__(self, app_key, app_secret):
        cmd.Cmd.__init__(self)
        self.app_key = app_key
        self.app_secret = app_secret
        self.current_path = ''
        self.prompt = "Dropbox> "

        self.api_client = None
        try:
            serialized_token = open(self.TOKEN_FILE).read()
            if serialized_token.startswith('oauth1:'):
                access_key, access_secret = serialized_token[len('oauth1:'):].split(':', 1)
                sess = session.DropboxSession(self.app_key, self.app_secret)
                sess.set_token(access_key, access_secret)
                self.api_client = client.DropboxClient(sess)
                print "[loaded OAuth 1 access token]"
            elif serialized_token.startswith('oauth2:'):
                access_token = serialized_token[len('oauth2:'):]
                self.api_client = client.DropboxClient(access_token)
                print "[loaded OAuth 2 access token]"
            else:
                print "Malformed access token in %r." % (self.TOKEN_FILE,)
        except IOError:
            print "not there"
            pass # don't worry if it's not there


def main():
    if APP_KEY == '' or APP_SECRET == '':
        exit("You need to set your APP_KEY and APP_SECRET!")
    term = DropboxTerm(APP_KEY, APP_SECRET)
    term.cmdloop()

if __name__ == '__main__':
    main()

