#modules that need to be installed
from m3u_parser import M3uParser
from pathvalidate import sanitize_filename
import requests
import numpy

#modules that ship with python
import stat
import os
import json 


def url_checker(url):
	try:
		#Get Url
		get = requests.get(url)
		# if the request succeeds 
		if get.status_code == 200:
			#return(f"{url}: is reachable")
			return True
		else:
			#return(f"{url}: is Not reachable, status_code: {get.status_code}")
			return False
	except requests.exceptions.RequestException as e:
        # print URL with Errs
		raise SystemExit(f"{url}: is Not reachable \nErr: {e}")


#----------------------------process tv stuff-------------------------------
tv_vod_urls = []
ok_tv_vod_urls = []
tv_vod_subfolder = 'tv/vod'

#check if TV VOD subfolder exists and handle it
if not os.path.exists(tv_vod_subfolder):
	print('folder does not exist')
	quit()

#check if TV VOD url file exists
if not os.path.exists('tv_vod_urls.txt'):
	print('file does not exist')
	quit()

#open TV VOD file and read lines
with open('tv_vod_urls.txt') as tv_vod_url_file:
	tv_vod_urls = tv_vod_url_file.readlines()

#strip return chars from array items
tv_vod_urls = numpy.char.strip(tv_vod_urls)

#filter out URLS that don't return 200
ok_tv_vod_urls[:] = filter(url_checker, tv_vod_urls)


#set up parser
parser = M3uParser(timeout=10, useragent='"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"')

#parse all URLs, convert to JSON and put them into a dictionary object
stream_list = ''

for url in ok_tv_vod_urls:
	parser.parse_m3u(url)
	json_string = parser.get_json()
	if stream_list:
		stream_list += json.loads(json_string)
	else:
		stream_list = json.loads(json_string)

#change into tv subfolder 
os.chdir(tv_vod_subfolder)

#process the streams into strm files!
for item in stream_list:
	category = item.get('category')
	name = item.get('name')
	url = item.get('url')

	if not os.path.exists(category)):
		os.makedirs(category)

	file = open(category + '/' + name + '.strm', 'w+')
	file.write(url)
	file.close()

#clean up files older than 48h and remove any empty folders
os.system('find . -type f -daystart -mtime +1 -exec rm {} \;')
os.system('find . -type d -empty -delete')
	
#change back to script folder
os.chdir('../../')



#---------------------------process movie stuff--------------------------------
movie_vod_urls = []
ok_movie_vod_urls = []
movie_vod_subfolder = 'movie/vod'

#check if Movie VOD subfolder exists
if not os.path.exists(movie_vod_subfolder):
	print('folder does not exist')
	quit()

#check if Movie VOD url file exists
if not os.path.exists('movie_vod_urls.txt'):
	print('file does not exist')
	quit()

#open Movie VOD file and read lines
with open('movie_vod_urls.txt') as movie_vod_url_file:
	movie_vod_urls = movie_vod_url_file.readlines()

#strip return chars from array items
movie_vod_urls = numpy.char.strip(movie_vod_urls)

#filter out URLS that don't return 200
ok_movie_vod_urls[:] = filter(url_checker, movie_vod_urls)

#set up parser
parser = M3uParser(timeout=10, useragent='"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"')

#parse all URLs, convert to JSON and put them into a dictionary object
stream_list = ''

for url in ok_movie_vod_urls:
	parser.parse_m3u(url)
	json_string = parser.get_json()
	if stream_list:
		stream_list += json.loads(json_string)
	else:
		stream_list = json.loads(json_string)

#change into tv subfolder 
os.chdir(movie_vod_subfolder)

#process the streams into strm files!
for item in stream_list:
	category = sanitize_filename(item.get('category')
	name = sanitize_filename(item.get('name'))
	url = item.get('url')

	if not os.path.exists(category)):
		os.makedirs(category)

	file = open(category + '/' + name + '.strm', 'w+')
	file.write(url)
	file.close()

#clean up files older than 48h and remove any empty folders
os.system('find . -type f -daystart -mtime +1 -exec rm {} \;')
os.system('find . -type d -empty -delete')	
	
#change back to script folder
os.chdir('../../')
