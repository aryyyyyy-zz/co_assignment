#starter-code
#first change added
from sys import stdin

def getRegister(token, flag) :

	if token =="R0":
		ans = "000"

	elif token=="R1":
		ans = "001"

	elif token=="R2":
		ans = "010"

	elif token=="R3":
		ans = "011"

	elif token=="R4":
		ans = "100"

	elif token=="R5":
		ans = "101"

	elif token=="R6":
		ans = "110"

	elif token=="FLAGS" and flag:
		ans = "111"
  
	else :
		ans = "999"

	return ans

lines = []
var_list = []

while True:
	line = input()

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

	line = list(line.split(" "))

	if line[0] == 'add' :
		ans += "00000" + "00" #unused bits added
		if (getRegister(line[1], False) == '999' or getRegister(line[1], False) == '999' or getRegister(line[1], False) == '999') :
			print("Invalid register name")
			quit()
		x = getRegister(line[1], False) + getRegister(line[2], False) + getRegister(line[3], False)
		ans += x

	if line[0] == 'ld' :
		ans += "00100"
		x = getRegister(line[1], False) 
		if x!="999" :
			ans += x
			if line[2] in var_list :
				n = var_list.index(line[2]) + len(lines) - len(var_list)
				ans += str(f'{n:08b}')
				
			else:
				print("Use of undefined variable")
				quit()

		else :
			print("Invalid register name")
			quit()

	if (line[0] == 'st') :
		ans += "00101" 
		x = getRegister(line[1], False) 
		if x!="999" :
			ans += x
			if line[2] in var_list :
				n = var_list.index(line[2]) + len(lines) - len(var_list)
				ans += str(f'{n:08b}')
				
			else:
				print("Use of undefined variable")
				quit()

		else :
			print("Typo in register name")
			quit()

	print(ans)
	ans = ""


