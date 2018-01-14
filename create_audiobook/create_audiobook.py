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

#--------------------------------------------------
FEED = "http://therandomscientist.de/feed/mp3/"
#--------------------------------------------------

if __name__ == '__main__':
    count = 0

    feed_ojt    = feed_parser(FEED)
    mp3_creat   = track_create(feed_ojt.epsiod_list)
    del feed_ojt
    with open("create_audiobook.ini") as ini_file:      # open ini-file
        for line in ini_file:                           # search in every line
            arg = line.split(":")
            if (len(arg)>1):
                for i in range(1,len(arg)):
                    count = count + 1
                    mp3_creat.create_track(arg[0], int(arg[i]), count)
    shutil.rmtree('../temp', ignore_errors=True)
