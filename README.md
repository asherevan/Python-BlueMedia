# Python-BlueMedia
A simple Python library using the BlueZ library for controling music playing (and getting song data) through a bluetooth speaker. I Have only tested it with [this](https://forums.raspberrypi.com/viewtopic.php?t=235519) tutorial on a Raspberry Pi 3B with Raspberry Pi OS. Please let me know if it works on anything else!

## Usage

### Properties

`bluemedia.BluetoothMediaController(BLUETOOTH_ADDRESS)`

 - `.start()` Start playback
   
 - `.pause()` Pause playback

 - `.get_current_track()` Returns a dictonary of values `title`, `artist`, and `album`
