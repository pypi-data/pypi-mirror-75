# based on tube mover calibration by Theo Sanderson
# github https://github.com/theosanderson/tube_checkout


import atexit
import json
import subprocess
import threading
import time

import urwid
from opentrons.protocol_api import ProtocolContext

from ondine_laser_control import laser

print("Starting...")

movement_distances = {"1": 0.1, "2": 1, "3": 10}
movement_distance = 0.1


# from https://github.com/theosanderson/tube_checkout
# -----------
def temporarily_kill_ot_server():
    """ Kills the OpenTrons robot server service, and sets it to restart at exit. """
    subprocess.check_output(
        "systemctl stop opentrons-robot-server", shell=True)

    def restart_ot_server():
        subprocess.check_output(
            "systemctl start opentrons-robot-server", shell=True)

    atexit.register(restart_ot_server)


class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self, *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()


watcher_thread = None


def set_button_purple(protocol_to_use: ProtocolContext):
    protocol_to_use._hw_manager.hardware._backend.gpio_chardev.set_button_light(red=True, blue=True, green=False)


def set_button_red(protocol_to_use: ProtocolContext):
    protocol_to_use._hw_manager.hardware._backend.gpio_chardev.set_button_light(red=True, blue=False, green=False)


def set_button_off(protocol_to_use: ProtocolContext):
    protocol_to_use._hw_manager.hardware._backend.gpio_chardev.set_button_light(red=False, blue=False, green=False)


def set_button_yellow(protocol_to_use: ProtocolContext):
    protocol_to_use._hw_manager.hardware._backend.gpio_chardev.set_button_light(red=True, blue=False, green=True)


def set_button_as_kill_switch(protocol_to_use: ProtocolContext):
    global watcher_thread
    set_button_red(protocol_to_use)

    def button_watcher():
        while not threading.current_thread().stopped():
            time.sleep(0.1)
            if protocol_to_use._hw_manager.hardware._backend.gpio_chardev.read_button():
                set_button_yellow(protocol_to_use)
                protocol_to_use._hw_manager.hardware.halt()

    watcher_thread = StoppableThread(target=button_watcher)
    watcher_thread.start()


def stop_watcher():
    watcher_thread.stop()


atexit.register(stop_watcher)

# ---------------------

temporarily_kill_ot_server()

import opentrons.execute
import logging

logging.disable(logging.ERROR)

protocol = opentrons.execute.get_protocol_api('2.5')

# turn on lights
protocol._hw_manager.hardware.set_lights(rails=True)

# press button to kill
set_button_as_kill_switch(protocol)

print("Homing... ")
protocol.home()

plate = protocol.load_labware('corning_96_wellplate_360ul_flat', 1)

laserController = laser.Controller(protocol=protocol, print_debug_messages=False)

laserController.move_to_well(plate["A1"], speed=100)

print("Moving to start position...")
laserController.move_z(plate["A1"].top(5).point.z, speed=100)


def updateOffsetsFile(x: float, y: float, z: float):
    with open(laser.offset_file, 'w') as outfile:
        json.dump({'x': x, 'y': y, 'z': z}, outfile)


initial_offsets = laser.read_offsets_file()

x_offset = initial_offsets['x']
y_offset = initial_offsets['y']
z_offset = initial_offsets['z']
top_of_well = plate["A1"].top().point


def set_movement_distance(distance):
    global movement_distance
    movement_distance = distance
    movement_distance_txt.set_text(("reverse", "Movement distance: {} mm".format(distance)))


def update_offset():
    global x_offset, y_offset, z_offset
    p = laserController.get_current_pos()
    x_offset = p.x - top_of_well.x
    y_offset = p.y - top_of_well.y
    z_offset = p.z - laserController.z_abs_min - top_of_well.z


def update_pos():
    pos = laserController.get_current_pos()
    update_offset()
    pos_txt.set_text(("reverse",
                      f"Current position: X: {round(pos.x, 2)} Y: {round(pos.y, 2)} Z: {round(pos.z, 2)} . Offset  X: {round(x_offset, 2)} Y: {round(y_offset, 2)} Z: {round(z_offset, 2)} "))


def save_offset():
    current_saved_offset_txt.set_text((
        "reverse",
        f"Saved offset:  X: {round(laserController.x_offset, 2)} "
        f"Y: {round(laserController.y_offset, 2)} "
        f"Z: {round(laserController.z_offset, 2)}"
    ))
    update_offset()
    laserController.x_offset = x_offset
    laserController.y_offset = y_offset
    laserController.z_offset = z_offset
    updateOffsetsFile(x=x_offset, y=y_offset, z=z_offset)
    message.set_text(f"Offset saved X: {x_offset} Y: {y_offset} Z: {z_offset}")


