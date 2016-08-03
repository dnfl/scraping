# -*- coding: utf-8 -*-
import bs4
import requests
import re


# Done as of 16/07/2015
def makeSoup(url):
	powder = requests.get(url).text
	#print url
	return bs4.BeautifulSoup(powder)
