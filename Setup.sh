#Install the flatpak version of firefox and SGDBoop for non-steam shortcut assets
flatpak install flathub org.mozilla.firefox flathub com.steamgriddb.SGDBoop -y 

#Move files to default install steam games directory
mkdir -p /home/$USER/.steam/steam/steamapps/common/Streaming
cp -a $(pwd)/Streaming /home/$USER/.steam/steam/steamapps/common   

#Run a python script to create the steam shortcuts and set the artwork for each streaming service
python3 -B CreateShortcuts.py