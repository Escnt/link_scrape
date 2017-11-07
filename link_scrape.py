# -*- coding: utf-8 -*-
import re
import urlparse
import urllib2
import time
from datetime import datetime
import robotparser
import Queue
def download(url, user_agent='wswp', num_retries=3): #对给定的页面进行下载
    print 'Downloading:', url
    headers = {'User-agent': user_agent}
    request = urllib2.Request(url, headers=headers)
    try:
        html = urllib2.urlopen(request).read().decode("utf-8")
    except urllib2.URLError as e:
        print 'Download error:', e.reason
        html = None
        if num_retries > 0: #下载不成功,则进行两次重试
            if hasattr(e, 'code') and 500 <= e.code < 600:
                # retry 5XX HTTP errors
                html = download(url, user_agent, num_retries-1)
    return html
def same_domain(url1, url2): #判断两个网址域名是否一样
    """Return True if both URL's belong to same domain
    """
    return urlparse.urlparse(url1).netloc == urlparse.urlparse(url2).netloc
def get_links(html):
    # a regular expression to extract all links from the webpage
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
    # list of all links from the webpage
    return webpage_regex.findall(html)
def link_crawler(seed_url,max_depth=3):
    fp1 = open("url_download", "a")
    fp2 = open("link", "a")
    m = 0 #为了方便url的计数
    # the queue of URL's that still need to be crawled
    crawl_queue = [seed_url]
    # the URL's that have been seen and at what depth
    seen = {seed_url: 0}
    url_id ={seed_url: 0}
    while crawl_queue:
        url = crawl_queue.pop()
        depth = seen[url]
        id = url_id[url]
        fp1.write('url_id: '+str(id)+'   depth: '+str(depth)+url+'\n')
        try:
            html = download(url)
            if depth != max_depth:
                for link in get_links(html):
                    link = urlparse.urljoin(seed_url, link)
                    if link not in seen:
                        m = m + 1
                        fp2.write('url_id: ' + str(id) + '-----> url_id: ' + str(m) + url + '\n')
                        seen[link] = depth + 1
                        url_id[link] = m
                        # check link is within same domain
                        if same_domain(seed_url, link):
                            # success! add this new link to queue
                            crawl_queue.append(link)
        except Exception as e:
            pass
    fp1.close()
    fp2.close()



if __name__ == '__main__':
    link_crawler('http://www.shu.edu.cn/')


