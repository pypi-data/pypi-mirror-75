import sys
from os import path
import requests
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from util import *


def find_favicon(soup):
    if soup.find('link', rel='shortcut icon'):
        return soup.find('link', rel='shortcut icon')
    elif soup.find('link', rel='icon'):
        return soup.find('link', rel='icon')
    elif soup.find('link', rel='mask-icon'):
        return soup.find('link', rel='mask-icon')
    else:
        return
    
def guess_favicon(url):
    if check(url+'/favicon.ico'):
        return url+'/favicon.ico'
    else:
        pass

def favicon(url,method='get',post_data=None,json_data=None):
    url = strip_url(url)
    soup = soupify(url,method=method,post_data=post_data,json_data=json_data)
    if find_favicon(soup) !=None:
        try:
            _favurl = find_favicon(soup)['href']
            return href_to_url(url,_favurl)
        except:
            return guess_favicon(url)

    else:
        return guess_favicon(url)

l = ['http://verisign.com', 'http://addthis.com', 'http://crashlytics.com', 'http://amazonaws.com', 'http://live.com', 'http://digicert.com', 'http://pubmatic.com', 'http://instagram.com', 'http://mathtag.com', 'http://gmail.com', 'http://linkedin.com', 'http://yahooapis.com', 'http://chartbeat.net']