# ---


MNEM_UPPER = False
REG_UPPER = False
HEX_UPPER = False


class WideInstructionError(ValueError):
    """Wide (32 bit) instruction"""


def dec16(code: int) -> str:

    # bits [15:11]
    match 0b1_1111 & (code >> 11):
        case 0b11101 | 0b11110 | 0b11111:
            raise WideInstructionError()

    # bits [15:10]
    opcode = 0b11_1111 & (code >> 10)

    if 0 == opcode >> 4:
        # 00xxxx
        return _dec16_Shift_immediate_etc(code)
    elif 0b010000 == opcode:
        # 010000
        return _dec16_Data_processing(code)
    elif 0b010001 == opcode:
        # 010001
        return _dec16_Special_data_instructions_etc(code)
    elif 0b01001 == opcode >> 1:
        # 01001x
        return _dec_LDR_literal(code)
    elif (0b0101 == opcode >> 2) or (0b011 == opcode >> 3) or (0b100 == opcode >> 3):
        # 0101xx, 011xxx, 100xxx
        return _dec16_Load_store_single_data_item(code)
    elif 0b10100 == opcode >> 1:
        # 10100x
        return _dec_ADR(code)
    elif 0b10101 == opcode >> 1:
        # 10101x
        return _dec16_ADD_SP_plus_immediate(code)
    elif 0b1011 == opcode >> 2:
        # 1011xx
        return _dec16_Miscellaneous(code)
    elif 0b11000 == opcode >> 1:
        # 11000x
        return _dec_STM(code)
    elif 0b11001 == opcode >> 1:
        # 11001x
        return _dec_LDM(code)
    elif 0b1101 == opcode >> 2:
        # 1101xx
        return _dec16_Conditional_branch_etc(code)
    elif 0b11100 == opcode >> 1:
        # 11100x
        return _dec_B_T2(code)

    raise ValueError()


def _dec16_Shift_immediate_etc(code: int) -> str:

    # bits [13:9]
    opcode = 0b1_1111 & (code >> 9)

    if 0 == opcode >> 2:
        # 000xx
        return _dec_LSL_immediate_etc(code, "LSLS")
    elif 0b001 == opcode >> 2:
        # 001xx
        return _dec_LSL_immediate_etc(code, "LSRS")
    elif 0b010 == opcode >> 2:
        # 010xx
        return _dec_LSL_immediate_etc(code, "ASRS")
    elif 0b01100 == opcode:
        # 01100
        return _dec_ADD_register_etc(code, "ADDS")
    elif 0b01101 == opcode:
        # 01101
        return _dec_ADD_register_etc(code, "SUBS")
    elif 0b01110 == opcode:
        # 01110
        return _dec_ADD_immediate_etc(code, "ADDS")
    elif 0b01111 == opcode:
        # 01111
        return _dec_ADD_immediate_etc(code, "SUBS")
    elif 0b100 == opcode >> 2:
        # 100xx
        return _dec_MOV_immediate_etc(code, "MOVS")
    elif 0b101 == opcode >> 2:
        # 101xx
        return _dec_MOV_immediate_etc(code, "CMP")
    elif 0b110 == opcode >> 2:
        # 110xx
        return _dec_MOV_immediate_etc(code, "ADDS")
    elif 0b111 == opcode >> 2:
        # 111xx
        return _dec_MOV_immediate_etc(code, "SUBS")

    raise ValueError()


def _dec16_Data_processing(code: int) -> str:

    # bits [9:6]
    opcode = 0b1111 & (code >> 6)

    match opcode:
        case 0:
            return _dec_AND_register_etc(code, "ANDS")
        case 0b0001:
            return _dec_AND_register_etc(code, "EORS")
        case 0b0010:
            return _dec_LSL_register_etc(code, "LSLS")
        case 0b0011:
            return _dec_LSL_register_etc(code, "LSRS")
        case 0b0100:
            return _dec_LSL_register_etc(code, "ASRS")
        case 0b0101:
            return _dec_AND_register_etc(code, "ADCS")
        case 0b0110:
            return _dec_AND_register_etc(code, "SBCS")
        case 0b0111:
            return _dec_LSL_register_etc(code, "RORS")
        case 0b1000:
            return _dec_AND_register_etc(code, "TST")
        case 0b1001:
            return _dec_RSB_immediate(code)
        case 0b1010:
            return _dec_AND_register_etc(code, "CMP")
        case 0b1011:
            return _dec_AND_register_etc(code, "CMN")
        case 0b1100:
            return _dec_AND_register_etc(code, "ORRS")
        case 0b1101:
            return _dec_MUL(code)
        case 0b1110:
            return _dec_AND_register_etc(code, "BICS")
        case 0b1111:
            return _dec_AND_register_etc(code, "MVNS")

    raise ValueError()


