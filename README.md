# Linux-Deck-Streaming-Services
Shell script which allows for access to streaming services from the steam deck's 'Game Mode' interface 

<h3>Script Information</h3>
    <ul>
        <li>The 'LaunchApp.sh' script will launch the flatpak version of firefox in fullscreen with optimal deck settings</li>
        <ul>
            <li>The script will act as a game executable in a non-steam game shortcut, but will need to be prefixed with 'bash' under the 'Target' field for the shortcut settings</li>
            <li>Can be used with any url. The desired url to launch can be added to the launch parameters of the steam shortcut settings</li>
            <ul>
                <li>Some common streaming urls can be found in the scripts comments</li>
            </ul>
        </ul>
        <li>The 'PartialSetup.sh' script can be run to partially set up the shortcuts</li>
        <ul>
            <li>This script will install firefox and SGDBoop for artwork, along with moving the required files to the boot drives steam directory</li>
            <li>The actual creation of the shortcuts themselves will have to be done manually from desktop mode, and artwork hand picked off SteamGridDB</li>
            <li>Full setup with creation of the steam shortcuts and setting of their artwork may come in the future</li>
        </ul>
    </ul>