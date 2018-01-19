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
                temp_file = title.replace("/","") + '_temp.mp3';
                file =str("%0.3o"% trac_num) + "." + title + " - " + self.episod_list[i].track_list[num-1].track_title + '.mp3';
                if not os.path.exists(folder):
                    os.makedirs(folder)
                if(os.path.isfile(folder + temp_file) ):
                    print "temp file is there ..."
                elif(os.path.isfile("../book/"+str("%0.3o"% trac_num)+ ' ' +self.episod_list[i].track_list[num-1].track_title.replace("/","").replace("&#xE4;","ae") + ".mp3") ):   
                    print "file is there ..."
                else:
                    mp3file = urllib.urlopen(self.episod_list[i].src.replace("https", "http"))
                    print "download ..."
                    with open(folder + temp_file,'wb') as output:
                        output.write(mp3file.read())
                            
                if not os.path.exists('../book/'):
                    os.makedirs('../book/')
                if(os.path.isfile('../book/' + file) ):
                    print file + " is there"
                else:
                    return self.cut_mp3(self.episod_list[i], num, trac_num)

                    
    def calc_str_to_ms(self, time_string):
        arg = time_string.split(":")
        return int(arg[0])*3600 +int(arg[1])*60 + int(float(arg[2]))
    
    def cut_mp3(self, episode, number, trac_num):
        input_file = "../temp/" + episode.title.replace("/","") + "_temp.mp3"
        output_file = "../book/"+str("%0.3o"% trac_num)+ ' ' +episode.track_list[number-1].track_title.replace("/","") + ".mp3"
        if(os.path.isfile(output_file.replace("&#xE4;","ae"))):
            print episode.track_list[number-1].track_title  + " file is there ..."
        else:
            in_file = open(input_file, "rb")
            out_file = open(output_file.replace("&#xE4;","ae"), "wb")
            cut_1 = 0
            cut_2 = 0
            if (len(episode.track_list) > number):
                cut_1 = int(episode.size) / self.calc_str_to_ms(episode.end_time) * self.calc_str_to_ms(episode.track_list[number-1].start_time)
                cut_2 = int(episode.size) / self.calc_str_to_ms(episode.end_time) * self.calc_str_to_ms(episode.track_list[number  ].start_time)
            else:
                cut_1 = episode.size / self.calc_str_to_ms(episode.end_time) * self.calc_str_to_ms(episode.track_list[number-1].start_time)
                cut_2 = episode.size / self.calc_str_to_ms(episode.end_time) * self.calc_str_to_ms(episode.end_time)
            cut_2 = cut_2 - cut_1
            buffersize = 1000
            while (buffersize < cut_1):
                buffer = in_file.read(buffersize) 
                cut_1 = cut_1 - 1000
            buffer = in_file.read(cut_1) 
            del buffer
            
            while (buffersize < (cut_2)):
                out_file.write(in_file.read(buffersize)) 
                cut_2 = cut_2 - 1000
            out_file.write(in_file.read(cut_2)) 
            
            in_file.close()
            out_file.close()
            print output_file + " created ...  "
        return output_file
        
        
        