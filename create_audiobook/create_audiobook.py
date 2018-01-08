'''
Created on 07.01.2018

@author: Marcel
'''
import urllib
import os


class episode(object):
    def __init__(self, data ):
        self.title           = data[1]            # title of episode
        self.enclosure_url   = data[0]            # url for download mp3
        self.start_time      = data[2]            # start time from main chapter
        self.stop_time       = data[3]           # stop time from main chapter


def find_epsisode(rss_info, list):
    item_step = 0;
    timing = []
    return_val = []
    opj_list = []  
    liste = list.split("-")
    timing.append(liste[0])
                   
    for i in range(1,(len(liste))):
        for line in rss_info:
            if (item_step == 0 and line.find("<item>") > 0):
                item_step = 1;
            elif (item_step == 1 and line.find(liste[0] + "</title>") > 0):
                item_step = 2;
            elif (item_step == 2 and line.find('enclosure url') > 0):
                return_val.append(line[(line.find('<enclosure url="')+len('<enclosure url="')):(line.find('" length="'))])
                item_step = 3
            elif ((item_step == 3 or item_step == 4) and line.find('<psc:chapter start="') > 0):
                timing.append(line[(line.find('<psc:chapter start="')+len('<psc:chapter start="')):(line.find('" title="'))])
                item_step = 4;
            elif (item_step == 4 and  line.find("</item>") > 0):
                item_step = 0
                return_val.append(timing[0])
                return_val.append(timing[int(liste[i])])
                return_val.append(timing[int(liste[i])+1])
                #epeside = episode(return_val)
                opj_list.append( episode(return_val))
    return opj_list

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
    data = (find_epsisode(response, cut_ini_option("FOLGE 1")))     
    for i in range(0, len(data)):
        download_cut_episode(data[i]) 