def _dec16_Special_data_instructions_etc(code: int) -> str:

    # bits [9:6]
    opcode = 0b1111 & (code >> 6)

    if 0 == opcode >> 2:
        # 00xx
        return _dec_ADD_register_T2_etc(code, "ADD")
    elif 0b0100 == opcode:
        # 0100 UNPREDICTABLE
        raise ValueError()
    elif 0b0101 == opcode or 0b011 == opcode >> 1:
        # 0101,011x
        return _dec_ADD_register_T2_etc(code, "CMP")
    elif 0b10 == opcode >> 2:
        # 10xx
        return _dec_ADD_register_T2_etc(code, "MOV")
    elif 0b110 == opcode >> 1:
        # 110x
        return _dec_BX_etc(code, "BX")
    elif 0b111 == opcode >> 1:
        # 111x
        return _dec_BX_etc(code, "BLX")

    raise ValueError()


def _dec16_Load_store_single_data_item(code: int) -> str:

    # bits [15:12]
    opa = 0b1111 & (code >> 12)
    # bits [11:9]
    opb = 0b111 & (code >> 9)

    if 0b0101 == opa and 0 == opb:
        # 0101, 000,
        return _dec_STR_register_etc(code, "STR")
    if 0b0101 == opa and 0b001 == opb:
        # 0101 001
        return _dec_STR_register_etc(code, "STRH")
    if 0b0101 == opa and 0b010 == opb:
        # 0101 010
        return _dec_STR_register_etc(code, "STRB")
    if 0b0101 == opa and 0b011 == opb:
        # 0101 011
        return _dec_STR_register_etc(code, "LDRSB")
    if 0b0101 == opa and 0b100 == opb:
        # 0101 100
        return _dec_STR_register_etc(code, "LDR")
    if 0b0101 == opa and 0b101 == opb:
        # 0101 101
        return _dec_STR_register_etc(code, "LDRH")
    if 0b0101 == opa and 0b110 == opb:
        # 0101 110
        return _dec_STR_register_etc(code, "LDRB")
    if 0b0101 == opa and 0b111 == opb:
        # 0101 111
        return _dec_STR_register_etc(code, "LDRSH")
    if 0b0110 == opa and 0 == opb >> 2:
        # 0110 0xx
        return _dec_STR_immediate_etc(code, "STR")
    if 0b0110 == opa and 1 == opb >> 2:
        # 0110 1xx
        return _dec_STR_immediate_etc(code, "LDR")
    if 0b0111 == opa and 0 == opb >> 2:
        # 0111 0xx
        return _dec_STRB_immediate_etc(code, "STRB")
    if 0b0111 == opa and 1 == opb >> 2:
        # 0111 1xx
        return _dec_STRB_immediate_etc(code, "LDRB")
    if 0b1000 == opa and 0 == opb >> 2:
        # 1000 0xx
        return _dec_STRH_immediate_etc(code, "STRH")
    if 0b1000 == opa and 1 == opb >> 2:
        # 1000 1xx
        return _dec_STRH_immediate_etc(code, "LDRH")
    if 0b1001 == opa and 0 == opb >> 2:
        # 1001 0xx
        return _dec_STR_immediate_T2_etc(code, "STR")
    if 0b1001 == opa and 1 == opb >> 2:
        # 1001 1xx
        return _dec_STR_immediate_T2_etc(code, "LDR")

    raise ValueError()


def _dec16_ADD_SP_plus_immediate(code: int) -> str:
    # TODO:
    raise NotImplementedError()


