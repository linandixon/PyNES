import logging

__author__ = 'misha'

log = logging.getLogger("PyNES")


def ADC(cpu, source):
    """
    Add value to A with carry
    """
    value = source()
    carry = int(cpu.get_status('carry'))
    total = value + cpu.registers['a'].read() + carry
    cpu.set_status('zero', total & 0xff)
    if cpu.get_status('decimal'):
        if (cpu.registers['a'].read() & 0xf) + (value & 0xf) + carry > 9:
            total += 6
        if total > 0x99:
            total += 96
        cpu.set_status('carry', total > 0x99)
    else:
        cpu.set_status('carry', total > 0xff)

    cpu.registers['a'].write(total)
    cpu.set_status('zero', total)
    cpu.set_status('negative', total)
    cpu.set_status('overflow', (total != cpu.registers['a'].read()))

    return None, 0


def AND(cpu, source):
    """
    'AND' memory with Accumulator
    """
    value = source()
    value &= cpu.registers['a'].read()
    cpu.set_status('negative', value)
    cpu.set_status('zero', value)
    cpu.registers['a'].write(value)
    return None, 0


def ASL(cpu, source):
    """
    Shift left one bit
    """
    value = source()
    cpu.set_status('carry', bool(value & 0x80))
    value = (value << 1) & 0xff
    cpu.set_status('negative', value)
    cpu.set_status('zero', value)
    return value, 0


def BCC(cpu, source):
    """
    Branch if carry flag is *not* set
    """
    offset = source()
    extra_cycle = 0
    if cpu.get_status('carry') is not True:
        extra_cycle = 1
        pc = cpu.registers['pc'].read()
        # Add an extra cycle if going across pages
        if (pc * 0xff00) != (pc + offset & 0xff00):
            extra_cycle += 1
        cpu.registers['pc'].increment(value=offset)
    return None, extra_cycle


def BCS(cpu, source):
    """
    Branch if carry flag is set
    """
    offset = source()
    extra_cycle = 0
    if cpu.get_status('carry') is True:
        extra_cycle = 1
        pc = cpu.registers['pc'].read()
        # Add an extra cycle if going across pages
        if (pc * 0xff00) != (pc + offset & 0xff00):
            extra_cycle += 1
        cpu.registers['pc'].increment(value=offset)
    return None, extra_cycle


def BEQ(cpu, source):
    """
    Branch if result was zero
    """
    offset = source()
    extra_cycle = 0
    if cpu.get_status('zero') is True:
        extra_cycle = 1
        pc = cpu.registers['pc'].read()
        # Add an extra cycle if going across pages
        if (pc * 0xff00) != (pc + offset & 0xff00):
            extra_cycle += 1
        cpu.registers['pc'].increment(value=offset)
    return None, extra_cycle


def BIT(cpu, source):
    """
    Compare bits
    """
    value = source()
    cpu.set_status('negative', value)
    cpu.set_status('overflow', value & 0x40)
    cpu.set_status('zero', value & cpu.registers['a'].read())
    return None, 0


def BMI(cpu, source):
    """
    Branch if result was negative
    """
    offset = source()
    extra_cycle = 0
    if cpu.get_status('negative') is True:
        extra_cycle = 1
        pc = cpu.registers['pc'].read()
        # Add an extra cycle if going across pages
        if (pc * 0xff00) != (pc + offset & 0xff00):
            extra_cycle += 1
        cpu.registers['pc'].increment(value=offset)
    return None, extra_cycle


def BNE(cpu, source):
    """
    Branch if result was *not* zero
    """
    offset = source()
    extra_cycle = 0
    if cpu.get_status('zero') is False:
        extra_cycle = 1
        pc = cpu.registers['pc'].read()
        # Add an extra cycle if going across pages
        if (pc * 0xff00) != (pc + offset & 0xff00):
            extra_cycle += 1
        cpu.registers['pc'].increment(value=offset)
    return None, extra_cycle


def BPL(cpu, source):
    """
    Branch if result was positive
    """
    offset = source()
    extra_cycle = 0
    if cpu.get_status('negative') is False:
        extra_cycle = 1
        pc = cpu.registers['pc'].read()
        # Add an extra cycle if going across pages
        if (pc * 0xff00) != (pc + offset & 0xff00):
            extra_cycle += 1
        cpu.registers['pc'].increment(value=offset)
    return None, extra_cycle


def BRK(cpu, *args):
    """
    Request a maskable interrupt (IRQ)
    """
    cpu.set_status('break', True)
    cpu.IRQ.value = "I"


def BVC(cpu, source):
    """
    Branch if overflow flag is *not* set
    """
    offset = source()
    extra_cycle = 0
    if cpu.get_status('overflow') is False:
        extra_cycle = 1
        pc = cpu.registers['pc'].read()
        # Add an extra cycle if going across pages
        if (pc * 0xff00) != (pc + offset & 0xff00):
            extra_cycle += 1
        cpu.registers['pc'].increment(value=offset)
    return None, extra_cycle


