Username="hahn"
SteamGamesDir=/home/$Username/.steam/steam/steamapps/common  
CurrentDir=`pwd` 
SteamTinkerVersion="12.12"                                                                                      
DownloadLocation="/home/$Username/Downloads/"
TinkerAlias=SteamTinkerLauncher.tar.gz

flatpak install flathub org.mozilla.firefox                                                                     #Install the flatpak version of firefox (if not already installed)

cd $DownloadLocation                                                                                            #Install steamtinker
curl -sSL https://github.com/sonic2kk/steamtinkerlaunch/archive/refs/tags/v12.12.tar.gz > SteamTinkerLauncher.tar.gz
tar xzf SteamTinkerLauncher.tar.gz -C $DownloadLocation
rm $TinkerAlias
cd steamtinkerlaunch-$SteamTinkerVersion
./steamtinkerlaunch
./steamtinkerlaunch compat add 

mkdir -p $SteamGamesDir/Streaming
cp -a $CurrentDir/Streaming $SteamGamesDir                                                                                  
cd $SteamGamesDir/Streaming/Assets                                               #Download assets
mkdir -p $SteamGamesDir/Streaming/Assets/Netflix
cd Netflix
curl -sS https://cdn2.steamgriddb.com/grid/8db700701ae6ebeb663f433c35abeeb8.png > Netflix_Box.png
curl -sS https://cdn2.steamgriddb.com/grid/befe326073e97f6b4335c72e186b7369.jpg > Netflix_Grid.jpg
curl -sS https://cdn2.steamgriddb.com/hero/d810302a6bb9bc97e7c9662b90a634a9.png > Netflix_Hero.png
curl -sS https://cdn2.steamgriddb.com/logo/92757b7ebf6d8edfef5e211249a38ab5.png > Netflix_Logo.png
curl -sS https://cdn2.steamgriddb.com/icon/4a06d868d044c50af0cf9bc82d2fc19f.ico > Netflix_Icon.ico
cd ..
mkdir -p $SteamGamesDir/Streaming/Assets/Prime
cd Prime
curl -sS https://cdn2.steamgriddb.com/grid/10c8f12e1fb3ed73b09ec0311a269a42.png > Prime_Box.png
curl -sS https://cdn2.steamgriddb.com/grid/e152ea66175587989ee431b09e85b337.png > Prime_Grid.png
curl -sS https://cdn2.steamgriddb.com/hero/304cb49033bca92dc8391e133ef1d750.png > Prime_Hero.png
curl -sS https://cdn2.steamgriddb.com/logo/58840eb65da053fbdea5f4d19dd3e00f.png > Prime_Logo.png
curl -sS https://cdn2.steamgriddb.com/icon/cfa31d8130bef0e6643e5de9d0a0cac9.ico > Prime_Icon.ico
cd ..
mkdir -p $SteamGamesDir/Streaming/Assets/Apple_TV
cd Apple_TV
curl -sS https://cdn2.steamgriddb.com/grid/eff7b4b3d1cbcdc29ff8b8412d86af56.jpg > Apple_Box.jpg
curl -sS https://cdn2.steamgriddb.com/grid/58d824c17ac25bd43fb42b087578071d.png > Apple_Grid.png
curl -sS https://cdn2.steamgriddb.com/hero/f39ab4e4f1135fd68862f122b6b22dd5.png > Apple_Hero.png
curl -sS https://cdn2.steamgriddb.com/logo/e637c9c15d72fcbeecdcf3bddc224054.png > Apple_Logo.png
curl -sS https://cdn2.steamgriddb.com/icon/7b1223235e9b545dffd56c4cac714b41.png > Apple_Icon.ico
cd ..
mkdir -p $SteamGamesDir/Streaming/Assets/Youtube
cd Youtube
curl -sS https://cdn2.steamgriddb.com/grid/b4c77e5ea1c199ea6a3e78f366287262.png > Youtube_Box.jpg
curl -sS https://cdn2.steamgriddb.com/grid/786929ce1b2e187510aca9b04a0f7254.jpg > Youtube_Grid.png
curl -sS https://cdn2.steamgriddb.com/hero/cfc5d9422f0c8f8ad796711102dbe32b.png > Youtube_Hero.png
curl -sS https://cdn2.steamgriddb.com/logo/9216f34dc82ae586c1d6c37bdb8e8edf.png > Youtube_Logo.png
curl -sS https://cdn2.steamgriddb.com/icon/995665640dc319973d3173a74a03860c.ico > Youtube_Icon.ico
cd ..
mkdir -p $SteamGamesDir/Streaming/Assets/Max
cd Max
curl -sS https://cdn2.steamgriddb.com/grid/27d049f461720c8fbc869279e7da7e41.png > Max_Box.png 
curl -sS https://cdn2.steamgriddb.com/grid/f045c10f3a39ac512783e0869bc45eb5.png > Max_Grid.png 
curl -sS https://cdn2.steamgriddb.com/hero/3a0babb7888bd5976ce3df45743615af.png > Max_Hero.png 
curl -sS https://cdn2.steamgriddb.com/logo/60a399eedc5ad40dbf3cd69cf3c178a6.png > Max_Logo.png 
curl -sS https://cdn2.steamgriddb.com/icon/9a29c32994158d26c4169dfd81ba440b.png > Max_Icon.ico 
cd ..

