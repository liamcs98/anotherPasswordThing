import re 
import os
import urllib.request
import hashlib
import google
import sys

#TODO
#General Clean up/ do some better practices...when I learn them
#Add Hob0's rules https://github.com/praetorian-inc/Hob0Rules/blob/master/hob064.rule
#Find way to secure google searches to prevent 

perpass = ''
partialMatch = []
likeperpass = []

def testPassBasic(password):
	score = 0
	#Count chars, Upper, Numbers, and Symbols
	length=len(password)
	upper= len(re.findall('[A-Z]', password))
	numbers = len(re.findall('[0-9]',password))
	symbols = len(re.findall('[!@#$%^&*()_+-=}{\\\\]', password))
	print("%i,%i,%i,%i" % (length, upper, numbers, symbols))

def onlineFetchTest(password):

	passwordsArray = []
	def getPassesFromOnline(url):
		html = urllib.request.urlopen(url)
		data = html.read()
		cleaned = data.decode("utf-8").splitlines()
		passwordsArray.append(cleaned)
	def searchArray(level):
		global partialMatch
		for x in passwordsArray:
			for i in x:
				if i == password:
					print("Exact match at %s" % level)
				if i.find(password) > -1:
					partialMatch.append(i)

	getPassesFromOnline("https://raw.githubusercontent.com/berzerk0/Probable-Wordlists/master/Real-Passwords/Top196-probable.txt")
	searchArray("very popular: Top 200")
	passwordsArray = []	
	getPassesFromOnline("https://raw.githubusercontent.com/berzerk0/Probable-Wordlists/master/Real-Passwords/Top3575-probable.txt")
	searchArray("Quite Popular: Top 35,000")
	passwordsArray = []
	getPassesFromOnline("https://raw.githubusercontent.com/berzerk0/Probable-Wordlists/master/Real-Passwords/Top95Thousand-probable.txt")
	searchArray("Popular: Top 100,000")

def testAgainstList(password, *files):
	global partialMatch
	pureMatches = 0
	partMatches = 0 
	cwd = os.getcwd()
	for x in files:
		if not os.path.exists(os.path.join(cwd,x)):
			print("This file doesn't exist?: "+x)
		else:	
			with open(os.path.join(cwd,x), 'r', errors="ignore") as passList:
				for i in passList:
					i = i.strip()
					if i == perpass:
						pureMatches += 1
					if i.find(perpass) > -1:
						partMatches += 1
						partialMatch.append(i)

def getPass():
	global perpass
	perpass = input("Enter the perspective Password:\n").strip(' ')
	print(perpass)

def rules():
	global perpass
	global likeperpass
	rules = {'o':'0', '0':'o'}
	for letter in perpass:
		if letter in rules:
			likeperpass.append(perpass.replace(letter,rules[letter]))

def googleHashSearch(password):

	def md5Hash(string):
		hash_object = hashlib.md5(string.encode())
		hash_object= hash_object.hexdigest()
		return hash_object
	results = 0
	for url in google.search(md5Hash(password), stop=100):
		results += 1
		if results == 1:
			print("Top result its: %s" % url)
		sys.stdout.write("\rSearching the internet for Hash. Results: %i" % results)
	if results == 0:
		print("No Hash results online found. (Thats a good thing)")


if __name__ == '__main__':
	print("Howdy mate! \nThis is a program to test a pass.\n(Oh and when you give me the pass, leading spaces will be removed)\n")
	getPass()
	#rules()
	testPassBasic(perpass)
	onlineFetchTest(perpass)
	testAgainstList(perpass, "rockyouInput.txt", "tuscl.txt")
	googleHashSearch(perpass)
