#! /usr/bin/env python
#
# pymp3cut
# (c) 2002 Jerome Alet <alet@librelogiciel.com>
# You're welcome to redistribute this software under the
# terms of the GNU General Public Licence version 2.0
# or, at your option, any higher version.
#
# You can read the complete GNU GPL in the file COPYING
# which should come along with this software, or visit
# the Free Software Foundation's WEB site http://www.fsf.org
#
# $Id: pymp3cut.py,v 1.8 2002/06/24 22:39:26 jalet Exp $
#
#
import sys
import os
import string
import getopt
import pmpcmp3

__author__ = "alet@librelogiciel.com (Jerome Alet)"

__version__ = "0.27"

__doc__ = """A command line tool to cut very big MP3 files without any
need for an intermediate conversion to wav and the associated disk space.
Each subpart can be postprocessed with a command of your choice (e.g. lame).

This tool should be ffaasstt !

command line usage :

        pymp3cut [options] inputfile

  inputfile is mandatory.
  This command currently can't be used as a filter.

options :

  -v | --version             prints MP3Cut's version number then exits.
  -h | --help                prints this message then exits.

  -c | --command cmd         uses cmd to postprocess each subpart. The command
                             must accept MP3 input on stdin and send its MP3
                             output to stdout : it will be used as a filter
                             using shell redirection.

  -p | --parts prefix,sec,total  splits the file in a number of subparts; each
                                 one is called 'prefix-####.mp3', has a length
                                 of 'sec' and the sum is equals to 'total'
                                 ([[hh:]mm:]ss).
                             
                                 NB : this option is mandatory if you doesn't
                                      use --timeline or --segment option

  -s | --segment prefix,start,end  cuts a segment in the middle of the file 
                                   begining at start and ending at end
                                   ([[hh:]mm:]ss). prefix can be - to send
                                   the segment to stdout.
                             
                                 NB : this option is mandatory if you doesn't
                                      use --timeline or --parts option

  -t | --timeline file.tml   uses file.tml as the timeline from which the
                             inputfile will be cut. A timeline file is a
                             text file which may contain empty lines or
                             comments which begin with #.
                             Any non-empty and non-comment line is expected
                             to be in the following format :

                               name    [[hh:]mm:]ss

                               name : the name to give to that particular
                                      subpart of the inputfile : a file named
                                      'name.mp3' will be created and will
                                      contain this subpart.

                               hh:mm:ss : the ending time at which this
                                          subpart ends in the input file,
                                          in hours:minutes:seconds format.

                               name and hh:mm:ss can be separated by any
                               amount of whitespace.

                               NB : this option is mandatory if you doesn't
                                    use --parts or --segment option

  -q | --quiet                 doesn't display a progress indicator.
                               only error and warning messages are printed.
"""

class MP3CutError :
        """MP3Cut's Exception class."""
        def __init__(self, value) :
                self.value = value

        def __str__(self) :
                return str(self.value)

class ProgressIndicator :
        """To display a progress indicator"""
        def __init__(self, verbose) :
                self.verbose = verbose

        def output(self, msg) :
                if self.verbose :
                        sys.stderr.write(msg)
                        sys.stderr.flush()

        def skip(self, duration) :
                self.output("Skipping %i seconds" % duration)

        def percent(self, pct) :
                self.output("\b\b\b\b%03i%%" % pct)

        def title(self, title) :
                self.output(title)

        def close(self) :
                self.output("\n")