steamtinkerlaunch addnonsteamgame 
    \ --appname="Netflix" 
    \ --exepath="bash /home/deck/.steam/steam/steamapps/common/Streaming/LaunchApp.sh" 
    \ --sStartdir="/home/deck/.steam/steam/steamapps/common/Streaming/" 
    \ --launchoptions="https://www.netflix.com/"
    \ --iconpath="$SteamGamesDir/Streaming/Assets/Netflix_Icon.ico"
    \ --hero="$SteamGamesDir/Streaming/Assets/Netflix_Hero.png"
    \ --logo="$SteamGamesDir/Streaming/Assets/Netflix_Logo.png"
    \ --boxart="$SteamGamesDir/Streaming/Assets/Netflix_Box.png"
    \ --tenfoot="$SteamGamesDir/Streaming/Assets/Netflix_Grid.jpg"
steamtinkerlaunch addnonsteamgame 
    \ --appname="Prime Video" 
    \ --exepath="bash /home/deck/.steam/steam/steamapps/common/Streaming/LaunchApp.sh" 
    \ --sStartdir="/home/deck/.steam/steam/steamapps/common/Streaming/" 
    \ --launchoptions="https://www.amazon.com/video"
    \ --iconpath="$SteamGamesDir/Streaming/Assets/Prime_Icon.ico"
    \ --hero="$SteamGamesDir/Streaming/Assets/Prime_Hero.png"
    \ --logo="$SteamGamesDir/Streaming/Assets/Prime_Logo.png"
    \ --boxart="$SteamGamesDir/Streaming/Assets/Prime_Box.png"
    \ --tenfoot="$SteamGamesDir/Streaming/Assets/Prime_Grid.png"
steamtinkerlaunch addnonsteamgame 
    \ --appname="Apple TV" 
    \ --exepath="bash /home/deck/.steam/steam/steamapps/common/Streaming/LaunchApp.sh" 
    \ --sStartdir="/home/deck/.steam/steam/steamapps/common/Streaming/" 
    \ --launchoptions="https://tv.apple.com/"
    \ --iconpath="$SteamGamesDir/Streaming/Assets/Apple_Icon.png"
    \ --hero="$SteamGamesDir/Streaming/Assets/Apple_Hero.png"
    \ --logo="$SteamGamesDir/Streaming/Assets/Apple_Logo.png"
    \ --boxart="$SteamGamesDir/Streaming/Assets/Apple_Box.jpg"
    \ --tenfoot="$SteamGamesDir/Streaming/Assets/Apple_Grid.jpg"
steamtinkerlaunch addnonsteamgame 
    \ --appname="Youtube" 
    \ --exepath="bash /home/deck/.steam/steam/steamapps/common/Streaming/LaunchApp.sh" 
    \ --sStartdir="/home/deck/.steam/steam/steamapps/common/Streaming/" 
    \ --launchoptions="https://www.youtube.com/"
    \ --iconpath="$SteamGamesDir/Streaming/Assets/Youtube_Icon.ico"
    \ --hero="$SteamGamesDir/Streaming/Assets/Youtube_Hero.png"
    \ --logo="$SteamGamesDir/Streaming/Assets/Youtube_Logo.png"
    \ --boxart="$SteamGamesDir/Streaming/Assets/Youtube_Box.png"
    \ --tenfoot="$SteamGamesDir/Streaming/Assets/Youtube_Grid.jpg"
steamtinkerlaunch addnonsteamgame 
    \ --appname="HBO Max" 
    \ --exepath="bash /home/deck/.steam/steam/steamapps/common/Streaming/LaunchApp.sh" 
    \ --sStartdir="/home/deck/.steam/steam/steamapps/common/Streaming/" 
    \ --launchoptions="https://www.max.com/"
    \ --iconpath="$SteamGamesDir/Streaming/Assets/Max_Icon.ico"
    \ --hero="$SteamGamesDir/Streaming/Assets/Max_Hero.png"
    \ --logo="$SteamGamesDir/Streaming/Assets/Max_Logo.png"
    \ --boxart="$SteamGamesDir/Streaming/Assets/Max_Box.png"
    \ --tenfoot="$SteamGamesDir/Streaming/Assets/Max_Grid.png"