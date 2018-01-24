'''
Created on 12.01.2018

@author: Marcel
'''
import feed_pars
import os
import urllib


class track_create(object):
    # safe episode list in track_create object
    def __init__(self, episod_list):
        self.episod_list = episod_list;

    # create a mp3 with title and track number of number in episode
    def create_track(self, title, num, trac_num):
        for i in range(0, len(self.episod_list)):
            # finde the right episode in the episode list
            if (self.episod_list[i].title == title):
                print "start create " + title
                folder = '../temp/';                                # temp foulder
                temp_file = title.replace("/","") + '_temp.mp3';    # temp title title
                file =str("%0.3d"% trac_num) + "." + title + " - " + self.episod_list[i].track_list[num-1].track_title + '.mp3';
                # create temp foulder if not exist
                if not os.path.exists(folder):
                    os.makedirs(folder)
                # do nothing if tempfile exist
                if(os.path.isfile(folder + temp_file) ):
                    print "temp file is there ..."
                # do nothing if mp3 exist
                elif(os.path.isfile("../book/"+str("%0.3d"% trac_num)+ ' ' +self.episod_list[i].track_list[num-1].track_title.replace("/","").replace("&#xE4;","ae").replace("&#xF6;","oe") + ".mp3") ):   
                    print "file is there ..."
                else:
                    # download episode
                    mp3file = urllib.urlopen(self.episod_list[i].src.replace("https", "http"))
                    print "download ..."
                    with open(folder + temp_file,'wb') as output:
                        output.write(mp3file.read())
                # create book folder if not exist            
                if not os.path.exists('../book/'):
                    os.makedirs('../book/')
                # do nothing if mp3 file exist
                if(os.path.isfile('../book/' + file) ):
                    print file + " is there"
                else:
                    return self.cut_mp3(self.episod_list[i], num, trac_num)

          
    # calc time in ms form time string                
    def calc_str_to_ms(self, time_string):
        arg = time_string.split(":")
        return int(arg[0])*3600 +int(arg[1])*60 + int(float(arg[2]))
    
    # function cut mp3 track out of a mp3 episdoe file
    def cut_mp3(self, episode, number, trac_num):
        createt_file = None;
        input_file = "../temp/" + episode.title.replace("/","") + "_temp.mp3"
        output_file = "../book/"+str("%0.3d"% trac_num)+ ' ' +episode.track_list[number-1].track_title.replace("/","") + ".mp3"
        # do nothing if file exist
        if(os.path.isfile(output_file.replace("&#xE4;","ae").replace("&#xF6;","oe"))):
            print episode.track_list[number-1].track_title  + " file is there ..."
        else:
            in_file = open(input_file, "rb")
            out_file = open(output_file.replace("&#xE4;","ae").replace("&#xF6;","oe"), "wb")
            createt_file = output_file;
            cut_1 = 0
            cut_2 = 0
            # calculate start and end cut in byte with the "rule of proportion"
            if (len(episode.track_list) > number):
                cut_1 = int(episode.size) / self.calc_str_to_ms(episode.end_time) * self.calc_str_to_ms(episode.track_list[number-1].start_time)
                cut_2 = int(episode.size) / self.calc_str_to_ms(episode.end_time) * self.calc_str_to_ms(episode.track_list[number  ].start_time)
            else:
                cut_1 = episode.size / self.calc_str_to_ms(episode.end_time) * self.calc_str_to_ms(episode.track_list[number-1].start_time)
                cut_2 = episode.size / self.calc_str_to_ms(episode.end_time) * self.calc_str_to_ms(episode.end_time)
            cut_2 = cut_2 - cut_1
            #print episode.track_list[number-1].start_time + " - " + episode.track_list[number].start_time + " - " + str(cut_2)
            buffersize = 1000
            # read data stream from start to cut 1 -> stream does not needed
            while (buffersize < cut_1):
                buffer = in_file.read(buffersize) 
                cut_1 = cut_1 - 1000
            buffer = in_file.read(cut_1) 
            del buffer
            # read data stram from cut 1 to cut 2 and save as mp3 track
            while (buffersize < (cut_2)):
                out_file.write(in_file.read(buffersize)) 
                cut_2 = cut_2 - 1000
            out_file.write(in_file.read(cut_2)) 
            
            in_file.close()
            out_file.close()
            print output_file + " created ...  "
        return createt_file
        
        
        