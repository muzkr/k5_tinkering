#!/usr/bin/env python3

import os
import sys
import io

EXCEPTIONS = (
    "Reset",
    "NMI",
    "HardFault",
    "",
    "SVCall",
    "",
    "PendSV",
    "SysTick",
)

IRQS = (
    "WWDT",
    "IWDT",
    "RTC",
    "DMA",
    "SARADC",
    "TIMER_BASE0",
    "TIMER_BASE1",
    "TIMER_PLUS0",
    "TIMER_PLUS1",
    "PWM_BASE0",
    "PWM_BASE1",
    "PWM_PLUS0",
    "PWM_PLUS1",
    "UART0",
    "UART1",
    "UART2",
    "SPI0",
    "SPI1",
    "IIC0",
    "IIC1",
    "CMP",
    "TIMER_BASE2",
    "GPIOA5",
    "GPIOA6",
    "GPIOA7",
    "GPIOB0",
    "GPIOB1",
    "GPIOC0",
    "GPIOC1",
    "GPIOA",
    "GPIOB",
    "GPIOC",
)


def read_word(input: io.BufferedReader) -> int:

    buf = bytearray(4)
    if 4 != input.readinto(buf):
        raise IOError()

    return (buf[3] << 24) | (buf[2] << 16) | (buf[1] << 8) | (buf[0])


def dec_vec(input: io.BufferedReader):

    sp = read_word(input)
    print("Initial SP: \t{:08x}".format(sp))

    for i, name in enumerate(EXCEPTIONS + IRQS):
        if not name:
            continue
        if i < len(EXCEPTIONS):
            name = name + "_Handler"
        else:
            name = "IRQ_" + str(i - len(EXCEPTIONS)) + "_" + name + "_Handler"

        vec = read_word(input)
        if 0 == vec:
            print(name + ": \t<INVALID:0>")
        elif 0 == vec % 2:
            print("{}: \t<INVALID:{:08x}>".format(name, vec))
        else:
            print("{}: \t{:08x}".format(name, vec - 1))


def main():

    if 2 == len(sys.argv):
        filename = sys.argv[1]
        offset = 0
    elif 3 == len(sys.argv):
        filename = sys.argv[1]
        offset = int(sys.argv[2])
    else:
        print("Usage: python3 " + sys.argv[0] + " <file> [<offset>]")
        return

    if os.path.exists(filename) and os.path.isfile(filename):
        pass
    else:
        print("File not found: " + filename)
        return

    if offset < 0:
        print("Invalid offset: " + str(offset))
        return
    elif offset >= os.path.getsize(filename):
        print(
            "Invalid offset: "
            + str(offset)
            + ": >= file size ("
            + str(os.path.getsize(filename))
            + ")"
        )
        return

    input: io.BufferedReader = io.open(filename, mode="rb")
    # print("seekable: " + str(input.seekable()))
    assert input.seekable()
    try:
        if offset != input.seek(offset):
            raise IOError("Seek fail")
        dec_vec(input)
    finally:
        input.close()


if __name__ == "__main__":
    main()
