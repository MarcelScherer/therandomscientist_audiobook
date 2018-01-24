'''
Created on 10.01.2018

@author: Marcel
'''

import urllib

# podcast episode
class episode(object):
    def __init__(self, title, src, track_list, end_time, size):
        self.title           = title            # title of episode
        self.src             = src              # url for download mp3
        self.track_list      = track_list       # track list - all tracks with start time and title
        self.end_time        = end_time         # end time of episode
        self.size            = size             # episode size in byte

# episode track -> track title and start time        
class track(object):
    def __init__(self, start_time, track_title):
        self.start_time = start_time
        self.track_title = track_title

# feed parser
class feed_parser(object):
    # the init function past the feed and create a list of all episodes in the feed
    def __init__(self, rss_info):
        self.epsiod_list = []  # list of all found episode
        self.count = 0;
        
        item_step = 0;
        # download mp3 feed xml
        rss = urllib.urlopen(rss_info)           
        print "parse feed ..."
        track_list = []
        title = ""
        src   = ""
        size = 0
        endtime = ""
        # look for episodes in the xml file
        for line in rss:
            # find the begin of the episode
            if (item_step == 0 and line.find("<item>") > 0):     
                item_step = 1;
            # find the title of the episode
            elif (item_step == 1 and line.find("</title>") > 0):
                title = line[line.find("; ")+2:line.find("</title>")] 
                title = self.fix_string(title)
                item_step = 2;
            # finde the link for download the mp3 file
            elif (item_step == 2 and line.find('enclosure url') > 0):  # search for url sorce
                src = line[(line.find('<enclosure url="')+len('<enclosure url="')):(line.find('" length="'))]
                size = line[(line.find('length="')+len('length="')):(line.find('" type="'))]
                item_step = 3
            # find the length (time) of the mp3 file
            elif (item_step == 3 and line.find('duration>') > 0):    
                endtime = line[(line.find('duration>')+len('duration>')):(line.find('</itunes:duration>'))]
                item_step = 4;
            # find title and start time of all chapter marks
            elif ((item_step == 4 or item_step == 5) and line.find('<psc:chapter start="') > 0):    # search for all tracks
                timming = (line[(line.find('<psc:chapter start="')+len('<psc:chapter start="')):(line.find('" title="'))])
                track_title = (line[(line.find('" title="')+len('" title="')):(line.find('"/>'))])
                if(track_title == ""):
                    track_title = title;
                track_list.append(track(timming, track_title))
                item_step = 5;
            # find the end of one episode
            elif (item_step == 5 and  line.find("</item>") > 0):   
                item_step = 0
                # create a episode object and add to epsiode list
                self.epsiod_list.append(episode(title, src, track_list, endtime, size))
                self.count = self.count + 1;
                track_list = []
                title = ""
                src   = ""
            # find the end but not all values of the episode found
            elif (line.find("</item>") > 0):
                item_step = 0
                track_list = []
                title = ""
                src   = ""
        # reverse list that the fist episode is the oldest
        self.epsiod_list.reverse()
        
    # function change "ä" to "ae" and "ö" to "oe" in a assci string
    def fix_string(self, enco):
        a=list(enco)
        for i in range(0,len(a)-1):
            if (ord(a[i]) == 195 and ord(a[i+1])==182):
                a[i] = chr(111)
                a[i+1] = chr(101)
            if (ord(a[i]) == 195 and ord(a[i+1])==164):
                a[i] = chr(97)
                a[i+1] = chr(101)
        return ''.join(a)
        