def _dec16_Miscellaneous(code: int) -> str:

    # bits [11:5]
    opcode = 0b111_1111 & (code >> 5)

    if 0 == opcode >> 2:
        # 00000xx
        raise NotImplementedError()
    if 1 == opcode >> 2:
        # 00001xx
        raise NotImplementedError()
    if 0b001000 == opcode >> 1:
        # 001000x
        return _dec_SXTH_etc(code, "SXTH")
    if 0b001001 == opcode >> 1:
        # 001001x
        return _dec_SXTH_etc(code, "SXTB")
    if 0b001010 == opcode >> 1:
        # 001010x
        return _dec_SXTH_etc(code, "UXTH")
    if 0b001011 == opcode >> 1:
        # 001011x
        return _dec_SXTH_etc(code, "UXTB")
    if 0b010 == opcode >> 4:
        # 010xxxx
        return _dec_PUSH(code)
    if 0b0110011 == opcode:
        # 0110011
        raise NotImplementedError()
    if 0b101000 == opcode >> 1:
        # 101000x
        raise NotImplementedError()
    if 0b101001 == opcode >> 1:
        # 101001x
        raise NotImplementedError()
    if 0b101011 == opcode >> 1:
        # 101011x
        raise NotImplementedError()
    if 0b110 == opcode >> 4:
        # 110xxxx
        return _dec_POP(code)
    if 0b1110 == opcode >> 3:
        # 1110xxx
        raise NotImplementedError()
    if 0b1111 == opcode >> 3:
        # 1111xxx
        return _dec16_Hint_instructions(code)

    raise ValueError()


def _dec16_Conditional_branch_etc(code: int) -> str:

    # bits [11:8]
    opcode = 0b1111 & (code >> 8)

    if 0b111 != opcode >> 1:
        return _dec_B(code)

    if 0b1110 == opcode:
        return _dec_UDF_etc(code, "UDF")
    elif 0b1111 == opcode:
        return _dec_UDF_etc(code, "SVC")


def _dec16_Hint_instructions(code: int) -> str:

    # bits [7:4]
    opa = 0b1111 & (code >> 4)
    # bits [3:0]
    opb = 0b1111 & code

    if 0 == opa and 0 == opb:
        return _mnem_case("NOP")
    if 0b0001 == opa and 0 == opb:
        return _mnem_case("YIELD")
    if 0b0010 == opa and 0 == opb:
        return _mnem_case("WFE")
    if 0b0011 == opa and 0 == opb:
        return _mnem_case("WFI")
    if 0b0100 == opa and 0 == opb:
        return _mnem_case("SEV")

    # UNDEFINED
    raise ValueError()


def dec32(code1: int, code2: int) -> str:

    # bits [15:11] = 11110
    if 0b11110 != 0b1_1111 & (code1 >> 11):
        raise ValueError()

    # bits [15] = 1
    if 1 != 1 & (code2 >> 15):
        raise ValueError()

    # ---------------
    #  Branch and miscellaneous control

    # bits [10:4]
    op1 = 0b111_1111 & (code1 >> 4)
    # bits [14:12]
    op2 = 0b111 & (code2 >> 12)

    if 0 == (op2 & ~0b010) and 0b011100 == (op1 >> 1):
        # 0x0 011100x
        return _dec32_MSR_register(code1, code2)
    elif 0 == (op2 & ~0b010) and 0b0111011 == op1:
        # 0x0 0111011, Miscellaneous control instructions

        # bits [7:4]
        match 0b1111 & (code2 >> 4):
            case 0b0100:
                # 0100
                return _dec32_DSB(code1, code2)
            case 0b0101:
                # 0101
                return _dec32_DMB(code1, code2)
            case 0b0110:
                # 0110
                return _dec32_ISB(code1, code2)

        raise ValueError()

    elif 0 == (op2 & ~0b010) and 0b011111 == (op1 >> 1):
        # 0x0 011111x
        return _dec32_MRS(code1, code2)
    elif 0b010 == op2 and 0b1111111 == op1:
        # 010 1111111
        return _dec32_UDF(code1, code2)
    elif 0b101 == (op2 & ~0b010):
        # 1x1
        return _dec_BL(code1, code2)

    raise ValueError()


