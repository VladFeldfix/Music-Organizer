import os
from os import walk
import shutil
class main:
	def __init__(self):
		s = self
		s.SETTINGS = {}
		s.open_settings()
		approve = input("From folder:\n%s\nTo folder:\n%s\nY/N?\n>" % (s.SETTINGS["FROM"][0],s.SETTINGS["TO"][0]))
		if approve == "y" or approve == "Y":
			s.transfer_files()
	
	def open_settings(s):
		f = open("settings.txt")
		for l in f.readlines():
			l = l.replace("\n","")
			if "#" in l:
				key = l.replace("#","")
				s.SETTINGS[key] = []
			else:
				s.SETTINGS[key].append(l)
		f.close()

	def transfer_files(s):
		from_fold = s.SETTINGS["FROM"][0]
		to_fold = s.SETTINGS["TO"][0]
		for root, dirs, files in os.walk(from_fold):
			for file in files:
				if ".mp3" in file:
					filefolder = file.split(" - ")
					orig_fold = "%s/%s" % (from_fold,file)
					#print(orig_fold)
					#D:\Users\Vlad\Downloads/LITTLE BIG - HYPNODANCER (Official Music Video).mp3
					dist_fold = "%s/%s" % (to_fold,filefolder[0])
					#print(dist_fold)
					#D:\Users\Vlad\Desktop\testfolder2/LITTLE BIG
					new_file = "%s/%s" % (dist_fold,file)
					#print(new_file)
					#D:\Users\Vlad\Desktop\testfolder2/LITTLE BIG/LITTLE BIG - HYPNODANCER (Official Music Video).mp3
					if not os.path.isdir(dist_fold):
						os.mkdir(dist_fold)
					if not os.path.exists(new_file):
						print(file)
						shutil.move(orig_fold, new_file)


main()