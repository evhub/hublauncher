#!/usr/bin/python

# NOTE:
# This is the code. If you are seeing this when you open the program normally, please follow the steps here:
# https://sites.google.com/site/evanspythonhub/having-problems

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# INFO AREA:
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Program by: Evan
# LAUNCHER made in 2012
# This program is a launcher for the HubPack.

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CONFIG AREA:
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# WARNING: DO NOT MODIFY THESE UNLESS YOU KNOW WHAT YOU ARE DOING!

# Current Program Version: (Must Be A Number)
myversion = "5.9"

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# DATA AREA: (IMPORTANT: DO NOT MODIFY THIS SECTION!)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

from rabbit.all import *

def defaults(datadict, myversion):
    newdict = datadict
    newdict["done"] = 0
    newdict["version"] = 0
    newdict["newversion"] = 1
    newdict["launcherversion"] = str(myversion)
    newdict["manager"] = 0
    return newdict

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CODE AREA: (IMPORTANT: DO NOT MODIFY THIS SECTION!)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def startconsole(handler=None, message=None, name="PythonPlus", height=None):
    """Initializes An Instance Of The PythonPlus Console."""
    root = Tkinter.Tk()
    root.title(str(name))
    if height != None:
        app = console(root, message, height)
    else:
        app = console(root, message)
    root.bind("<Escape>", lambda event: root.destroy())
    root.bind("<MouseWheel>", app.scroll)
    if handler != None:
        box = entry(app)
        box.main.bind("<Control-z>", lambda event: box.main.delete(0, "end"))
        root.bind("<Return>", handler)
        return root, app, box
    else:
        return root, app