def _dec32_MSR_register(code1: int, code2: int) -> str:
    # TODO
    raise NotImplementedError()


def _dec32_DSB(code1: int, code2: int) -> str:
    # TODO
    raise NotImplementedError()


def _dec32_DMB(code1: int, code2: int) -> str:
    # TODO
    raise NotImplementedError()


def _dec32_ISB(code1: int, code2: int) -> str:
    # TODO
    raise NotImplementedError()


def _dec32_MRS(code1: int, code2: int) -> str:
    # TODO
    raise NotImplementedError()


def _dec32_UDF(code1: int, code2: int) -> str:
    # TODO
    raise NotImplementedError()


def _mnem_case(mnem: str) -> str:
    if MNEM_UPPER:
        return mnem.upper()
    else:
        return mnem.lower()


def _reg_case(n: int) -> str:
    if REG_UPPER:
        return _reg_name(n)
    else:
        return _reg_name(n).lower()


def _hex_case(n: int) -> str:
    return _format_hex(n, upper=HEX_UPPER)


def _format_hex(n: int, /, upper=True) -> str:

    neg = False
    if n < 0:
        neg = True
        n = -n

    if upper:
        s = f"0x{n:X}"
    else:
        s = f"0x{n:x}"

    if neg:
        return "-" + s
    else:
        return s


def _cond_ext(n: int) -> str:

    match n:
        case 0:
            ext = "EQ"
        case 0b0001:
            ext = "NE"
        case 0b0010:
            ext = "CS"
        case 0b0011:
            ext = "CC"
        case 0b0100:
            ext = "MI"
        case 0b0101:
            ext = "PL"
        case 0b0110:
            ext = "VS"
        case 0b0111:
            ext = "VC"
        case 0b1000:
            ext = "HI"
        case 0b1001:
            ext = "LS"
        case 0b1010:
            ext = "GE"
        case 0b1011:
            ext = "LT"
        case 0b1100:
            ext = "GT"
        case 0b1101:
            ext = "LE"
        case 0b1110:
            ext = "AL"
        case _:
            raise ValueError()

    return ext


_REG_SP = 13
_REG_LR = 14
_REG_PC = 15


def _reg_name(n: int) -> str:
    if n == _REG_SP:
        return "SP"
    elif n == _REG_LR:
        return "LR"
    elif n == _REG_PC:
        return "PC"
    else:
        return f"R{n}"


def _reg_list(n: int) -> str:

    s = "{"
    # for i in range(8):
    #     if 0 == n & (1 << i):
    #         continue
    #     if "{" == s:
    #         s = s + f" R{i}"
    #     else:
    #         s = s + f", R{i}"

    _MAX_BITS = 16

    i = 0
    while i < _MAX_BITS:
        if 0 == (n & (1 << i)):
            i += 1
            continue

        j = i + 1
        while j < _MAX_BITS:
            if 0 == (n & (1 << j)):
                break
            else:
                j += 1
                continue

        if j == i + 1:
            # 1
            s1 = _reg_name(i)
        elif j == i + 2:
            # 2
            s1 = _reg_name(i) + ", " + _reg_name(i + 1)
        else:
            # > 2
            s1 = _reg_name(i) + " - " + _reg_name(j - 1)

        if "{" == s:
            s = s + " " + s1
        else:
            s = s + ", " + s1

        i = j
        # -- END OF WHILE

    return s + " }"


def _sign_extend32(n: int, bits: int) -> int:

    assert bits <= 32

    sign = 1 & (n >> (bits - 1))
    if sign:
        # while bits < 32:
        #     n |= 1 << bits
        #     bits += 1
        # n = -((0xFFFFFFFF & ~n) + 1)

        # n = n & ~(1 << (bits - 1))  # Clear sign
        n = (0xFFFF_FFFF << bits) | n  # Fill high bits with 1
        n = 0xFFFF_FFFF & (~n + 1)  # Absolute value
        n = -n

    return n


