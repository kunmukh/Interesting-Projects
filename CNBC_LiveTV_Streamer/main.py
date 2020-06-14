#!/usr/bin/env python3.6
# Kunal Mukherjee
# 3/15/20
# CNBC TV 18 Live Streamer

# import the libraries
import urllib.request
import os
import re
from selenium import webdriver, common
from webdriver_manager.chrome import ChromeDriverManager


# from the url get the video element html
def getVideoSourceHTML(urlName):

    # set up headless chrome option
    options = webdriver.ChromeOptions()
    options.add_argument('headless')

    # adding the headless option to selenium webdriver
    chromeDriver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)

    # use the chrome driver to open the url
    chromeDriver.get(urlName)

    # this will get the initial html - before javascript
    html1 = chromeDriver.page_source

    # this will get the html after on-load javascript
    html2 = chromeDriver.execute_script("return document.documentElement.innerHTML;")

    # get the video from element from the xpath
    try:
        videoElement = chromeDriver.find_element_by_xpath\
            ('/html/body/div[8]/div[2]/section/div/div/div/div[1]/div[2]/div[2]/video/source')

        # print the video element
        # print(videoElement)

        # get the source code of the element
        m3u8_source_html = videoElement.get_attribute("outerHTML")
        print("m3u8 file src HTML: ", m3u8_source_html)

        # close the chromedriver
        chromeDriver.close()

        # return the video source html for parsing
        return m3u8_source_html
    except common.exceptions.NoSuchElementException:
        print("No such element found. Program terminating")
        exit()


# get the m3u8 file url from the html
def getm3u8Url(source_html):
    # parse out the url
    parsed_string = re.compile('"(.*?)"', re.DOTALL).findall(source_html)

    m3u8_url = parsed_string[0]
    print("m3u8 file url: ", m3u8_url)

    return m3u8_url


# get the video link from the m3u8 file
def getVideoUrlfromm3u8(url):
    # download the m3u8 file
    urllib.request.urlretrieve(url, 'videoSource.m3u8')

    # open the file and read lines
    m3u8_file = open('videoSource.m3u8', 'r')
    lines = m3u8_file.readlines()

    # get the link which has RESOLUTION=896x504
    video_url = [lines[lines.index(line) + 1] for line in lines if "RESOLUTION=896x504" in line][0]

    # print the url
    print("Video url: ", video_url)

    # parse the url and take the url till the .m3u8
    parsed_video_url = video_url.partition("?")[0]

    # return the video url
    return parsed_video_url


# play video using streamlink
def playVideo(streamUrl):
    print("Starting the LIVE Video Stream in your native player")

    # open a pipe and play with the native player
    os.popen("streamlink " + streamUrl + " BEST")


def main():
    # part 1: web-scrape the website to get the video source
    m3u8_source = getVideoSourceHTML("https://www.cnbctv18.com/live-tv/")

    # part 2: parse the m3u8 url from the html
    m3u8_url = getm3u8Url(m3u8_source)

    # part 3: download the m3u8 file and get the video url
    video_url = getVideoUrlfromm3u8(m3u8_url)

    print("Final Video URL: ", video_url)

    # part 4: use streamlink to run the stream
    playVideo(video_url)


if __name__ == '__main__':
    main()