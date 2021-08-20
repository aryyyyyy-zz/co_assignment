import os
from sys import stdin

class Memory:
	def __init__(self):
		MEMORY_SIZE = 256
		self.memory = []
		for i in range(MEMORY_SIZE):
			self.memory.append('0'*16)
	
	def write(self, index, instruction):
		self.memory[index] = instruction

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

	def run(self, input_lines):

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
		if opCode == 0:
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
		if opCode == 1:
			regA = int(instruction[7:10], 2)
			regB = int(instruction[10:13], 2)
			regC = int(instruction[13:16], 2)

			val = self.registers.getValue(regB) - self.registers.getValue(regC)

			
			if (val < 0):
				val = 0
				self.registers.setValue(7, 8)
			else:
				self.resetFlag()

			self.registers.setValue(regA, val)
			self.pc += 1

		# MOV IMM
		if opCode == 2:
			regA = int(instruction[5:8], 2)
			val = int(instruction[8:16], 2)
			self.registers.setValue(regA, val)
			self.pc += 1
		
		# MOV REG
		if opCode == 3:
			regA = int(instruction[10:13], 2)
			regB = int(instruction[13:16], 2)
			self.registers.setValue(regA, self.registers.getValue(regB))
			self.pc += 1

		# LOAD
		if opCode == 4:
			regA = int(instruction[5:8], 2)
			memAddress = int(instruction[8:16], 2)
			self.registers.setValue(regA, self.memory.read(memAddress))
			self.pc += 1

		# STORE
		if opCode == 5:
			regA = int(instruction[5:8], 2)
			memAddress = int(instruction[8:16], 2)
			self.memory.write(memAddress, self.registers.getValue(regA))
			self.pc += 1

		# MUL
		if opCode == 6:
			regA = int(instruction[7:10], 2)
			regB = int(instruction[10:13], 2)
			regC = int(instruction[13:16], 2)

			val = self.registers.getValue(regB) * self.registers.getValue(regC)

			if (val > 255):
				self.registers.setValue(7, 8)
			else:
				self.resetFlag()

			val = val % 256
			self.registers.setValue(regA, val)
			self.pc += 1
			

		# DIV
		if (opCode == 7):
		   
			regA = int(instruction[10:13], 2)
			regB = int(instruction[13:16], 2)

			quotient = self.registers.getValue(regA) // self.registers.getValue(regB)
			remainder = self.registers.getValue(regA) % self.registers.getValue(regB)
			self.registers.setValue(0, quotient)
			self.registers.setValue(1, remainder)
			self.pc += 1

			self.resetFlag()

		# RIGHT SHIFT
		if opCode == 8:
			reg = int(instruction[5:8], 2)
			imm = int(instruction[8:16], 2)
			val = self.registers.getValue(reg) >> imm
			self.registers.setValue(reg, val)
			self.pc += 1

			self.resetFlag()

		# LEFT SHIFT
		if opCode == 9:
			reg = int(instruction[5:8], 2)
			imm = int(instruction[8:16], 2)
			val = self.registers.getValue(reg) << imm
			self.registers.setValue(reg, val)
			self.pc += 1

			self.resetFlag()

		# EXCLUSIVE OR
		if opCode == 10:
			regA = int(instruction[7:10], 2)
			regB = int(instruction[10:13], 2)
			regC = int(instruction[13:16], 2)

			val = self.registers.getValue(regB) ^ self.registers.getValue(regC)

			self.registers.setValue(regA, val)
			self.pc += 1

			self.resetFlag()

		# OR 
		if opCode == 11:
			regA = int(instruction[7:10], 2)
			regB = int(instruction[10:13], 2)
			regC = int(instruction[13:16], 2)

			val = self.registers.getValue(regB) | self.registers.getValue(regC)

			self.registers.setValue(regA, val)
			self.pc += 1

			self.resetFlag()

		# AND
		if opCode == 12:
			regA = int(instruction[7:10], 2)
			regB = int(instruction[10:13], 2)
			regC = int(instruction[13:16], 2)

			val = self.registers.getValue(regB) & self.registers.getValue(regC)

			self.registers.setValue(regA, val)
			self.pc += 1

			self.resetFlag()

		# INVERT
		if opCode == 13:
			regA = int(instruction[10:13], 2)
			regB = int(instruction[13:16], 2)

			val = ~self.registers.getValue(regB) & 255
			self.registers.setValue(regA, val)
			self.pc += 1

			self.resetFlag()
		
		#CMP
		if opCode == 14:
			regA = int(instruction[10:13], 2)
			regB = int(instruction[13:16], 2)

			if regA == regB:
				self.registers.setValue(7, 1)
			elif regA > regB:
				self.registers.setValue(7, 2)
			else:
				self.registers.setValue(7, 4)
			self.pc += 1

		#UNCONDITIONAL JUMP
		if opCode == 15:
			addr = int(instruction[8:16], 2)
			self.pc = addr
			self.resetFlag()

		#LT JUMP
		if opCode == 16:
			if self.registers.getValue(7) == 4:
				addr = int(instruction[8:16], 2)
				self.pc = addr
			else:
				self.pc += 1
			self.resetFlag()
			
		#GT JUMP
		if opCode == 17:
			if self.registers.getValue(7) == 2:
				addr = int(instruction[8:16], 2)
				self.pc = addr
			else:
				self.pc += 1
			self.resetFlag()

		#EQ JUMP
		if opCode == 18:
			if self.registers.getValue(7) == 1:
				addr = int(instruction[8:16], 2)
				self.pc = addr
			else:
				self.pc += 1
			self.resetFlag()

		#HLT
		if opCode == 19:
			self.resetFlag()
			self.isHalted = True
			self.pc += 1


	def printLine(self):
		print(f'{(self.pc - 1):08b} ',end='')
		for i in range(self.registers.getLength()):
			print(f'{self.registers.getValue(i):016b} ', end = '')
		print()

	def memoryDump(self):
		for i in range(self.memory.getSize()):
			print(self.memory.read(i))

def main():
	input_lines = os.read(0, 10**6).strip().splitlines() 
	for x in range(len(input_lines)):
		input_lines[x] = input_lines[x].decode("utf-8")
	sim = Simulator()
	sim.run(input_lines)

main()
