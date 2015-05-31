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

import httplib
import urllib2
import re


def crawl():
    """
    Get data from server

    :return: HTML context in string
    """
    url = 'http://www.cc98.org/hottopic.asp'
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

    print 'Connecting...'
    request = urllib2.Request(url=url, headers=headers)
    try:
        result = urllib2.urlopen(request, timeout=30)
    except httplib.error:
        print 'Connection failed.'
        return ""

    raw_data = result.read()
    page_html = raw_data.decode('utf8')
    return page_html


def return_sample_data():
    """
    This function is used for offline developing.

    :return: a sample html file
    """
    f = open('sample/sample.html', 'r')
    return f.read()


def analysis(data):
    """
    Extract information from page.

    :param data: HTML string
    :return: none
    """
    pattern = r'<!--data update @ (.*)-->'
    print 'Collected in', re.findall(pattern, data)[0]
    pattern = r'<TD align=middle class=tablebody1>(.\d+)</td><TD align=middle class=tablebody1>(.\d+)</td><TD align=middle class=tablebody1>(.\d+)</td>'
    result = re.findall(pattern, data)
    for i in result:
        print i[0], i[1], i[2]


if __name__ == "__main__":
    html = crawl()
    if html != "":
        analysis(html)