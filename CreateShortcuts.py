"""
CreateShortcuts.py

Current Bugs
    -Steam doesn't populate the non-steam games with the right artwork. Likely due to steam using some kind of hashing when normally storing those values

TODO
    -Need to add in better documentation of current script progress and exception handling
    -Need to better optimize the GrabAndSetArtworkForGivenAppIDs function 
"""

import os, binascii, json, logging
from urllib.request import Request, urlopen

GlobalLogger = logging.getLogger()
GlobalLogger.setLevel(logging.DEBUG)

User = os.getlogin()
SteamUserData = "/home/" + User + "/.steam/steam/userdata/"
SteamGameData = "/home/" + User + "/.steam/steam/steamapps/common"
PathToUserConfig = SteamUserData + os.listdir(SteamUserData)[0] + "/config/grid/"
PathToSteamShortcutsFile = SteamUserData + os.listdir(SteamUserData)[0] + "/config/shortcuts.vdf"

def GenerateAppID(ExeName, AppName):
    UniqueID = "".join([ExeName, AppName])
    AppID = binascii.crc32(str.encode(UniqueID)) | 0x80000000
    return AppID

def GrabAndSetArtworkForGivenAppIDs(ArtworkLinks, AppIDs):
    for StreamingAppType in ArtworkLinks: 
        for ArtworkType in ArtworkLinks[StreamingAppType]["Artwork"]:
            #Set the artwork values to something usable and query steamgriddb for the artwork
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

            #Create the files in the users userdata/<UserID>/grid/ directory, set to the appropriate AppID
            FullFileName = AppIDs[StreamingAppType] + ArtworkSuffix + ArtworkFileType
            with open(PathToUserConfig + FullFileName, "wb") as FetchedFile:
                FetchedFile.write(ReturnedValue)
    
def GenerateVDFEntriesAndReturnAppIDs(StreamingServices):
    PathToScript = "bash " + '"/home/' + User + '/.steam/steam/steamapps/common/Streaming/LaunchApp.sh"'
    PathToDirectory = '"/home/' + User + '/.steam/steam/steamapps/common/Streaming/"'

    #Check for an existing shortcuts.vdf file, and if doesn't exist, create one. Determine how many non-steam games already exist
    if not os.path.exists(PathToSteamShortcutsFile):
        logging.info("Creating shortcuts file at '" + PathToSteamShortcutsFile + "'")
        with open(PathToSteamShortcutsFile, "wb") as NewlyCreatedFile:
            NewlyCreatedFile.write(b'\x00' + b'shortcuts' + b'\x00\x08\x08')
    with open(PathToSteamShortcutsFile, "rb") as SteamShortcutsFile:
        SteamShortcutsFileContentsTrimmed = SteamShortcutsFile.readlines()[0][:-2]
        CurrentIteration = SteamShortcutsFileContentsTrimmed.count(b'appid')
        CurrentIteration += 1 if CurrentIteration != 0 else 0

    #For each streaming service, create a non-steam game and populate its attributes
    logging.info("Appending new items to '" + PathToSteamShortcutsFile + "' ...")
    TotalContentsToAppend = b''
    CurrentAppIDList = {}
    for Key in StreamingServices:
        CurrentAppID = str(GenerateAppID("LaunchApp.sh", str(Key))).encode('utf-8')
        Iteration = str(CurrentIteration).encode('utf-8')
        AppNameBytes = str(Key).encode('utf-8')                                        
        PathToScriptBytes = str(PathToScript).encode('utf-8')                            
        StartDirectoryBytes = str(PathToDirectory).encode('utf-8')      
        LaunchOptionsBytes = str('"' + str(StreamingServices[Key]["Link"]) + '"').encode('utf-8')   

        CurrentRow = b'\x00' + Iteration + b'\x00' + \
                        b'\x02' + b'appid' + b'\x00' + CurrentAppID + b'\x00' + \
                        b'\x01' + b'AppName' + b'\x00' + AppNameBytes + b'\x00' + \
                        b'\x01' + b'Exe' + b'\x00' + PathToScriptBytes + b'\x00' + \
                        b'\x01' + b'StartDir' + b'\x00' + StartDirectoryBytes + b'\x00' + \
                        b'\x01' + b'icon' + b'\x00\x00' + \
                        b'\x01' + b'ShortcutPath' + b'\x00\x00' + \
                        b'\x01' + b'LaunchOptions' + b'\x00' + LaunchOptionsBytes + b'\x00' + \
                        b'\x02' + b'IsHidden' + b'\x00\x00\x00\x00\x00' + \
                        b'\x02' + b'AllowDesktopConfig' + b'\x00\x01\x00\x00\x00' + \
                        b'\x02' + b'AllowOverlay' + b'\x00\x01\x00\x00\x00' + \
                        b'\x02' + b'OpenVR' + b'\x00\x00\x00\x00\x00' + \
                        b'\x02' + b'Devkit' + b'\x00\x00\x00\x00\x00' + \
                        b'\x01' + b'DevkitGameID' + b'\x00\x00' + \
                        b'\x01' + b'DevkitOverrideAppID' + b'\x00\x00' + \
                        b'\x02' + b'LastPlayTime' + b'\x00\x00\x00\x00\x00' + \
                        b'\x01' + b'FlatpakAppID' + b'\x00\x00' + \
                        b'\x00' + b'tags' + b'\x00' + \
                    b'\x08' + \
                    b'\x08' 
        TotalContentsToAppend += CurrentRow
        CurrentIteration += 1 
        CurrentAppIDList[Key] = CurrentAppID.decode('utf-8')
        
    #Append the created non-steam games to the existing shortcuts.vdf file
    with open(PathToSteamShortcutsFile, "wb") as SteamShortcutsFileEnding:
        SteamShortcutsFileEnding.write(SteamShortcutsFileContentsTrimmed + TotalContentsToAppend + b'\x08\x08')
    return CurrentAppIDList

if __name__ == "__main__":
    logging.info("Installing firefox ...")
    #os.system("flatpak install flathub org.mozilla.firefox -y")

    logging.info("Moving the files to '" + SteamGameData + "' ...")
    #os.makedirs(SteamGameData + "/Streaming")
    #os.system("cp -a $(pwd)/Streaming " + "'" + SteamGameData + "'")

    with open("Script Assets/StreamingServices.json", "r") as StreamingFile:
        StreamingServices = json.load(StreamingFile)
    AppIDs = GenerateVDFEntriesAndReturnAppIDs(StreamingServices)
    GrabAndSetArtworkForGivenAppIDs(StreamingServices, AppIDs)
