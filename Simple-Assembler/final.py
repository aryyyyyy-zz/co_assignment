import os

# ------------------------------------- CONSTANTS -----------------------------------------------
errors = {
	'a': "Typos in instruction name or register name",
	'b' : "Use of undefined variables",
	'c' : "Use of undefined labels",
	'd' : "Illegal use of FLAGS register",
	'e' : "Illegal Immediate values (less than 0 or more than 255)",
	'f' : "Misuse of labels as variables or vice-versa",
	'g' : "Variables not declared at the beginning",
	'h' : "Missing hlt instruction",
	'i' : "hlt not being used as the last instruction",
	'j' : "Wrong syntax used for instructions",
	'k' : "General syntax error"
}

a_commands = {'add': "00000",'sub': "00001", 'mul': "00110", 'xor': "01010", 'or': "01011", 'and': "01100"}
b_commands = {'mov'  : "00010", 'rs' : "01000", 'ls' : "01001"}
c_commands = {'mov' : "00011", 'div' : "00111", 'not' : "01101", 'cmp' : "01110"}  #cmp affects flag
d_commands = {'ld': "00100", 'st': "00101"}
e_commands = {'je': '10010', 'jgt': '10001', 'jlt': '10000', 'jmp': '01111'}
f_commands = {"hlt": "10011"} 

instruction_length = {'a' : 4, 'b' : 3, 'c' : 3, 'd': 3, 'e': 2, 'f': 1}


#error line number - empty line counted 
#empty lines : zero


#--------------------------------------------------- HELPER FUNCTIONS ------------------------------------------------

def getRegister(reg, n, instruction = 'add'):
	global indices

	reg_list = {'R0' : "000", 'R1' : "001", 'R2' : "010", 'R3' : "011",
	'R4' : "100", 'R5' : "101", 'R6' : "110"}

	if reg in reg_list.keys():
		ans = reg_list[reg]
	
	elif reg == 'FLAGS':
		if instruction == "mov":
			ans = '111'
		else:
			print("Line", indices[n], ":", errors['d'])
			quit()
	
	else:
		print("Line", indices[n], ":", errors['a'])
		quit()

	return ans


#--------------------------------------------------- DISPLAY FUNCTION -------------------------------

def display():
	global output
	for binSol in output:
		print(binSol)


#--------------------------------------------------- COMMAND HANDLERS -------------------------------

def handle_a(cmd, n): #cmd = ["sub", "R1", "R2", "R3"]

	ans = ""
	ans += a_commands[cmd[0]] + "00" #unused bits added
	ans += getRegister(cmd[1], n) + getRegister(cmd[2], n) + getRegister(cmd[3], n)
	output.append(ans)

def handle_mov(cmd, n): #mov R1 #imm | mov R1 R2 | mov R1 FLAGS
	ans = ""
	global indices

	if cmd[2][0] == '$':
		ans += "00010" + getRegister(cmd[1], n)
		s = cmd[2][1:]
		if s.isnumeric():
			if(0<=int(s)<=255):
				ans+=str(f'{int(s):08b}')
			else:
				print("Line", indices[n], ":", errors['e'])
				quit()
		else:
			print("Line", indices[n], ":", errors['e'])
			quit()

	else:
		ans += "00011" + "00000" + getRegister(cmd[1], n) + getRegister(cmd[2],n,'mov')

	output.append(ans)

def handle_b(cmd, n):
	ans = ""
	global indices
	if cmd[2][0] == '$':
		ans += b_commands[cmd[0]] + getRegister(cmd[1], n)
		s = cmd[2][1:]
		if s.isnumeric():
			if(0<=int(s)<=255):
				ans+=str(f'{int(s):08b}')
			else:
				print("Line", indices[n], ":", errors['e'])
				quit()
		else:
			print("Line", indices[n], ":", errors['a'])
			quit()
	else:
		print("Line", indices[n], ":", errors['j'])
		quit()
	output.append(ans)

def handle_c(cmd, n):
	
	ans = c_commands[cmd[0]] + "00000" + getRegister(cmd[1], n) + getRegister(cmd[2], n,'mov')
	output.append(ans)
	
