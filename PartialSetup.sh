#Install the flatpak version of firefox and SGDBoop for non-steam shortcut assets
flatpak install flathub org.mozilla.firefox flathub com.steamgriddb.SGDBoop -y 

#Move files to default install steam games directory
mkdir -p /home/$USER/.steam/steam/steamapps/common/Streaming
cp -a $(pwd)/Streaming /home/$USER/.steam/steam/steamapps/common   