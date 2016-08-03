# -*- coding: utf-8 -*-
import bs4
import requests
import re
import os
from sys import argv
from PIL import Image
from StringIO import StringIO
# Manga site specific module imports

from makesoup import makeSoup as maS
import Scrap_Batoto as Bato

'''
# function for saving manga images
Image.open(StringIO(payload.content)).save("manga2.png", "png")
'''

'''
LOOK UP raise_for_status() function in requests modules to make sure 
that response headers are good
'''


# gets current working directory in form of Unicode String u'..'
#cwd = os.getcwdu()
#print cwd

# Do not forget to put the closing '/' at the end of the URL or the script 
# won t be able to check for equality when determining whether to break the loop

url = argv[1]
print isinstance(url, str)
if url == None or not isinstance(url, str):
	print 'The input is invalid'
if url[-1] != '/':
	url = url + '/' 

################### TO CHANGE url must always finish with a '/' or the check for last page of last chapter will not work
# and generate NoneType Error while trying to find a comic_page id in the info page of manga
#url = 'http://bato.to/comic/_/comics/hai-to-gensou-no-grimgal-r15252'



#potage = maS(url)

# dico {chapterNumber : First page URI}
#dico_linkchapitres = Bato.makeChapterLinksDict(potage)


#for chapter in dico_linkchapitres.keys():
#	dico_linkchapitres


def checkForDir(chemin, dir):
	#T This function requires the OS module
	# chemin is the path at which to check for the existence of dir
	# dir is the dir whose existence is checked passed as a STRING
	listdir = os.listdir(chemin)
	if dir in listdir:
		return True
	else: 
		return False


def downloadManga(url):
	#prompt = raw_input('Do you want to DL all available chapters from Batoto? \n Y/n')
	mangaDir = ''
	titleDir = ''
	potage = maS(url)
	Title = Bato.mangaName(potage)
	chapterURIs = Bato.makeChapterLinksDict(potage)
	
	#Title = "BOUDA"
	print Title
	
	# current working directory
	cwd = os.getcwdu()

	if raw_input('The current working Directory is: ' + cwd + '\n'+
		'Continuing will create a "Manga" directory and put a \n'+
		'"' + Title + 
		'"\ndirectory in it. Do you want to proceed? Y/n ==> ')\
		!= 'Y':
		print 'User aborted'
		return 2
	else:
		print 'Checking for Manga Directory...'
		
		#for direct in listdir:
		#	print direct
				
		mangaDir = cwd+'/Manga'
		if checkForDir(cwd, 'Manga'):
			print 'Manga directory exists'
		else:
			print 'Manga directory does not exist'
			print 'Creating Manga directory'
			os.mkdir(mangaDir)
		print mangaDir
		os.chdir(mangaDir)
		titleDir = mangaDir+ '/' + Title
		if checkForDir(mangaDir, Title):
			print Title + ' directory exists'
		else:
			print Title + ' directory does not exist'
			print 'Creating ' + Title + ' directory'
			os.mkdir(titleDir)
		#print os.getcwdu() + '\n'
		for chapitre in chapterURIs.keys():
			os.chdir(titleDir)
			if checkForDir(titleDir, chapitre):
				print chapitre +' already has a dir. Passing on downloading'
				
			else:
				print 'Creating chapter directory'
				currentChapterDir = titleDir+ '/' + chapitre
				os.mkdir(currentChapterDir)
				print currentChapterDir + ' directory created'
				os.chdir(currentChapterDir)
				currentChapterPagesDir = Bato.makeChapterPageDic(maS(chapterURIs[chapitre]), url, chapterURIs)
				for page in currentChapterPagesDir.keys():
					print "Saving " + page
					dessin = requests.get(currentChapterPagesDir[page]).content
					Image.open(StringIO(dessin)).save(page + ".png", "png")

			

downloadManga(url)

