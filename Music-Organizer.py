# Download SmartConsole.py from: https://github.com/VladFeldfix/Smart-Console/blob/main/SmartConsole.py
from SmartConsole import *
import shutil

class main:
    # constructor
    def __init__(self):
        # load smart console
        self.sc = SmartConsole("Music Organizer", "1.0")

        # set-up main memu
        self.sc.add_main_menu_item("RUN", self.run)

        # get settings
        self.get_settings()

        # test all paths
        self.sc.test_path(self.new_music)
        self.sc.test_path(self.music_folder)

        self.sc.start()
    
    def get_settings(self):
        # get settings
        self.new_music = self.sc.get_setting("New music location")
        self.music_folder = self.sc.get_setting("My music location")

    def run(self):
        self.get_settings()
        # go over new music folder
        for root, dirs, files in os.walk(self.new_music):
            for file in files:
                if ".mp3" in file:
                    old_file_name = root+"/"+file
                    singer_song = file.split(" - ")
                    if len(singer_song) == 2:
                        singer = singer_song[0]
                        if not os.path.isdir(self.music_folder+"/"+singer):
                            os.makedirs(self.music_folder+"/"+singer)
                        new_filename = self.music_folder+"/"+singer+"/"+file
                        self.sc.print(new_filename)
                        shutil.move(old_file_name,new_filename)

        # restart
        self.sc.restart()

main()