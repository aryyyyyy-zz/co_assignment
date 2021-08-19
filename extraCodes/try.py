from sys import stdin

def getRegister(token, flag) :

	if int(token[1]) in range(7) and token[0]=="R":
		ans = str(f'{int(token[1]):03b}')
	
	elif token=="FLAGS" and flag:
		ans = "111"
  
	else :
		ans = "999"

	return ans

lines = []
var_list = []
inst = []
flag = False
a_commands = {'add': "00000",'sub': "00001", 'mul': "00110", 'xor': "01010", 'or': "01011", 'and': "01100"}
b_commands = {'mov'  : "00010", 'rs' : "01000", 'ls' : "01001"}
c_commands = {'mov' : "00011", 'div' : "00111", 'not' : "01101", 'cmp' : "01110"}  #cmp affects flag
d_commands = {'ld': "00100", 'st': "00101"}
f_commands = {"hlt": "10011"}

for line in stdin:
	
	if line == '': # If empty string is read then stop the loop
		break
	lines.append(line)
	
ans = ""

for line in lines:
	line = list(line.split(" "))
	if line[0] == 'var':
		var_list.append(line[1])
	else:
		break

for line in lines[len(var_list) : ]:

	if lines.index(line) == len(lines) - 1:

		if line == "hlt" :
			ans +=f_commands[line] + "0"*11
			print(ans)
			break

		else :
			#last instrcution is not hlt
			flag = True

	line = list(line.split(" "))

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

	elif (line[0] in b_commands.keys()) and (line[0] in c_commands.keys()):
		if len(line) != 3:
			print("ERROR: Invalid syntax")
			quit()
		if line[2][0] == "R":
			ans += c_commands[line[0]] + "00000"
			if (getRegister(line[1], False) == '999' or getRegister(line[2], False) == '999') :
				print("ERROR: Invalid register name")
				quit()
			x = getRegister(line[1], False) + getRegister(line[2], False)
			ans += x
		else:
			ans += b_commands[line[0]]
			if (getRegister(line[1], False) == '999') :
				print("ERROR: Invalid register name")
				quit()
			ans += getRegister(line[1], False)
			line[2] = ""+ line[2][1:]
			#print(line[2])
			if (0 <= int(line[2]) <= 255):
				ans += str(f'{int(line[2]):08b}')
			else:
				print("Illegal Immediate Value")
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
		ans += str(f'{int(line[2]):08b}')

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
		if x!="999" :
			ans += x
			if line[2] in var_list :
				n = var_list.index(line[2]) + len(lines) - len(var_list)
				ans += str(f'{n:08b}')
				
			else:
				print("ERROR: Use of undefined variable")
				quit()

		else :
			print("ERROR: Invalid register name")
			quit()

	elif line[0] in f_commands.keys() :

		if len(line) != 1 :
			print("ERROR: Invalid syntax")
			quit()

		if lines.index(line[0]) != len(lines) - 1:
			print("ERROR: hlt not being used as the last instruction")
			quit()

	else:
		print("Invalid Instruction")
		quit()
	print(ans)
	ans = ""

	if flag :
		print("ERROR: Missing hlt instruction")
		quit()
