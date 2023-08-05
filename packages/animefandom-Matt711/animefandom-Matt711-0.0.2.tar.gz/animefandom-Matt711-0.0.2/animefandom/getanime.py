"""
Author: Matthew Murray
Description: Scrape anime articles summaries from fandom anime pages
"""
from bs4 import BeautifulSoup
import urllib.request
class AnimeFandom:
    def __init__(self, url):
        self.url = url
    def getSummary(self):
        page = urllib.request.urlopen(self.url)
        soup = BeautifulSoup(page, "lxml")
        allPar = soup.find_all('p')
        del allPar[0]
        summary = ""
        for i in range(len(allPar)):
            uncleanLines = allPar[i].find_all('a')
            paragraph = allPar[i].contents
            for j, line in enumerate(paragraph):
                if line in uncleanLines:
                    paragraph[j] = line.contents[0]
            summary+="".join(paragraph)
        summary = summary.replace("\n","")
        return summary
