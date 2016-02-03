from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import time


def getNames(bsObj):
	""" Returns list of all business names on page """
	names = []
	for name in bsObj.findAll("p", {"class":"brand-color li-font-weight"}):
		name = name.get_text()
		names.append(name)
	return names

def getAddresses(bsObj):
	""" Returns list of all addresses on page """
	addresses = []
	for address in bsObj.findAll("p", {"class":"li-font-weight"}):
		address = address.get_text()
		# Strips tel out of address
		addressClean = address.split("Tel:")[0]
		addresses.append(addressClean)
	addresses = addresses[1::2]	# deletes every odd item (names were being included)
	return addresses

def getTel(bsObj):
	tels = []
	""" Stores all tel nums on page """
	for tel in bsObj.findAll("span", text=re.compile("Tel"), attrs = {"class":"pull-right"}):
		tel = tel.get_text()
		tels.append(tel)
	return tels

def getNextPage(bsObj):
	""" Returns next page if available, or None othersise """
	try:
		nextButton = bsObj.find("a", text = "Next", attrs = {"class" : "btn btn-default next-btn margin-top-pagen-5"})["href"]
	except TypeError:
		print("Final page reached")
	else:
		return nextButton



""" MAIN LOOP - through all available pages of results """

html = urlopen("http://www.qataronlinedirectory.com/103120/company-list/companies-qatar/BEAUTY-SALONS")
bsObj = BeautifulSoup(html, "html.parser")

loopCount = 0


while True:
	loopCount += 1
	time.sleep(2)
	# print/store data from that page
	print("\n/////////////////// COMMENCING LOOP %d ////////////////////////" % loopCount) 
	print("------------------------NAMES----------------------------------")
	print(getNames(bsObj))
	print("------------------------ADDRESSES------------------------------")
	print(getAddresses(bsObj))
	print("----------------------ß--TELS-----------------------------------")
	print(getTel(bsObj))
	print("\n\n")

	# update bsObj to the next page if present
	try:
		nextPage = urlopen(getNextPage(bsObj))
		bsObj = BeautifulSoup(nextPage, "html.parser")
	except:

		print("Exiting main loop")
		break


""" 23/01/16 ----------------------------
All working. Next:
1. Plan arrangement of database		e.g what fields we need (industry?), how to arrange in tables

---------------------------------------"""


"""
# IDEA. Index into functions for MYSQL storage?
Eg.

def storeData:
	for listing in len(array of names/address to get length):
		name = getNames(bsObj)[listing]
		address = getAddresses(bsObj[listing]
		tel = getTel(bsObj)[listing]
		THEN STORE EACH VARIABLE TO A ROW IN MYSQL

"""


