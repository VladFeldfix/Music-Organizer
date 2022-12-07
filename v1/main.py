import os
import time
from os import walk
import shutil

#get folder names
from_folder = input("from: ")
to_folder = input("to: ")

#get all the to folders
all_folders = []
for root, dirs, files in os.walk(to_folder):
	for i in dirs:
		all_folders.append(i)

#get all files from_folder
for root, dirs, files in os.walk(from_folder):
	for i in files:
		if ".mp3" in i:
			artist = i.split(" - ")[0]
			moving = False
			for f in all_folders:
				if artist == f:
					try:
						shutil.move(from_folder+"/"+i, to_folder+"/"+f)
					except:
						print("%s already exist in %s" % (i,to_folder+"/"+f))
					print(i,"was transfared from",from_folder,"to",to_folder+"/"+f)
					time.sleep(0.1)
					moving = True
			if not moving:
				newFolder = to_folder+"/"+artist
				os.mkdir(newFolder)
				print("new folder",newFolder,"was created")
				shutil.move(from_folder+"/"+i, newFolder)
				print(i,"was transfared from",from_folder,"to",newFolder)
				time.sleep(0.1)

print("done")
input("Press Enter to exit")