import numpy as np
import cv2
import requests
import os
import imutils
import json
import base64
import subprocess
from pyzm.helpers.Base import Base

class AlprBase(Base):
    def __init__(self, logger=None,options={}, alpr_options={}, url=None, apikey=None, tempdir='/tmp'):
        super().__init__(logger)
        if not apikey:
            self.logger.Debug (1,'No API key specified, hopefully you do not need one')
        self.apikey = apikey
        #print (self.apikey)
        self.tempdir = tempdir
        self.url = url
        self.options = options
        self.alpr_options = alpr_options

    def setkey(self, key=None):
        self.apikey = key
        self.logger.Debug(2,'Key changed')

    def stats(self):
        self.logger.Debug(1,'stats not implemented in base class')

    def detect(self, object):
        self.logger.Debug(1,'detect not implemented in base class')

    def prepare(self, object):
        if not isinstance(object, str):
            self.logger.Debug(
                1,'Supplied object is not a file, assuming blob and creating file'
            )
            self.filename = self.tempdir + '/temp-plate-rec.jpg'
            cv2.imwrite(filename, object)
            self.remove_temp = True
        else:
            self.logger.Debug(1,f'supplied object is a file {object}')
            self.filename = object
           
            self.remove_temp = False
  

    def getscale(self):
        if self.options.get('resize') and self.options.get('resize') != 'no':
            img = cv2.imread(self.filename)
            img_new = imutils.resize(img,
                                     width=min(int(self.options.get('resize')),
                                               img.shape[1]))
            oldh, oldw, _ = img.shape
            newh, neww, _ = img_new.shape
            rescale = True
            xfactor = neww / oldw
            yfactor = newh / oldh
            img = None
            img_new = None
            self.logger.Debug(
                2,'ALPR will use {}x{} but Object uses {}x{} so ALPR boxes will be scaled {}x and {}y'
                .format(oldw, oldh, neww, newh, xfactor, yfactor))
        else:
            xfactor = 1
            yfactor = 1
        return (xfactor, yfactor)


