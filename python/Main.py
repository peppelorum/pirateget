# -*- coding: utf-8 -*-
#
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <p@bergqvi.st> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return. Peppe Bergqvist
# ----------------------------------------------------------------------------
#

import os
import sys

from BeautifulSoup import BeautifulSoup
import requests
import simplejson
#import envoy
from optparse import OptionParser
import unicodedata


class Pirateget():

    def which(self, program):
        def is_exe(fpath):
            return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

        fpath, fname = os.path.split(program)
        if fpath:
            if is_exe(program):
                return program
        else:
            for path in os.environ["PATH"].split(os.pathsep):
                exe_file = os.path.join(path, program)
                if is_exe(exe_file):
                    return exe_file

        return None

    def checkReqs(self):
        """
        Check that ffmpeg is installed
        """
        if not self.which('ffmpeg'):
            print 'ffmpeg seems not to be installed'
            sys.exit()

    def getVideo(self, url, filename):
        filename = unicodedata.normalize('NFKD', filename).encode('ascii','ignore')
        command = 'ffmpeg -i \"%s\" -acodec copy -vcodec copy -absf aac_adtstoasc "%s.mp4"' % (url, filename)
        os.system(command)
#        envoy.run(command)

    def sort_by_age(self, d):
        '''a helper function for sorting'''
        return int(d['meta']['quality'].split('x')[0])

    def run(self, url, path, filename):
        if url.startswith("http://svt") or url.startswith("http://www.svt") is not True:
            print("Bad URL. Not SVT Play?")
            sys.exit()

        r = requests.get(url)
        soup = BeautifulSoup(r.content, convertEntities=BeautifulSoup.HTML_ENTITIES)

        if not filename:
            try:
                filename = soup.find('title').text.replace(' | SVT Play', '')
            except:
                filename = 'could not parse'

        if path:
            filename = os.path.join(path, filename)

        video = requests.get('http://pirateplay.se/api/get_streams.js?url='+ url)

        json = simplejson.loads(video.content)
        json = sorted(json, key=self.sort_by_age, reverse=True)
        url = json[0]['url']

        self.getVideo(url, filename)


def main():
    parser = OptionParser(usage="usage: %prog [options] url")
    parser.add_option("-p", "--path",
                      action="store", # optional because action defaults to "store"
                      dest="path",
                      default=False,
                      help="Path to save the MP4 to",)
    parser.add_option("-f", "--filename",
                      action="store", # optional because action defaults to "store"
                      dest="filename",
                      default=False,
                      help="Filename to save the MP4 to",)
    (options, args) = parser.parse_args()

    if len(args) != 1:
        parser.error("wrong number of arguments")

    obj = Pirateget()
    obj.checkReqs()
    obj.run(args[0], options.path, options.filename)

    print options
    print args

if __name__ == '__main__':
    main()