def handle_d(cmd, variables, instructionSize, n): #st R4 xyz
	global indices
	ans = ""
	ans += d_commands[cmd[0]] + getRegister(cmd[1], n)
	if cmd[2] in variables:
		n = variables.index(cmd[2]) + instructionSize
		ans += str(f'{n:08b}')
	else :
		print("Line", indices[n], ":", errors['b'])
		quit()
	output.append(ans)

def handle_e(line, labels, n):
	global indices

	ans = ''
	ans += e_commands[line[0]] + '000'
	if str(line[1]) in labels.keys():
		ans += str(f'{int(labels[line[1]]):08b}')
	else:
		print("Line", indices[n], ":", errors['c'])
		quit()
	output.append(ans)

	

#def setFlag: 
#def getFlag:


# -------------------------------------- LISTS ---------------------------------------------------
lines = []
variables = []
labels = {}
output = []


# --------------------------------------------- HANDLING INPUT --------------------------------------

input_lines = os.read(0, 10**6).strip().splitlines() 
i=0
size=len(input_lines)
instruction=[];
for x in range(len(input_lines)):
	line = input_lines[x].decode('utf-8') 
	lines.append(line)
	
   
#--------------------------------------------- MAKING VARIABLE AND LABEL LIST --------------------------------------

indices = [] #indices of non-empty lines

for i in range(len(lines)):
	if lines[i] != "":
		indices.append(i+1)

while lines.count("") != 0 :
	lines.remove("") 

index = 0
for line in lines:

	line = line.split(' ')
	string = "\t".join(line)
	line = string.split('\t')
		
	if line[0] == 'var':
		if len(line) != 2:
			print("Line", indices[index], ":", errors['j'])
			quit()

		if line[1] in variables:
			print("Line", indices[index], ":", errors['k'])
			quit()

		variables.append(line[1])

	else:
		break

	index += 1
		
#print(variables)

lines = lines[len(variables):]

for i in range(len(lines)):

	lines[i] = list(lines[i].split(' '))
	string = "\t".join(lines[i])
	lines[i] = string.split("\t")

		
	if lines[i][0][-1] == ':':
		labels[lines[i][0][:-1]] = i 
		lines[i] = lines[i][1:]

# ----------------------------------------- MAIN LOOP -------------------------------------

index = len(variables) 

if not (1 <= len(indices) <= 256) :
	print("ERROR: Code limit exceeded")
	quit()

for line in lines:

	# A COMMANDS
	if line[0] in a_commands.keys():
		if len(line) != instruction_length['a']:
			print("Line", indices[index], ":", errors['j'])
			#print()
			quit()
			
		handle_a(line, index)

	
	# MOV COMMAND
	elif line[0] == 'mov':
		if len(line) != instruction_length['b']:
			print("Line", indices[index], ":", errors['j'])
			quit()
		handle_mov(line, index)
		
	
	# B COMMANDS
	elif line[0] in b_commands.keys():
		if len(line) != instruction_length['b']:
			print("Line", indices[index], ":", errors['j'])
			quit()
			
		handle_b(line, index)
	
	# C COMMANDS
	elif line[0] in c_commands.keys():
		if len(line) != instruction_length['c']:
			print("Line", indices[index], ":", errors['j'])
			quit()
			
		handle_c(line, index)
	
	# D COMMANDS
	elif line[0] in d_commands.keys():
		if len(line) != instruction_length['d']:
			print("Line", indices[index], ":", errors['j'])
			quit()
			
		handle_d(line, variables, len(lines), index)


	# E COMMANDS
	elif line[0] in e_commands.keys():
		if len(line) != instruction_length['e']:
			print("Line", indices[index], ":", errors['j'])
			quit()
		handle_e(line, labels, index)

	# F COMMANDS
	elif line[0] in f_commands.keys():
		if lines.index(line) == len(lines) - 1:
			if len(line) != 1:
				print("Line", indices[index], ":", errors['j'])
				quit()
			ans = f_commands[line[0]] + "0"*11
			output.append(ans)
			display()
		else:
			print("Line", indices[index], ":", errors['i'])
			quit()

	# VAR DECLARATION
	elif line[0] == "var" :
		print("Line", indices[index], ":", errors['g'])
		quit()		
  
	# INVALID COMMAND ERROR
	else:
		print("Line", indices[index], ":", errors['a'])  
		quit()
		
	index += 1








	