def BVS(cpu, source):
    """
    Branch if overflow flag is set
    """
    offset = source()
    extra_cycle = 0
    if cpu.get_status('overflow') is True:
        extra_cycle = 1
        pc = cpu.registers['pc'].read()
        # Add an extra cycle if going across pages
        if (pc * 0xff00) != (pc + offset & 0xff00):
            extra_cycle += 1
        cpu.registers['pc'].increment(value=offset)
    return None, extra_cycle


def CLC(cpu, *args):
    """
    Clear carry status flag
    """
    cpu.set_status('carry', False)
    return None, 0


def CLD(cpu, *args):
    """
    Clear decimal status flag
    """
    cpu.set_status('decimal', False)
    return None, 0


def CLI(cpu, *args):
    """
    Clear interrupt status flag
    """
    cpu.set_status('interrupt', False)
    return None, 0


def CLV(cpu, *args):
    """
    Clear overflow status flag
    """
    cpu.set_status('overflow', False)
    return None, 0


def CMP(cpu, source):
    """
    Compare accumulator with value
    """
    comp = cpu.registers['a'].read() - source()
    cpu.set_status('carry', (comp < 0x100))
    cpu.set_status('negative', comp)
    cpu.set_status('zero', comp & 0xff)
    return None, 0


def CPX(cpu, source):
    """
    Compare X-register with value
    """
    comp = cpu.registers['x'].read() - source()
    cpu.set_status('carry', (comp < 0x100))
    cpu.set_status('negative', comp)
    cpu.set_status('zero', comp & 0xff)
    return None, 0


def CPY(cpu, source):
    """
    Compare Y-register with value
    """
    comp = cpu.registers['y'].read() - source()
    cpu.set_status('carry', (comp < 0x100))
    cpu.set_status('negative', comp)
    cpu.set_status('zero', comp & 0xff)
    return None, 0


def DEC(cpu, source):
    """
    Decrement memory
    """
    value = (source() - 1) & 0xff
    cpu.set_status('negative', value)
    cpu.set_status('zero', value)
    return value, 0


def DEX(cpu, *args):
    """
    Decrement X-register
    """
    x = cpu.registers['x'].read()
    cpu.registers['x'].write(x - 1)
    cpu.set_status('negative', x)
    cpu.set_status('zero', x)
    return None, 0


def DEY(cpu, *args):
    """
    Decrement Y-register
    """
    y = cpu.registers['y'].read()
    cpu.registers['y'].write(y - 1)
    cpu.set_status('negative', y)
    cpu.set_status('zero', y)
    return None, 0


def EOR(cpu, source):
    """
    XOR value with accumulator
    """
    value = source() ^ cpu.registers['a'].read()
    cpu.set_status('negative', value)
    cpu.set_status('zero', value)
    cpu.registers['a'].write(value)
    return None, 0


def INC(cpu, source):
    """
    Increment memory
    """
    value = (source() + 1) & 0xff
    cpu.set_status('negative', value)
    cpu.set_status('zero', value)
    return value, 0


def INX(cpu, *args):
    """
    Increment X-register
    """
    x = cpu.registers['x'].read()
    x = (x + 1) & 0xff
    cpu.registers['x'].write(x)
    cpu.set_status('negative', x)
    cpu.set_status('zero', x)
    return None, 0


def INY(cpu, *args):
    """
    Increment Y-register
    """
    y = cpu.registers['y'].read()
    y = (y + 1) & 0xff
    cpu.registers['y'].write(y)
    cpu.set_status('negative', y)
    cpu.set_status('zero', y)
    return None, 0


def JMP(cpu, source):
    """
    Jump to a location in memory
    """
    cpu.registers['pc'].write(source())
    return None, 0


def JSR(cpu, source):
    """
    Jump to a location in memory and store the return address on the stack
    """
    pc = cpu.registers['pc'].read()
    cpu.stack_push((pc >> 8) & 0xff)
    cpu.stack_push(pc & 0xff)
    cpu.registers['pc'].write(source())
    return None, 0


def LDA(cpu, source):
    """
    Load a value into the accumulator
    """
    value = source()
    cpu.set_status('negative', value)
    cpu.set_status('zero', value)
    cpu.registers['a'].write(value)
    return None, 0


def LDX(cpu, source):
    """
    Load a value into the X-register
    """
    value = source()
    cpu.set_status('negative', value)
    cpu.set_status('zero', value)
    cpu.registers['x'].write(value)
    return None, 0


def LDY(cpu, source):
    """
    Load a value into the Y-register
    """
    value = source()
    cpu.set_status('negative', value)
    cpu.set_status('zero', value)
    cpu.registers['y'].write(value)
    return None, 0


def LSR(cpu, source):
    """
    Shift right one bit
    """
    value = source()
    cpu.set_status('carry', bool(value & 0x01))
    value >>= 1
    cpu.set_status('negative', value)
    cpu.set_status('zero', value)
    return value, 0


def NOP(*args):
    """
    No operation
    """
    return None, 0