class PlateRecognizer(AlprBase):
    def __init__(self, url=None, apikey=None, options={}, alpr_options={}, tempdir='/tmp'):
        """Wrapper class for platerecognizer.com

        Args:
            url (string, optional): URL for service. Defaults to None.
            apikey (string, optional): API key. Defaults to None.
            options (dict, optional): Config options. Defaults to {}.
            alpr_options (dict, optional): Various ALPR options. Defaults to {}.
            tempdir (str, optional): Path to store image for analysis. Defaults to '/tmp'.
        """        
        AlprBase.__init__(self, options=options,  alpr_options=alpr_options, url=url, apikey=apikey, tempdir=tempdir)
        if not url:
            self.url = 'https://api.platerecognizer.com/v1'

        self.logger.Debug(
            1,'PlateRecognizer ALPR initialized with options: {} and url: {}'.
            format(alpr_options, self.url))
        self.options = options

    def stats(self):
        """Returns API statistics

        Returns:
            HTTP Response: HTTP response of statistics API
        """        
        if self.alpr_options.get('alpr_api_type') != 'cloud':
            self.logger.Debug (1,'local SDK does not provide stats')
            return {}
        try:
            if self.apikey:
                 headers={'Authorization': 'Token ' + self.apikey}
            else:
                headers={}
            response = requests.get(
                self.url + '/statistics/',
               headers=headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            response = {'error': str(e)}
        else:
            response = response.json()
        return response

    def detect(self, object):
        """Detects license plate using platerecognizer

        Args:
            object (image): image buffer

        Returns:
            boxes, labels, confidences: 3 objects, containing bounding boxes, labels and confidences
        """        
        bbox = []
        labels = []
        confs = []
        alpr_options = self.alpr_options
        self.prepare(object)
        if alpr_options.get('stats') == 'yes':
            self.logger.Debug(1,'Plate Recognizer API usage stats: {}'.format(
                json.dumps(self.stats())))
        with open(self.filename, 'rb') as fp:
            try:
                platerec_url = self.url
                if self.alpr_options.get('alpr_api_type') == 'cloud':
                    platerec_url += '/plate-reader'
                payload = self.alpr_options.get('regions')
                response = requests.post(
                   platerec_url,
                    #self.url ,
                    files=dict(upload=fp),
                    data=payload,
                    headers={'Authorization': 'Token ' + self.apikey})
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                response = {
                    'error':
                    f'Plate recognizer rejected the upload with: {e}.',
                    'results': []
                }
                self.logger.Error(
                    f'Plate recognizer rejected the upload with {e}'
                )
            else:
                response = response.json()
                self.logger.Debug(2,'ALPR JSON: {}'.format(response))

        (xfactor, yfactor) = self.getscale()

        if self.remove_temp:
            os.remove(filename)

        if response.get('results'):
            for plates in response.get('results'):
                label = plates['plate']
                dscore = plates['dscore']
                score = plates['score']
                if dscore >= alpr_options.get('min_dscore') and score >= alpr_options.get(
                        'min_score'):
                    x1 = round(int(plates['box']['xmin']) * xfactor)
                    y1 = round(int(plates['box']['ymin']) * yfactor)
                    x2 = round(int(plates['box']['xmax']) * xfactor)
                    y2 = round(int(plates['box']['ymax']) * yfactor)
                    labels.append(label)
                    bbox.append([x1, y1, x2, y2])
                    confs.append(plates['score'])
                else:
                    self.logger.Debug(
                        1,'ALPR: discarding plate:{} because its dscore:{}/score:{} are not in range of configured dscore:{} score:{}'
                        .format(label, dscore, score, alpr_options.get('min_dscore'),
                                alpr_options.get('min_score')))

        self.logger.Debug (2,'Exiting ALPR with labels:{}'.format(labels))
        return (bbox, labels, confs)


class OpenAlpr(AlprBase):
    def __init__(self, options={}, alpr_options={}, url=None, apikey=None, tempdir='/tmp'):
        """Wrapper class for Open ALPR service

        Args:
            options (dict, optional): Various ALPR options. Defaults to {}.
            alpr_options (dict, optional): Various ALPR options. Defaults to {}.
            url (string, optional): URL for service. Defaults to None.
            apikey (string, optional): API Key for service. Defaults to None.
            tempdir (str, optional): Temporary path to analyze image. Defaults to '/tmp'.
        """
        AlprBase.__init__(self, url=url,options=options, alpr_options=alpr_options, apikey=apikey, tempdir=tempdir)
        if not url:
            self.url = 'https://api.openalpr.com/v2/recognize'

        self.logger.Debug(
            1,'Open ALPR initialized with options {} and url: {}'.
            format(alpr_options, self.url))
        self.alpr_options = alpr_options
        self.options = options

    def detect(self, object):
        """Detection using OpenALPR

        Args:
            object (image): image buffer

        Returns:
            boxes, labels, confidences: 3 objects, containing bounding boxes, labels and confidences
        """        
        bbox = []
        labels = []
        confs = []

        self.prepare(object)
     
        with open(self.filename, 'rb') as fp:
            try:
                alpr_options = self.alpr_options
                params = ''
                if alpr_options.get('country'):
                    params = params + '&country=' + alpr_options.get('country')
                if alpr_options.get('state'):
                    params = params + '&state=' + alpr_options.get('state')
                if alpr_options.get('recognize_vehicle'):
                    params = params + '&recognize_vehicle=' + \
                        str(alpr_options.get('recognize_vehicle'))

                rurl = '{}?secret_key={}{}'.format(self.url, self.apikey,
                                                   params)
                self.logger.Debug(1,'Trying OpenALPR with url:' + rurl)
                response = requests.post(rurl, files={'image': fp})
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                response = {
                    'error':
                    f'Open ALPR rejected the upload with {e}',
                    'results': []
                }
                self.logger.Debug(
                    1,f'Open APR rejected the upload with {e}'
                )
            else:
                response = response.json()
                self.logger.Debug(1,'OpenALPR JSON: {}'.format(response))

        (xfactor, yfactor) = self.getscale()

        rescale = False

        if self.remove_temp:
            os.remove(filename)

        if response.get('results'):
            for plates in response.get('results'):
                label = plates['plate']
                conf = float(plates['confidence']) / 100
                if conf < options.get('min_confidence'):
                    self.logger.Debug(
                        1,'OpenALPR: discarding plate: {} because detected confidence {} is less than configured min confidence: {}'
                        .format(label, conf, alpr_options.get('min_confidence')))
                    continue

                if plates.get(
                        'vehicle'):  # won't exist if recognize_vehicle is off
                    veh = plates.get('vehicle')
                    for attribute in ['color', 'make', 'make_model', 'year']:
                        if veh[attribute]:
                            label = label + ',' + veh[attribute][0]['name']

                x1 = round(int(plates['coordinates'][0]['x']) * xfactor)
                y1 = round(int(plates['coordinates'][0]['y']) * yfactor)
                x2 = round(int(plates['coordinates'][2]['x']) * xfactor)
                y2 = round(int(plates['coordinates'][2]['y']) * yfactor)
                labels.append(label)
                bbox.append([x1, y1, x2, y2])
                confs.append(conf)

        return (bbox, labels, confs)

class OpenAlprCmdLine(AlprBase):
    def __init__(self, cmd=None, options={}, tempdir='/tmp'):
        """Wrapper class for OpenALPR command line utility

        Args:
            cmd (string, optional): The cli command. Defaults to None.
            options (dict, optional): Various ALPR options. Defaults to {}.
            tempdir (str, optional): Temporary path to analyze image. Defaults to '/tmp'.
        """        
        AlprBase.__init__(self, options=options, url='unused', apikey='unused', tempdir=tempdir)
        self.options = options
        self.cmd = cmd + ' ' + self.options.get('openalpr_cmdline_params')
        if self.cmd.lower().find('-j') == -1:
            self.logger.Debug (2,'Adding -j to OpenALPR for json output')
            self.cmd = self.cmd + ' -j'
      

    def detect(self, object):
        """Detection using OpenALPR command line

        Args:
            object (image): image buffer

         Returns:
            boxes, labels, confidences: 3 objects, containing bounding boxes, labels and confidences
        """             
        bbox = []
        labels = []
        confs = []

        self.prepare(object)
        self.cmd = self.cmd + ' ' + self.filename
        self.logger.Debug (1,'OpenALPR CmdLine Executing: {}'.format(self.cmd))
        response = subprocess.check_output(self.cmd, shell=True)      
        self.logger.Debug (1,'OpenALPR CmdLine Response: {}'.format(response))
        try:
            response = json.loads(response)
        except ValueError as e:
            self.logger.Error ('Error parsing JSON from command line: {}'.format(e))
            response = {}

        (xfactor, yfactor) = self.getscale()

        rescale = False

        if self.remove_temp:
            os.remove(filename)

        if response.get('results'):
            for plates in response.get('results'):
                label = plates['plate']
                conf = float(plates['confidence']) / 100
                if conf < self.options.get('min_confidence'):
                    self.logger.Debug(
                        1,'OpenALPR cmd line: discarding plate: {} because detected confidence {} is less than configured min confidence: {}'
                        .format(label, conf, options.get('min_confidence')))
                    continue
                
                x1 = round(int(plates['coordinates'][0]['x']) * xfactor)
                y1 = round(int(plates['coordinates'][0]['y']) * yfactor)
                x2 = round(int(plates['coordinates'][2]['x']) * xfactor)
                y2 = round(int(plates['coordinates'][2]['y']) * yfactor)
                labels.append(label)
                bbox.append([x1, y1, x2, y2])
                confs.append(conf)

        return (bbox, labels, confs)
