"""Read the tutorial endpoint through its Linux PCI resource mapping.

Run only against the lab endpoint. This does not access system RAM.
Default mode is read-only; --test-scratch enables the documented scratch test.
"""
import argparse
import mmap
import os
from pathlib import Path
import re
import struct
import time


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('bdf', help='Exact PCI address, e.g. 0000:03:00.0')
    parser.add_argument('--test-scratch', action='store_true')
    args = parser.parse_args()
    if not re.fullmatch(r'[0-9a-fA-F]{4}:[0-9a-fA-F]{2}:[0-1][0-9a-fA-F]\.[0-7]', args.bdf):
        parser.error('Use a complete domain:bus:device.function address')
    device = Path('/sys/bus/pci/devices') / args.bdf
    if (device / 'driver').exists():
        raise SystemExit('A driver owns this device. Use its supported interface.')
    flags = (os.O_RDWR if args.test_scratch else os.O_RDONLY) | os.O_SYNC
    fd = os.open(device / 'resource0', flags)
    access = mmap.ACCESS_WRITE if args.test_scratch else mmap.ACCESS_READ
    try:
        with mmap.mmap(fd, 4096, access=access) as bar:
            read = lambda off: struct.unpack_from('<I', bar, off)[0]
            magic, build = read(0), read(4)
            if (magic, build) != (0x47554944, 0x00020001):
                raise SystemExit('Signature/build mismatch; no writes performed')
            before = read(12)
            time.sleep(0.01)
            after = read(12)
            print(f'MAGIC={magic:08x} BUILD={build:08x}')
            print(f'COUNTER {before:08x} -> {after:08x}')
            if before == after:
                raise SystemExit('Counter did not change during the sample window')
            if args.test_scratch:
                original = read(8)
                try:
                    for value in (0x11223344, 0xa5a55a5a, 0):
                        struct.pack_into('<I', bar, 8, value)
                        if read(8) != value:
                            raise SystemExit('Scratch readback mismatch')
                finally:
                    struct.pack_into('<I', bar, 8, original)
                    if read(8) != original:
                        raise SystemExit('Could not restore original scratch value')
                print('SCRATCH_PASS')
            print('GUIDE_BAR_HOST_PASS')
    finally:
        os.close(fd)


if __name__ == '__main__':
    main()
