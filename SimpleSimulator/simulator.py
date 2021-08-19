class Memory:
    def __init__(self):
        MEMORY_SIZE = 256
        self.memory = []
        for i in range(MEMORY_SIZE):
            self.memory.append(0)

class Registers:
    def __init__(self):
        self.registers = [0, 0, 0, 0, 0, 0, 0, 0]
        
class Simulator:
    def __init__(self):
        self.memory = Memory()
        self.pc = 0
        self.isHalted = False

    def run(self):
        pass

    def getRegisterValue(self):
        pass