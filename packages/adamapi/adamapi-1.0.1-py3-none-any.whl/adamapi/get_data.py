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
from osgeo import gdal,ogr
from matplotlib import pyplot as plt
import imageio
import json
import requests
import errno

import logging
logger=logging.getLogger('adamapi')

from . import AdamApiError

class GetData(object):
    def __init__(self,client):
        self.LOG=logger
        self.client=client

    def getData(self, datasetId, timeStart=None, timeEnd=None, geometry=None, tile=None, outputFormat='tif', scale=None, outputFname=None, cache=False ):
        """
        Method to retrive tif,png,gif
        @ datasetId: datasetId, required
        @ timeStart: available start date in format %Y-%m-%d to retrive the image, required
        @ timeEnd: available end date in format %y-%m-%d to retrive the image, required
        @ geometry: searchin bbox to subset the image
        @ tile: mgrs_tile or path and row
        @ outputFormat: the output_file extension(tif,png,gif,urlpng,urltif), default tif
        @ scale: scaling image parameter
        @ outputFname: output filename
        """

        if timeStart is None:
            raise AdamApiError( 'timeStart is required' )
        if timeEnd is None:
            timeEnd = timeStart
        timeEnd_have_HHMMSS = self._have_HHMMSS( timeEnd )

        supported_out = [ 'tif', 'gif', 'png', 'png_preview' ]
        if outputFormat not in supported_out:
            raise AdamApiError( 'outputFormat %s not supported. %s' %( outputFormat, str( supported_out ) ) )
        if outputFormat == 'gif' and outputFname is None:
            outputFname = datasetId.replace( ':','_')


        timeStart  = self._stringToDate( timeStart )
        timeEnd    = self._stringToDate( timeEnd )
        timeTarget = timeEnd
        if timeStart > timeEnd:
            raise AdamApiError( 'timeStart is greater than timeEnd' )


        delta = timedelta( days=1 )
        params = {}
        url_list = []
        filename_list = []
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
                'product': datasetId.split(":",1)[0],
                'scale': scale,
                'cache': cache,
                'type': 'api'
            }

            if tile:
                params['tile']=tile

            try:
                if geometry:
                    if type(geometry) is str:
                        params['wkt_string'] = ogr.CreateGeometryFromJson(geometry).ExportToWkt()
                    elif type(geometry) is dict:
                        params['wkt_string'] = ogr.CreateGeometryFromJson(json.dumps(geometry)).ExportToWkt()
                    response=self.client.client(os.path.join('subset','subset.json'),params,"POST")
                    self.LOG.info("Get Data request executed")
                else:
                    response=self.client.client(os.path.join('subset','subset.json'),params,"GET")
                    self.LOG.info("Get Data request executed")
            except requests.exceptions.HTTPError as er:
                #if response.status_code != 200:
                timeTarget -= delta
                continue
            else:
                response=response.json()
                for(key,value)  in response.items():
                    try:
                        subset_resp=response['merge']
                    except:
                        subset_resp=response[key]

                    if outputFormat in [ 'png', 'gif' ]:
                        raster_url = os.path.join( self.client.getAdamCore(), 'media', 'maps', subset_resp['mapserver'] )
                    elif outputFormat == 'tif':
                        raster_url = os.path.join( self.client.getAdamCore(), 'media', 'maps', subset_resp['merged'] )
                    elif outputFormat == 'png_preview':
                        raster_url = os.path.join( self.client.getAdamCore(), 'media', 'maps', subset_resp['final'] )

                    url_list.append( raster_url )
                    #save data
                    if outputFname is not None:
                        fname = outputFname + "_" + timeTarget.strftime("%Y-%m-%d") + "_" + str(index) + "." + outputFormat
                        filename_list.append( fname )
                        image_response = self.client.client( raster_url, {} , "GET" )
                        self._checkDirFile(fname)
                        with open( fname, 'wb' ) as f:
                            f.write( image_response.content )
            #dec target date
            timeTarget -= delta

        images = []
        if outputFormat=='gif':
            for image in filename_list:
                images.append(imageio.imread(image))
                os.remove( image )
            gif_name = outputFname + ".gif"
            self._checkDirFile(gif_name)
            imageio.mimsave( gif_name, images, duration=1 )
            filename_list = [ gif_name ]

        self.LOG.info("Get Data request finished and image produced")

        if outputFname is None:
            return url_list
        else:
            return filename_list


    def getChart( self, datasetId, timeStart=None, timeEnd=None, latitude=None, longitude=None, outputFormat='json', outputFname=None, tile=None ):
        """
        Method to retrive an ADAM chart in format json or png
        @ datasetId:  datasetId, required
        @ timeStart: available start date in format %Y-%m-%d to retrive the image, required
        @ timeEnd: available end date in format %y-%m-%d to retrive the image, required
        @ latitude: value of the latitude point
        @ longitude: value of the longitude point
        @ outputFormat: the output_file extension(tif,png,gif), default tif
        @ outputFname: output filename
        @ tile: optional,only for sentinel and landsat products
        """
        if timeStart is None or timeEnd is None or latitude is None or longitude is None:
            raise AdamApiError( 'Required parameter missed, latitude, longitude, timeStart and timeEnd are required' )
        supported_out = [ 'png', 'json' ]
        if outputFormat not in supported_out:
            raise AdamApiError( 'outputFormat %s not supported. %s' %( outputFormat, str( supported_out ) ) )
        if outputFormat == 'png' and outputFname is None:
            outputFname = datasetId.replace( ':','_')

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
        params['lat'] = latitude
        params['lon'] = longitude
        params['type']='api'

        if tile:
            params['tile']=tile

        response=self.client.client(os.path.join('chart','chart.json'),params,"GET")
        serie=response.json()
        if outputFormat=='json':
            filename=serie
        else:
            for s in serie['serie']:
                dates.append(s[0])
                values.append(s[1])

            plt.figure(figsize=(12,7))
            plt.xticks(rotation = -45)
            plt.xlabel('DATE',fontweight = 'bold', fontsize = 15)
            plt.ylabel(serie['ylabel'], fontweight = 'bold', fontsize = 15)
            plt.title(serie['label']+" from "+timeStart+" to "+timeEnd, fontweight = 'bold', fontsize = 20,pad = 20)
            plt.plot(dates,values)
            filename=outputFname+".png"
            plt.savefig(filename)

        return filename

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
            '%Y%m%d',
            '%Y-%m-%d'
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
