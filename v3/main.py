# select a user
# get device location
# get music folder location
# save locations on a settings.txt file
# make a list of what music is on my computer now
# tranfer only song that are NOT on lasttransaction.txt list
# update last transaction list

import os
from os import walk
import shutil

class main:
	def __init__(self):
		s = self
		s.open_settings()
		if s.COMPUTER_LOCATION == "":
			print("ERROR! computer music location is missing in settings.txt")
			s.exit()
		if s.DEVICE_LOCATION == "":
			print("ERROR! device location is missing in settings.txt")
			s.exit()
		if s.USERS == []:
			print("ERROR! there are no users in settings.txt")
			s.exit()
		s.select_user()
		s.get_comp_list()
		s.transfer()

	def open_settings(s):
		f = open("settings.txt")
		op = ""
		s.USERS = []
		s.COMPUTER_LOCATION = ""
		s.DEVICE_LOCATION = ""
		for l in f.readlines():
			l = l.replace("\n","")
			#switch operation
			if l == "#users:":
				op = "collect_users"
			elif l == "#comp_loc:":
				op = "comp_loc"
			elif l == "#dev_loc:":
				op = "dev_loc"
			#perform operation
			if op == "collect_users":
				s.USERS.append(l)
			elif op == "comp_loc":
				s.COMPUTER_LOCATION = l
			elif op == "dev_loc":
				s.DEVICE_LOCATION = l
		del s.USERS[0]
		f.close()

	def select_user(s):
		print("Select a user please:")
		i = 0
		for u in s.USERS:
			i += 1
			print("%s. %s" % (i, u))
		print("%s. Exit" % (i+1))
		try:
			selection = int(input(">"))
			if selection < i+1:
				s.SELECTED_USER = s.USERS[selection-1]
			elif selection == i+1:
				s.exit()
			else:
				print("ERROR! invalid input")
				s.select_user()
		except:
			print("ERROR! invalid input")
			s.select_user()
	
	def get_comp_list(s):
		s.COMPUTER_LIST = []
		for root, dirs, files in os.walk(s.COMPUTER_LOCATION):
			for i in files:
				if ".mp3" in i:
					s.COMPUTER_LIST.append(i)

	def transfer(s):
		transactionlistlocation = "%s/%s/lasttransaction.txt" % (os.getcwd(),s.SELECTED_USER)
		if not os.path.exists(transactionlistlocation):
			print("ERROR! %s has no folder" % (s.SELECTED_USER))
			s.exit()
		else:
			f = open(transactionlistlocation)
			lasttransaction_list = []
			for lt in f.readlines():
				lasttransaction_list.append(lt)

			for song in s.COMPUTER_LIST:
				if song not in lasttransaction_list:
					shutil.move(song, s.DEVICE_LOCATION)
			f.close()

	def exit(s):
		input("Press any key to exit:\n>")

main()