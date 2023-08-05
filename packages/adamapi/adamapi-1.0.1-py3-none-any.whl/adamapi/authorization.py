"""
Copyright (c) 2020 MEEO s.r.l.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os
import requests
import re
import logging
logger = logging.getLogger( 'adamapi' )

from . import AdamApiError


class Auth():
    def __init__( self, key=None, url=None ):
        """
        Authorization class used to manage users credentials
        """
        self.key = key
        self.url = url
        self.authorized = False

    def getApiKey(self,username,password):
        url=os.path.join( 'sso', 'api', 'getapikey' )
        params={
            'username':username,
            'password':password
        }
        r=self.client( url, params, "POST", authorization_required = False)
        if r.status_code in range(400,500):
            return AdamApiError(r['error'])
        else:
            return r['api_key']

    def authorize( self ):
        """
        try to autorize the adamapi to the target adam instance
        """
        #verify if key are valid
        self._check()

        url = os.path.join( 'accounts', 'api', 'auth' )
        r=self.client( url, {}, "GET", authorization_required = False )
        res = r.json()
        if r.status_code !=200:
            raise AdamApiError( res['response'] )
        else:
            logger.info( res )
            self.authorized = True
            return res[ 'response' ]

    def _check( self ):
        """
        verify if the user key and the adam url are valid
        """
        self.getKey()
        self.getAdamCore()

        if self.key is None:
            raise AdamApiError( "key can not be None" )
        if self.url is None:
            raise AdamApiError( "url (adam endpoint) can not be None" )

    def setKey( self, key ):
        """
        set the user key
        """
        self.key = key

    def setAdamCore( self, url ):
        """
        set the adam endpoint url
        """
        self.url = url

    def getKey( self ):
        """
        key priority:
        1 - use the key declared on this module
        2 - use a key exported as envvars
        3 - try to retrieve the key from $HOME/.adamapirc
        """
        if self.key is not None:
            pass
        elif os.environ.get( 'ADAMAPI_KEY') is not None:
            self.key = os.environ.get( 'ADAMAPI_KEY' )
            logger.debug( 'Get key from envvar' )
        else:
            try:
                self.key = self._getRc()[ 'key' ]
                logger.debug( 'Get key from adamapirc' )
            except:
                None
        if self.key is None: #again
            logger.warning( "API key not specified" )
        return self.key

    def getAdamCore( self ):
        """
        adam endpoint priority:
        1 - use the url declared on this module
        2 - use a url exported as envvars
        3 - try to retrieve the url from $HOME/.adamapirc
        """
        if self.url is not None:
            pass
        elif os.environ.get( 'ADAMAPI_URL') is not None:
            self.url = os.environ.get( 'ADAMAPI_URL' )
            logger.debug( 'Get url from envvar' )
        else:
            try:
                self.url = self._getRc()[ 'url' ]
                logger.debug( 'Get url from adamapirc' )
            except:
                None
        if self.url is None: #again
            logger.warning( "ADAM API endpoint not specified" )
        return self.url

    def _getRc( self ):
        """
        check if ~/.adamapirc file exist ant try to extract url and key from it
        """
        api_rc = os.environ.get( 'ADAMAPI_RC', os.path.expanduser( '~/.adamapirc' ) )
        config_dict = {}
        if os.path.isfile( api_rc ):
            with open( api_rc ) as f:
                for line in f.readlines():
                    line = line.strip()
                    if line.lstrip( '#' ) == line:
                        try:
                            key, val = line.split( '=', 1 )
                            config_dict[ key.strip() ] = val.strip()
                        except:
                            logger.warning( 'Invalid settings in "%s" - %s' %( api_rc, line ) )
        return config_dict

    def client( self, query, params, request_type, authorization_required = True ):
        """
        The client method that perform the request appending the Authorization header
        """
        
        #verify if the user already call the authorize method of the Auth instance
        if authorization_required and not self.authorized:
            self.authorize()

        headers={ 'Authorization': self.key }
        #verify if the passed url already include the host or if the adamcore url have to be prepended
        if re.match( r'^http[s]?://.+', query ):
            url = query
        else:
            url = os.path.join( self.url, query )

        if request_type not in [ 'GET', 'POST' ]:
            raise AdamApiError( "Request type not supported" )

        logger.info( "%s request started", request_type )
        if request_type == 'GET':
            r=requests.get( url, params=params,headers=headers )
        elif request_type == 'POST':
            r=requests.post( url,data=params,headers=headers )
        r.raise_for_status()
        return r
