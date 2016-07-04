#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import re
import urllib2
import json
import os


def get_urls(url):
    result = re.findall(r"(http://.*?/)*", url)

    # phase 1
    try:
        response = urllib2.urlopen("%s" % url)
        html = response.read()

        result = re.findall(r"<div\sid=\"tab-......-[0-9]+\">(<div><a\shref|<span\shref)=\"(.*?)\"", html)
        pages = []
        for r in result:
            pages.append(r[1])
    except Exception as e:
        print e

    # phase 2
    video_url = []
    for i, r in enumerate(pages):
        try:
            request = urllib2.Request(r)
            request.add_header('User-Agent', 'Mozilla/5.0')
            response = urllib2.urlopen(request)
            html = response.read()
            result = re.findall(r"var\splaylist\s=\s(\[.*?\]);", html, re.S)
            j = json.loads(result[0])
            size = len(j[0]['sources'])
            max = j[0]['sources'][size - 1]['file']
            video_url.append(max)
        except Exception as e:
            print e
    return video_url


def download_by_aria2c(video_list):
    for i, l in enumerate(video_list):
        print "%02d" % (i)
        os.system("aria2c '%s' -o %02d.mp4" % (l, i))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get URLs for Animes")
    parser.add_argument("--base", "-b", required=True)
    args = parser.parse_args()

    download_by_aria2c(get_urls(args.base))
