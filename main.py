import sys
import os
import json
import logging
from czyrksys import Czyrksys
import boto
from boto.s3.key import Key
from boto.s3.connection import S3Connection

S3_BUCKET = '13fxml.com'
if 'S3_ACCESS_KEY' not in os.environ or 'S3_SECRET_KEY' not in os.environ:
    logging.error('Make sure S3_ACCESS_KEY and S3_SECRET_KEY env vars are set')
    sys.exit()
else:
    S3_ACCESS_KEY = os.environ['S3_ACCESS_KEY']
    S3_SECRET_KEY = os.environ['S3_SECRET_KEY'] 
    ROUTER_CREDS = os.environ['ROUTER_CREDS']

def s3_update():
    """
    Update the devices.json file for the web app
    """
    devices = json.dumps(Czyrksys().fetch_devices(only_active=True))
    # Need to set the calling format since we have a period in our bucket name
    OrdinaryCallingFormat = boto.config.get('s3', 'calling_format', 'boto.s3.connection.OrdinaryCallingFormat')
    conn = S3Connection(S3_ACCESS_KEY, S3_SECRET_KEY, calling_format=OrdinaryCallingFormat)
    b = conn.get_bucket(S3_BUCKET)
    k = Key(b)
    k.key = '/whoishome/devices.json'
    k.set_contents_from_string(devices)
    
if __name__ == '__main__':
    Czyrksys(ROUTER_CREDS).update_rows(only_active=True)
    s3_update()
