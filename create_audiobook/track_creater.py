'''
Created on 12.01.2018

@author: Marcel
'''
import feed_pars
import os
import urllib
import sys
sys.path[0:0] = '../pydub' # puts the /foo directory at the start of your path
import pydub
pydub.AudioSegment.converter = r"..\\ffmpeg\\bin\\ffmpeg.exe"
from pydub import AudioSegment

class track_create(object):
    
    def __init__(self, episod_list):
        self.episod_list = episod_list;

    def create_track(self, title, num, trac_num):
        for i in range(0, len(self.episod_list)):
            if (self.episod_list[i].title == title):
                folder = '../temp/';
                temp_file = title + '_temp.mp3';
                file =str("%0.3o"% trac_num) + "." + title + " - " + self.episod_list[i].track_list[num-1].track_title + '.mp3';
                if not os.path.exists(folder):
                    os.makedirs(folder)
                mp3file = urllib.urlopen(self.episod_list[i].src.replace("https", "http"))
                if(os.path.isfile(folder + temp_file) ):
                    print "temp file is there ..."
                else:
                    print "download ..."
                    with open(folder + temp_file,'wb') as output:
                        output.write(mp3file.read())
                            
                if not os.path.exists('../book/'):
                    os.makedirs('../book/')
                if(os.path.isfile('../book/' + file) ):
                    print file + " is there"
                else:
                    sound = AudioSegment.from_file(folder + temp_file , "mp3" )    
                    track = sound[self.episod_list[i].track_list[num-1].start_time:self.episod_list[i].track_list[num].start_time]
                    track.export('../book/' + file, format="mp3")
                    print "create " + file + " ..."

        