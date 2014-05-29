import flickrapi
import json
import os
import sys
import time
import requests
import string
from PIL import Image
from StringIO import StringIO
from requests.exceptions import ConnectionError


# set these here or using flickr.API_KEY in your application
api_key = unicode('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
api_secret = unicode('xxxxxxxxxxxxxxxx')

flickr = flickrapi.FlickrAPI(api_key, api_secret)

""" Validates a filename """
def validate(filename):        
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    return ''.join(c for c in filename if c in valid_chars)[:12]


def go(query, folder, num):
    """Download full size images from Flickr.

    Don't print or republish images without permission.
    """ 
    BASE_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), folder)
 
    if not os.path.exists(BASE_PATH):
        os.makedirs(BASE_PATH)

	pg = 1
	while num > 0:
		photos = flickr.photos.search(text=query, format='parsed-json', per_page=num%501, page=pg)
		photos = photos['photos']

		for photo in photos['photo']:
			url = 'http://farm' + str(photo['farm']) + '.staticflickr.com/' + str(photo['server']) + '/' + str(photo['id']) + '_' + str(photo['secret']) + '_m.jpg'

			try:
				image_r = requests.get(url)
			except ConnectionError, e:
				print 'Could not download %s' % url
				continue
		 
			title = photo['title']
			print 'Downloading', title
		 
			file = open(os.path.join(BASE_PATH, '%s.jpg') % validate(title), 'wb+')
			try:
				Image.open(StringIO(image_r.content)).save(file, 'JPEG')
			except IOError, e:
				# Throw away some gifs...blegh.
				print 'could not save %s' % url
				continue
			finally:
				file.close()
	
		pg += 1
		num -= 500

try:
    print "Press CTRL-C to exit"
    while (1):
        go(raw_input('Text: '), raw_input('Folder: '), raw_input('Number of results: '))
except:
    pass

    
