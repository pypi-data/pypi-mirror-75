from opentrons import protocol_api
from ondine_laser_control import laser

metadata = {
    'protocolName': 'Laser Test Protocol',
    'author': 'Caden <ckeese@ondinebio.com>',
    'description': 'Test Protocol for laser control',
    'apiLevel': '2.5'
}


def run(protocol: protocol_api.ProtocolContext):
    plate = protocol.load_labware('corning_96_wellplate_360ul_flat', 1)
    tiprack_1 = protocol.load_labware('opentrons_96_tiprack_300ul', 2)
    # reservior = protocol.load_labware("usascientific_12_reservoir_22ml", 7)

    p300 = protocol.load_instrument('p300_single_gen2', 'right', tip_racks=[tiprack_1])

    laserController = laser.Controller(protocol=protocol)

    p300.pick_up_tip()

    p300.aspirate(100, plate['A1'])

    laserController.move_to_well(well=plate['A3'])

    laserController.turn_on_laser(seconds_to_off=5)

    p300.dispense(100, plate['A3'])

    p300.drop_tip()
    # laser.turn_on_laser(seconds_to_off=5)
