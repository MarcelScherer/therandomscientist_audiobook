'''
Created on 10.01.2018

@author: Marcel
'''

class episode(object):
    def __init__(self, data ):
        self.title           = data[1]            # title of episode
        self.enclosure_url   = data[0]            # url for download mp3
        self.start_time      = data[2]            # start time from main chapter
        self.stop_time       = data[3]            # stop time from main chapter

class feed_parser(object):
    def __init__(self, rss_info, list):
        self.opj_list = [] 
        self.count = 0;
        
        item_step = 0;
        timing = []
        title = []
        return_val = [] 
        liste = list.split("-")
        timing.append(liste[0])
                       
        for i in range(0,((len(liste) - 1))):
            print "parse feed ..."
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
                    title_string = (line[(line.find('" title="')+len('" title=""')):(line.find('"/>'))])
                    if (title_string == "-" or title_string == ""):
                        title.append(liste[0])
                    else:
                        title.append(title_string)
                    item_step = 4;
                elif (item_step == 4 and  line.find("</item>") > 0):
                    item_step = 0
                    return_val.append(title[int(liste[i+1])])
                    return_val.append(timing[int(liste[i+1])])
                    return_val.append(timing[int(liste[i+1])+1])
                    #epeside = episode(return_val)
                    print return_val
                    self.opj_list.append( episode(return_val))
                    self.count = self.count + 1;
                    
    def get_episode(self, num):
        return self.opj_list[num]
        
    def get_count(self):
        return int(self.count)

        