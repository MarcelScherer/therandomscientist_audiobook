'''
Created on 20.01.2018

@author: Marcel
'''

from pydub import AudioSegment
AudioSegment.converter = "../ffmpeg/bin/ffmpeg.exe"

def mp3_fade_in_out(path_to_file):
    if (path_to_file != None):
        print "fade in and out: " + path_to_file
        #song_raw = AudioSegment.from_file(path_to_file.replace(".mp3",""),"mp3")
        song_raw = AudioSegment.from_file(path_to_file,"mp3")
        # 2 sec fade in, 3 sec fade out
        song = song_raw.fade_in(5000).fade_out(5000)
        song.export(path_to_file, format="mp3")