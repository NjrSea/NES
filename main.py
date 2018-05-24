import argparse

from cpu import CPU
from nes_test import NesTestLog
from ram import RAM
from ppu import PPU
from rom import ROM


def main():
    # set up command line argument parser
    parser = argparse.ArgumentParser(description="NES Emulator.")
    parser.add_argument('rom_path',
                        metavar='R',
                        type=str,
                        help='path to nes rom')
    parser.add_argument('--test')

    args = parser.parse_args()

    # TODO: validate rom path is correct
    print(args.rom_path)

    # load rom
    with open(args.rom_path, 'rb') as file:
        rom_bytes = file.read()

    # create ram
    ram = RAM()

    # create ppu
    ppu = PPU()

    rom = ROM(rom_bytes)

    # create cpu
    cpu: CPU = CPU(ram, ppu)
    cpu.start_up()
    cpu.load_rom(rom)

    # check if running test rom
    if args.test:
        # load in the test log
        with open('test_log.log', 'r') as nes_test_file:
            nes_test_log = NesTestLog(nes_test_file.readlines())
        while True:
            cpu.identify()
            nes_test_log.compare(cpu)
            cpu.execute()
    else:
        while True:
            cpu.identify()
            cpu.execute()


if __name__ == '__main__':
    main()

