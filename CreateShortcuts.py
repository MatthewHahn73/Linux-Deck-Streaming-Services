"""
CreateShortcuts.py

Current Bugs
    -Steam doesn't populate the non-steam games with the right artwork. 
        -Steamgriddb picks a different appid
            -Still doesn't load some of the artwork? Only the icon

TODO
    -Need to add in better documentation of current script progress and exception handling
    -Need to better optimize the GrabAndSetArtworkForGivenAppIDs function 
"""

import os, json, logging, random
import Assets.VDF as vdf
from urllib.request import Request, urlopen

GlobalLogger = logging.getLogger()
GlobalLogger.setLevel(logging.DEBUG)

User = os.getlogin()
SteamUserData = "/home/" + User + "/.steam/steam/userdata/"
SteamGameData = "/home/" + User + "/.steam/steam/steamapps/common"
PathToUserConfig = SteamUserData + os.listdir(SteamUserData)[0] + "/config/grid/"
PathToSteamShortcutsFile = SteamUserData + os.listdir(SteamUserData)[0] + "/config/shortcuts.vdf"

#Generates a random appid
def GenerateRandomAppID():
    return random.randint(0, 2147483647)

#Queries steamdb for the artwork for each given streaming service and creates the file in the <User ID>/config/grid directory of the steam user
def GrabAndSetArtworkForGivenAppIDs(ArtworkLinks, AppIDs):
    for StreamingAppType in ArtworkLinks: 
        for ArtworkType in ArtworkLinks[StreamingAppType]["Artwork"]:
            ArtworkTypeParsed = ArtworkType.replace(" - Horizontal", "").replace(" - Vertical", "")
            ArtworkURL = "https://cdn2.steamgriddb.com/" + ArtworkTypeParsed + "/" + ArtworkLinks[StreamingAppType]["Artwork"][ArtworkType]
            ArtworkFileName, ArtworkFileType = os.path.splitext(ArtworkURL)
            ArtworkSuffix = {
                "grid - Vertical": "p",
                "grid - Horizontal": "",
                "hero": "_hero", 
                "logo": "_logo",
                "icon": "_icon"
            }.get(ArtworkType, "")
            logging.info("Fetching '" + StreamingAppType + "' artwork at '" + ArtworkURL + "' ...")
            SteamGridDBRequest = Request(url=ArtworkURL, headers={
                            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                            'Accept-Encoding': 'none',
                            'Accept-Language': 'en-US,en;q=0.8',
                            'Connection': 'close'
                        })
            ReturnedValue = urlopen(SteamGridDBRequest).read()

            FullFileName = str(AppIDs[StreamingAppType]) + ArtworkSuffix + ArtworkFileType
            with open(PathToUserConfig + FullFileName, "wb") as FetchedFile:
                FetchedFile.write(ReturnedValue)
    
#Creates a shortcuts file in the steam directory if one doesn't exist. Creates shortcut entries in the vdf file for each streaming service
def GenerateVDFEntriesAndReturnAppIDs(StreamingServices):
    PathToScript = "bash " + '"/home/' + User + '/.steam/steam/steamapps/common/Streaming/LaunchApp.sh"'
    PathToDirectory = '"/home/' + User + '/.steam/steam/steamapps/common/Streaming/"'

    if not os.path.exists(PathToSteamShortcutsFile):
        logging.info("Creating shortcuts file at '" + PathToSteamShortcutsFile + "'")
        with open(PathToSteamShortcutsFile, "wb") as NewlyCreatedShortcutsFile:
            NewlyCreatedShortcutsFile.write(b'\x00' + b'shortcuts' + b'\x00\x08\x08')
        NewlyCreatedShortcutsFile.close()

    logging.info("Appending new items to '" + PathToSteamShortcutsFile + "' ...")
    ShortcutsDict = vdf.binary_load(open(PathToSteamShortcutsFile, "rb"))
    CurrentIteration = len(ShortcutsDict["shortcuts"])
    CurrentAppIDList = {}

    for Key in StreamingServices:
        GeneratedAppID = GenerateRandomAppID()
        ShortcutsDict["shortcuts"][str(CurrentIteration)] = {
                "appid" : GeneratedAppID, 
                "AppName" : str(Key), 
                "Exe" : PathToScript, 
                "StartDir" : PathToDirectory, 
                "icon" : "",
                "ShortcutPath" : "", 
                "LaunchOptions" : str('"' + str(StreamingServices[Key]["Link"]) + '"'), 
                "IsHidden" : 0, 
                "AllowDesktopConfig" : 1, 
                "AllowOverlay" : 1,
                "OpenVR" : 0,
                "Devkit" : 0, 
                "DevkitGameID" : "",
                "DevkitOverrideAppID" : 0,
                "LastPlayTime" : 0, 
                "FlatpakAppID" : "", 
                "tags" : {}
            }
        CurrentIteration += 1 
        CurrentAppIDList[Key] = GeneratedAppID
    ShortcutsDictParsed = vdf.binary_dump(ShortcutsDict, open(PathToSteamShortcutsFile, "wb"))
    return CurrentAppIDList
        
if __name__ == "__main__":
    logging.info("Installing firefox ...")
    os.system("flatpak install flathub org.mozilla.firefox -y")

    logging.info("Moving the files to '" + SteamGameData + "' ...")
    os.makedirs(SteamGameData + "/Streaming")
    os.system("cp -a $(pwd)/Streaming " + "'" + SteamGameData + "'")

    with open("Assets/StreamingServices.json", "r") as StreamingFile:
        StreamingServices = json.load(StreamingFile)
    AppIDs = GenerateVDFEntriesAndReturnAppIDs(StreamingServices)
    GrabAndSetArtworkForGivenAppIDs(StreamingServices, AppIDs)
