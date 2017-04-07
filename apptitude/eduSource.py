from bs4 import BeautifulSoup
import numpy as np
import grequests as async
import requests, json, re, gc
from urllib.parse import unquote
# from cramBuilder import bagOfWords

'''
Our site extractor:

    1. To traverse through google's results, use start endpoint:
        -> &start = (curPages * 10)
    2. Google's results are stored at: div id="res", & the links are at <h3 class="r">
    3. Extract these links and strip any superfluous characters in the url.
    4. Because we can't parse ppt or pdf, store them for 'relevant link display'
    5. Update current page.

    TODO: setup fetchknowledge, & NLP / TL;DR Algorithm
        -> For NLP (TL;DR) ALgorithm, look into how to make one using the NLTK framework.
            There are tutorials online for this.
'''


class NoteTaker(object):
    # default constructor: our sites for knowledge, current place in search, & knowledge
    def __init__(self, topic='', page=0, sites=[], relevant=[], size=1):
        self.topic = topic; self.page = page
        self.sites = sites; self.relevant = relevant
        self.size = size

    # we're slicing at [7:] because for whatever reason, /url?q= is appending to the front.
    # there is a chance that the anchor tag doesn't have a pertinent URL on some searches.
    # we also remove garbage at the back of the url as well.
    def takeNotes(self):
        try:
            _search = requests.get('https://www.google.com/search?q=' + self.topic + '&start=' + str(self.page * 10))
            webObject = BeautifulSoup(_search.text, "html.parser").find(id="res")
            _search.close()
            for url in webObject.find_all('h3'):
                try:
                    site = url.find('a')['href'][7:] #slice at beginning to remove crap
                    site = unquote(site[:site.find('&')]) #remove appended crap
                    ext = site[-4:]; vid = site.find('youtube')
                    if ext == '.pdf' or ext == '.ppt' or vid != -1:
                        self.relevant.append(site)
                    else:
                        self.sites.append(site)
                except Exception as e:
                    pass #dont catch the exception.
            # update the current page.
            self.page += 1
            # prevent duplicates, but lose order.
            self.sites = list(set(self.sites))
        except Exception as e:
            print("Exception: " + e.__class__.__name__)
        return self.fetchKnowledge() #pull the actual data.


    def parseData(self, response):
        try:
            site = BeautifulSoup(response.content.decode('utf-8'), "html.parser")
            site.script.decompose()
            return ' '.join(''.join([''.join(data.findAll(text=True))
                for data in site.findAll('p')]).replace(".", ". ").split())
        except Exception as e:
            print("Exception: " + e.__class__.__name__)
        return ''

    def fetchKnowledge(self):
        results = async.map([async.get(url, timeout=6) for url in self.sites])

        knowledge = [self.parseData(result) for result in results]
        #we're iterating over the queue which stored our data in the parallel
        #processes, we use None for the sentinel value so when there is no element
        #remaining, it terminates.
        bigdata = ''.join([data for data in knowledge])
        self.size = len(bigdata)
        return bigdata
