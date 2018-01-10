'''
Created on 07.01.2018

@author: Marcel
'''
import urllib
import os
from feed_pars import feed_parser
from feed_pars import episode
import pydub
pydub.AudioSegment.converter = r"..\\ffmpeg\\bin\\ffmpeg.exe"
from pydub import AudioSegment

def download_cut_episode(episode):
    folder = '../temp/'
    file = episode.title + '_temp.mp3'
    if not os.path.exists(folder):
        os.makedirs(folder)
    mp3file = urllib.urlopen(episode.enclosure_url)
    if(os.path.isfile(folder + file) ):
        print "file is there ..."
    else:
        print "download ..."
        with open(folder + file,'wb') as output:
          output.write(mp3file.read())
    
    if not os.path.exists('../book/'):
        os.makedirs('../book/')
    if(os.path.isfile(folder + file) ):
        sound = AudioSegment.from_file(folder + file , "mp3" )    
        track = sound[episode.start_time:episode.stop_time]
        track.export('../book/' + episode.title + '.mp3', format="mp3")
    

              
# function return the option from option tag
def cut_ini_option(option_tag):
    with open("create_audiobook.ini") as ini_file:      # open ini-file
        for line in ini_file:                           # search in every line
            if option_tag in line:                      # check if option tag is in line
                position = line.find(":")               # find first :
                return line[position+2:]                # return option -> all behind first ": "
    

if __name__ == '__main__':
    rss_feed = cut_ini_option("RSS-FEED")               # get rss feed from ini-file
    out_string = cut_ini_option("NOT_IN")   
    response = urllib.urlopen(rss_feed)                 # load rss info from feed
    
    parser1 = feed_parser(response, cut_ini_option("FOLGE 1"))     
    for i in range(0, parser1.get_count()):
        download_cut_episode(parser1.get_episode(i)) 
        
    parser2 = feed_parser(response, cut_ini_option("FOLGE 2"))  
    print parser2.get_count()   
    for i in range(0, parser2.get_count()):
        download_cut_episode(parser2.get_episode(i)) 

