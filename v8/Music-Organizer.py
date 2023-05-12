# GENERAL INFORMATION
## This small application will help you to keep your music folder organized

# HOW TO USE
## Download the application
## Set all the settings according to PART V
## Run Music-Organizer.exe file

from PersonalAssistant import *
from PersonalAssistant import FIELD
import os
import shutil

class main:
    def __init__(self):
        # set up Personal Assistant
        self.pa = PersonalAssistant(__file__, "Music-Organizer", "8.0")

        # MAIN MENU
        self.pa.main_menu["RUN"] = self.run
        self.pa.display_menu()

        # run GUI
        self.pa.run()

    def run(self):
        ## RUN
        #- Start the app

        # get settings
        new_music_folder = self.pa.get_setting("New Music Location")
        music_folder = self.pa.get_setting("Music Folder")

        # calc workload
        workload = 0
        done = 0
        for root, dirs, files in os.walk(new_music_folder):
            for file in files:
                if ".mp3" in file:
                    workload += 1

        # go over each file
        for root, dirs, files in os.walk(new_music_folder):
            for file in files:
                if ".mp3" in file:
                    old_file_name = root+"/"+file
                    singer_song = file.split(" - ")
                    if len(singer_song) == 2:
                        singer = singer_song[0]
                        song_name = singer_song[1]
                        if not os.path.isdir(music_folder+"/"+singer):
                            os.makedirs(music_folder+"/"+singer)
                        new_filename = music_folder+"/"+singer+"/"+file
                        done += 1
                        self.pa.print(new_filename)
                        shutil.copy(old_file_name,new_filename)

        self.pa.restart()

main()


# SETTINGS
# Database location --> The location of the user database. For example: database.db

# RELATED FILES
## users.csv - This is the file the app generates when clicking on EXPORT this file contains the following columns:
#- User Id
#- Name
#- Phone
#- Sex
#- Birth date
#- Photo