class MP3File :
        """A class for MP3 files"""
        def __init__(self, file = None) :
                """Initialize an MP3File."""
                self.file = file
                self.timeline = None
                bitrate = self.get_bitrate()
                if bitrate is None :
                        raise MP3CutError, "%s doesn't seem to be an MP3 file" % repr(file)
                self.bitrate = bitrate
                self.parts_prefix = None
                self.parts_sec = None
                self.parts_total = None
                self.segment_prefix = None
                self.segment_start = None
                self.segment_end = None

        def get_bitrate(self) :
                """Returns the bitrate of the MP3 file or None if the file is not in MP3 format."""
                try :
                        info = pmpcmp3.mp3info(self.file)
                        if info and info.has_key("BITRATE") and (type(info["BITRATE"]) == type(0)) :
                                return info["BITRATE"] * 1000
                except KeyError :
                        pass

        def subfile(self, infile, bytespersec, name, duration, verbose) :
                progress = ProgressIndicator(verbose)
                length = duration * bytespersec
                mustclose = 0
                if name == "*SKIP*" :
                        progress.skip(duration)
                        infile.seek(length, 1)
                        progress.close()
                        return
                elif name == "-" :
                        filename = "stdout"
                        outfile = sys.stdout
                else :
                        filename = "%s.mp3" % name
                        outfile = open(filename, "wb")
                        mustclose = 1
                progress.title("Writing %s (%i sec) :     " % (filename, duration))
                rwrite = 0L
                for blocknumber in range(duration) :
                        inblock = infile.read(bytespersec)
                        outfile.write(inblock)
                        readlen = len(inblock)
                        rwrite = rwrite + readlen
                        progress.percent((rwrite * 100L) / length)
                        if readlen != bytespersec :
                                break   # EOF
                if mustclose :        
                        outfile.close()
                progress.close()

        def read_timeline(self, timelinefile) :
                """Cuts the current MP3 file according to its timeline.

                   timelinefile : a file of lines. Each line looks like :

                              name endtime

                              name and endtime can be separated by any amount of whitespace.
                              empty lines and comments are skipped.
                              comments are lines which begin with a '#'.

                              name : the name to give to the resulting mp3 file (without extension).
                                     if name is equal to '*SKIP*' then no file is produced, but
                                     instead a seek is made in the input file to skip this part.

                              endtime : the time hh:mm:ss at which this part ends in the original
                                        mp3 file.
                """                           
                try :
                        file = open(timelinefile, "r")
                        self.timeline = file.readlines()
                        file.close()
                except IOError, msg :
                        raise MP3CutError, msg

        def calculate_parts(self, partsopt) :
                try :
                        (prefix, sec, total) = string.split(partsopt,',')
                        split = string.split(total, ':')
                        while len(split) < 3 :
                                split.insert(0, "0")
                        (hours,minutes,seconds) = map(int, split)
                        total = hours * 3600 + minutes * 60 + seconds
                        self.parts_prefix = prefix
                        self.parts_sec = int(sec)
                        self.parts_total = total
                except ValueError :
                        # skip current line which is invalid
                        raise MP3CutError, "Invalid --part option %s" % partsopt

        def calculate_segment(self, segmentopt) :
                try :
                        (prefix, start, end) = string.split(segmentopt,',')
                        split = string.split(start, ':')
                        while len(split) < 3 :
                                split.insert(0, "0")
                        (hours,minutes,seconds) = map(int, split)
                        start = hours * 3600 + minutes * 60 + seconds
                        split = string.split(end, ':')
                        while len(split) < 3 :
                                split.insert(0, "0")
                        (hours,minutes,seconds) = map(int, split)
                        end = hours * 3600 + minutes * 60 + seconds
                        self.segment_prefix = prefix
                        self.segment_start = int(start)
                        self.segment_end = int(end)
                except ValueError :
                        # skip current line which is invalid
                        raise MP3CutError, "Invalid --segment option %s" % segmentopt

        def cut(self, command = None, verbose = 0) :
                """Cuts the current MP3 file according to its timeline.

                     command : a complete command line with options to launch
                               a command on each subfile after the cut. May be used
                               for example to downmix from stereo to mono using
                               lame. Each subfile will then be piped into this command,
                               which must accept MP3 input on stdin and send MP3 output on
                               stdout. NB : you don't have to use the shell redirectors,
                               since your command will be launched like this :

                                 yourcommand <tempfile >finalfile

                     verbose : 1 to write a progress indicator, else 0 (default)
                """              
                if self.timeline is None :
                        raise MP3CutError, "Timeline not set."
                if (command is not None) and (not string.strip(command)) :
                        raise MP3CutError, "Empty command."
                if command :
                        raise MP3CutError, "Postprocessing commands are currently unsupported."
                mustclose = 0
                if hasattr(self.file, "read") :
                        mp3file = self.file
                else :
                        mp3file = open(self.file, "rb")
                        mustclose = 1
                curtime = 0
                for line in self.timeline :
                        # skip empty lines and comments
                        line = string.strip(line)
                        if line and (line[0] != '#') :
                                try :
                                        (title, ends) = string.split(line)
                                        split = string.split(ends, ':')
                                        while len(split) < 3 :
                                                split.insert(0, "0")
                                        (hours,minutes,seconds) = map(int, split)
                                        endtime = hours * 3600 + minutes * 60 + seconds
                                        self.subfile(mp3file, self.bitrate / 8, title, (endtime - curtime), verbose)
                                        curtime = endtime
                                except ValueError :
                                        # skip current line which is invalid
                                        warning_or_error("Skipping invalid timeline entry : %s" % line)
                                except IOError, msg :
                                        raise MP3CutError, msg
                if mustclose :
                        mp3file.close()

        def cut_parts(self, command = None, verbose = 0) :
                """Cuts the current MP3 file according to its timeline.

                     command : a complete command line with options to launch
                               a command on each subfile after the cut. May be used
                               for example to downmix from stereo to mono using
                               lame. Each subfile will then be piped into this command,
                               which must accept MP3 input on stdin and send MP3 output on
                               stdout. NB : you don't have to use the shell redirectors,
                               since your command will be launched like this :

                                 yourcommand <tempfile >finalfile

                     verbose : 1 to write a progress indicator, else 0 (default)
                """              
                if self.parts_sec is None or self.parts_total is None or self.parts_prefix is None :
                        raise MP3CutError, "Parts not set."
                if (command is not None) and (not string.strip(command)) :
                        raise MP3CutError, "Empty command."
                if command :
                        raise MP3CutError, "Postprocessing commands are currently unsupported."
                mustclose = 0
                if hasattr(self.file, "read") :
                        mp3file = self.file
                else :
                        mp3file = open(self.file, "rb")
                        mustclose = 1
                curtime = 0
                j = 0
                for i in range(self.parts_sec, self.parts_total, self.parts_sec) :
                        try :
                                endtime = i
                                j = j + 1
                                title = "" + self.parts_prefix + "-" + string.zfill(repr(j), 4)
                                self.subfile(mp3file, self.bitrate / 8, title, (endtime - curtime), verbose)
                                curtime = endtime
                        except ValueError :
                                # skip current line which is invalid
                                warning_or_error("Skipping invalid timeline entry : %s" % line)
                        except IOError, msg :
                                raise MP3CutError, msg
                if mustclose :
                        mp3file.close()

        def cut_segment(self, command = None, verbose = 0) :
                """Cuts the current MP3 file according to start and end times

                     command : a complete command line with options to launch
                               a command on each subfile after the cut. May be used
                               for example to downmix from stereo to mono using
                               lame. Each subfile will then be piped into this command,
                               which must accept MP3 input on stdin and send MP3 output on
                               stdout. NB : you don't have to use the shell redirectors,
                               since your command will be launched like this :

                                 yourcommand <tempfile >finalfile

                     verbose : 1 to write a progress indicator, else 0 (default)
                """              
                if self.segment_start is None or self.segment_end is None or self.segment_prefix is None :
                        raise MP3CutError, "Parts not set."
                if (command is not None) and (not string.strip(command)) :
                        raise MP3CutError, "Empty command."
                if command :
                        raise MP3CutError, "Postprocessing commands are currently unsupported."
                mustclose = 0
                if hasattr(self.file, "read") :
                        mp3file = self.file
                else :
                        mp3file = open(self.file, "rb")
                        mustclose = 1
                curtime = 0
                j = 0
                try :
                        j = j + 1
                        if self.segment_prefix == "-" :
                                title = "-"
                        else :
                                title = "" + self.segment_prefix + "-" + string.zfill(repr(j), 4)
                        self.subfile(mp3file, self.bitrate / 8, "*SKIP*", self.segment_start, verbose)
                        self.subfile(mp3file, self.bitrate / 8, title, (self.segment_end - self.segment_start), verbose)
                except ValueError :
                        # skip current line which is invalid
                        #warning_or_error("Skipping invalid timeline entry : %s" % line)
                        return
                except IOError, msg :
                        #raise MP3CutError, msg
                        return
                if mustclose :
                        mp3file.close()