def _dec_ADD_immediate_etc(code: int, mnem: str) -> str:

    # bits [8:6]
    imm3 = 0b111 & (code >> 6)
    # bits [5:3]
    rn = 0b111 & (code >> 3)
    # bits [2:0]
    rd = 0b111 & code

    if rd == rn:
        # XXX Rn, #imm3
        return "{} {}, #{}".format(
            _mnem_case(mnem),
            _reg_case(rn),
            _hex_case(imm3),
        )
    else:
        # XXX Rd, Rn, #imm3
        return "{} {}, {}, #{}".format(
            _mnem_case(mnem),
            _reg_case(rd),
            _reg_case(rn),
            _hex_case(imm3),
        )


def _dec_ADD_register_etc(code: int, mnem: str) -> str:

    # bits [8:6]
    rm = 0b111 & (code >> 6)
    # bits [5:3]
    rn = 0b111 & (code >> 3)
    # bits [2:0]
    rd = 0b111 & code

    if rd == rn:
        # XXX Rn, Rm
        return "{} {}, {}".format(
            _mnem_case(mnem),
            _reg_case(rn),
            _reg_case(rm),
        )
    else:
        # XXX Rd, Rn, Rm
        return "{} {}, {}, {}".format(
            _mnem_case(mnem),
            _reg_case(rd),
            _reg_case(rn),
            _reg_case(rm),
        )


def _dec_ADD_register_T2_etc(code: int, mnem: str) -> str:

    # bits [7]
    dn = 1 & (code >> 7)
    # bits [6:3]
    rm = 0b1111 & (code >> 3)
    # bits [2:0]
    rdn = 0b111 & code

    rdn = (dn << 3) | rdn

    return "{} {}, {}".format(
        _mnem_case(mnem),
        _reg_case(rdn),
        _reg_case(rm),
    )


def _dec_ADR(code: int) -> str:

    # bits [10:8]
    rd = 0b111 & (code >> 8)
    imm8 = 0xFF & code

    imm32 = imm8 << 2

    return "{} {}, {}, #{}".format(
        _mnem_case("ADD"),
        _reg_case(rd),
        _reg_case(_REG_PC),
        _hex_case(imm32),
    )


def _dec_AND_register_etc(code: int, mnem: str) -> str:

    # bits[5:3]
    rm = 0b111 & (code >> 3)
    # bits [2:0]
    rdn = 0b111 & code

    return "{} {}, {}".format(
        _mnem_case(mnem),
        _reg_case(rdn),
        _reg_case(rm),
    )


def _dec_B(code: int) -> str:

    # bits [11:8]
    cond = 0b1111 & (code >> 8)
    # bits [7:0]
    imm8 = 0xFF & code

    imm32 = _sign_extend32(imm8 << 1, 9)

    # return "B{} [PC, #{:#X}]".format(_cond_ext(cond), imm32)
    return "{}{} [{}, #{}]".format(
        _mnem_case("B"),
        _mnem_case(_cond_ext(cond)),
        _reg_case(_REG_PC),
        _hex_case(imm32),
    )


def _dec_B_T2(code: int) -> str:

    # bits [10:0]
    imm11 = 0x7FF & code
    imm32 = _sign_extend32(imm11 << 1, 12)

    # return f"B [PC, #{imm32:#X}]"
    return "{} [{}, #{}]".format(
        _mnem_case("B"),
        _reg_case(_REG_PC),
        _hex_case(imm32),
    )


def _dec_BL(code1: int, code2: int) -> str:

    # bits [10]
    s = 1 & (code1 >> 10)
    # bits [9:0]
    imm10 = 0b11_1111_1111 & code1

    # bits [13]
    j1 = 1 & (code2 >> 13)
    # bits [11]
    j2 = 1 & (code2 >> 11)
    # bits [10:0]
    imm11 = 0b111_1111_1111 & code2

    i1 = 1 & ~(j1 ^ s)
    i2 = 1 & ~(j2 ^ s)
    # S:I1:I2:imm10:imm11:’0’
    imm25 = (s << 24) | (i1 << 23) | (i2 << 22) | (imm10 << 12) | (imm11 << 1)
    imm32 = _sign_extend32(imm25, 25)

    # return f"BL [PC, #{imm32:#X}]"
    return "{} [{}, #{}]".format(
        _mnem_case("BL"),
        _reg_case(_REG_PC),
        _hex_case(imm32),
    )


