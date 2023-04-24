import sys
import os

sys.path.insert(1, "D:/Users/Vlad/Projects/Applications/FOXY-FUNCTIONS")
from FoxyFunctions import ff

class main:
    def __init__(self):
        # create a foxy object
        self.ff = ff("MUSIC ORGANIZER", "6.0")

        # load settings
        self.settings = self.ff.get_settings()

        # display main menu
        self.display_menu()
    
    def display_menu(self):
        # display header
        self.ff.display_header()

        # display main menu
        main_menu = (("START", self.start), ("SETTINGS", self.set_settings), ("HELP", self.help), ("EXIT", self.exit))
        self.ff.display_menu("MAIN MENU", main_menu)
    
    def start(self):
        # get gloval variables
        NEWFILES = self.settings["NEW FILES LOCATION"]
        MUSICALBUM = self.settings["MUSIC ALBUM"]

        # go over each new file
        for root, dirs, files in os.walk(NEWFILES):
            for file in files:
                if ".mp3" in file:
                    fl = file.split(" - ")
                    artist = fl[0]
                    song = fl[1]

                    # create a new file if it dosent exit
                    if not os.path.isdir(MUSICALBUM+"/"+artist):
                        os.makedirs(MUSICALBUM+"/"+artist)
                    
                    file_name = NEWFILES+"/"+file
                    new_name = MUSICALBUM+"/"+artist+"/"+file

                    if not os.path.exists(new_name):
                        self.ff.indexed_print(new_name)
                        os.rename(file_name, new_name)
                    else:
                        self.ff.indexed_print("FILE ALREADY EXISTS "+new_name)
        
        # go back to main menu
        input("DONE >")
        self.display_menu()

    def set_settings(self):
        # set new settings
        self.ff.set_settings(self.settings)

        # go back to main menu
        self.display_menu()
    
    def help(self):
        # display readme file
        self.ff.help()

        # go back to main menu
        self.display_menu()
    
    def exit(self):
        # exit the program
        self.ff.exit()

main()