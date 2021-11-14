import vlc
import os
from colorama import Fore, init
import time

init()


g = Fore.LIGHTGREEN_EX
b = Fore.LIGHTBLUE_EX
r = Fore.LIGHTRED_EX
R = Fore.RESET


if not os.path.isfile("directory.txt"):
    path = input("Enter Path: ")
    file = open("directory.txt", "w")
    file.write(path)
    file.close()


def zero(number):
    if number < 10:
        out = "00" + str(number)
    elif number < 100:
        out = "0" + str(number)
    else:
        out = str(number)

    return out


def zeroten(number):
    if number < 10:
        out = "0" + str(number)
    else:
        out = str(number)

    return out


def toTime(milli):
    millis = int(milli)
    seconds=(millis/1000)%60
    seconds = int(seconds)
    minutes=(millis/(1000*60))%60
    minutes = int(minutes)
    hours=(millis/(1000*60*60))%24

    string = zeroten(int(hours)) + ":" +  zeroten(minutes) + ":" + zeroten(seconds)

    return string


class Player():
    def __init__(self):
        os.system("clear")

        print("Player")
        print("======")
        print("")
        
        self.showFiles()


    def playfile(self):
        try:
            self.player
        except AttributeError:
            varExists = False
        else:
            varExists = True
        
        if varExists:
            if self.player.is_playing():
                self.player.stop()

        self.playing = True
        self.player = vlc.MediaPlayer(self.path + "/" + self.song)
        self.player.play()

        time.sleep(1)

        self.progress()


    def stop(self):
        try:
            self.playing
        except AttributeError:
            pass
        else:
            if self.playing:
                self.player.stop()
                self.song = "None"
        
        self.__init__()


    def help(self):
        os.system("clear")
        print("Help")
        print("====")
        print("")
        print(g+"###"+R+"\tPlays song or open Directory")
        print(g+"player"+R+"\tShows the Player")
        print(g+"help"+R+"\tShows this help")
        print(g+"exit"+R+"\tCloses this program")
        print(g+"back"+R+"\tJumps a directory up")
        print("")
        print("[ Press enter to go back ]")
        
        input()
        self.__init__()


    def showFiles(self):
        try:
            self.song
        except AttributeError:
            print("Song: "+r+"None"+R)
        else:
            if self.song == "None":
                print("Song: " + r + self.song + R) 
            else:
                print("Song: " + g + self.song + R) 

        try:
            self.path
        except AttributeError:
            file = open("directory.txt", "r")
            self.path = file.read()

        print("Path: " + self.path)

        print("")
        
        count = 0
        items = []

        for songs in os.scandir(self.path):
            if songs.name.endswith(".mp3"):
                print(zero(count) + " | " + g + songs.name + R)
            elif songs.is_dir():
                print(zero(count) + " | " + b + songs.name + R)

            count += 1

            items.append(songs.name)

        print("")
        choose = input("[+] | ")

        if choose == "exit":
            quit()
        elif choose == "player":
            try:
                self.playing
            except AttributeError:
                self.__init__()
            else:
                if self.playing:
                    self.progress()
                else:
                    self.__init__()
        elif choose == "help":
            self.help()
        elif choose == "stop":
            self.stop()
        elif choose == "back":
            splitted = self.path.split("/")
            without = "/".join(splitted[:-1])
            self.path = "/" + without.strip("/")
            self.__init__()
        else:
            if items[int(choose)].endswith(".mp3"):
                self.song = items[int(choose)]
                self.playfile()
            else:
                self.path = self.path + "/" + items[int(choose)]
                self.__init__()


    def progress(self):
        try:
            os.system("clear")
            print("Player")
            print("======")
            print("")
            print("Song:    " + g + self.song + R)
            print("Current: " + toTime(self.player.get_time()))
            print("Length:  " + toTime(self.player.get_length()))
            print("")

            percent = int(self.player.get_time() / self.player.get_length() * 50)
            rest = 50 - percent

            done = "="*percent
            undone = " "*rest

            print("[" + done + undone + "] " + "{:3d}".format(percent * 2) + "%")

            print("")
            print("[ Press ctrl+c to go back ]")

            time.sleep(1)

            if percent >= 49:
                self.__init__()
                self.playing = False
            else:
                self.progress()

        except KeyboardInterrupt:
            self.__init__()


Player()