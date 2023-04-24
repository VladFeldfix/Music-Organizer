import os
import time
from os import walk
import shutil
from database import *

class main:
	def __init__(self):
		s = self
		s.load_obj() #load all the objects
		s.settings = s.database.fileTOdict("config.set",";") #load settings
		s.mymusic = s.database.fileTOdict("myMusic.csv",",") #load my music database
		s.readfromfolder()

	def readfromfolder(s):
		#get the music filder from settings, or update settings
		try:
			folder = s.settings["music_location"]
		except:
			s.settings["music_location"] = input("Where is your music folder?\n>")
			folder = s.settings["music_location"]
			s.database.updateFile(filename="config.set", data=s.settings, sep=";")

		#make a list of music files in a given folder
		if type(folder) is list:
			fld = folder[0]
		else:
			fld = folder
		for root, dirs, files in os.walk(fld):
			for i in files:
				if ".mp3" in i:
					filename = root.replace("\\","/").replace(",","")+'/'+i.replace("\\","/").replace(",","")
					if not s.database.keyExist(dictt=s.mymusic, key=filename):
						s.mymusic[filename] = ""
		s.database.updateFile(filename="myMusic.csv", data=s.mymusic, sep=",")
		#sprint(s.mymusic)
		con = int(input("myMusic.csv was updated!\nWhat would you like to do today?\n1. Add new music\n2. Upload music to the phones\n3. exit\n>"))
		if con == 1:
			s.add_new_music()
		elif con == 2:
			s.update_phone()

	def add_new_music(s):
		#get folder names
		from_folder = input("Tranfer new music from: ")
		to_folder = s.settings["music_location"][0]

		for root, dirs, files in os.walk(from_folder):
			for i in files:
				if ".mp3" in i:
					transfer = False
					#get the name of the artist
					artist = i.split(" - ")[0]
					#check if the file exists or not
					if os.path.isfile(to_folder+"/"+artist+"/"+i):
						print("%s already exists in %s" % (i, to_folder))
					else:
						#if the folder dosent exist, create it
						if not os.path.exists(to_folder+"/"+artist):
							os.mkdir(to_folder+"/"+artist)
							transfer = True
						else:
							transfer = True
					#if file tranffare was approved
					if transfer:
						shutil.move(from_folder+"/"+i, to_folder+"/"+artist+"/"+i)
						print("%s was successfully transferred from %s to %s" % (i,from_folder,to_folder+"/"+artist))
		s.readfromfolder()

	def update_phone(s):
		#get folder names
		from_folder = s.settings["music_location"][0]
		to_folder = input("Your phone location: ")
		userslst = ""
		i = 0
		for n in s.mymusic["filename"]:
			i += 1
			if n != "":
				userslst += "%s. %s\n" % (str(i), n)
		user = int(input("Who are you?\n%s>" % (userslst)))-1
		for root, dirs, files in os.walk(from_folder):
			for i in files:
				if ".mp3" in i:
					#get the name of the artist
					artist = i.split(" - ")[0]
					#if i user likes that song
					key = from_folder.replace("\\","/")+"/"+artist+"/"+i
					try:
						a = s.mymusic[key][user]
						go = True
					except:
						go = False

					if go:
						if s.mymusic[key][user]:
							transfer = False
							#check if the file exists or not
							if os.path.isfile(to_folder+"/"+artist+"/"+i):
								print("%s already exists in %s" % (i, to_folder))
							else:
								#if the folder dosent exist, create it
								if not os.path.exists(to_folder+"/"+artist):
									os.mkdir(to_folder+"/"+artist)
									transfer = True
								else:
									transfer = True
							#if file tranffare was approved
							if transfer:
								shutil.copyfile(from_folder+"/"+artist+"/"+i, to_folder+"/"+artist+"/"+i)
								print("%s was successfully copied from %s to %s" % (i,from_folder,to_folder+"/"+artist))
						else:
							print("%s was not transferred because %s don’t like this song" % (i,s.mymusic["filename"][user]))
					else:
						print("%s was not transferred because %s don’t like this song" % (i,s.mymusic["filename"][user]))
		s.readfromfolder()

	def load_obj(s):
		s.database = database(s)


main()