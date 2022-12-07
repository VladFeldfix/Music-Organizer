import os
from os import walk
import shutil
class main:
	def __init__(self):
		s = self
		s.SETTINGS = {}
		s.open_settings()
		s.setup()
		s.create_blacklist()
		s.BLACKLIST = s.getblacklist()
		s.transfer()

	def setup(s):
		print("Choose a username:")
		i = 0
		for u in s.SETTINGS["USERS"]:
			i += 1
			print("%s. %s" % (i,u))
		s.SELECTEDUSER = int(input(">"))-1

	def open_settings(s):
		#this method creates the SETTINGS dictionary
		f = open("settings.txt")
		for l in f.readlines(): 
			try:
				l = l.replace("\n","")
				if "#" in l:
					key = l.replace("#","")
					s.SETTINGS[key] = []
				else:
					s.SETTINGS[key].append(l)
			except:
				pass
		f.close()
		#print(s.SETTINGS)

	def getblacklist(s):
		f = open("%sblacklist.txt" % (s.SETTINGS["USERS"][s.SELECTEDUSER]), "r", encoding='utf-8')
		result = []
		for l in f.readlines():
			result.append(l.replace("\n",""))
		return result
		f.close()

	def create_blacklist(s):
		on_device = []
		last_trans = []
		for root, dirs, files in os.walk(s.SETTINGS["DEV_LOC"][0]):
			for file in files:
				on_device.append(file)
		f = open("%slog.txt" % (s.SETTINGS["USERS"][s.SELECTEDUSER]), "r", encoding='utf-8')
		for line in f.readlines():
			last_trans.append(line.replace("\n",""))
		f.close()
		delta = [i for i in on_device + last_trans if i not in on_device or i not in last_trans]
		f = open("%sblacklist.txt" % (s.SETTINGS["USERS"][s.SELECTEDUSER]), "r", encoding='utf-8')
		lines = f.readlines()
		f = open("%sblacklist.txt" % (s.SETTINGS["USERS"][s.SELECTEDUSER]), "w", encoding='utf-8')
		for d in delta:
			f.write("%s\n" % (d))
		f.close()

	def transfer(s):
		com_loc = s.SETTINGS["COM_LOC"][0]
		dev_loc = s.SETTINGS["DEV_LOC"][0]
		print("Computer folder:\n%s\nDevice folder:\n%s\n" % (com_loc,dev_loc))
		approve = input("Y/N?\n>")
		if approve == "y" or approve == "Y":
			f = open("%slog.txt" % (s.SETTINGS["USERS"][s.SELECTEDUSER]), "r", encoding='utf-8')
			lines = f.readlines()
			f = open("%slog.txt" % (s.SETTINGS["USERS"][s.SELECTEDUSER]), "w", encoding='utf-8')
			for line in lines:
				f.write(line)
			for root, dirs, files in os.walk(com_loc):
				for i in files:
					if ".mp3" in i:
						origin = "%s/%s" % (root,i)
						dist_dir = "%s%s" % (dev_loc,root.replace(com_loc,""))
						moveto = "%s/%s" % (dist_dir,i)
						if not os.path.isdir(dist_dir):
							os.mkdir(dist_dir)
						if not os.path.exists(moveto) and not i in s.BLACKLIST:
							print(i)
							f.write("%s\n" % (i))
							shutil.copyfile(origin, moveto)
			f.close()

main()