def display_version_and_quit() :
        """Displays version number, then exists successfully."""
        print __version__
        sys.exit(0)

def display_usage_and_quit() :
        """Displays command line usage, then exists successfully."""
        print __doc__
        sys.exit(0)

def warning_or_error(message) :
        sys.stderr.write("%s\n" % message)
        sys.stderr.flush()

def parse_commandline(argv, short, long) :
        """Parses the command line, controlling options."""
        # split options in two lists: those which need an argument, those which don't
        withoutarg = []
        witharg = []
        lgs = len(short)
        i = 0
        while i < lgs :
                ii = i + 1
                if (ii < lgs) and (short[ii] == ':') :
                        # needs an argument
                        witharg.append(short[i])
                        ii = ii + 1 # skip the ':'
                else :
                        # doesn't need an argument
                        withoutarg.append(short[i])
                i = ii
        for option in long :
                if option[-1] == '=' :
                        # needs an argument
                        witharg.append(option[:-1])
                else :
                        # doesn't need an argument
                        withoutarg.append(option)

        # we begin with all possible options unset
        parsed = {}
        for option in withoutarg + witharg :
                parsed[option] = None

        # then we parse the command line
        args = []       # to not break if something unexpected happened
        try:
                options,args = getopt.getopt(argv, short, long)
                if options :
                        for (o, v) in options :
                                # we skip the '-' chars
                                lgo = len(o)
                                i = 0
                                while (i < lgo) and (o[i] == '-') :
                                        i = i + 1
                                o = o[i:]
                                if o in witharg :
                                        # needs an argument : set it
                                        parsed[o] = v
                                elif o in withoutarg :
                                        # doesn't need an argument : boolean
                                        parsed[o] = 1
                                else :
                                        # should never occur
                                        raise MP3CutError, "Unexpected problem when parsing command line."
                elif (not args) and sys.stdin.isatty() : # no option and no argument, we need to display help if stdin a tty
                        return
        except getopt.error,msg :
                warning_or_error(msg)
                return
        return (parsed, args)

