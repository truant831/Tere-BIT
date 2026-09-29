#!/usr/bin/env python3
from pathlib import Path
import sys

FLASH_DATA_OFFSET = 0x100000
DISK_SIZE = 0x100000
SECTOR_SIZE = 512
SECTORS = DISK_SIZE // SECTOR_SIZE

DELTA = 0x9E3779B1
SECTOR_STEP = 0x38C9CDA0
SEED0 = 0x9E37A9EA
BLOCK_STEP = 0x41C64E6D

def keystream_sector(lba: int) -> bytes:
    state = (SEED0 + lba * SECTOR_STEP) & 0xFFFFFFFF
    out = bytearray()
    for _ in range(32):
        for k in range(-1, 15):
            v = (state + k * DELTA) & 0xFFFFFFFF
            out.append((v >> 24) & 0xFF)
        state = (state + BLOCK_STEP) & 0xFFFFFFFF
    return bytes(out)

def decrypt_disk(full_flash: bytes) -> bytes:
    if len(full_flash) < FLASH_DATA_OFFSET + DISK_SIZE:
        raise ValueError("Input must contain the full 2 MiB RP2040 flash dump")

    raw = full_flash[FLASH_DATA_OFFSET:FLASH_DATA_OFFSET + DISK_SIZE]
    out = bytearray(DISK_SIZE)

    for lba in range(SECTORS):
        start = lba * SECTOR_SIZE
        sec = raw[start:start + SECTOR_SIZE]
        ks = keystream_sector(lba)
        out[start:start + SECTOR_SIZE] = bytes(a ^ b for a, b in zip(sec, ks))

    return bytes(out)

def main():
    if len(sys.argv) not in (2, 3):
        print(f"Usage: {sys.argv[0]} backup.bin [decrypted_flash_disk.img]")
        raise SystemExit(2)

    src = Path(sys.argv[1])
    dst = Path(sys.argv[2]) if len(sys.argv) == 3 else Path("decrypted_flash_disk.img")

    disk = decrypt_disk(src.read_bytes())
    dst.write_bytes(disk)

    print(f"Wrote {len(disk)} bytes to {dst}")
    print(
        f"Boot signature: {disk[510:512].hex()}  "
        f"OEM: {disk[3:11].decode('ascii', 'replace')}"
    )

if __name__ == "__main__":
    main()
