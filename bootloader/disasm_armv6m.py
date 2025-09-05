#!/usr/bin/env python3

import sys
from armv6m import dec16, dec32, WideInstructionError


def parse_line(line: str) -> tuple[str, int, str | None]:

    # Code line format:
    # <addr>: <code> [;<comment>]

    try:
        i = line.index(":")
        addr = line[:i].strip()
    except ValueError:
        raise

    try:
        j = line.index(";", i)
        code = line[i + 1 : j].strip()
        comment = line[j + 1 :].strip()
    except ValueError:
        code = line[i + 1 :].strip()
        comment = None

    if "" == addr or "" == code:
        raise ValueError()

    try:
        code = int(code, base=16)
    except ValueError:
        raise

    return (addr, code, comment)


def disasm_lines(lines: list[str]):

    i = 0
    while i < len(lines):
        line = lines[i]
        try:
            addr, code, comment = parse_line(line)
        except:
            print(line + " \t;;; [!!!] Invalid code line")
            return

        # if comment is None:
        #     comment = ""

        try:
            asm = dec16(code)
            print(f"{addr}: {code:04x} \t; {asm}")
            i += 1
            continue
        except WideInstructionError:
            if i == len(lines) - 1:
                print(f"{addr}: {code:04x}" + " \t; [...] Wide (32 bit) instruction")
                return

            # Process it below..
            pass
        except NotImplementedError:
            print(f"{addr}: {code:04x}" + " \t; [!!!] To be implemented..")
            # return
            raise
        except:
            print(f"{addr}: {code:04x}" + " \t; [!!!] Invalid instruction")
            return

        # ----------------
        # 32-bit instruction

        line1 = lines[i + 1]
        try:
            addr1, code1, comment1 = parse_line(line1)
        except:
            # print(line)
            print(f"{addr}: {code:04x}" + " \t; [...]")
            print(line1 + " \t;;; [!!!] Invalid code line")
            return

        try:
            asm = dec32(code, code1)
            print(f"{addr}: {code:04x}" + " \t; [...]")
            print(f"{addr1}: {code1:04x} \t; {asm}")
            i += 2
            continue
        except NotImplementedError:
            print(f"{addr}: {code:04x}" + " \t; [...]")
            print(f"{addr1}: {code1:04x}" + " \t; [!!!] To be implemented..")
            # return
            raise
        except:
            print(f"{addr}: {code:04x}" + " \t; [...]")
            print(f"{addr1}: {code1:04x}" + " \t; [!!!] Invalid instruction")
            return


def main():

    print(sys.argv[0] + ": Arm v6-M disassemble tool")

    while True:
        print("")
        print(
            "Input one or more code lines + blank line to disassemble. Press Ctrl-C to quit"
        )

        lines = []

        # The first line
        line = input("> ")
        # Discard blank lines
        while True:
            line = line.strip()
            if "" != line:
                lines.append(line)
                break
            line = input()

        # More lines
        while True:
            line = input()
            line = line.strip()
            if "" == line:
                break
            lines.append(line)

        print("--")

        if len(lines) > 0:
            disasm_lines(lines)


if __name__ == "__main__":
    main()
