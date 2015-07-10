#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# cc98 hot topic crawler
# Copyright (C) 2015 James Swineson
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

from __future__ import unicode_literals
import sys
import os
import httplib
import urllib2
import re
import json
import pprint

class MyPrettyPrinter(pprint.PrettyPrinter):
    def format(self, object, context, maxlevels, level):
        if isinstance(object, unicode):
            return (('"' + object + '"').encode('utf8'), True, False)
        return pprint.PrettyPrinter.format(self, object, context, maxlevels, level)

def downloadFile(url, file_name):
    #file_name = url.split('/')[-1]
    u = urllib2.urlopen(url)
    f = open(file_name, 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print "Downloading: %s Bytes: %s" % (file_name, file_size)

    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8)*(len(status)+1)
        print status,

    f.close()
    print ""

def crawl(url):
    """
    Get data from server

    :return: HTML context in string
    """
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36'
    cookie = ''
    connection = 'keep-alive'
    cache_control = 'max-age=0'
    accept_encoding = ''
    accept_language = 'zh-CN,zh;q=0.8,zh-TW;q=0.6,en-US;q=0.4,en-GB;q=0.2'
    accept = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'

    headers = {
        'Connection': connection,
        'Cache-Control': cache_control,
        'accept': accept,
        'User-Agent': user_agent,
        'Accept-Encoding': accept_encoding,
        'Accept-Language': accept_language,
        'Cookie': cookie
    }

    request = urllib2.Request(url=url, headers=headers)
    try:
        result = urllib2.urlopen(request, timeout=30)
    except httplib.error:
        return ""

    raw_data = result.read()
    page_html = raw_data.decode('utf8')
    return page_html

def extractID(url):
    pattern = r'id=([0123456789abcdef]+)'
    result = re.findall(pattern, url)
    return result[0]

def getPicture(data):
    pattern = r'<img style="width: 500px;height: 500px;" src="(.*)">'
    result = re.findall(pattern, data)
    return result[0]

def getInf(id):
    # http://www.beiwo.ac/users/getSoundByIdWithAjax?id=5455fe1be4b06ba70c54300e&code=0
    url = 'http://www.beiwo.ac/users/getSoundByIdWithAjax?id=' + id + '&code=0'
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36'
    cookie = ''
    connection = 'keep-alive'
    cache_control = 'max-age=0'
    accept_encoding = ''
    accept_language = 'zh-CN,zh;q=0.8,zh-TW;q=0.6,en-US;q=0.4,en-GB;q=0.2'
    accept = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'

    headers = {
        'Connection': connection,
        'Cache-Control': cache_control,
        'accept': accept,
        'User-Agent': user_agent,
        'Accept-Encoding': accept_encoding,
        'Accept-Language': accept_language,
        'Cookie': cookie
    }

    request = urllib2.Request(url=url, headers=headers)
    try:
        result = urllib2.urlopen(request, timeout=30)
    except httplib.error:
        return ""

    raw_data = result.read()
    page_html = raw_data.decode('utf-8')
    return page_html

def getTitle(data):
    pattern = r'<a class="textAbridge" title="(.*)" style="display: block;width:100%;color:#3e3e3e;">'
    result = re.findall(pattern, data)
    return result[0]

def getAuthor(data):
    pattern = r'<a class="textAbridge" title="(.*)" style="font-size:13px;display: block;width:160px;color:#656565;">'
    result = re.findall(pattern, data)
    return result[0]

def getDescription(data):
    pattern = r'<div class="myTable" id="lyricsId" style="display: none;margin-top: 0px;"><pre style="font-size: 12px;color: #797979;line-height: 18px;">(.*)</pre></div>'
    result = re.findall(pattern, data)
    return result[0]

def download(id, path):
    print "Music ID: ", id
    print "Downloading metadata..."
    data = json.loads(getInf(id))
    print "Title: ", data[u'items'][0][u'title]
    with open(str(path) + "metadata.txt", "w") as metadata:
        metadata.write("ID: %s\nMetadata: \n" % id)
        datastring = MyPrettyPrinter().pformat(data)
        metadata.write(datastring)
    print "Downloading song..."
    downloadFile(data[u'items'][0][u'sound'][u'url'], path + data[u'items'][0][u'sound'][u'name'])
    print "Downloading cover..."
    downloadFile(data[u'items'][0][u'cover'][u'url'], path + data[u'items'][0][u'cover'][u'name'])
    print "Download finished.\n"

def downloadWrapper(url, path='.'):
    id = extractID(url)
    if id != "":
        fullpath = (path + "/" + id + "/").replace("//", "/")
        if not os.path.exists(fullpath):
            os.makedirs(fullpath)
        download(id, fullpath)
    else:
        print "Wrong URL!"

def batchDownload(urls):
    for u in urls:
        downloadWrapper(u)

def batchGetUrl(file):
    with open(file,'r') as f:
        a = f.read().splitlines()
    return a

if __name__ == "__main__":
    # url = 'http://www.beiwo.ac/users/audioIndexPc?id=5455fe1be4b06ba70c54300e'
    batchDownload(batchGetUrl(sys.argv[1]))
