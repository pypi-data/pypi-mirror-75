import asyncio
import json as jsonLib
import os
from typing import Dict

import flask
from flask import request
from flask import jsonify
from flask_socketio import SocketIO, emit
import subprocess
import threading
import time
import opentrons.execute
import logging
from opentrons.protocol_api import ProtocolContext
from opentrons.types import Point

from ondine_laser_control import laser
from ondine_laser_control.laser import Controller

watcher_thread = None


def restart_ot_server():
    subprocess.check_output(
        "systemctl start opentrons-robot-server", shell=True)


def kill_ot_server():
    """ Kills the OpenTrons robot server service, and sets it to restart at exit. """
    subprocess.check_output(
        "systemctl stop opentrons-robot-server", shell=True)


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


def updateOffsetsFile(x: float, y: float, z: float, z_offset_where_100mw_cm_2_in_mm):
    with open(laser.offset_file, 'w') as outfile:
        jsonLib.dump({'x': x, 'y': y, 'z': z, "100mw_calibration": z_offset_where_100mw_cm_2_in_mm}, outfile)


def get_initial_offsets() -> Dict[str, float]:
    initial_offsets = laser.read_offsets_file()
    return initial_offsets


def get_current_position() -> Point:
    return laserController.get_current_pos()


protocol = opentrons.execute.get_protocol_api('2.5')
global plate
global laserController  # type:Controller
loop = asyncio.get_event_loop()


def setProtocol():
    global protocol
    local_protocol = opentrons.execute.get_protocol_api('2.5')  # can't do this because it hangs for some reason
    protocol = local_protocol


def init_calibration():
    kill_ot_server()
    logging.disable(logging.ERROR)
    asyncio.set_event_loop(loop)
    setProtocol()
    global protocol
    # turn on lights
    protocol._hw_manager.hardware.set_lights(rails=True)
    # press button to kill
    set_button_as_kill_switch(protocol)
    print("Homing... ")
    protocol.home()
    global plate
    plate = protocol.load_labware('corning_96_wellplate_360ul_flat', 1)
    global laserController
    laserController = laser.Controller(protocol=protocol, print_debug_messages=False)


def end_calibration():
    global protocol, laserController
    protocol.home()
    protocol = None
    laserController = None
    plate = None
    restart_ot_server()


app = flask.Flask(__name__)
app.config["DEBUG"] = True
socket_io = SocketIO(app, cors_allowed_origins='*', manage_session=False, always_connect=True, ping_timeout=200,
                     cookie=None, engineio_logger=True)

# simulate calls without actually doing anything
SIMULATE = False
if SIMULATE:
    print("\n\n\n\n\n\n\n********* SIMULATING ************\n\n\n\n\n\n\n")


@socket_io.on('connect')
def on_connect():
    print("On Connect")
    return True
    # return {'ok': True}


@socket_io.on('init')
def on_init():
    print("On Init:")
    if not SIMULATE:
        init_calibration()
    print("initialized calibration")
    return {"ok": True, "zAbsMin": laserController.z_abs_min,
            "laser100mwDistance": laserController.z_offset_where_100mw_cm_2_in_mm}


@socket_io.on('moveToPos1')
def handle_move_to_pos_1():
    global laserController
    if not SIMULATE:
        laserController.move_to_well(plate["A1"], speed=100)
        laserController.move_z(plate["A1"].top(5).point.z, speed=100)
    current_position = get_current_position()
    current_well_top = plate["A1"].top().point
    print("Moved to position 1")

    return {
        "currentPosition": {
            "x": current_position.x, "y": current_position.y, "z": current_position.z
        },
        "currentWellTop": {
            "x": current_well_top.x, "y": current_well_top.y, "z": current_well_top.z
        },
        "currentOffset": {
            "x": laserController.x_offset, "y": laserController.y_offset, "z": laserController.z_offset
        }
    }


@socket_io.on('moveToPos2')
def handle_move_to_pos_2():
    global laserController
    laserController.move_to_well(plate["A12"], speed=100)
    laserController.move_z(plate["A12"].top(5).point.z, speed=100)
    current_position = get_current_position()
    current_well_top = plate["A12"].top().point
    print("Moved to position 2")

    return {
        "currentPosition": {
            "x": current_position.x, "y": current_position.y, "z": current_position.z
        },
        "currentWellTop": {
            "x": current_well_top.x, "y": current_well_top.y, "z": current_well_top.z
        },
        "currentOffset": {
            "x": laserController.x_offset, "y": laserController.y_offset, "z": laserController.z_offset
        }
    }


@socket_io.on('moveToPos3')
def handle_move_to_pos_3():
    global laserController
    laserController.move_to_well(plate["H12"], speed=100)
    laserController.move_z(plate["H12"].top(5).point.z, speed=100)
    current_position = get_current_position()
    current_well_top = plate["H12"].top().point
    print("Moved to position 3")

    return {
        "currentPosition": {
            "x": current_position.x, "y": current_position.y, "z": current_position.z
        },
        "currentWellTop": {
            "x": current_well_top.x, "y": current_well_top.y, "z": current_well_top.z
        },
        "currentOffset": {
            "x": laserController.x_offset, "y": laserController.y_offset, "z": laserController.z_offset
        }
    }


@socket_io.on('move')
def handle_move(json):
    global laserController
    print("Move incoming")
    print(json)
    x: float = json["x"]
    y: float = json["y"]
    z: float = json["z"]
    laserController._move(position=Point(x=x, y=y, z=z), speed=10)

    current_position = get_current_position()
    return {"ok": True, "currentPosition": {
        "x": current_position.x, "y": current_position.y, "z": current_position.z
    }}


@socket_io.on('updateLaserOffsets')
def handle_update_offsets(json):
    global laserController
    laserController.x_offset = json["offset"]["x"]
    laserController.y_offset = json["offset"]["y"]
    laserController.z_offset = json["offset"]["z"]
    print(
        f"Updated laser offsets to x:{laserController.x_offset} y:{laserController.y_offset} z:{laserController.z_offset}")
    return True


@socket_io.on('saveCalibration')
def handle_save(json):
    global laserController
    laserController.x_offset = json["offset"]["x"]
    laserController.y_offset = json["offset"]["y"]
    laserController.z_offset = json["offset"]["z"]

    updateOffsetsFile(x=laserController.x_offset, y=laserController.y_offset, z=laserController.z_offset,
                      z_offset_where_100mw_cm_2_in_mm=laserController.z_offset_where_100mw_cm_2_in_mm)
    print(
        f"saved laser offsets as x:{laserController.x_offset} y:{laserController.y_offset} z:{laserController.z_offset}"
    )
    return True


@socket_io.on('saveLaserDistCalibration')
def handle_save(json):
    global laserController
    laserController.z_offset_where_100mw_cm_2_in_mm = json["newCalibration"]

    updateOffsetsFile(x=laserController.x_offset, y=laserController.y_offset, z=laserController.z_offset,
                      z_offset_where_100mw_cm_2_in_mm=laserController.z_offset_where_100mw_cm_2_in_mm)
    print(
        f"saved laser 100mw calibration as {laserController.z_offset_where_100mw_cm_2_in_mm}"
    )
    return True


@socket_io.on('end')
def end_cal():
    end_calibration()
    print("Ended Calibration")
    return True


@socket_io.on('disconnect')
def on_disconnect():
    print('Client disconnected')


socket_io.run(app, host="0.0.0.0")
