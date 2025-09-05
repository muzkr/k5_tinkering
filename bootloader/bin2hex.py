#!/usr/bin/env python3

import argparse
import sys, os, io


def bin2hex_hw(hw, /, addr):

    addr_str = f"{addr:04x}"
    if 0 != len(addr_str) % 2:
        addr_str = "0" + addr_str

    print(f"{addr_str}: {hw:04x}")


def bin2hex(input: io.BufferedReader, /, base, size):

    assert base >= 0 and 0 == (base % 2)
    assert size >= 0 and 0 == (size % 2)

    addr = base
    size_done = 0
    buf = bytearray(2)

    while size_done < size:
        if 2 != input.readinto(buf):
            raise EOFError("EOF")
        hw = (buf[1] << 8) | buf[0]
        bin2hex_hw(hw, addr=addr)
        addr += 2
        size_done += 2


def main():

    # Usage:
    # bin2hex.py [--offset <offset>] [--size <size>] [--base <base>] <file>
    ap = argparse.ArgumentParser(
        description="Convert binary file to hex representation"
    )

    int1 = lambda s: int(s, 0)

    ap.add_argument(
        "--offset",
        default=0,
        type=int1,
        help="offset from beginning of the file, in bytes. Default 0",
    )
    ap.add_argument(
        "--base",
        default=0,
        type=int1,
        help="base address. Should be multiple of 2. Default 0. -1 means the same as offset",
    )
    ap.add_argument(
        "--size",
        default=-1,
        type=int1,
        help="size of data to convert, in bytes. Should be multiple of 2. -1 (default) means til EOF",
    )
    ap.add_argument("file", help="input file")

    args = ap.parse_args()
    offset: int = args.offset
    base: int = args.base
    size: int = args.size
    file: str = args.file

    def print_int1(name, n):
        if n <= 0:
            print(f"{name} = {n}")
        else:
            print(f"{name} = 0x{n:08x} ({n})")

    # --------------------------
    #  Validate offset

    print_int1("offset", offset)

    if offset < 0:
        print("Invalid offset: negative")
        return

    # --------------------------
    #  base

    print_int1("base", base)

    if -1 == base:
        print(f"base = -1. Use offset instead: 0x{offset:08x}")
        base = offset
    elif base < 0:
        print("Invalid base: negative")
        return

    if 0 != base % 2:
        print("Invalid base: not multiple of 2")
        return

    # -------------------------
    #   size

    print_int1("size", size)

    if -1 == size:
        pass
    elif size < 0:
        print("Invalid size: negative")
        return
    elif 0 != size % 2:
        print("Invalid size: not a multiple of 2")

    # -------------------------
    #  file

    if os.path.exists(file) and os.path.isfile(file):
        pass
    else:
        print("File not found: " + file)
        return

    # ----------------------
    #  file size

    file_size = os.path.getsize(file)
    print(f"file size = {file_size}")

    if offset > file_size:
        print(f"Invalid offset: > file size ({offset} > {file_size})")
        return

    if -1 == size:
        print("size = -1. Use file size (excluding offset) instead")
        size = file_size - offset
        size -= size % 2
        print_int1("size", size)
    elif offset + size > file_size:
        print(
            "Invalid size: > file size (excluding offset) ({} - {} = {})".format(
                file_size, offset, file_size - offset
            )
        )
        return

    if base + size > 0x100000000:
        print(
            "Invalid base: base + size (0x{:08x} + {1} = 0x{:x}) out of 32-bit address space".format(
                base, size, base + size
            )
        )
        return

    # -------------------

    input: io.BufferedReader = open(file, mode="rb")
    assert input.seekable()
    try:
        if offset > 0:
            input.seek(offset)
        bin2hex(input, base=base, size=size)
    finally:
        input.close()


if __name__ == "__main__":
    main()
