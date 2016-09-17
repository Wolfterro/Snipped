#!/usr/bin/env python2
# -*- coding: utf-8 -*-

'''
The MIT License (MIT)

Copyright (c) 2016 Wolfgang Almeida <wolfgang.almeida@yahoo.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

#===================================
# Created by: Wolfterro
# Version: 1.0 - Python 2.x
# Date: 12/09/2016 - (DD/MM/YYYY)
#===================================

from __future__ import print_function
from StringIO import StringIO
from urllib2 import urlparse
from time import sleep

import os
import sys
import json
import pycurl
import urllib
import urllib2

# Version
# =======
VERSION = "1.0"

# Defining default encoding to UTF-8
# ==================================
reload(sys)
sys.setdefaultencoding('utf-8')

# Authorization Token
# You can fill the variable below with your Authorization Token
# (Api Token) instead of typing it.
#
# Use an empty string to make the program ask for it. 
#==============================================================
AUTH_TOKEN = ""


#===================================================
# POST / UPDATE METHODS: POSTING SNIPPETS ON GLOT.IO
# --------------------------------------------------
#
# The methods below are used to post and
# update snippets on 'https://glot.io'
#
#===================================================

# Getting filenames and their paths
# =================================
def getFilenames():
	argc = len(sys.argv)
	filenames = []
	count = 0
	for files in sys.argv:
		count += 1
		if count <= 2:
			continue

		if os.path.isfile(os.path.abspath(files)) == True:
			fpaths = os.path.abspath(files)
			filenames.append("%s" % (fpaths))
	
	return filenames

# Printing selected filenames and return them in full path
# ========================================================
def printFilenames():
	filenames = getFilenames()
	if len(filenames) == 0:
		print("\n[Snipped] Error! No valid files selected! Exiting ...")
		sys.exit(0)

	count = 0
	print("\n-------------------------\n")
	print("[Snipped] Selected files: ")
	for file in filenames:
		if count >= 6:
			print(" - %s - DISCARDED" % (os.path.basename(file)))
		else:
			print(" - %s" % (os.path.basename(file)))
		count += 1
	print("\n-------------------------\n")

	return filenames

# Method for print the available languages
# ========================================
def printAvailableLangs():
	langUrl = "https://run.glot.io/languages"
	availableLangsList = []

	try:
		response = urllib2.urlopen(langUrl).read().decode('utf-8')
	except Exception:
		print("[Snipped] Error! Could not list available languages!")
		print("[Snipped] Check your Internet connection and try again!")
		sys.exit(1)

	config = json.loads(response)
	for langs in config:
		availableLangsList.append("%s" % (langs['name']))

	print("[Snipped] Printing available languages...")
	for langs2 in availableLangsList:
		if langs2 in availableLangsList[len(availableLangsList) - 1]:
			sys.stdout.write("%s" % (langs2))
			sleep(0.05)
			sys.stdout.flush()
		else:
			sys.stdout.write("%s - " % (langs2))
			sleep(0.05)
			sys.stdout.flush()
	print("\n")
	
	return availableLangsList

# Selection Method: Language
# ==========================
def selectLanguage(availableLangsList):
	selectedLang = raw_input("[Snipped] Select your language of choice: ").lower()
	
	if selectedLang not in availableLangsList:
		print("[Snipped] Error! Language not available! Try again...\n")
		selectedLang = selectLanguage(availableLangsList)
	
	return selectedLang

# Selection Method: Title
# =======================
def selectTitle():
	selectedTitle = raw_input("[Snipped] Input a title for your snippet: ")
	if selectedTitle != "":
		return selectedTitle
	else:
		return "Untitled"

# Selection Method: Availability
# ==============================
def selectAvailability():
	selectedAvailability = raw_input("[Snipped] Do you want your snippet to be public? [y/N]: ").upper()
	if selectedAvailability == "Y":
		return True
	else:
		return False

# Selection Method: Authorization Token
# =====================================
def selectAuthToken():
	if AUTH_TOKEN == "":
		selectedAuthToken = raw_input("[Snipped] Insert your Authorization Token (blank for Anonymous snippet): ")
		return selectedAuthToken
	else:
		return AUTH_TOKEN

# Selection Method: Authorization Token
# Mandatory and only used to update snippets
# ==========================================
def selectMandatoryAuthToken():
	if AUTH_TOKEN == "":
		selectedAuthToken = raw_input("[Snipped] Insert your Authorization Token (obligatory): ")
		if selectedAuthToken == "":
			print("[Snipped] Error! No Authorization Token given! Exiting ...")
			sys.exit(0)
		else:
			return selectedAuthToken
	else:
		return AUTH_TOKEN

# Selection Method: URL of the snippet to be updated
# Returns a valid URL to update the snippet
# ==================================================
def selectURLToUpdate():
	urlToUpdate = raw_input("[Snipped] Insert the URL of the snippet to be updated: ")

	if urlToUpdate == "":
		print("[Snipped] Error! No URL given! Try Again...")
		urlToUpdate = selectURLToUpdate()

	isValidUrl = checkUrlDomain(urlToUpdate)
	if isValidUrl == True:
		validUrlToUpdate = "https://snippets.glot.io/snippets/%s" % (getSnippetID(urlToUpdate))
		return validUrlToUpdate
	else:
		print("[Snipped] Error! Invalid URL! Exiting ...")
		sys.exit(0)

# Method to get confirmation from the user
# ========================================
def confirmPostAction(numFiles):
	if numFiles > 6:
		print("[Snipped] Warning! Only the first 6 files will be used!")

	confirm = raw_input("[Snipped] Are these informations correct? Do you wish to proceed? [y/N]: ").upper()
	if confirm != "Y":
		print("[Snipped] Exiting ...")
		sys.exit(0)

# Method to process the contents and the names of chosen files
# ============================================================
def processContentFromFiles(filenames):
	contentList = []
	count = 0
	for file in filenames:
		if count == 6:
			break
		try:
			content = open(file, "rb")
			dict_files = {
				"name"		:	os.path.basename(file),
				"content"	:	content.read()
			}
			contentList.append(dict_files)
			count += 1
		except IOError:
			print("[Snipped] Error! Could not read file '%s'! Exiting ..." % (os.path.basename(file)))
			sys.exit(1)
	
	return contentList

# Method to show the Post (Authorized or Anonymous) response
# ==========================================================
def showPostOrUpdateResponse(postResponse):
	try:
		response = json.loads(postResponse)

		if "message" in response:
			if response['message'] == "Wrong auth token":
				print("[Snipped] Error! Snippet could not be created!")
				print("[Snipped] Check your Authorization Token and try again!")
				sys.exit(1)

		if response['id'] != None:
			print("[Snipped] Successful! Snippet created at https://glot.io/snippets/%s" % (response['id']))
		else:
			print("[Snipped] Error! Snippet could not be created/updated!")
			print("[Snipped] Check your Authorization Token or Internet connection and try again!")
			sys.exit(1)
	except Exception as ee:
		print("[Snipped] Warning! Could not receive or decode response from server!")
		print("[Snipped] Check the website if the snippet was posted/updated correctly!")
		print("[Snipped] Error: %s" % (ee))

# Assembling Method: Post (Authorized or Anonymous) Request
# =========================================================
def assemblePostOrUpdateRequest(selectedLang, selectedTitle, selectedAuthToken, selectedAvailability, filenames, updateURL, action):
	
	processedContents = processContentFromFiles(filenames)
	urlPost = "https://snippets.glot.io/snippets/"

	dict_post_request = {
		"language"	: selectedLang,
		"title" 	: selectedTitle,
		"public" 	: selectedAvailability,
		"files"		: processedContents
	}

	data = json.dumps(dict_post_request)
	buff = StringIO()						# In case the server response gets bigger than expected

	curl = pycurl.Curl()
	
	if action == "POST":
		curl.setopt(pycurl.URL, urlPost)
		curl.setopt(pycurl.POST, 1)

		if selectedAuthToken != "":
			curl.setopt(pycurl.HTTPHEADER, ['Authorization: Token ' + selectedAuthToken, 'Content-type: application/json'])
		else:
			curl.setopt(pycurl.HTTPHEADER, ['Content-type: application/json'])
	
	elif action == "UPDT":
		curl.setopt(pycurl.URL, updateURL)
		curl.setopt(pycurl.CUSTOMREQUEST, "PUT")
		curl.setopt(pycurl.HTTPHEADER, ['Authorization: Token ' + selectedAuthToken, 'Content-type: application/json'])

	curl.setopt(pycurl.POSTFIELDS, data)
	curl.setopt(pycurl.WRITEFUNCTION, buff.write)
	
	try:
		curl.perform()
		curl.close()
		postResponse = buff.getvalue()
		showPostOrUpdateResponse(postResponse)
	except Exception:
		print("[Snipped] Error! Snippet could not be created/updated!")
		print("[Snipped] Check your Authorization Token or Internet connection and try again!")
		sys.exit(1)

# Method to gather information about the snippet to Post
# ==============================================
def getSnippetInformationToPostOrUpdate(action):
	availableLangsList = printAvailableLangs()			# Returns a list
	
	# Values to be used to assemble the request
	# =========================================
	selectedLang = selectLanguage(availableLangsList)	# Returns a string
	selectedTitle = selectTitle()						# Returns a string
	
	if action == "POST":
		selectedAuthToken = selectAuthToken()				# Returns a string
		updateURL = None
	elif action == "UPDT":
		selectedAuthToken = selectMandatoryAuthToken()		# Returns a string
		updateURL = selectURLToUpdate()					# Returns a string
	
	selectedAvailability = selectAvailability()			# Returns a boolean

	filenames = printFilenames()						# Returns a list
	confirmPostAction(len(filenames))
	
	if action == "POST":
		print("[Snipped] Creating snippet \"%s\" ...\n" % (selectedTitle))
	elif action == "UPDT":
		print("[Snipped] Updating snippet to \"%s\" ...\n" % (selectedTitle))
	
	assemblePostOrUpdateRequest(selectedLang, selectedTitle, selectedAuthToken, 
		selectedAvailability, filenames, updateURL, action)

#===============================================
# DELETE METHODS: DELETING SNIPPETS FROM GLOT.IO
# ----------------------------------------------
#
# The methods below are used to delete snippets
# from 'https://glot.io'
#
#===============================================

# Method to show the Delete (Authorized) response
# ===============================================
def showDeleteResponse(deleteResponse):
	response = json.loads(deleteResponse)

	if "message" in response:
		if response['message'] == "Wrong auth token":
			print("\n[Snipped] Error! Snippet could not be deleted!")
			print("[Snipped] Check your Authorization Token and try again!")
			sys.exit(1)

# Assembling Method: Delete (Authorized) Request
# ==============================================
def assembleDeleteRequest(getID, selectedAuthToken):
	urlDelete = "https://snippets.glot.io/snippets/%s" % (getID)
	
	curl = pycurl.Curl()
	curl.setopt(pycurl.URL, urlDelete)
	curl.setopt(pycurl.HTTPHEADER, ['Authorization: Token ' + selectedAuthToken])
	curl.setopt(pycurl.CUSTOMREQUEST, 'DELETE')
	curl.setopt(pycurl.WRITEFUNCTION, showDeleteResponse)
	curl.perform()
	curl.close()

	# Server doesn't return a 'successful' response
	print("\n[Snipped] Snippet deleted! Check your account just to make sure!")

# Method to get confirmation from the user
# ========================================
def confirmDeleteAction():
	print("[Snipped] Warning! This process CANNOT be undone!!")
	confirm = raw_input("[Snipped] Are you sure? Do you wish to proceed? [y/N]: ").upper()
	
	if confirm == "Y":
		return True
	else:
		return False

# Method to select the URL of the snippet to delete, in case
# the user didn't provide it in the command line.
# ==========================================================
def selectUrlToDelete():
	urlToDelete = raw_input("[Snipped] Insert the URL of the snippet to be deleted: ")

	if urlToDelete == "":
		print("[Snipped] Error! No URL given! Try Again...")
		urlToDelete, trash = selectUrlToDelete()

	isValidUrl = checkUrlDomain(urlToDelete)
	if isValidUrl == True:
		return [urlToDelete, True]

# Method to gather information about the snippet to Delete
# ========================================================
def getSnippetInformationToDelete(urlToDelete):
	if urlToDelete == None:
		urlToDelete, validUrl = selectUrlToDelete()
	else:
		validUrl = checkUrlDomain(urlToDelete)

	if validUrl == True:
		if AUTH_TOKEN == "":
			selectedAuthToken = raw_input("[Snipped] Insert your Authorization Token (obligatory): ")
		else:
			selectedAuthToken = AUTH_TOKEN
		
		if selectedAuthToken == "":
			print("[Snipped] Error! No Authorization Token given! Exiting ...")
			sys.exit(0)
		
		getID = getSnippetID(urlToDelete)
		
		if confirmDeleteAction() == True:
			assembleDeleteRequest(getID, selectedAuthToken)
		else:
			print("[Snipped] Exiting ...")
			sys.exit(0)

#===========================================
# GET METHODS: GETTING SNIPPETS FROM GLOT.IO
# ------------------------------------------
#
# The methods below are used to get snippets
# from 'https://glot.io'
#
#===========================================

# Checking, creating and accessing the Main directory
# This directory will be used to store the snippets
# directories with their files
# ====================================================
def mainDirectory():
	if os.path.exists("Codes"):
		os.chdir("Codes")
	else:
		print("[Snipped] Creating directory 'Codes' ...")
		os.makedirs("Codes")
		os.chdir("Codes")

# Checking, creating and accessing the code's directory
# This directory will be used to store the codes from
# the snippet
# =====================================================
def codeDirectory(snippetDir, snippetID):
	if os.path.exists("%s-[%s]" % (snippetDir, snippetID)):
		os.chdir("%s-[%s]" % (snippetDir, snippetID))
	else:
		print("[Snipped] Creating directory '%s-[%s]' ..." % (snippetDir, snippetID))
		os.makedirs("%s-[%s]" % (snippetDir, snippetID))
		os.chdir("%s-[%s]" % (snippetDir, snippetID))

# Method to get the information about the snippet 
# from it's JSON data
# ===============================================
def getSnippetJson(snippetUrl, apiUrl):
	try:
		response = urllib2.urlopen(apiUrl).read().decode('utf-8')
	except Exception:
		print("[Snipped] Error! Could not open URL '%s'!" % (snippetUrl))
		print("[Snipped] Check the URL or Internet connection and try again!")
		sys.exit(1)

	getConfigJson = json.loads(response)

	getTitle = getConfigJson["title"].encode('utf-8')
	numberOfCodes = len(getConfigJson["files"])
	snippetDir = getTitle.replace("/", "-")

	return [getTitle, numberOfCodes, snippetDir, getConfigJson]

# Method to create the code files
# ===============================
def getSnippetCodes(numberOfCodes, getSnippetJson):
	for x in range(0, numberOfCodes):
		getFilename = getSnippetJson["files"][x]["name"].replace("/", "-")
		
		print("[Snipped] Creating file '%s' ..." % (getFilename), end="")
		fileCode = open(getFilename, "wb")
		fileCode.write(getSnippetJson["files"][x]["content"].encode('utf-8'))
		fileCode.close()
		print(" OK!")

# Method to get the snippet URL to download
# =========================================
def getSnippetInformationToDownload(snippetUrl):
	mainDirectory()

	if snippetUrl == None:
		snippetUrl = raw_input("[Snipped] Insert the Snippet's URL: ")
	
	isValidUrl = checkUrlDomain(snippetUrl)

	if isValidUrl == True:
		snippetID = getSnippetID(snippetUrl)
		apiUrl = "https://snippets.glot.io/snippets/" + snippetID

		print("")

		getTitle, numberOfCodes, snippetDir, getConfigJson = getSnippetJson(snippetUrl, apiUrl)
		codeDirectory(snippetDir, snippetID)
		getSnippetCodes(numberOfCodes, getConfigJson)

#==============================================
# COMMON METHODS: ESSENTIAL METHODS FOR SNIPPED
# ---------------------------------------------
#
# These methods are not exclusive, they are
# used by multiple operations
#
#==============================================

# Method to check the URL domain
# ==============================
def checkUrlDomain(urlToCheck):
	url_split = urlparse.urlsplit(urlToCheck)

	if str(url_split[1]) != "glot.io" and str(url_split[1]) != "snippets.glot.io":
		print("[Snipped] Error! Wrong website! Check the URL and try again!")
		sys.exit(1)
	else:
		return True

# Method to get the ID from the URL
# =================================
def getSnippetID(urlToCheck):
	return os.path.basename(urlToCheck)

#==============================================
# ---------------------------------------------
# ---------------------------------------------
# ---------------------------------------------
#==============================================

# Help menu
# =========
def showHelpMenu():
	print("[Options]:")
	print("----------\n")

	print(" -h || --help\t\tShow this help menu.")
	print(" -p || --post\t\tSelect files to be posted. At least one file is required.")
	print(" -d || --delete\t\tDelete snippet on the website. Cannot be undone!!")
	print(" -g || --get\t\tDownload the snippet files to your computer.")
	print(" -u || --update\t\tUpdate the snippet files on the website. At least one file is required.\n")

	print("[Examples]:")
	print("-----------\n")

	print("Help:")
	print("-----")
	print("./Snipped.py [-h / --help]\n")
	
	print("Post Snippets (Authorization Token is optional):")
	print("------------------------------------------------")
	print("./Snipped.py [-p / --post] [FILE 1] [FILE 2] ... [FILE 6]\n")
	
	print("Delete Snippets (Requires Authorization Token):")
	print("-----------------------------------------------")
	print("./Snipped.py [-d / --delete] [URL]\n")

	print("Update Snippets (Requires Authorization Token):")
	print("-----------------------------------------------")
	print("./Snipped.py [-u / --update] [FILE 1] [FILE 2] ... [FILE 6]\n")
	
	print("Get Snippets:")
	print("-------------")
	print("./Snipped.py [-g / --get] [URL]\n")

	print("======================================\n")

	print(" *** This program is licensed under MIT License ***\n")

	print("The software is provided \"as is\", without warranty of any kind, express or")
	print("implied, including but not limited to the warranties of merchantability, ")
	print("fitness for a particular purpose and noninfringiment.\n")

	print("Copyright (c) 2016 Wolfgang Almeida <wolfgang.almeida@yahoo.com>")
	print("GitHub Repo: https://github.com/Wolfterro/Snipped\n")

# Main Method
# ===========
def main():
	argc = len(sys.argv)
	
	possibleArgs = ["-p", 
					"-h",
					"-d",
					"-g",
					"-u", 
					"--post", 
					"--help",
					"--delete",
					"--get",
					"--update"]

	print("===========================================")
	print("Snipped: Snippet client for glot.io! - v%s" % (VERSION))
	print("===========================================\n")

	if argc > 2:
		# Check if first option exists
		# ============================
		if str(sys.argv[1]) not in possibleArgs:
			print("[Snipped] Error! Unknown option!")
			print("[Snipped] Use -h or --help to list available options.\n")
		
		# Checking
		# ========
		elif str(sys.argv[1]) == "-p" or str(sys.argv[1]) == "--post":
			getSnippetInformationToPostOrUpdate("POST")	# No need to pass the files as an argument

		elif str(sys.argv[1]) == "-d" or str(sys.argv[1]) == "--delete":
			getSnippetInformationToDelete(str(sys.argv[2]))
		
		elif str(sys.argv[1]) == "-g" or str(sys.argv[1]) == "--get":
			getSnippetInformationToDownload(str(sys.argv[2]))

		elif str(sys.argv[1]) == "-u" or str(sys.argv[1]) == "--update":
			getSnippetInformationToPostOrUpdate("UPDT")
	
	elif argc == 2:
		# Check if first option exists
		# ============================
		if str(sys.argv[1]) not in possibleArgs:
			print("[Snipped] Error! Unknown option!")
			print("[Snipped] Use -h or --help to list available options.\n")
		
		# Checking
		# ========
		elif str(sys.argv[1]) == "-h" or str(sys.argv[1]) == "--help":
			showHelpMenu()
		
		elif str(sys.argv[1]) == "-p" or str(sys.argv[1]) == "--post":
			print("[Snipped] Error! No files given! At least one file required!")
			print("[Snipped] Use -h or --help to list available options.\n")
		
		elif str(sys.argv[1]) == "-d" or str(sys.argv[1]) == "--delete":
			getSnippetInformationToDelete(None)

		elif str(sys.argv[1]) == "-g" or str(sys.argv[1]) == "--get":
			getSnippetInformationToDownload(None)

		elif str(sys.argv[1]) == "-u" or str(sys.argv[1]) == "--update":
			print("[Snipped] Error! No files given! At least one file required!")
			print("[Snipped] Use -h or --help to list available options.\n")
	
	else:
		print("[Snipped] Error! No options given!")
		print("[Snipped] Use -h or --help to list available options.\n")

if __name__ == "__main__":
	main()