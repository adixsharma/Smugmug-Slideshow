import urllib #import functions from an external library or source
import xml.etree.ElementTree as ET #imports functions and renames import as ET for efficiency
import re #imports functions for regular expressions
import sqlite3 as lite #imports functions and renames import as ET for efficiency
import random
import numpy
import numpy.random
import Image

SitemapIndexURL = "http://manish.smugmug.com/sitemap-index.xml" 

def fetchURLContent(url): #defines a function with a parameter "url"
	ufile = urllib.urlopen(url)
	content = ufile.read()
	return content #content is returned


def parseCategoryURLNodes(xmlToParse):#defines a function with a parameter "xmlToParse"
	sitemapIndexParent = ET.fromstring(xmlToParse)
	listOfLocs = []  #creates an empty array
	sitemapObjectList = sitemapIndexParent.findall('{http://www.sitemaps.org/schemas/sitemap/0.9}sitemap')
	
	for sitemap in sitemapObjectList:
		loc = sitemap.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
		url = re.sub(r'.gz','',loc.text)  #replaces .gz with nothing in image url
		listOfLocs.append(url) #adds the modified url in array listoflocs
	return listOfLocs	

def parseGalleryURLNodes(xmlToParse):
	gallerymapIndexParent = ET.fromstring(xmlToParse)
	rowset = []
	urlObjectList = gallerymapIndexParent.findall('{http://www.sitemaps.org/schemas/sitemap/0.9}url')
	
	for imageObj in urlObjectList:
		loc = imageObj.find('{http://www.google.com/schemas/sitemap-images/1.1}image/{http://www.google.com/schemas/sitemap-images/1.1}loc')
		dateTaken = imageObj.find('{http://www.google.com/schemas/sitemap-images/1.1}image/{http://www.google.com/schemas/sitemap-images/1.1}creation_date')
		galleryName = imageObj.find('{http://www.google.com/schemas/sitemap-images/1.1}image/{http://www.google.com/schemas/sitemap-images/1.1}collection')

		if loc is not None:
			url = re.sub(r'/0/L/','/0/X2/',loc.text)  #removes '/0/L/' from whole image url and subs in '/0/X2/' for the largest image file format
			url = re.sub(r'-L.jpg','-X2.jpg',url) #removes '-L.jpg' from the image url and replaces it with '-X2.jpg' to complete the large image file url
			imageTuple = (url, dateTaken.text, galleryName.text) # takes date the picture was taken as well as the gallery name and stores it
			rowset.append(imageTuple)
		else:
			print "Skipping insert because image location is null..."  #if url cannot be changed as it is formatted differently, it is skipped

	return rowset

def insertRows(rowsToInsert):
	con = lite.connect('testdb')
	with con:
		cur = con.cursor()
		cur.executemany("insert into image_urls(url,date_taken,gallery_name) values(?,?,?)", rowsToInsert) #inserts urls of images, date the picture was taken and the gallery name in a table
	print "Done inserting URLs for gallery..."
		
def deleteURLs():
	con = lite.connect('testdb')
	with con:
		cur = con.cursor()
		cur.execute("DELETE FROM image_urls")	

def getURLs():
	con = lite.connect('testdb')
	with con:
		cur = con.cursor()
		cur.execute("SELECT * FROM image_urls")

		rows = cur.fetchall()
		Images = []
		for row in rows:
			image_obj = Image.Image(row)
			Images.append(image_obj)

		return Images

def getPageOfImages(offset, limit):
	if (offset is None): 
		offset = 0
	if (limit is None):
		limit = 5

	con = lite.connect('testdb')
	with con:
		cur = con.cursor()
		cur.execute("SELECT * FROM image_urls order by id limit " + str(limit) + " offset " + str(offset))

		rows = cur.fetchall()
		Images = []
		for row in rows:
			image_obj = Image.Image(row)
			Images.append(image_obj)

		return Images


def initializeURLs():
	xmlString = fetchURLContent(SitemapIndexURL)
	galleryMapURLs = parseCategoryURLNodes(xmlString)
	allTuples = []

	i = 1 #deliberately started with index 1, because the first gallery contains the list of gallery URLs, not the gallery sitemaps
	while i < len(galleryMapURLs):
		galleryURLsXML = fetchURLContent(galleryMapURLs[i])
		rowsToInsert = parseGalleryURLNodes(galleryURLsXML)
		allTuples.extend(rowsToInsert)
		# insertRows(rowsToInsert)
		i = i + 1;
	
	random.shuffle(allTuples)
	# 		deleteURLs()
	insertRows(allTuples)
	print allTuples



	

"""print "Done inserting all records..."
for u in allTuples:
	print u
"""