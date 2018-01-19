'''
Created on 17.01.2018

@author: Marcel
'''
from mutagen.id3 import ID3NoHeaderError
from mutagen.id3 import ID3, TIT2, TALB, TPE1, TPE2, COMM, USLT, TCOM, TCON, TDRC, TRCK, APIC, error
from mutagen.mp3 import MP3

def add_mp3_tag(path_to_mp3):

    # Create MP3File instance.
    if(path_to_mp3 != None):
        folder = "../book/"
        trac = path_to_mp3[path_to_mp3.find(folder)+len(folder):path_to_mp3.find(folder)+len(folder)+3]
        file = path_to_mp3[path_to_mp3.find(folder)+len(folder)+4:].replace("/","").replace("&#xE4;","ae")
        # create ID3 tag if not present
        try: 
            tags = ID3(folder + trac + " " + file)
        except ID3NoHeaderError:
            print "Adding ID3 header;",
            tags = ID3()
        
        tags["TIT2"] = TIT2(encoding=3, text=unicode(file.replace(".mp3","")))
        tags["TALB"] = TALB(encoding=3, text=u'The Random Scientist Audiobook')
        tags["TPE2"] = TPE2(encoding=3, text=u'The Random Scientist Audiobook')
        tags["COMM"] = COMM(encoding=3, lang=u'eng', desc='desc', text=u'mutagen comment')
        tags["TPE1"] = TPE1(encoding=3, text=u'Dr. Stefan Dillinger')
        tags["TCOM"] = TCOM(encoding=3, text=u'mutagen Composer')
        tags["TDRC"] = TDRC(encoding=3, text=u'2017')
        tags["TRCK"] = TRCK(encoding=3, text=unicode(trac))
        
        tags.save(folder + trac + " " + file)
        
        
        audio = MP3(folder + trac + " " + file, ID3=ID3)    
        audio.tags.add(
            APIC(
                encoding=3, # 3 is for utf-8
                mime='image/png', # image/jpeg or image/png
                type=3, # 3 is for the cover image
                desc=u'Cover',
                data=open('../TheRandomScientist_small_white.jpg').read()
            )
        )
        audio.save(folder + trac + " " + file)
        
