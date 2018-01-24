'''
Created on 07.01.2018

@author: Marcel
'''
import urllib
import os
from feed_pars import feed_parser
from feed_pars import episode
from track_creater import track_create
import shutil
from mp3_add_tag import add_mp3_tag
from mp3_fade import mp3_fade_in_out


#--------------------------------------------------
FEED = "http://therandomscientist.de/feed/mp3/"
#--------------------------------------------------

if __name__ == '__main__':
    # delete temp foulder if it exist
    shutil.rmtree('../temp', ignore_errors=True)
    count = 0
    mp3_list = []
    # create a feed object where is a list of all episode objects
    feed_ojt    = feed_parser(FEED)
    # create a mp3_create object where can create mp3 tracs
    mp3_creat   = track_create(feed_ojt.epsiod_list)
    del feed_ojt
    with open("create_audiobook.ini") as ini_file:      # open ini-file
        for line in ini_file: 
            # split ini input for episode and track numbers                          
            arg = line.split(":")
            if (len(arg)>1):
                for i in range(1,len(arg)):
                    count = count + 1
                    #create a mp3 for all tracks in one episode
                    mp3_list.append(mp3_creat.create_track(arg[0], int(arg[i]), count))
    # delete temp foulder
    shutil.rmtree('../temp', ignore_errors=True)
     
    for i in range(1,len(mp3_list)+1):
        # fade all mp3 in and out in the mp3_list
        mp3_fade_in_out(mp3_list[i-1])
        # create mp3 tags for all mp3 in the mp3 list
        add_mp3_tag((mp3_list[i-1]))


