# Linux-Deck-Streaming-Services
Script which allows the user to access streaming services from the steam deck's 'Game Mode' interface 

<h3>Script Information</h3>
    <ul>
        <li>The script has three main tasks</li>
        <ul>
            <li>It will install the flatpak version of firefox to the users system if it doesn't exist already</li>
            <li>It will move the required files into a 'Streaming' folder in the users steam game directory</li>
            <li>It will create the non-steam shortcuts for each streaming service with their appropriate configurations</li>
        </ul>
        <li>The steam shortcuts act as 'apps' in the Game Mode interface and launch firefox in kiosk mode with optimal scaling settings for the steam decks resolution</li>
        <li>Manual configuration of the controller settings for web browser navigation may still be required</li>
        <li>Manual addition of artwork from the desktop is still required, if wanted</li>
        <ul>
            <li>I would recommend using <a href="https://flathub.org/apps/com.steamgriddb.SGDBoop">SGDBoop</a></li>
        </ul>
    </ul>

Credit to https://github.com/ValvePython/vdf for the vdf parsing