#!/usr/bin/python

import glob
import json
import os
import os.path
import requests
import sys
import time
import xml.dom.minidom
import yaml

try:
    xmlFile = sys.argv[1]
except Exception as e:
    print str(e)
    sys.exit(0)

apic = sys.argv[2]

with open( xmlFile, 'r' ) as config:
    config = yaml.safe_load( config )


auth = {
    'aaaUser': {
        'attributes': {
            'name': 'admin',
            'pwd': 'password'
            }
        }
    }

status = 0
while( status != 200 ):
    url = 'http://%s/api/aaaLogin.json' % apic
    while(1):
        try:
            r = requests.post( url, data=json.dumps(auth), timeout=1, verify=False )
            break;
        except Exception as e:
            print "timeout"
    status = r.status_code
    print r.text
    cookies = r.cookies
    time.sleep(1)

def runConfig( status ):
            with open( cfgFile, 'r' ) as payload:
                if( status==200):
                    time.sleep(5)
                else:
                    raw_input( 'Hit return to process %s' % cfgFile )

                data = payload.read()
                print '++++++++ REQUEST (%s) ++++++++' % cfgFile
                print data
                print '-------- REQUEST (%s) --------' % cfgFile
                url = 'http://%s/api/node/mo/.xml' % apic
                r = requests.post( url,
                                   cookies=cookies,
                                   data=data, verify=False )
                result = xml.dom.minidom.parseString( r.text )
                status = r.status_code
                print '++++++++ RESPONSE (%s) ++++++++' % cfgFile
                print result.toprettyxml()
                print '-------- RESPONSE (%s) --------' % cfgFile
                print status

runConfig( status )
