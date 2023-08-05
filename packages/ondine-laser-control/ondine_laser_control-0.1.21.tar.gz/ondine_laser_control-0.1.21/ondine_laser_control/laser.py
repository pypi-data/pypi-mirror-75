import json
import typing
import time
from typing import Any, Coroutine
from opentrons import hardware_control
from opentrons.protocol_api import ProtocolContext, InstrumentContext
from opentrons.protocol_api.labware import Well
from opentrons.types import Point, Mount
from pydantic import BaseModel
import serial

offset_file = '/data/laser_calibration.json'

arduino = serial.Serial(
    port='/dev/ttyACM0',
    baudrate=9600,
    timeout=30
)


def make_sure_port_is_started():
    arduino.write(b'LLLLLLLL')


def turn_on_laser():
    arduino.write(b'H')


def turn_off_laser():
    arduino.write(b'L')


def read_offsets_file():
    try:
        with open(offset_file) as json_file:
            offsets = json.load(json_file)
    except FileNotFoundError:
        print("offsets file not found at " + offset_file)
        offsets = {'x': 11.3, 'y': 4.3, 'z': 0.38, "100mw_calibration": 13.88}
    return offsets


initial_offsets = read_offsets_file()


class Controller(BaseModel):

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        make_sure_port_is_started()

    print_debug_messages = True
    x_offset: float = initial_offsets["x"]
    y_offset: float = initial_offsets["y"]
    z_offset: float = initial_offsets["z"]
    mount: Mount = Mount.LEFT
    protocol: ProtocolContext
    z_abs_min = 49.5  # where the end of ferule is against base plate
    z_min = 60  # generally should have to go lower than this
    z_max = 241.0
    z_min_buffer = 20.0
    z_offset_where_100mw_cm_2_in_mm = initial_offsets["100mw_calibration"]

    class Config:
        arbitrary_types_allowed = True

    @property
    def _hardware(self) -> hardware_control.api.API:
        return self.protocol._hw_manager.hardware

    def get_current_pos(self, adjusted=False) -> Point:
        # the docs says it return a coroutine but it actually returns a point
        pos: Coroutine[Any, Any, Point] = self._hardware.gantry_position(self.mount)
        pt: Point = typing.cast(Point, pos)
        if adjusted:
            pt = Point(pt.x - self.x_offset, pt.y - self.y_offset, pt.z - self.z_offset - self.z_abs_min)
        return pt

    def _move_unadjusted_z(self, position: Point, speed: float):
        """
        move with a z that is not true for the laser, ie if the plate is at 32 to match that with the laser you would need to be at 32+z_abs_min
        """

        if self.protocol.is_simulating():
            return
        if position.z < self.z_min:
            if self.print_debug_messages:
                print(f"z below z_min:{self.z_min}, reset to {self.z_min + self.z_min_buffer}")
            position = Point(z=self.z_min + self.z_min_buffer, x=position.x, y=position.y)
        elif position.z > self.z_max:
            if self.print_debug_messages:
                print(f"z above z_max:{self.z_max}, reset to {self.z_max}")
            position = Point(z=self.z_max, x=position.x, y=position.y)
        self._hardware.move_to(self.mount, position, speed=speed)

    def _move_z_dangerous(self, z_position: float, speed: float = 20):
        cur_point = self.get_current_pos()
        new_point = Point(cur_point.x, cur_point.y, z_position)
        if new_point.z < self.z_min:
            if self.print_debug_messages:
                print(f"z below z_abs_min:{self.z_min}, reset to {self.z_abs_min + self.z_min_buffer}")
            new_point = Point(z=self.z_abs_min + self.z_min_buffer, x=new_point.x, y=new_point.y)
        self._hardware.move_to(self.mount, new_point, speed=speed)

    def move_z(self, z_position: float, speed: float = 20):
        cur_point = self.get_current_pos()
        new_point = Point(cur_point.x, cur_point.y, z_position + self.z_abs_min + self.z_offset)
        self._move_unadjusted_z(new_point, speed=speed)

    def move_to_transit_z(self):
        self.move_z(self.z_max - self.z_abs_min)

    def move_close_to_home_quick(self):
        self.move_z(self.z_max, speed=400)

    def home_z(self):
        self.move_close_to_home_quick()
        self._hardware.home_z(self.mount)

    def move_x(self, x_position: float, speed: float = 20):
        cur_point = self.get_current_pos()
        new_point = Point(x_position + self.x_offset, cur_point.y, cur_point.z)
        self._move(new_point, speed=speed)

    def move_y(self, y_position: float, speed: float = 20):
        cur_point = self.get_current_pos()
        new_point = Point(cur_point.x, y_position + self.y_offset, cur_point.z)
        self._move(new_point, speed=speed)

    def _move(self, position: Point, speed: float = None):
        if self.protocol.is_simulating():
            return
        self._hardware.move_to(self.mount, position, speed=speed)

    def turn_on_laser(self, seconds_to_off: int = None):
        self.protocol.comment(f"Turning on Laser for {seconds_to_off} seconds")
        if not self.protocol.is_simulating:
            turn_on_laser()
            if seconds_to_off is not None:
                time.sleep(seconds_to_off)
                turn_off_laser()

    def move_to_well(self, well: Well, height_of_liquid: float = 0, speed: float = 20):
        self.move_to_transit_z()
        p = well.top().point
        self.protocol.comment(f"Moving Laser to {Well.display_name}")
        adjusted_point = Point(x=p.x + self.x_offset, y=p.y + self.y_offset, z=self.get_current_pos().z)

        self._move(adjusted_point, speed=speed)

        p_bottom_z = well.bottom().point.z

        self.move_z(p.z + self.z_offset_where_100mw_cm_2_in_mm - p_bottom_z + height_of_liquid, speed=speed)

    def _print_pos(self):
        if self.print_debug_messages:
            pos = self.get_current_pos()
            print(f"x:{pos.x} y:{pos.y} z:{pos.z}")

    def move_relx(self, amt: float):
        pos = self.get_current_pos(adjusted=True)
        self.move_x(pos.x + amt)
        self._print_pos()

    def move_rely(self, amt: float):
        pos = self.get_current_pos(adjusted=True)
        self.move_y(pos.y + amt)
        self._print_pos()

    def move_relz(self, amt: float):
        pos = self.get_current_pos(adjusted=True)
        self.move_z(pos.z + amt)
        self._print_pos()
