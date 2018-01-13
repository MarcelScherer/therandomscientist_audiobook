'''
Created on 12.01.2018

@author: Marcel
'''
import feed_pars
import os
import urllib


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
                    print "file cut has to be programm .."

                    
    def calc_str_to_ms(self, time_string):
        arg = time_string.split(":")
        return int(arg[0])*3600 +int(arg[1])*60 + int(float(arg[2]))

        