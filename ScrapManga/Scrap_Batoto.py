# -*- coding: utf-8 -*-

import bs4
import requests
from makesoup import makeSoup as maS

"""
Module pertaining to scraping manga from Batoto
Contains functions for retrieving:

- > list of chapters and store it into a dict 
		{chap_number:URI}
- > all images URIs of a chapter and store them in a dict 
		{page_number:URI}

More to come


"""

# BATOTO
# AT LAST PAGE OF LAST CHAPTER, REDIRECTS TO MANGA HOME PAGE
# Go to chapter list
# then: 
# create dict for chapter names and url of first page named 'chapter_dict'
# -> liste_li soup.find(class_='chapter_list').find_all('li')
# -> for i in liste_li:
# -> 	chapter_dict[i.a.text.strip()] = i.a['href']

#  ******************************************************************************
# FUNCTIONS
# MangaChapterListURI = URL FOR THE CHAPTER LIST

def mangaName(BSoupObject, mute=True):
	# The BSoupObject passed must be that of the info and chapter list page for the manga
	mangaTitle = BSoupObject.find(class_="ipsType_pagetitle").string.strip(' \r\n')
	if mute == False:
		print mangaTitle
	return mangaTitle


def makeChapterLinksDict(BSoupObject):
	# Have the dict passed in argument or initialized in the function??
	# for now, init in the function
	chapter_dict = {}
	dan = BSoupObject.select("tr.row.lang_English.chapter_row")
	for i in dan:
		
		#print i.a["title"][:i.a["title"].find('|')-1]
		chapter_dict[i.a["title"][:i.a["title"].find('|')-1]] = i.a["href"]

	return chapter_dict
	# returns a dict with { chapterName : URI }


def makeChapterPageDic(BSoupObject, MangaChapterListURI, chapter_dict, pages_dict=None):
	# BSoupObject is a BSoup Object containning link for next page and image URI for current page
	# MangaChapterListURI is the base URI of the manga with list of chapters and details
	# chapter_dict is the dict of {chap_number:URI}
	# pages_dict is dict {Page number:image URI}
	

	#print MangaChapterListURI
	if pages_dict == None:  #Initialization of the loop -> creating a dict 
	# which will recursively be passed and hold the {Page number:image URI}
		print 'creating pages_dict'
		pages_dict = dict()
	
	
	# dan = BSoupObject.find_all(id="comic_page")[0]
	# why use the list when there is only one instance of #comic_page
	dan = BSoupObject.find(id='comic_page')

	page_number = dan["alt"][dan["alt"].index('Page '):-10]
	pages_dict[page_number] = dan["src"]
	try:
	# if next page is list of chapters then break loop and return pages_dict
		if dan.parent["href"] == MangaChapterListURI:
			return pages_dict
		

	except AttributeError:
		print '****************'

	URI_next = dan.parent["href"]										#.encode('utf-8')

	if dan.parent["href"] in chapter_dict.values():
		return pages_dict

	return makeChapterPageDic(maS(URI_next), MangaChapterListURI, chapter_dict, pages_dict)

