import os

def getRegister(token, flagsMod) :

	registerNames = ["R0", "R1", "R2", "R3", "R4", "R5", "R6"]

	if token in registerNames :
	#if int(token[1]) in range(7) and token[0]=="R" :
		ans = str(f'{int(token[1]):03b}')
	
	elif token == "FLAGS" :
		if flagsMod:
			ans = "111"

		else :
			print("ERROR: Illegal use of flags register")
			quit()
  
	else :
		ans = "999"

	return ans

ans = ""
bin_solution = []
input_lines = []
var_list = []
label_list = {}
flag = False
a_commands = {'add': "00000",'sub': "00001", 'mul': "00110", 'xor': "01010", 'or': "01011", 'and': "01100"}
b_commands = {'mov'  : "00010", 'rs' : "01000", 'ls' : "01001"}
c_commands = {'mov' : "00011", 'div' : "00111", 'not' : "01101", 'cmp' : "01110"}  #cmp affects flag
d_commands = {'ld': "00100", 'st': "00101"}
e_commands = {'je': '10010', 'jgt': '10001', 'jlt': '10000', 'jmp': '01111'}
f_commands = {"hlt": "10011"}

#input_lines = list(map(str, sys.stdin.readlines()))
lines = os.read(0, 10**6).strip().splitlines() 
i=0;
size=len(lines)
instruction=[];
for x in range(len(lines)):
    line = lines[x].decode('utf-8') 
    
    input_lines.append(line)

for line in input_lines:
	line = list(line.split(" "))

	if line[0] == 'var':

		if len(line) != 2 :
			print("Invalid syntax")
			quit()

		var_list.append(line[1])

	else:
		break

#print(var_list)
#finds all labels and records their index in dict
randomIndexVariable = 0

for inst in input_lines[len(var_list) : ]:
	inst = list(inst.split(' '))
	#word followed by ":"
	if inst[0].find(":") != -1 :
		if inst[0].find(":") == len(inst[0]) - 1:
			label = inst[0]
			label_list[label] =  str(f'{randomIndexVariable:08b}')

	randomIndexVariable += 1

#print(label_list)
	
for line_s in input_lines[len(var_list) : ]:

	ans = ""

	line = list(line_s.split(' '))

	while (line.count("") != 0):
		line.remove("")

	if line[0] in label_list.keys():
		line = line[1:]

	if input_lines.index(line_s) == len(input_lines) - 1:

		if line[0] == "hlt" :
			if len(line) != 1:
				print("ERROR: Invalid Syntax")
				quit()
			ans +=f_commands[line[0]] + "0"*11
			bin_solution.append(ans)
			break

		else :
			#last instruction is not hlt
			flag = True

	if line[0] in a_commands.keys() :

		if len(line) != 4 :
			print("ERROR: Invalid syntax")
			quit()

		ans += a_commands[line[0]] + "00" #unused bits added
		
		if (getRegister(line[1], False) == '999' or getRegister(line[2], False) == '999' or getRegister(line[3], False) == '999') :
			print("ERROR: Invalid register name")
			quit()
		x = getRegister(line[1], False) + getRegister(line[2], False) + getRegister(line[3], False)
		ans += x

	elif line[0]=="mov":
	#command is 'mov'

		if len(line) != 3:
			print("ERROR: Invalid syntax")
			quit()

		if getRegister(line[2], True) != '999' :
			ans += c_commands[line[0]] + "00000"

			if getRegister(line[1], False) == '999' :
				print("ERROR: Invalid register name")
				quit()

			x = getRegister(line[1], False) + getRegister(line[2], True)
			ans += x

		else:
			ans += b_commands[line[0]]
			if (getRegister(line[1], False) == '999') :
				print("ERROR: Invalid register name")
				quit()
			ans += getRegister(line[1], False)

			if line[2][0] == '$' and line[2][1:].isnumeric():
				num = ""+ line[2][1:]
				#print(line[2])
				if (0 <= int(num) <= 255):
					ans += str(f'{int(num):08b}')
				else:
					print("Illegal Immediate Value")
					quit()

			else: 
				print("ERROR: Invalid syntax")
				quit()

	elif line[0] in b_commands.keys():
		if len(line) != 3:
			print("ERROR: Invalid syntax")
			quit()

		ans += b_commands[line[0]]

		if (getRegister(line[1], False) == '999') :
			print("ERROR: Invalid register name")
			quit()

		ans += getRegister(line[1], False)

		if line[2][0] == '$' and line[2][1:].isnumeric():
			num = ""+ line[2][1:]
			#print(line[2])
			if (0 <= int(num) <= 255):
				ans += str(f'{int(num):08b}')
			else:
				print("Illegal Immediate Value")
				quit()

		else: 
			print("ERROR: Invalid syntax")
			quit()

	elif line[0] in c_commands.keys():

		if len(line) != 3:
			print("ERROR: Invalid syntax")
			quit()

		ans += c_commands[line[0]] + "00000"
		if (getRegister(line[1], False) == '999' or getRegister(line[2], False) == '999') :
			print("ERROR: Invalid register name")
			quit()
		x = getRegister(line[1], False) + getRegister(line[2], False)
		ans += x

	elif line[0] in d_commands.keys() :

		if len(line) != 3 :
			print("ERROR: Invalid syntax")
			quit()

		ans += d_commands[line[0]]
		x = getRegister(line[1], False) 
		if x != "999" :
			ans += x
			if line[2] in var_list :
				n = var_list.index(line[2]) + len(input_lines) - len(var_list)
				ans += str(f'{n:08b}')
				
			else:
				print("ERROR: Use of undefined variable")
				quit()

		else :
			print("ERROR: Invalid register name")
			quit()

	elif line[0] in e_commands.keys() :
		if len(line) != 2:
			print("ERROR: Invalid Syntax")
			quit()

		ans += e_commands[line[0]] + '0'*3
		label = line[1] + ":"

		if label in label_list.keys():
			ans += label_list[label]
		else:
			print('ERROR: Invalid Label')
			quit()


	elif line[0] in f_commands.keys() :

		if len(line) != 1 :
			print("ERROR: Invalid syntax")
			quit()

		if input_lines.index(line_s) != len(input_lines) - 1:
			print("ERROR: hlt not being used as the last instruction")
			quit()

		# ans += f_commands[line[0]] + "0"*11

	elif line[0] == "var" :
		print("ERROR: Variables not declared in the beginning")
		quit()

	else :
		print("ERROR: Invalid syntax")
		quit()

	bin_solution.append(ans)
	
	if flag :
		print("ERROR: Missing hlt instruction")
		quit()

for bin in bin_solution:
	print(bin)