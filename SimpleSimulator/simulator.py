import os

class Memory:
    def __init__(self):
        MEMORY_SIZE = 256
        self.memory = []
        for i in range(MEMORY_SIZE):
            self.memory.append('0'*16)
    
    def write(self, index, instruction):
        self.memory[i] = instruction

    def read(self, index):
        return self.memory[index]
    
    def getSize(self):
        return len(self.memory)

    

class Registers:
    def __init__(self):
        self.registers = [0, 0, 0, 0, 0, 0, 0, 0]
    
    def getValue(self, index):
        return self.registers[index]

    def setValue(self, index, value):
        self.registers[index] = value

    def getLength(self):
        return len(self.registers)
        
class Simulator:
    def __init__(self):
        self.memory = Memory()
        self.pc = 0
        self.isHalted = False
        self.registers = Registers()

    def run(self):
        input_lines = os.read(0, 10**6).strip().splitlines() 

        for i in  range(len(input_lines)):
            self.memory.write(i, input_lines[i])

        while (not self.isHalted):
            instruction = self.memory.read(self.pc)
            self.execute(instruction)
            self.printLine()


        self.memoryDump()
        
    def resetFlag(self):
        self.registers.setValue(7, 0)

    def execute(self, instruction):
        opCode = int(instruction[0:5], 2)

        # ADD
        if (opCode == 0):
            regA = int(instruction[7:10], 2)
            regB = int(instruction[10:13], 2)
            regC = int(instruction[13:16], 2)

            val = self.registers.getValue(regB) + self.registers.getValue(regC)
            if (val > 255):
                self.registers.setValue(7, 8)
            
            elif (val < 0):
                val = 0
                self.registers.setValue(7, 8)
            else:
                self.resetFlag()

            val = val % 256
            self.registers.setValue(regA, val)
            self.pc += 1
        
        # SUB
        
            

    def printLine(self):
        print(f'{(self.pc - 1):08b} ',end='')
        for i in range(self.registers.getLength()):
            print(f'{self.registers.getValue(i):16b} ', end = '')
        print()

    def memoryDump(self):
        for i in range(self.memory.getSize()):
            print(self.memory.read(i))


    