def show_or_exit(key):
    message.set_text("")
    global movement_distance, top_of_well
    if key in movement_distances.keys():
        set_movement_distance(movement_distances[key])
    if key in ("U", "u"):
        save_offset()
        top_of_well = plate["A1"].top().point
        laserController.move_to_well(plate["A1"], speed=100)
        laserController.move_z(plate["A1"].top(5).point.z, speed=100)
        update_pos()
    if key in ("I", "i"):
        save_offset()
        top_of_well = plate["A12"].top().point
        laserController.move_to_well(plate["A12"], speed=100)
        laserController.move_z(plate["A12"].top(5).point.z, speed=100)
        update_pos()

    if key in ("O", "o"):
        save_offset()
        top_of_well = plate["H12"].top().point
        laserController.move_to_well(plate["H12"], speed=100)
        laserController.move_z(plate["H12"].top(5).point.z, speed=100)
        update_pos()

    if key in ('h', 'H'):
        protocol.home()

    if key in ('q', 'Q'):
        raise urwid.ExitMainLoop

    if key in ('s', 'S'):
        save_offset()

    if key == "shift up":
        laserController.move_relz(movement_distance)
        update_pos()

    if key == "shift down":
        laserController.move_relz(-movement_distance)
        update_pos()
    if key == "up":
        laserController.move_rely(movement_distance)
        update_pos()
    if key == "down":
        laserController.move_rely(-movement_distance)
        update_pos()
    if key == "left":
        laserController.move_relx(-movement_distance)
        update_pos()
    if key == "right":
        laserController.move_relx(movement_distance)
        update_pos()


text_header = (u"Laser Calibration")

header = urwid.AttrWrap(urwid.Text(text_header), 'header')

pos_txt = urwid.Text(('reverse', u"Current position: "))

current_saved_offset_txt = urwid.Text(('reverse', u"Saved offset: "))
current_saved_offset_txt.set_text((
    "reverse",
    f"Saved offset:  X: {round(laserController.x_offset, 2)} "
    f"Y: {round(laserController.y_offset, 2)} "
    f"Z: {round(laserController.z_offset, 2)}"
))

movement_distance_txt = urwid.Text(('reverse', u"Movement distance: "))

message = urwid.Text(('reverse', u""))

num_key_expl = ", ".join([f"{k}: {movement_distances[k]}mm " for k in movement_distances])

keyboard = urwid.Text(f"""\
KEYBOARD SHORTCUTS:
Number keys - set movement distance: {num_key_expl}
Arrow keys - move horizontally by movement distance
Shift + up and down Arrow keys - move vertically by movement distance
u - move to well A1
i - move to well A12
o - move to well H12
s - save calibration 
h - home
q - exit
""")

instructions = urwid.Text(f"""\
CALIBRATION INSTRUCTIONS
1. Place 96 well plate in slot 1
2. Move laser mount so that bottom of metal ferule is centered and level with top of well A1
3. press s to save calibration
4. Press i to move laser mount over A12
5. Move laser mount so that bottom of metal ferule is centered and level with top of well A12
6. press s to save calibration
7. Press o to move laser mount over H12
8. Move laser mount so that bottom of metal ferule is centered and level with top of well H12
9. press s to save calibration
10. Press u to move laser mount over A1 again
11. press h to home
12. press q to quit
""")

blank = urwid.Divider()
div = urwid.Divider(u'-')
content = [blank, pos_txt, blank, current_saved_offset_txt, blank, movement_distance_txt, blank, message, div, keyboard,
           div, instructions]
listbox = urwid.Pile(content)
fill = urwid.Filler(listbox, "top")
frame = urwid.Frame(urwid.AttrWrap(fill, 'body'), header=header)
palette = [
    ('body', 'black', 'light gray', 'standout'),
    ('reverse', 'light gray', 'black'),
    ('header', 'white', 'dark red', 'bold'),
    ('important', 'dark blue', 'light gray', ('standout', 'underline')),
    ('editfc', 'white', 'dark blue', 'bold'),
    ('editbx', 'light gray', 'dark blue'),
    ('editcp', 'black', 'light gray', 'standout'),
    ('bright', 'dark gray', 'light gray', ('bold', 'standout')),
    ('buttn', 'black', 'dark cyan'),
    ('buttnf', 'white', 'dark blue', 'bold'),
]
update_pos()

# init movement distance text
movement_distance_txt.set_text(("reverse", "Movement distance: {} mm".format(movement_distance)))

loop = urwid.MainLoop(frame, palette, unhandled_input=show_or_exit)
loop.run()
print("Quitting...")
watcher_thread.stop()
