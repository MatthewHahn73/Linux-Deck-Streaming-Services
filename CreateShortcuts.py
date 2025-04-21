"""
CreateShortcuts.py

Current Bugs
    -Steam doesn't populate the non-steam games with the right artwork. Likely due to steam using some kind of hashing when normally storing those values

TODO
    -Need to compact all the logic into one script. Move Setup.sh logic to here
    -Need to add in better documentation of current script progress and exception handling
    -Need to better optimize the GrabAndSetArtworkForGivenAppIDs function 
    -Need to find a better way to get the StreamingServices and ArtworkLinks values 
"""

import os, binascii, json, logging
from urllib.request import Request, urlopen

SteamUserData = "/home/" + os.getlogin() + "/.steam/steam/userdata/"
PathToUserConfig = SteamUserData + os.listdir(SteamUserData)[0] + "/config/grid/"
PathToSteamShortcutsFile = SteamUserData + os.listdir(SteamUserData)[0] + "/config/shortcuts.vdf"

def GrabAndSetArtworkForGivenAppIDs(ArtworkLinks, AppIDs):
    for StreamingAppType in ArtworkLinks: 
        for Artwork in ArtworkLinks[StreamingAppType]:
            #Set the artwork values to something usable
            ArtworkType = Artwork.replace(" - Horizontal", "").replace(" - Vertical", "")
            ArtworkURL = "https://cdn2.steamgriddb.com/" + ArtworkType + "/" + ArtworkLinks[StreamingAppType][Artwork]
            ArtworkFileName, ArtworkFileType = os.path.splitext(ArtworkURL)
            ArtworkSuffix = {
                "grid - Vertical": "p",
                "grid - Horizontal": "",
                "hero": "_hero", 
                "logo": "_logo",
                "icon": "_icon"
            }.get(Artwork, "")
            #Query steamgriddb for the artwork
            SteamGridDBRequest = Request(url=ArtworkURL, headers={
                            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                            'Accept-Encoding': 'none',
                            'Accept-Language': 'en-US,en;q=0.8',
                            'Connection': 'keep-alive'
                        })
            ReturnedValue = urlopen(SteamGridDBRequest).read()
            #Create the files in the users userdata/<UserID>/grid/ directory, set to the appropriate AppID
            FullFileName = AppIDs[StreamingAppType] + ArtworkSuffix + ArtworkFileType
            with open(PathToUserConfig + FullFileName, "wb") as FetchedFile:
                FetchedFile.write(ReturnedValue)
    
def GenerateAppID(ExeName, AppName):
    UniqueID = "".join([ExeName, AppName])
    AppID = binascii.crc32(str.encode(UniqueID)) | 0x80000000
    return AppID

def GenerateVDFEntriesAndReturnAppIDs(StreamingServices):
    PathToScript = "bash " + '"/home/deck/.steam/steam/steamapps/common/Streaming/LaunchApp.sh"'
    PathToDirectory = '"/home/deck/.steam/steam/steamapps/common/Streaming/"'

    #Check for an existing shortcuts.vdf, if doesn't exist, create one
    if not os.path.exists(PathToSteamShortcutsFile):
        with open(PathToSteamShortcutsFile, "wb") as NewlyCreatedFile:
            NewlyCreatedFile.write(b'\x00' + b'shortcuts' + b'\x00\x08\x08')
       
    #Open the shortcuts.vdf file for its contents and determine how many non-steam games already exist
    with open(PathToSteamShortcutsFile, "rb") as SteamShortcutsFile:
        SteamShortcutsFileContentsTrimmed = SteamShortcutsFile.readlines()[0][:-2]
        CurrentIteration = SteamShortcutsFileContentsTrimmed.count(b'appid')
        CurrentIteration += 1 if CurrentIteration != 0 else 0

    #For each streaming service, create a non-steam game and populate its attributes
    TotalContentsToAppend = b''
    CurrentAppIDList = {}
    for Key in StreamingServices:
        CurrentAppID = str(GenerateAppID("LaunchApp.sh", str(Key))).encode('utf-8')
        Iteration = str(CurrentIteration).encode('utf-8')
        AppNameBytes = str(Key).encode('utf-8')                                        
        PathToScriptBytes = str(PathToScript).encode('utf-8')                            
        StartDirectoryBytes = str(PathToDirectory).encode('utf-8')      
        LaunchOptionsBytes = str('"' + str(StreamingServices[Key]) + '"').encode('utf-8')   

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
    AppIDs = GenerateVDFEntriesAndReturnAppIDs({
        "Prime Video" : "https://www.amazon.com/video",
        "Youtube" : "https://www.youtube.com/", 
        "Netflix" : "https://www.netflix.com/", 
        "HBO Max" : "https://www.max.com/", 
        "Apple TV" : "https://tv.apple.com/"
    })
    GrabAndSetArtworkForGivenAppIDs({
        "Prime Video" : {
            "grid - Vertical" : "10c8f12e1fb3ed73b09ec0311a269a42.png", 
            "grid - Horizontal" : "e152ea66175587989ee431b09e85b337.png", 
            "hero" : "304cb49033bca92dc8391e133ef1d750.png", 
            "logo" : "58840eb65da053fbdea5f4d19dd3e00f.png", 
            "icon" : "f64b2463cf1dba199491c885dff932f3.ico"
        }, 
        "Youtube" : {
            "grid - Vertical" : "f7df4b3972375bc784cd61ada708046f.jpg", 
            "grid - Horizontal" : "98f67d0c03e88f22c2d9f2930848b8fa.jpg", 
            "hero" : "4a9f57c5dadf5bc6555a2e754ca3cfa7.png", 
            "logo" : "9216f34dc82ae586c1d6c37bdb8e8edf.png", 
            "icon" : "995665640dc319973d3173a74a03860c.ico"
        }, 
        "Netflix" : {
            "grid - Vertical" : "8db700701ae6ebeb663f433c35abeeb8.png", 
            "grid - Horizontal" : "befe326073e97f6b4335c72e186b7369.jpg", 
            "hero" : "d810302a6bb9bc97e7c9662b90a634a9.png", 
            "logo" : "92757b7ebf6d8edfef5e211249a38ab5.png", 
            "icon" : "4a06d868d044c50af0cf9bc82d2fc19f.ico"
        }, 
        "HBO Max" : {
            "grid - Vertical" : "27d049f461720c8fbc869279e7da7e41.png", 
            "grid - Horizontal" : "f045c10f3a39ac512783e0869bc45eb5.png", 
            "hero" : "d6f07f83059edd69be854095a7ddd520.png", 
            "logo" : "60a399eedc5ad40dbf3cd69cf3c178a6.png", 
            "icon" : "501fe32ad8686901bb423ede39d6ce04.png"
        }, 
        "Apple TV" : {
            "grid - Vertical" : "eff7b4b3d1cbcdc29ff8b8412d86af56.jpg", 
            "grid - Horizontal" : "58d824c17ac25bd43fb42b087578071d.png", 
            "hero" : "f39ab4e4f1135fd68862f122b6b22dd5.png", 
            "logo" : "e637c9c15d72fcbeecdcf3bddc224054.png", 
            "icon" : "7b1223235e9b545dffd56c4cac714b41.png"
        }
    }, AppIDs)
