'''
Created on 10.01.2018

@author: Marcel
'''
import urllib

class episode(object):
    def __init__(self, title, src, track_list, end_time, size):
        self.title           = title            # title of episode
        self.src             = src              # url for download mp3
        self.track_list      = track_list       # start time from main chapter
        self.end_time        = end_time
        self.size            = size
        
class track(object):
    def __init__(self, start_time, track_title):
        self.start_time = start_time
        self.track_title = track_title

class feed_parser(object):
    def __init__(self, rss_info):
        self.epsiod_list = [] 
        self.count = 0;
        
        item_step = 0;
        rss = urllib.urlopen(rss_info)           
        print "parse feed ..."
        track_list = []
        title = ""
        src   = ""
        size = 0
        endtime = ""
        for line in rss:
            if (item_step == 0 and line.find("<item>") > 0):
                item_step = 1;
            elif (item_step == 1 and line.find("</title>") > 0):
                title = line[line.find("; ")+2:line.find("</title>")]
                item_step = 2;
            elif (item_step == 2 and line.find('enclosure url') > 0):
                src = line[(line.find('<enclosure url="')+len('<enclosure url="')):(line.find('" length="'))]
                size = line[(line.find('length="')+len('length="')):(line.find('" type="'))]
                item_step = 3
            elif (item_step == 3 and line.find('duration>') > 0):    
                endtime = line[(line.find('duration>')+len('duration>')):(line.find('</itunes:duration>'))]
                item_step = 4;
            elif ((item_step == 4 or item_step == 5) and line.find('<psc:chapter start="') > 0):
                timming = (line[(line.find('<psc:chapter start="')+len('<psc:chapter start="')):(line.find('" title="'))])
                track_title = (line[(line.find('" title="')+len('" title="')):(line.find('"/>'))])
                if(track_title == ""):
                    track_title = title;
                track_list.append(track(timming, track_title))
                item_step = 5;
            elif (item_step == 5 and  line.find("</item>") > 0):
                item_step = 0
                self.epsiod_list.append(episode(title, src, track_list, endtime, size))
                self.count = self.count + 1;
                track_list = []
                title = ""
                src   = ""
            elif (line.find("</item>") > 0):
                item_step = 0
                track_list = []
                title = ""
                src   = ""
        self.epsiod_list.reverse()

        