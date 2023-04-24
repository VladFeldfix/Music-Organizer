from FoxyFunctions import ff
import os

class main:
    def __init__(self):
        # activate GUI
        main_menu = (("RUN", self.start),)
        self.ff = ff("MUSIC ORGANIZER", "7.0", main_menu)

        # run gui
        self.ff.run()
    
    def start(self):
        pass
        # get gloval variables
        NEWFILES = self.ff.settings_get("New media location")
        MUSICALBUM = self.ff.settings_get("Music album location")

        if os.path.isdir(NEWFILES):
            
            # calculate workload
            steps = 0
            for root, folders, files in os.walk(NEWFILES):
                for file in files:
                    if ".mp3" in file:
                        steps += 1

            # go over each new file
            steps_done = 0
            for root, dirs, files in os.walk(NEWFILES):
                for file in files:
                    if ".mp3" in file:
                        steps_done += 1
                        percent = steps_done / steps
                        self.ff.progress_bar_value_set(percent*100)

                        fl = file.split(" - ")
                        artist = fl[0]
                        song = fl[1]

                        # create a new file if it dosent exit
                        if not os.path.isdir(MUSICALBUM+"/"+artist):
                            os.makedirs(MUSICALBUM+"/"+artist)
                        
                        file_name = NEWFILES+"/"+file
                        new_name = MUSICALBUM+"/"+artist+"/"+file

                        if not os.path.exists(new_name):
                            self.ff.write(new_name)
                            os.rename(file_name, new_name)
                        else:
                            self.ff.write("File already exists "+new_name)
            
            # go back to main menu
            self.ff.write("DONE!")
        else:
            self.ff.error("There is no such location: "+NEWFILES)
main()