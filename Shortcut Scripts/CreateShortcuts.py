import random
from urllib.request import Request, urlopen

StreamingServices = {
    "Prime" : "https://www.amazon.com/video",
    "Youtube" : "https://www.youtube.com/", 
    "Netflix" : "https://www.netflix.com/", 
    "HBO Max" : "https://www.max.com/", 
    "Apple TV" : "https://tv.apple.com/"
}

def GenerateAppID():
    return random.randint(0, 9999)

def GrabIconFileFromSteamGridDB(AppName):
    match AppName: 
        case "Prime Video":
            FileGUID = "f64b2463cf1dba199491c885dff932f3.ico"
        case "Youtube":
            FileGUID = "995665640dc319973d3173a74a03860c.ico"
        case "Netflix":
            FileGUID = "4a06d868d044c50af0cf9bc82d2fc19f.ico" 
        case "HBO Max":
            FileGUID = "501fe32ad8686901bb423ede39d6ce04.png" 
        case "Apple TV":
            FileGUID = "7b1223235e9b545dffd56c4cac714b41.png" 
        case _:
            pass 
    SteamGridDBRequest = Request(url="https://cdn2.steamgriddb.com/icon/" + FileGUID, headers={
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                    'Accept-Encoding': 'none',
                    'Accept-Language': 'en-US,en;q=0.8',
                    'Connection': 'keep-alive'
                })
    ReturnedValue = urlopen(SteamGridDBRequest).read()
    with open("Assets/Icons/" + AppName + ".ico", "wb") as FetchedFile:
        FetchedFile.write(ReturnedValue)

def GenerateVDFEntries():
    PathToSteamShortcutsFile = "/home/$USER/.steam/steam/userdata/$STEAMID/config/shortcuts.vdf"
    PathToScript = "bash " + '"/home/deck/.steam/steam/steamapps/common/Streaming/LaunchApp.sh"'
    PathToDirectory = "/home/deck/.steam/steam/steamapps/common/Streaming/"
    ReplacementsBlueprint = { 
        "<Iteration>" : "",
        "<Generated APPID>" : "",
        "<App Name>" : "",
        "<Path to EXE>" : "",
        "<Path to Start Directory>" : "",
        "<Launch Options>" : ""
    }

    with open("Shortcut Scripts/DummyFile.vdf", "rb") as DummyFile:
        DummyFileContents = DummyFile.readlines()

    with open("Shortcut Scripts/shortcuts.vdf", "rb") as SteamShortcutsFile:
        SteamShortcutsFileContentsTrimmed = SteamShortcutsFile.readlines()[0][:-2]
        CurrentIteration = SteamShortcutsFileContentsTrimmed.count(b'shortcuts') - 1
    
    TotalContentsToAppend = b''
    for Iteration, Key in enumerate(StreamingServices):
        if CurrentIteration > 0:
            CurrentIteration += 1 
        CurrentList = ReplacementsBlueprint.copy()
        CurrentFileContents = DummyFileContents.copy()[0]
        CurrentAppID = GenerateAppID().to_bytes(2, 'little')

        CurrentList["<Iteration>"] = str(CurrentIteration).encode('utf-8')
        CurrentList["<Generated APPID>"] = CurrentAppID                                             #Set the appid
        CurrentList["<App Name>"] = str(Key).encode('utf-8')                                        #Set the app Name
        CurrentList["<Path to EXE>"] = str(PathToScript).encode('utf-8')                            #Set the path to the script
        CurrentList["<Path to Start Directory>"] = str(PathToDirectory).encode('utf-8')             #Set the path to the directory
        CurrentList["<Launch Options>"] = ('"' + StreamingServices[Key] + '"').encode('utf-8')      #Set the launch Options

        for Key in CurrentList:
            CurrentFileContents = CurrentFileContents.replace(Key.encode('utf-8'), CurrentList[Key])
        TotalContentsToAppend += CurrentFileContents
        
    with open("Shortcut Scripts/shortcuts.vdf", "wb") as SteamShortcutsFileEnding:
        SteamShortcutsFileEnding.write(SteamShortcutsFileContentsTrimmed + TotalContentsToAppend + b'\x08\x08')

if __name__ == "__main__":
    GenerateVDFEntries()
