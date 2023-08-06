import requests

def strip_url(url):
    return url.strip('/')

def url_to_domain(url):
    domain = strip_url(url).split("://")
    return domain[1]

def href_to_url(url,href):
    url = strip_url(url)
    if href.startswith("//"):
        return href[2:]
    elif href.startswith("data"):
        return href
    elif href.startswith('/'):
        return url+href
    elif href.startswith('.'):
        return url.rsplit('/',1)[0]+'/'+href
    else:
        return href

def check(url,method='get',post_data=None,json_data=None,timeout=2):
    if method=='get':
        try:
            return requests.get(url,params=json_data,timeout=timeout).status_code == 200
        except:
            return False
    elif method=='post':
        try:
            return requests.post(url,data=post_data,json=json_data,timeout=timeout).status_code == 200
        except:
            return False
    else:
        return False

def checklist(urllist):
    l = []
    for url in urllist:
        if check(url):
            l.append(url)
    return l

