"""
Zero-page indexed addressing with Y-Register
"""
size = 1


def read(cpu, param):
    address = param + cpu.registers['y'].read()
    return cpu.memory.read(address)


def write(cpu, param, value):
    address = param + cpu.registers['y'].read()
    cpu.memory.write(address, value)


def print(param):
    return "{0:#04x},Y".format(param)