class main(base):
    def __init__(self, myversion="0.0"):
        self.myversion = str(myversion)
        self.root, self.app, self.box = startconsole(self.handler, "Welcome To The HubLauncher (Version: " + self.myversion + ").\nRetrieving Data...", "HubLauncher")
        self.datadict = defaults({}, self.myversion)
        self.myversionx = 0.0
        myversiony = myversion.split(".")
        for x in xrange(0, len(myversiony)):
            self.myversionx += int(myversiony[x])*10**((x+1)*-2)
        if getos("win"):
            self.windows = True
        else:
            self.windows = False
        self.returned = 0
        self.dolocalwrite = 0
        if self.windows:
            self.programdirectory = os.environ["APPDATA"]
            self.hubdirectory = self.programdirectory + "\\HubLauncher\\"
            self.user = os.environ["USERPROFILE"]
        else:
            self.programdirectory = os.environ["HOME"]
            self.hubdirectory = self.programdirectory + '/Library/Application Support/HubLauncher/'
        self.register(self.retrieve, 200)

    def retrieve(self):
        makedir(self.hubdirectory)

        try:
            download("http://dl.dropbox.com/u/11683904/Data.dat", self.hubdirectory + "Data.dat")
        except IOError:
            self.app.display("Unable To Retrieve Data From Server. Launcher Will Use Last Data Download.")

        try:
            data = openfile(self.hubdirectory + "Data.dat")
        except IOError:
            self.app.display("Unable To Retrieve Last Data Download. Launcher Will Proceed With Default Values.")
        else:
            try:
                for x in readfile(data).splitlines():
                    datatemp = x.split("=")
                    self.datadict[datatemp[0]] = datatemp[1]
            except IndexError:
                self.app.display("Server Data Error Detected. Launcher Will Use Default Values.")
            finally:
                data.close()

        try:
            self.local = openfile(self.hubdirectory + "Local.dat")
        except IOError:
            self.local = openfile(self.hubdirectory + "Local.dat", "wb")
        else:
            try:
                for x in readfile(self.local).splitlines():
                    datatemp = x.split("=")
                    self.datadict[datatemp[0]] = datatemp[1]
            except IndexError:
                self.app.display("Local Data Error Detected. Launcher Will Use Default Values.")

        try:
            self.datadict["done"] = str(self.datadict["done"])
            if self.windows:
                self.datadict["manager"] = str(self.datadict["manager"])
            else:
                self.datadict["manager"] = "0"
            self.datadict["launcherversion"] = str(self.datadict["launcherversion"])
            self.datadict["version"] = str(self.datadict["version"])
            self.datadict["newversion"] = str(self.datadict["newversion"])
        except ValueError:
            self.app.display("Data Value Errors Detected. Launcher Will Proceed With Default Values.")
            self.datadict = defaults(self.datadict, self.myversion)

        self.launcherversionx = 0.0
        launcherversiony = self.datadict["launcherversion"].split(".")
        for x in xrange(0, len(launcherversiony)):
            self.launcherversionx += int(launcherversiony[x])*10**((x+1)*-2)

        self.mypackx = 0.0
        mypacky = self.datadict["version"].split(".")
        for x in xrange(0, len(mypacky)):
            self.mypackx += int(mypacky[x])*10**((x+1)*-2)

        self.packx = 0.0
        packy = self.datadict["newversion"].split(".")
        for x in xrange(0, len(packy)):
            self.packx += int(packy[x])*10**((x+1)*-2)

        self.app.display("Data Retrieval Complete.")

        if isyes(self.datadict["done"]) == False:
            self.app.display("First Time Setup Will Now Be Performed.")
            self.run()

        else:
            if self.myversionx < self.launcherversionx:
                self.app.display("A New Version Of The HubLauncher Is Available For Download From The Website (Version: " + self.datadict["launcherversion"] + ").")
            if self.mypackx < self.packx:
                self.app.display("A New HubPack Version Is Available. Would You Like To Update? [Y/n] (Current Version: " + self.datadict["version"] + "; New Version: " + self.datadict["newversion"] + ")")
                if formatisno(self.get()) == False:
                    self.run()
                else:
                    self.dolaunch()
            else:
                self.app.display("No New HubPack Version Detected. Force Update Anyway? [y/N] (Current Version: " + self.datadict["version"] + ")")
                if formatisyes(self.get()):
                    self.run()
                else:
                    self.dolaunch()

    def run(self):
        self.app.display("Would You Like To Use The HubPack+? [Y/n]")
        self.whatpack = superformat(self.get())
        self.app.display("Downloading...")
        self.register(self.download, 200)

    def download(self):
        try:
            if isno(self.whatpack) == False:
                self.raw = download("http://dl.dropbox.com/u/11683904/HubPack%2B.zip")
            else:
                self.raw = download("http://dl.dropbox.com/u/11683904/HubPack.zip")
            self.app.display("Download Complete.")

        except IOError:
            self.app.display("An Internet Connection Is Required. Please Run The Installer Again When You Are Connected To The Internet.")
            self.dolaunch()

        else:
            self.extracommand = 0
            self.temproot, trash = os.path.split(self.raw[0])
            if self.windows:
                self.cmdtorun = 'xcopy /E /Y /Q "' + self.temproot + '\\forinstall\\*.*" "' + self.programdirectory + '\\.minecraft\\"'
                self.domm()
            else:
                self.cmdtorun = 'cp -Rf "' + self.temproot + '/forinstall/." ~/library/"application support"/minecraft/'
                self.nextinstall()

    def domm(self):
        self.app.display("Also Set Up Minecraft Manager? [Y/n]")
        if formatisno(self.get()) == False:
            if isyes(self.datadict["manager"]):
                self.app.display("Also Set Current Minecraft To Minecraft Manager Vanilla? [y/N]")
                if formatisyes(self.get()):
                    self.dovanilla = 1
                else:
                    self.dovanilla = 0
                self.app.display("Also Reset Minecraft Manager Bin List? [y/N]")
                if formatisyes(self.get()):
                    self.dobinlist = 1
                else:
                    self.dobinlist = 0
                self.mmready()
            else:
                self.dovanilla = 1
                self.dobinlist = 1
                self.mmready()
        else:
            self.nextinstall()

    def mmready(self):
        if self.dobinlist == 1:
            self.modhubdirectory = self.hubdirectory.replace(" ", "*")
        if self.dovanilla == 1:
            self.directory1 = self.hubdirectory + "BinStore\\Vanilla\\bin\\"
            self.firstcmd = 'xcopy /E /Y /Q "' + self.programdirectory + '\\.minecraft\\bin\\*.*" "' + self.directory1 + '"'
        self.directory2 = self.hubdirectory + "BinStore\\HubPack\\bin\\"
        self.secondcmd = 'xcopy /E /Y /Q "' + self.programdirectory + '\\.minecraft\\bin\\*.*" "' + self.directory2 + '"'
        self.extracommand = 1
        self.app.display("Downloading...")
        self.register(self.mmdownload, 200)

    def mmdownload(self):
        try:
            download("http://dl.dropbox.com/u/11683904/MinecraftManager.exe", self.user + "\\desktop\\MinecraftManager.exe")
            self.app.display("Download Complete.")
        except IOError:
            self.app.display("An Internet Connection Is Required. Minecraft Manager Installation Will Be Skipped.")
            self.extracommand = 0
        self.nextinstall()

    def nextinstall(self):
        self.app.display("Also Delete Current Mods? [Y/n]")
        if formatisno(self.get()):
            self.delmods = 0
        else:
            self.delmods = 1
        self.app.display("Installing...")
        self.register(self.install, 200)

    def install(self):
        try:
            hubpack = openzip(self.raw[0])
            unzip(hubpack, self.temproot)

        finally:
            hubpack.close()
            os.remove(self.raw[0])

        try:
            if self.delmods == 1:
                if self.windows:
                    runcmd('rmdir /S /Q "' + self.programdirectory + '\\.minecraft\\mods"')
                    runcmd('rmdir /S /Q "' + self.programdirectory + '\\.minecraft\\coremods"')
                else:
                    runcmd('rm -rf ~/library/"application support"/minecraft/mods')
                    runcmd('rm -rf ~/library/"application support"/minecraft/coremods')
            if self.extracommand == 1:
                if self.dovanilla == 1:
                    makedir(self.directory1)
                    runcmd(self.firstcmd)
                runcmd(self.cmdtorun)
                makedir(self.directory2)
                runcmd(self.secondcmd)
                if self.dobinlist == 1:
                    try:
                        manager = openfile(self.programdirectory + "\\.minecraft\\BinList.dat", "wb")
                        manager.write("HubPack:" + self.modhubdirectory + "BinStore\\HubPack\\bin?Vanilla:" + self.modhubdirectory + "BinStore\\Vanilla\\bin?")
                    finally:
                        manager.close()

            else:
                runcmd(self.cmdtorun)

        finally:
            if self.windows:
                for ziproot, zipdirs, zipfiles in os.walk(self.temproot + "\\forinstall\\", topdown=False):
                    for trashname in zipfiles:
                        os.remove(os.path.join(ziproot, trashname))
                    for trashname in zipdirs:
                        os.rmdir(os.path.join(ziproot, trashname))
                os.rmdir(self.temproot + "\\forinstall\\")

            else:
                for ziproot, zipdirs, zipfiles in os.walk(self.temproot + "/forinstall/", topdown=False):
                    for trashname in zipfiles:
                        os.remove(os.path.join(ziproot, trashname))
                    for trashname in zipdirs:
                        os.rmdir(os.path.join(ziproot, trashname))
                os.rmdir(self.temproot + "/forinstall/")

        self.app.display("Installation Complete.")

        self.app.display("Saving Data...")

        writer = "done=1\nversion=" + str(self.datadict["newversion"])
        if self.extracommand == 1:
            writer += "\nmanager=1"
        elif isyes(self.datadict["manager"]):
            writer += "\nmanager=1"
        try:
            writefile(self.local, writer)
        except IOError:
            self.app.display("Unable To Save Data.")
        finally:
            self.local.close()

        self.dolaunch()

    def dolaunch(self):
        self.app.display("Launch Minecraft? [Y/n]")
        if formatisno(self.get()) == False:
            self.app.display("Launching Minecraft...")
            self.register(self.launch, 200)
        else:
            self.root.destroy()

    def launch(self):
        if self.windows:
            if isyes(self.datadict["manager"]):
                os.startfile(self.user + "\\desktop\\MinecraftManager.exe")
            else:
                os.startfile(self.user + "\\desktop\\Minecraft.exe")
        else:
            runcmd("open /Applications/Minecraft.app")
        self.root.destroy()

if __name__ == "__main__":
    main(myversion).start()