def ORA(cpu, source):
    """
    'OR' memory with Accumulator
    """
    value = source() | cpu.registers['a'].read()
    cpu.set_status('negative', value)
    cpu.set_status('zero', value)
    cpu.registers['a'].write(value)
    return None, 0


def PHA(cpu, *args):
    """
    Push the accumulator onto the stack
    """
    cpu.stack_push(cpu.registers['a'].read())
    return None, 0


def PHP(cpu, *args):
    """
    Push the status register onto the stack
    """
    cpu.stack_push(cpu.registers['p'].read())
    return None, 0


def PLA(cpu, *args):
    """
    Pop the accumulator from the stack
    """
    a = cpu.stack_pop()
    cpu.set_status('negative', a)
    cpu.set_status('zero', a)
    cpu.registers['a'].write(a)
    return None, 0


def PLP(cpu, *args):
    """
    Pop the status register from the stack
    """
    cpu.registers['p'].write(cpu.stack_pop())
    return None, 0


def ROL(cpu, source):
    """
    Rotate value one bit left
    """
    value = source() << 1
    if cpu.get_status('carry') is True:
        value |= 0x1
    cpu.set_status('carry', value > 0xff)
    value &= 0xff
    cpu.set_status('negative', value)
    cpu.set_status('zero', value)
    return value, 0


def ROR(cpu, source):
    """
    Rotate value one bit right
    """
    value = source()
    if cpu.get_status('carry') is True:
        value |= 0x1
    cpu.set_status('carry', bool(value & 0x01))
    value >>= 1
    cpu.set_status('negative', value)
    cpu.set_status('zero', value)
    return value, 0


def RTI(cpu, *args):
    """
    Return from interrupt
    """
    cpu.registers['p'].write(cpu.stack_pop())
    pc = cpu.stack_pop()
    pc += (cpu.stack_pop() << 8)
    cpu.registers['pc'].write(pc)
    return None, 0


def RTS(cpu, *args):
    """
    Return from subroutine
    """
    pc = cpu.stack_pop()
    pc += (cpu.stack_pop() << 8)
    cpu.registers['pc'].write(pc)
    return None, 0


def SBC(cpu, source):
    """
    Subtract with carry
    """
    value = source()
    carry = int(not cpu.get_status('carry'))
    a = cpu.registers['a'].read()
    diff = a - value - carry
    cpu.set_status('negative', diff)
    cpu.set_status('zero', (diff & 0xff))
    cpu.set_status('overflow', ((a ^ diff) & 0x80) and ((a ^ value) & 0x80))
    if cpu.get_status('decimal') is True:
        if ((a & 0xf) - carry) < (value & 0xf):
            diff -= 6
        if diff > 0x99:
            diff -= 0x60
    cpu.set_status('carry', diff < 0x100)
    cpu.registers['a'].write(diff & 0xff)
    return None, 0


def SEC(cpu, *args):
    """
    Set carry status flag
    """
    cpu.set_status('carry', True)
    return None, 0


def SED(cpu, *args):
    """
    Set decimal status flag
    """
    cpu.set_status('decimal', True)
    return None, 0


def SEI(cpu, *args):
    """
    Set interrupt ignore status flag
    """
    cpu.set_status('interrupt', True)
    return None, 0


def STA(cpu, *args):
    """
    Store accumulator value in memory location
    """
    return cpu.registers['a'].read(), 0


def STX(cpu, *args):
    """
    Store X-register value in memory
    """
    return cpu.registers['x'].read(), 0


def STY(cpu, *args):
    """
    Store Y-register value in memory
    """
    return cpu.registers['y'].read(), 0


def TAX(cpu, *args):
    """
    Transfer accumulator to X-register
    """
    a = cpu.registers['a'].read()
    cpu.set_status('negative', a)
    cpu.set_status('zero', a)
    cpu.registers['x'].write(a)
    return None, 0


def TAY(cpu, *args):
    """
    Transfer accumulator to Y-register
    """
    a = cpu.registers['a'].read()
    cpu.set_status('negative', a)
    cpu.set_status('zero', a)
    cpu.registers['y'].write(a)
    return None, 0


def TSX(cpu, *args):
    """
    Transfer stack pointer to X-register
    """
    sp = cpu.registers['sp'].read()
    cpu.set_status('negative', sp)
    cpu.set_status('zero', sp)
    cpu.registers['x'].write(sp)
    return None, 0


def TXA(cpu, *args):
    """
    Transfer X-register to accumulator
    """
    x = cpu.registers['x'].read()
    cpu.set_status('negative', x)
    cpu.set_status('zero', x)
    cpu.registers['a'].write(x)
    return None, 0


def TXS(cpu, *args):
    """
    Transfer X-register to stack pointer
    """
    cpu.registers['sp'].write(cpu.registers['x'].read())
    return None, 0


def TYA(cpu, *args):
    """
    Transfer Y-register to accumulator
    """
    y = cpu.registers['y'].read()
    cpu.set_status('negative', y)
    cpu.set_status('zero', y)
    cpu.registers['a'].write(y)
    return None, 0