def _dec_BX_etc(code: int, mnem: str) -> str:

    # bits [6:3]
    rm = 0b1111 & (code >> 3)

    return "{} {}".format(
        _mnem_case(mnem),
        _reg_case(rm),
    )


def _dec_LDM(code: int) -> str:

    # bits [10:8]
    rn = 0b111 & (code >> 8)
    # bits [7:0]
    registers = 0xFF & code

    wback = 0 == (1 & (registers >> rn))

    if REG_UPPER:
        reg_list = _reg_list(registers)
    else:
        reg_list = _reg_list(registers).lower()

    if wback:
        fmt = "{} {}!, {}"
    else:
        fmt = "{} {}, {}"

    return fmt.format(
        _mnem_case("LDM"),
        _reg_case(rn),
        reg_list,
    )


def _dec_LDR_literal(code: int) -> str:

    # bits [10:8]
    rt = 0b111 & (code >> 8)
    # bits [7:0]
    imm32 = (0xFF & code) << 2

    return "{} {} [{}, #{}]".format(
        _mnem_case("LDR"),
        _reg_case(rt),
        _reg_case(_REG_PC),
        _hex_case(imm32),
    )


def _dec_LSL_immediate_etc(code: int, mnem: str) -> str:

    # bits [10:6]
    imm5 = 0b1_1111 & (code >> 6)
    # bits [5:3]
    rm = 0b111 & (code >> 3)
    # bits [2:0]
    rd = 0b111 & code

    return "{} {}, {}, #{}".format(
        _mnem_case(mnem),
        _reg_case(rd),
        _reg_case(rm),
        _hex_case(imm5),
    )


def _dec_LSL_register_etc(code: int, mnem: str) -> str:
    # bits[5:3]
    rm = 0b111 & (code >> 3)
    # bits [2:0]
    rdn = 0b111 & code

    # XXX Rd, Rn, Rm
    return "{0} {1}, {1}, {2}".format(
        _mnem_case(mnem),
        _reg_case(rdn),
        _reg_case(rm),
    )


def _dec_MOV_immediate_etc(code: int, mnem: str) -> str:

    # bits[10:8]
    rd = 0b111 & (code >> 8)
    # bits [7:0]
    imm8 = 0xFF & code

    return "{} {}, #{}".format(
        _mnem_case(mnem),
        _reg_case(rd),
        _hex_case(imm8),
    )


def _dec_MUL(code: int) -> str:

    # bits [5:3]
    rn = 0b111 & (code >> 3)
    # bits [2:0]
    rdm = 0b111 & code

    if rn == rdm:
        # MULS <Rn>, <Rm>
        return "{} {}, {}".format(
            _mnem_case("MULS"),
            _reg_case(rn),
            _reg_case(rdm),
        )
    else:
        # MULS <Rd>, <Rn>, <Rm>
        return "{} {}, {}, {}".format(
            _mnem_case("MULS"),
            _reg_case(rdm),
            _reg_case(rn),
            _reg_case(rdm),
        )


def _dec_POP(code: int) -> str:

    # bits [8]
    p = 1 & (code >> 8)
    # bits [7:0]
    regs = 0xFF & code

    regs = (p << 15) | regs

    if REG_UPPER:
        reg_list = _reg_list(regs)
    else:
        reg_list = _reg_list(regs).lower()

    return "{} {}".format(
        _mnem_case("POP"),
        reg_list,
    )


def _dec_PUSH(code: int) -> str:

    # bits [8]
    m = 1 & (code >> 8)
    # bits [7:0]
    regs = 0xFF & code

    regs = (m << 14) | regs

    if REG_UPPER:
        reg_list = _reg_list(regs)
    else:
        reg_list = _reg_list(regs).lower()

    return "{} {}".format(
        _mnem_case("PUSH"),
        reg_list,
    )


def _dec_RSB_immediate(code: int) -> str:

    # bits [5:3]
    rn = 0b111 & (code >> 3)
    # bits [2:0]
    rd = 0b111 & code

    if rd == rn:
        return "{} {}, #0".format(
            _mnem_case("RSBS"),
            _reg_case(rn),
        )
    else:
        return "{} {}, {}, #0".format(
            _mnem_case("RSBS"),
            _reg_case(rd),
            _reg_case(rn),
        )


