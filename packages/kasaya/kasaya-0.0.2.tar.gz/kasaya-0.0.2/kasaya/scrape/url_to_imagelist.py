import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from util import *

def imagelist(url,method='get',post_data=None,json_data=None):
    l = []
    url = strip_url(url)
    soup = soupify(url,method=method,post_data=post_data,json_data=json_data)
    for link in soup.find_all("img"):
        try:
            imgurl = link['src']
            l.append(href_to_url(url,imgurl))
        except:
            pass
    return l