
# -*- coding: utf-8 -*-
# vim:fileencoding=utf8
# CDDL HEADER START
#
# The contents of this file are subject to the terms of the
# Common Development and Distribution License (the "License").
# You may not use this file except in compliance with the License.
#
# You can obtain a copy of the license in the LICENSE.CDDL file
# or at http://dev.sikevux.se/LICENSE.txt
# See the License for the specific language governing permissions
# and limitations under the License.
#
# When distributing Covered Code, include this CDDL HEADER in each
# file and include the License file LICENSE.CDDL
# If applicable, add the following below this CDDL HEADER, with the
# fields enclosed by brackets "[]" replaced with your own identifying
# information: Portions Copyright [yyyy] [name of copyright owner]
#
# CDDL HEADER END
# 
#
# Copyright 2011 Patrik Greco All rights reserved.
# Use is subject to license terms.
#

import os
import sys
import re
import unicodedata

from BeautifulSoup import BeautifulSoup
import requests

bitrate = 2400

def f5(seq, idfun=None):
# order preserving
    if idfun is None:
        def idfun(x): return x
    seen = {}
    result = []
    for item in seq:
        marker = idfun(item)
        # in old Python versions:
        # if seen.has_key(marker)
        # but in new ones:
        if marker in seen: continue
        seen[marker] = 1
        result.append(item)
    return result

def getVideo(filename, rtmp, swf):

    print("Running RTMPDump on " + rtmp + " and saving it as " + filename + ".mp4")
    print 'rtmpdump -r ' + rtmp + ' --swfVfy=' + swf + ' -o ' + filename + '.mp4'
    os.system('rtmpdump -r ' + rtmp + ' --swfVfy=' + swf + ' -o "' + filename + '.mp4"')


def getSwfUrl(html):
    p = re.compile('data="([^"]+.swf)"')
    ret = p.search(r.content)
    if not ret:
        raise Exception('Unable to find player swf, is URL working?')

    return 'http://svtplay.se'+ ret.group().split('data="')[1].strip('"')

user_input_url = raw_input('URL to SVT Play you want to download: ')

if user_input_url.startswith("http://svt") is not True:
    print("Bad URL. Not SVT Play?")
    sys.exit()

r = requests.get(user_input_url)

swfUrl = getSwfUrl(r.content)

soup = BeautifulSoup(r.content)
filename = soup.find('title').text.replace(' | SVT Play', '') +' - '+ soup.findAll('h2')[0].text

p = re.compile('rtmp[e]?:[^|&]+,bitrate:[0-9]+')
videos = f5(p.findall(r.content))
for video in videos:
    urlQuality = video.split(',bitrate:')

    if int(urlQuality[1]) == bitrate:
        filename = unicodedata.normalize('NFKD', filename).encode('ascii','ignore')
        getVideo(filename, urlQuality[0], swfUrl)

