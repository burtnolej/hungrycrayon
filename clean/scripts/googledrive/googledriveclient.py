from __future__ import print_function
import httplib2
import os
import io

from apiclient import discovery
from apiclient.http import MediaIoBaseDownload

import googleapiclient

from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

from datetime_util import MyDT
import datetime
import pickle

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

fields = ['name','id','mimeType','modifiedTime','lastModifyingUser']

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
#SCOPES = 'https://www.googleapis.com/auth/drive.metadata.readonly'
SCOPES = 'https://www.googleapis.com/auth/drive.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Drive API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'drive-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def download(http,dir,fileid,mimeType,filename):
    
    service = discovery.build('drive', 'v3', http=http)
    request = service.files().export_media(fileId=fileid,mimeType=mimeType)
    
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download {0}".format(int(status.progress() * 100)))

    filename = filename.replace(" ","")
    filepath = os.path.join(dir,filename)

    with open(filepath,'wb') as out:
            out.write(fh.getvalue()) 
    
def gdrivelist(http):
        
    service = discovery.build('drive', 'v3', http=http)
    
    field_str = "nextPageToken, files({0})".format(",".join(fields))
    
    results = service.files().list(pageSize=50,fields=field_str).execute()
    items = results.get('files', [])
      
    return(items)

def gdrivegetlastfilerevisiontime(http,fileId):
    
    service = discovery.build('drive', 'v3', http=http)
    
    results = service.revisions().list(fileId=fileId).execute()
    
    #for revision in results['revisions']:
    #    
    #    print(revision['modifiedTime'],revision['id'])
        
    return(results['revisions'][-1]['modifiedTime'])

def gdrivegetrevisioncontent(http,fileId,revid):
    
    service = discovery.build('drive', 'v3', http=http)
    
    fields = ["kind"]
    
    field_str = "files({0})".format(",".join(fields))
    
    results = service.revisions().get(fileId=fileId,revisionId=revid).execute()
    
def main():


    #gfilesofinterest = ['Prep 4 Individual Schedules','Prep 4 schedule new work period','Prep 5 and 6 schedule new work period',
    #          'Prep 6 Individual Schedules','Copy of Prep 5 Individual Schedules']

    gfilesofinterest = ['Prep 4 Individual Schedules',
                        'Prep 4 schedule new work period',
                        'Prep 5 and 6 schedule new work period',
                        'Prep 6 Individual Schedules',
                        'Prep 5 Individual Schedules',
                        'Prep 5 Individual Schedules - 2nd Semester',
                        'Prep 6 Individual Schedules - 2nd Semester',
                        'Master Schedule Prep 5 & 6',
                        'Stan Schedule',
                        'Sonja Schedule',
                        'Samantha Schedule',
                        'Aaron Schedule',
                        'Dylan Schedule',
                        'Issey Schedule',
                        'Jess Schedule',
                        'Karolina Schedule',
                        'Moira Schedule',
                        'Alyssa L. Schedule',
                        'Paraic Schedule',
                        'Thea Schedule',
                        'Jacki Schedule',
                        'Amelia Schedule',
                        'Eric Schedule']  
    

    picklefilename = "metastore.dat"
    
    #dir = "/mnt/bumblebee-burtnolej/googledrive"
    dir = "googledrive"
    cdir = os.path.join(dir,"current")

    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    
    gfilelist = gdrivelist(http)
     
    #for gfile in gfilelist:
    #    print(gfile['name'])
    #exit()
    
    store = {}
    
    now = datetime.datetime.now().strftime('%y%m%d-%H%M%S')

    targetdir = os.path.join(dir,now)

    nohistory = False
    
    try:
        with open(picklefilename,"r") as f:
            prevstore = pickle.load(f)
    except IOError: # no history file
        nohistory = True
    
    for gfile in gfilelist:

        if gfile['name'] in gfilesofinterest:
            filemeta = {}
            filemeta['name'] = gfile['name']
            filemeta['id'] = gfile['id']

            try:
                lastmodtime = gdrivegetlastfilerevisiontime(http,gfile['id'])
                mydt = MyDT.str('US/Eastern',dt_str=lastmodtime[:-1],dt_str_fmt='%Y-%m-%dT%H:%M:%S.%f')
            
                filemeta['lastmodsecs'] = mydt.secs
                filemeta['lastmod'] = str(mydt)
                
                if nohistory == True:
                    print("no history, downloading")
                elif filemeta['lastmodsecs'] > prevstore[gfile['id']]['lastmodsecs']:
                    print(filemeta['name']," has changed, downloading")
                    pass
                else:
                    print(filemeta['name']," has not changed,skipping: ",prevstore[gfile['id']]['lastmod'])
                    continue
                
                try:
                    os.mkdir(targetdir)
                except OSError: # already created
                    pass
            

                filemeta['lastmodtag'] = now # name of directory where files downloaded too
            
                store[gfile['id']] = filemeta
                    
                    
            except googleapiclient.errors.HttpError, e:
                print(filemeta['name'],"The file does not support revisions.")
                
            downloadtype = None
            
            if gfile['mimeType'] == 'application/vnd.google-apps.spreadsheet':
                downloadtype = 'application/x-vnd.oasis.opendocument.spreadsheet'
                fileext = "ods"
            elif gfile['mimeType'] == 'application/vnd.google-apps.document':
                downloadtype = 'application/vnd.oasis.opendocument.text'
                fileext = "odt"
                
            if downloadtype <> None:
                download(http,targetdir,gfile['id'],downloadtype,gfile['name'] + "." + fileext)

    if store <> {}:
        with open(picklefilename, 'w') as f:
            pickle.dump(store, f)
            
        try:
            os.remove(cdir)
        except OSError:
            pass # doesnt exist
        os.symlink(targetdir,cdir)
        
    else:
        print("no revisions found, not updating pickle")
    
    print(targetdir,cdir)
if __name__ == '__main__':
    main()
