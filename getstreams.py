#!/usr/bin/python3
from m3u_parser import M3uParser
from pathvalidate import sanitize_filename
import os
import stat
import json 
import requests
import numpy
import shutil
import re
import time

def remove_duplicate_year(s):
	arr = s.split(" ")
	for i in range(len(arr)-1):
		if re.match(r"\(\d{4}\)", arr[i]) and re.match(r"\(\d{4}\)", arr[i+1]) and arr[i] == arr[i+1]:
			arr.pop(i+1)
			return " ".join(arr)
	return s

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


def is_empty_dir(dirname):
    return not any(os.scandir(dirname))


#----------------------------process tv stuff-------------------------------
tv_vod_urls = []
ok_tv_vod_urls = []
tv_vod_subfolder = 'TV'
time_threshold = time.time() - 48 * 3600  # 48 hours in seconds

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

#strip return chars from read lines
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

#process the streams into strm files, using sanitize_filename to remove invalid characters from folder/file names
for item in stream_list:
	category = sanitize_filename(item.get('category'))
	name = sanitize_filename(item.get('name'))
	category = remove_duplicate_year(category)
	name = remove_duplicate_year(name)
	url = item.get('url')
	if not os.path.exists(category):
		os.makedirs(category)
	file = open(category + '/' + name + '.strm', 'w+')
	file.write(url)
	file.close()

#clean up files older than 48h and remove any empty folders (linux)
#os.system('find . -type f -daystart -mtime +1 -exec rm {} \;')
#os.system('find . -type d -empty -delete')

# clean up files older than 48h and remove any empty folders (windows)
# Walk through all subdirectories and files within the current directory
for root, dirs, files in os.walk(".", topdown=False):
    for file in files:
        # Get the full path of the file
        filepath = os.path.join(root, file)

        # Check if the file has not been modified in the last 48 hours
        if os.path.getmtime(filepath) < time_threshold:
            # Delete the file
            os.remove(filepath)
            print(f"Deleted {filepath}")

    for dir in dirs:
        # Get the full path of the directory
        dirpath = os.path.join(root, dir)

        # Check if the directory is empty
        if is_empty_dir(dirpath):
            # Delete the directory
            os.rmdir(dirpath)
            print(f"Deleted empty directory {dirpath}")

#change back to script folder
os.chdir('../')

#-------------------------------process movie stuff----------------------------
movie_vod_urls = []
ok_movie_vod_urls = []
movie_vod_subfolder = 'Movies'
time_threshold = time.time() - 48 * 3600  # 48 hours in seconds

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
	name = sanitize_filename(item.get('name'))
	url = item.get('url')


	if not os.path.exists(name):
		os.makedirs(name)

	file = open(name + '/' + name+ '.strm', 'w+')

	file.write(url)
	file.close()

#clean up files older than 48h and remove any empty folders (linux)
#os.system('find . -type f -daystart -mtime +1 -exec rm {} \;')
#os.system('find . -type d -empty -delete')

# clean up files older than 48h and remove any empty folders (windows)
# Walk through all subdirectories and files within the current directory
for root, dirs, files in os.walk(".", topdown=False):
    for file in files:
        # Get the full path of the file
        filepath = os.path.join(root, file)

        # Check if the file has not been modified in the last 48 hours
        if os.path.getmtime(filepath) < time_threshold:
            # Delete the file
            os.remove(filepath)
            print(f"Deleted {filepath}")

    for dir in dirs:
        # Get the full path of the directory
        dirpath = os.path.join(root, dir)

        # Check if the directory is empty
        if is_empty_dir(dirpath):
            # Delete the directory
            os.rmdir(dirpath)
            print(f"Deleted empty directory {dirpath}")

#change back to script folder
os.chdir('../')
