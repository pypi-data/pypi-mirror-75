import requests
from bs4 import BeautifulSoup

def soupify(url,method='get',post_data=None,json_data=None):
    if method=='get':
        try:
            html = requests.get(url,params=json_data).content
            return BeautifulSoup(html,features="lxml")
        except:
            pass
    elif method=='post':
        try:
            html = requests.post(url,data=post_data,json=json_data).content
            return BeautifulSoup(html,features="lxml")
        except:
            pass
    else:
        pass