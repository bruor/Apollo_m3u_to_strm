I created this because I couldn't find any tools that would work with Apollo's M3U feeds. 
PR's welcome as there are probably things that could be donea little more sanely.
Especially error handling :) 

You will need to install some additional libraries for this script to run properly. 

I'm using Jellyfin and wrote this script so that it can be placed in the root of my media folder.  I then use separate sub-folders 
for strm file storage along side my media library.  This is why I have a subfolder variable declared and CD into it when generating
the folder structure and strm files. 

I truncate and re-write URLs to the strm files that already exist so that their last modified times are updated. 
My plan is to run this from a bash script so that after I've refreshed the strm files on disk, it can scan for any 
files that were not updated on the same date that the script was run and delete them.  After that I'll do a subsequent search
for empty directories and delete those. 

You'll need to modify the script to match your folder structure along with the commands that change directories before files are created.
You'll also need to create/populate 2 text files that house your M3U URLs. There are currently 24 TV VOD URLs active, and 1 for movies.
In the TV file I just added 50 URLs for future expansion since the script checks to see if they exist before consuming them. 
