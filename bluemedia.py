import dbus
import dbus.mainloop.glib
import dbus.service
from gi.repository import GLib

class BluetoothMediaController(dbus.service.Object):
    def __init__(self, device_address):
        dbus.service.Object.__init__(self, dbus.SystemBus(), "/org/bluez")
        self.bus = dbus.SystemBus()
        self.device_path = f"/org/bluez/hci0/dev_{device_address.replace(':', '_')}"
        self.player_path = None
        self._find_player()

    def _find_player(self):
        obj_manager = dbus.Interface(self.bus.get_object('org.bluez', '/'), 'org.freedesktop.DBus.ObjectManager')
        objects = obj_manager.GetManagedObjects()
        for path, interfaces in objects.items():
            if 'org.bluez.MediaPlayer1' in interfaces and path.startswith(self.device_path):
                self.player_path = path
                break

    def play(self):
        player = self._get_player_interface()
        if player:
            player.Play()

    def pause(self):
        player = self._get_player_interface()
        if player:
            player.Pause()

    def next(self):
        player = self._get_player_interface()
        if player:
            player.Next()

    def previous(self):
        player = self._get_player_interface()
        if player:
            player.Previous()

    def get_current_track(self):
        player = self._get_player_interface()
        if player:
            properties = dbus.Interface(player, 'org.freedesktop.DBus.Properties')
            metadata = properties.Get('org.bluez.MediaPlayer1', 'Track')
            return {
                'title': metadata.get('Title', 'Unknown'),
                'artist': metadata.get('Artist', 'Unknown'),
                'album': metadata.get('Album', 'Unknown')
            }

    def _get_player_interface(self):
        if self.player_path:
            obj = self.bus.get_object('org.bluez', self.player_path)
            iface = dbus.Interface(obj, 'org.bluez.MediaPlayer1')
            return iface


if __name__ == "__main__":
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    device_address = '90:8C:43:40:14:F4'
    controller = BluetoothMediaController(device_address)
    loop = GLib.MainLoop()

    # Example usage:
    controller.play()
    GLib.timeout_add_seconds(5, controller.pause)
    track_info = controller.get_current_track()
    print(f"Currently playing: {track_info['title']} by {track_info['artist']} from the album {track_info['album']}")
    GLib.timeout_add_seconds(10, loop.quit)

    loop.run()
