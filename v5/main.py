#MUSIC ORGANIZER
import os
import shutil
import FoxyFunctions as ff
FF = ff.FoxyFunctions()

class main:
	def __init__(s):
		#version control
		print("Music Organizer Version 5.2")

		#set global variables
		s.SELECTEDUSER = None
		s.NEWMUSICLOCATION = None
		s.MYMUSICLOCATION = None
		s.DEVICELOCATION = None
		
		#call choose_user
		s.choose_user()

	def choose_user(s):
		#get user names from file and display users on screen
		s.USERS = []
		file = open("users.txt","a", encoding='utf-8')
		file = open("users.txt","r", encoding='utf-8')
		menu = []
		for line in file.readlines():
			username = line.replace("\n","")
			s.USERS.append(username)
			menu.append((username,s.main_menu))
		file.close()
		menu.append(("*Add a new user",s.add_user))
		menu.append(("*Delete a user",s.delete_user))
		menu.append(("Exit",FF.exit))
		FF.display_menu("CHOOSE USER:",menu)

	def add_user(s,n):
		print("\nADD USER:")
		#get previous content
		file = open("users.txt","r", encoding='utf-8')
		previous_content = file.read()
		file.close()
		#get new username
		approve = False
		while not approve:
			username = input(">")
			try:
				os.mkdir(username)
				approve = True
			except:
				print("Invalid Input! Try again")
		#add new user to users.txt
		file = open("users.txt","w", encoding='utf-8')
		file.write(previous_content)
		file.write(username+"\n")
		file.close()
		print("New user added successfully!")
		s.choose_user()

	def delete_user(s,n):
		print("\nDELETE USER:")
		#select user to delete
		approve = False
		warning = "N"
		while not approve:
			try:
				delete_user = int(input("Wich user would you like to delete?\n>"))-1
				if delete_user >= 0:
					approve = True
				else:
					raise TypeError()
			except:
				print("Invalid Input! Try again")
		#delete selected user
		warning = input("WARNING! You are about to delete: %s\nWhen deleting a user all data will be lost!\nWould you like to continue? Y/N >" % (s.USERS[delete_user]))
		if warning.upper() == "Y":
			try:
				shutil.rmtree(s.USERS[delete_user])
				file = open("users.txt","w", encoding='utf-8')
				deleted_username = s.USERS.pop(delete_user)
				for user in s.USERS:
					file.write("%s\n" % (user))
				file.close()
				print("Username: %s was successfully deleted" % (deleted_username))
			except Exception as e:
				print("Error: %s" % (e))
		else:
			print("No users were deleted")
		s.choose_user()

	def main_menu(s,n):
		s.SELECTEDUSER = n
		username = s.USERS[s.SELECTEDUSER]
		file = open("%s/settings.txt" % (username), "a", encoding='utf-8')
		file = open("%s/settings.txt" % (username), "r", encoding='utf-8')
		s.NEWMUSICLOCATION = file.readline().replace("\n","")
		s.MYMUSICLOCATION = file.readline().replace("\n","")
		s.DEVICELOCATION = file.readline().replace("\n","")
		file.close()
		FF.display_settings([
			("SELECTED USER", s.USERS[s.SELECTEDUSER]),
			("NEW MUSIC LOCATION", s.NEWMUSICLOCATION),
			("MY MUSIC LOCATION", s.MYMUSICLOCATION),
			("DEVICE LOCATION", s.DEVICELOCATION),
		])
		FF.display_menu("MAIN MENU:",[
			("Get new music",s.get_new_music),
			("Transfare to device",s.transfare_to_device),
			("Settings",s.settings),
			("See my activity log",s.seefile),
			("See my blacklist",s.seefile),
			("Exit",FF.exit)])
	
	def get_new_music(s,n):
		print("\nGET NEW MUSIC:")
		input("Make sure all new music is named in the follwing format: FolderName - SongName\nPress Enter to continue >")
		for root, dirs, files in os.walk(s.NEWMUSICLOCATION):
			for file in files:
				try:
					foldername = file.split(" - ")[0]
					orig_fold = "%s/%s" % (s.NEWMUSICLOCATION,file)
					dist_fold = "%s/%s" % (s.MYMUSICLOCATION,foldername)
					new_file = "%s/%s" % (dist_fold,file)
					if not os.path.isdir(dist_fold):
						print("New folder created:",dist_fold)
						os.mkdir(dist_fold)
					if not os.path.exists(new_file):
						print("From:", orig_fold)
						print("To:", new_file)
						shutil.move(orig_fold, new_file)
				except:
					print("Failed to transfer: %s" % (file))
		print("DONE!")
		s.main_menu(s.SELECTEDUSER)

	def transfare_to_device(s,n):
		print("\nTRANSFARE TO DEVICE:")
		#get previous activaty log
		log = s.file_to_list("%s/log.txt" % (s.USERS[s.SELECTEDUSER]))
		add_to_log = []
		#transfare only files that were not transfared before
		for root, dirs, files in os.walk(s.MYMUSICLOCATION):
			for file in files:
				if not file in log and ".mp3" in file:
					try:
						foldername = root.split("\\")[-1]
						orig_fold = root+"/"+file
						dist_fold = "%s/%s" % (s.DEVICELOCATION,foldername)
						new_file = "%s/%s" % (dist_fold,file)
						if not os.path.isdir(dist_fold):
							print("New folder created:",dist_fold)
							os.mkdir(dist_fold)
						if not os.path.exists(new_file):
							print("From:", orig_fold)
							print("To:", new_file)
							shutil.copy(orig_fold, new_file)
						add_to_log.append(file)
					except:
						print("Failed to transfer: %s" % (file))
		
		#add new songs to log
		file = open("%s/log.txt" % (s.USERS[s.SELECTEDUSER]),"r", encoding='utf-8')
		previous_content = file.read()
		file.close()
		file = open("%s/log.txt" % (s.USERS[s.SELECTEDUSER]),"w", encoding='utf-8')
		file.write(previous_content)
		for song in add_to_log:
			file.write(song+"\n")
		file.close()
		
		#create user freindly black list
		on_pc = s.folder_to_list(s.MYMUSICLOCATION)
		on_device = s.folder_to_list(s.DEVICELOCATION)
		blacklist = list(set(on_pc) - set(on_device))
		blacklistfilename = "%s/blacklist.txt" % (s.USERS[s.SELECTEDUSER])
		file = open(blacklistfilename, "a", encoding='utf-8')
		file = open(blacklistfilename, "w", encoding='utf-8')
		blacklist.sort()
		for song in blacklist:
			if ".mp3" in song:
				file.write(song+"\n")
		file.close()

		print("DONE!")
		s.main_menu(s.SELECTEDUSER)

	def folder_to_list(s,folder):
		result = []
		for root, dirs, files in os.walk(folder):
			for file in files:
				result.append(file)
		return result

	def file_to_list(s,filename):
		result = []
		file = open(filename, "a", encoding='utf-8')
		file = open(filename, "r", encoding='utf-8')
		for line in file.readlines():
			result.append(line.replace("\n",""))
		file.close()
		return result

	def settings(s,n):
		print("\nSETTINGS:")
		s.NEWMUSICLOCATION = input("Enter New music location: >") or s.NEWMUSICLOCATION
		s.MYMUSICLOCATION = input("Enter My music folder location: >") or s.MYMUSICLOCATION
		s.DEVICELOCATION = input("Enter Device location: >") or s.DEVICELOCATION
		file = open("%s/settings.txt" % (s.USERS[s.SELECTEDUSER]),"w", encoding='utf-8')
		file.write(s.NEWMUSICLOCATION+"\n")
		file.write(s.MYMUSICLOCATION+"\n")
		file.write(s.DEVICELOCATION+"\n")
		file.close()
		s.main_menu(s.SELECTEDUSER)

	def seefile(s,n):
		if n == 3:
			filename = "%s\\log.txt" % (s.USERS[s.SELECTEDUSER])
		else:
			filename = "%s\\blacklist.txt" % (s.USERS[s.SELECTEDUSER])
		log = open(filename, "a", encoding='utf-8')
		log.close()
		os.system(filename)
		s.main_menu(s.SELECTEDUSER)
main()