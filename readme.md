I created this from scratch after being unable to find anything that would work with Apollo's M3U formatting. 
I'm fairly new to python so if you have suggestions I'm open to them.  There are probably things that could be done
a little more sanely, such as handling failures if files don't exist or URLs fail to parse etc.  

You will need to install some additional libraries for this script to run properly. 

I'm using Jellyfin and wrote this script so that it can be placed in the root of my media folder.  I then use separate sub-folders 
for strm file storage along side my media library.  This is why I have a subfolder variable declared and CD into it when generating
the folder structure and strm files. 

I truncate and re-write URLs to the strm files that already exist so that their last modified times are updated. 
My plan is to run this from a bash script so that after I've refreshed the strm files on disk, it can scan for any 
files that were not updated on the same date that the script was run and delete them.  After that I'll do a subsequent search
for empty directories and delete those. 