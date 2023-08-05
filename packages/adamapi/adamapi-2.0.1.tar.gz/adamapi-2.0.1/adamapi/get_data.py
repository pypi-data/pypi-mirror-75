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


from datetime import timedelta, datetime, timezone
import os
from osgeo import ogr
import imageio
import json
import requests
import errno
import csv

import logging
logger=logging.getLogger('adamapi')

from . import AdamApiError

class GetData(object):
    def __init__(self,client):
        self.LOG=logger
        self.client=client
        self.default_getdata_kwargs={'outputFormat':'tif','cache':False}
        self.default_getchart_kwargs={'outputFormat':'json'}

    def getData(self, datasetId, timeStart, **kwargs):
        """
        Method to retrive tif,png,gif
        @ datasetId: datasetId, required
        @ timeStart: available start date in format %Y-%m-%d to retrive the image, required
        @ timeEnd: available end date in format %y-%m-%d to retrive the image, required
        @ geometry: searchin bbox to subset the image
        @ tile: mgrs_tile or path and row
        @ outputFormat: the output_file extension(tif,png,gif,png_preview), default tif
        @ scale: scaling image parameter
        @ outputFname: output filenaime
        @ filter: dafault true
        """
        self._initializeDefaultValue('getdata',kwargs,timeStart=timeStart)

        timeEnd_have_HHMMSS = self._have_HHMMSS( kwargs['timeEnd'] )

        supported_out = [ 'tif', 'gif', 'png', 'png_preview' ]
        if kwargs['outputFormat'] not in supported_out:
            raise AdamApiError( 'outputFormat %s not supported. %s' %( kwargs['outputFormat'], str( supported_out ) ) )
        if kwargs['outputFormat'] == 'gif' and ( kwargs['outputFname'] is None or 'outputFname' not in kwargs.keys()):
            kwargs['outputFname'] = datasetId.replace( ':','_')

        timeStart  = self._stringToDate( timeStart )
        timeEnd    = self._stringToDate( kwargs['timeEnd'] )
        timeTarget = timeEnd
        if timeStart > timeEnd:
            raise AdamApiError( 'timeStart is greater than timeEnd' )

        delta = timedelta( days=1 )
        params = {}
        url_list = []
        filename_list = []
        errorResponse=None
        while timeTarget.date() >= timeStart.date():
            index=0
            #handle different time format start date and end date
            if timeTarget.date() == timeStart.date():
                start_date_str = timeStart.strftime( '%Y-%m-%dT%H:%M:%SZ' )
            else:
                start_date_str = timeTarget.strftime( '%Y-%m-%dT00:00:00Z' )
            if timeTarget.date() == timeEnd.date() and timeEnd_have_HHMMSS:
                end_date_str = timeEnd.strftime( '%Y-%m-%dT%H:%M:%SZ' )
            else:
                end_date_str = timeTarget.strftime( '%Y-%m-%dT23:59:59Z' )
            params = {
                'start_date': start_date_str,
                'end_date': end_date_str,
                'dataset_id': datasetId.split(":",1)[0],
                'type': 'api'
            }
            if 'timeEnd' in kwargs.keys():
                del kwargs['timeEnd']

            params.update(kwargs)

            try:
                if 'geometry' in kwargs.keys() and kwargs['geometry'] is not None:
                    if type(kwargs['geometry']) is str:
                        params['wkt_string'] = ogr.CreateGeometryFromJson(kwargs['geometry']).ExportToWkt()
                    elif type(kwargs['geometry']) is dict:
                        params['wkt_string'] = ogr.CreateGeometryFromJson(json.dumps(kwargs['geometry'])).ExportToWkt()
                    response=self.client.client(os.path.join('subset','subset.json'),params,"POST", force_raise = True )
                    self.LOG.info("Get Data request executed")
                else:
                    response=self.client.client(os.path.join('subset','subset.json'),params,"GET", force_raise = True )
                    self.LOG.info("Get Data request executed")
            except requests.exceptions.HTTPError as er:
                errorResponse=er
                self.LOG.error(er.response.json()['message'])
                timeTarget -= delta
                continue
            else:
                response=response.json()
                for(key,value)  in response.items():
                    try:
                        subset_resp=response['merge']
                    except:
                        subset_resp=response[key]

                    if kwargs['outputFormat'] in [ 'png', 'gif' ]:
                        raster_url = os.path.join( self.client.getAdamCore(), 'media', 'maps', subset_resp['mapserver'] )
                    elif kwargs['outputFormat'] == 'tif':
                        raster_url = os.path.join( self.client.getAdamCore(), 'media', 'maps', subset_resp['warped'] )
                    elif ['outputFormat'] == 'png_preview':
                        raster_url = os.path.join( self.client.getAdamCore(), 'media', 'maps', subset_resp['final'] )

                    url_list.append( raster_url )
                    #save data
                    if 'outputFname' in kwargs.keys() and kwargs['outputFname'] is not None:
                        fname = kwargs['outputFname'] + "_" + timeTarget.strftime("%Y-%m-%d") + "_" + str(index) + "." + kwargs['outputFormat']
                        filename_list.append( fname )
                        image_response = self.client.client( raster_url, {} , "GET" )
                        self._checkDirFile(fname)
                        with open( fname, 'wb' ) as f:
                            f.write( image_response.content )
            #dec target date
            timeTarget -= delta

        images = []
        if kwargs['outputFormat']=='gif':
            for image in filename_list:
                images.append(imageio.imread(image))
                os.remove( image )
            gif_name = kwargs['outputFname'] + ".gif"
            self._checkDirFile(gif_name)
            imageio.mimsave( gif_name, images, duration=1 )
            filename_list = [ gif_name ]

        self.LOG.info("Get Data request finished and image produced")

        if 'outputFname' in kwargs.keys() and kwargs['outputFname'] is None:
            if not url_list:
                raise AdamApiError(errorResponse.response.json()['title'])
            else:
                return url_list
        else:
            if not filename_list:
                raise AdamApiError(errorResponse.response.json()['title'])
            else:
                return filename_list

    def getChart(self,datasetId,timeStart,timeEnd,**kwargs):
        """
        Method to retrive an ADAM chart in format json or png
        @ datasetId:  datasetId, required
        @ timeStart: available start date in format %Y-%m-%d to retrive the image, required
        @ timeEnd: available end date in format %y-%m-%d to retrive the image, required
        @ latitude: value of the latitude point
        @ longitude: value of the longitude point
        @ outputFormat: the output_file extension(json,csv) default json
        @ outputFname: output filename
        @ tile: optional,only for sentinel and landsat products
        """
        self._initializeDefaultValue('getchart',kwargs)

        supported_out = [ 'csv', 'json' ]
        if kwargs['outputFormat'] not in supported_out:
            raise AdamApiError( 'outputFormat %s not supported. %s' %( kwargs['outputFormat'], str( supported_out ) ) )
        if kwargs['outputFormat'] == 'csv' and ('outputFname' not in kwargs.keys() or kwargs['outputFname'] is None):
            kwargs['outputFname'] = datasetId.replace( ':','_')

        if self._have_HHMMSS( timeStart ):
            timeStart = self._stringToDate( timeStart ).strftime('%Y-%m-%dT%H:%M:%SZ')
        else:
            timeStart = self._stringToDate( timeStart ).strftime('%Y-%m-%dT00:00:00Z')
        if self._have_HHMMSS( timeEnd ):
            timeEnd = self._stringToDate( timeEnd ).strftime('%Y-%m-%dT%H:%M:%SZ')
        else:
            timeEnd = self._stringToDate( timeEnd ).strftime('%Y-%m-%dT23:59:59Z')

        params={}
        values=[]
        dates=[]
        params['pid'] = datasetId.split(':',1)[0]
        params['start_date'] = timeStart
        params['end_date'] = timeEnd
        params['lat'] = kwargs['latitude'] if 'latitude' in kwargs.keys() else None
        params['lon'] = kwargs['longitude'] if 'longitude' in kwargs.keys() else None
        params['type']='api'

        params.update(kwargs)

        response=self.client.client(os.path.join('chart','chart.json'),params,"GET")
        serie=response.json()
        if kwargs['outputFormat']=='json':
            filename=serie
        else:
            csv_name = kwargs['outputFname'] + ".csv"
            self._checkDirFile(csv_name)
            filename=csv_name
            with open(csv_name,"w",newline='') as csv_file:
                writer=csv.writer(csv_file,delimiter='|')
                writer.writerow(['Date','Value','Unit'])
                for s in serie["serie"]:
                    writer.writerow([s[0],s[1],serie['ylabel']])

        return filename

    def _initializeDefaultValue(self,function,args_dict,timeStart=None):
        if function=='getdata':
            default_kwargs=self.default_getdata_kwargs
        else:
            default_kwargs=self.default_getchart_kwargs

        for (key,value) in default_kwargs.items():
            if key not in args_dict:
                args_dict[key]=value
        if timeStart:
            if 'timeEnd' not in args_dict.keys() or args_dict['timeEnd'] is None:
                args_dict['timeEnd']=timeStart

    def _stringToDate( self, datestr ):
        """
        Convert string to date
        """
        fmt_list = [
            '%Y.%m.%d %H:%M:%S',
            '%Y%m%d %H:%M:%S',
            '%Y-%m-%dT%H:%M:%S',
            '%Y-%m-%dT%H:%M:%S.%f',
            '%Y-%m-%dT%H:%M:%SZ',
            '%Y-%m-%dT%H:%M:%S.%fZ',
            '%Y-%m-%d %H:%M:%S',
            '%Y.%m.%d',
            '%Y-%m-%d',
            '%Y%m%d'
        ]

        if isinstance( datestr, datetime ):
            return datestr

        terget_date = None
        for fmt in fmt_list:
            try:
                terget_date = datetime.strptime( datestr, fmt ).replace( tzinfo = timezone.utc )
                break
            except Exception as ex:
                None

        if terget_date is None:
            raise AdamApiError( 'Format not recognised for date %s' %( datestr ) )
        return terget_date


    def _have_HHMMSS( self, datestr ):
        """
        verify if a temporal parameter have time hh:mm:ss or not
        """
        fmt_list = [
            '%Y.%m.%d %H:%M:%S',
            '%Y%m%d %H:%M:%S',
            '%Y-%m-%dT%H:%M:%S',
            '%Y-%m-%dT%H:%M:%S.%f',
            '%Y-%m-%dT%H:%M:%SZ',
            '%Y-%m-%dT%H:%M:%S.%fZ',
            '%Y-%m-%d %H:%M:%S'
        ]
        for fmt in fmt_list:
            try:
                terget_date = datetime.strptime( datestr, fmt ).replace( tzinfo = timezone.utc )
                return True
            except Exception as ex:
                None
        return False



    def _checkDirFile(self,filename):
        dirname = os.path.dirname( filename )
        if dirname.strip():
            try:
                os.makedirs( dirname )
            except OSError as ose:
                if ose.errno!=errno.EEXIST:
                    raise AdamApiError( ose )