def _dec_STM(code: int) -> str:

    # bits [10:8]
    rn = 0b111 & (code >> 8)
    # bits [7:0]
    registers = 0xFF & code

    if REG_UPPER:
        reg_list = _reg_list(registers)
    else:
        reg_list = _reg_list(registers).lower()

    return "{} {}!, {}".format(
        _mnem_case("STM"),
        _reg_case(rn),
        reg_list,
    )


def _dec_STR_immediate_etc(code: int, mnem: str) -> str:

    # bits [10:6]
    imm5 = 0b1_1111 & (code >> 6)
    # bits [5:3]
    rn = 0b111 & (code >> 3)
    # bits [2:0]
    rt = 0b111 & code

    imm32 = imm5 << 2

    if 0 == imm32:
        return "{} {}, [{}]".format(
            _mnem_case(mnem),
            _reg_case(rt),
            _reg_case(rn),
        )
    else:
        return "{} {}, [{}, #{}]".format(
            _mnem_case(mnem),
            _reg_case(rt),
            _reg_case(rn),
            _hex_case(imm32),
        )


def _dec_STR_immediate_T2_etc(code: int, mnem: str) -> str:

    # bits [10:8]
    rt = 0b111 & (code >> 8)
    # bits [7:0]
    imm8 = 0xFF & code

    imm32 = imm8 << 2

    if 0 == imm32:
        return "{} {}, [{}]".format(
            _mnem_case(mnem),
            _reg_case(rt),
            _reg_case(_REG_SP),
        )
    else:
        return "{} {}, [{}, #{}]".format(
            _mnem_case(mnem),
            _reg_case(rt),
            _reg_case(_REG_SP),
            _hex_case(imm32),
        )


def _dec_STR_register_etc(code: int, mnem: str) -> str:

    # bits [8:6]
    rm = 0b111 & (code >> 6)
    # bits [5:3]
    rn = 0b111 & (code >> 3)
    # bits [2:0]
    rt = 0b111 & code

    return "{} {}, [{}, {}]".format(
        _mnem_case(mnem),
        _reg_case(rt),
        _reg_case(rn),
        _reg_case(rm),
    )


def _dec_STRB_immediate_etc(code: int, mnem: str) -> str:

    # bits [10:6]
    imm5 = 0b1_1111 & (code >> 6)
    # bits [5:3]
    rn = 0b111 & (code >> 3)
    # bits [2:0]
    rt = 0b111 & code

    imm32 = imm5

    if 0 == imm32:
        return "{} {}, [{}]".format(
            _mnem_case(mnem),
            _reg_case(rt),
            _reg_case(rn),
        )
    else:
        return "{} {}, [{}, #{}]".format(
            _mnem_case(mnem),
            _reg_case(rt),
            _reg_case(rn),
            _hex_case(imm32),
        )


def _dec_STRH_immediate_etc(code: int, mnem: str) -> str:

    # bits [10:6]
    imm5 = 0b1_1111 & (code >> 6)
    # bits [5:3]
    rn = 0b111 & (code >> 3)
    # bits [2:0]
    rt = 0b111 & code

    imm32 = imm5 << 1

    if 0 == imm32:
        return "{} {}, [{}]".format(
            _mnem_case(mnem),
            _reg_case(rt),
            _reg_case(rn),
        )
    else:
        return "{} {}, [{}, #{}]".format(
            _mnem_case(mnem),
            _reg_case(rt),
            _reg_case(rn),
            _hex_case(imm32),
        )


def _dec_SXTH_etc(code: int, mnem: str) -> str:

    # bits [5:3]
    rm = 0b111 & (code >> 3)
    # bits [2:0]
    rd = 0b111 & code

    return "{} {}, {}".format(
        _mnem_case(mnem),
        _reg_case(rd),
        _reg_case(rm),
    )


def _dec_UDF_etc(code: int, mnem: str) -> str:
    imm8 = 0xFF & code
    return "{} #{}".format(_mnem_case(mnem), _hex_case(imm8))