def mp3cut(arguments) :
        short_options = "c:p:s:t:hvq"
        long_options = ["command=", "parts=", "segment=", "timeline=", "help", "version", "quiet" ]
        try :
                parsedcmdline = parse_commandline(arguments[1:], short_options, long_options)
                if parsedcmdline is None :
                        display_usage_and_quit()

                # get parsed options and remaining arguments
                (cmdline, args) = parsedcmdline

                # see if we have to display usage or version
                # if this is the case then the program ends here
                if (cmdline["version"] is not None) or (cmdline["v"] is not None) :
                        display_version_and_quit()
                elif (not args) or (cmdline["help"] is not None) or (cmdline["h"] is not None) :
                        display_usage_and_quit()
                else :
                        if len(args) > 1 :
                                args = args[0:1]
                                warning_or_error("pymp3cut currently accepts a single file argument, remaining files won't be cut.")
                        timeline = cmdline["timeline"] or cmdline["t"]
                        parts = cmdline["parts"] or cmdline["p"]
                        segment = cmdline["segment"] or cmdline["s"]
                        if not timeline and not parts and not segment:
                                raise MP3CutError, "Invalid timeline, parts or segment."
                        boolt = (timeline or 0) and 1        
                        boolp = (parts or 0) and 1
                        bools = (segment or 0) and 1
                        if (boolt + boolp + bools) != 1:
                                raise MP3CutError, "Use timeline OR parts OR segment."
                        file = MP3File(args[0])
                        if timeline :
                                file.read_timeline(timeline)
                                file.cut(cmdline["command"] or cmdline["c"], verbose = not (cmdline["quiet"] or cmdline["q"]))
                        elif parts :
                                file.calculate_parts(parts)
                                file.cut_parts(cmdline["command"] or cmdline["c"], verbose = not (cmdline["quiet"] or cmdline["q"]))
                        elif segment :
                                file.calculate_segment(segment)
                                file.cut_segment(cmdline["command"] or cmdline["c"], verbose = not (cmdline["quiet"] or cmdline["q"]))
        except MP3CutError, msg :
                warning_or_error(msg)
                sys.exit(-1)

if __name__ == "__main__" :
        mp3cut(sys.argv)
