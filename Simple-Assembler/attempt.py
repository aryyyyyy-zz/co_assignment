from sys import stdin

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
    'j' : "Wrong syntax used for instructions"
}

a_commands = {'add': "00000",'sub': "00001", 'mul': "00110", 'xor': "01010", 'or': "01011", 'and': "01100"}
b_commands = {'mov'  : "00010", 'rs' : "01000", 'ls' : "01001"}
c_commands = {'mov' : "00011", 'div' : "00111", 'not' : "01101", 'cmp' : "01110"}  #cmp affects flag
d_commands = {'ld': "00100", 'st': "00101"}
e_commands = {'je': '10010', 'jgt': '10001', 'jlt': '10000', 'jmp': '01111'}
f_commands = {"hlt": "10011"} 

instruction_length = {'a' : 4, 'b' : 3, 'c' : 3, 'd': 3, 'e': 2, 'f': 1}







#--------------------------------------------------- HELPER FUNCTIONS ------------------------------------------------

def getRegister(reg, instruction = 'add'):
    reg_list = {'R0' : "000", 'R1' : "001", 'R2' : "010", 'R3' : "011",
    'R4' : "100", 'R5' : "101", 'R6' : "110"}

    if reg in reg_list.keys():
        ans = reg_list[reg]
    
    elif reg == 'FLAGS':
        if instruction == "mov":
            ans = '111'
        else:
            print(errors['d'])
            quit()
    
    else:
        print(errors['a'])
        quit()

    return ans







#--------------------------------------------------- COMMAND HANDLERS -------------------------------

def handle_a(cmd): #cmd = ["sub", "R1", "R2", "R3"]
    ans = ""
    ans += a_commands[cmd[0]] + "00" #unused bits added
    ans += getRegister(cmd[1]) + getRegister(cmd[2]) + getRegister(cmd[3])
    print(ans)

def handle_mov(cmd): #mov R1 #imm | mov R1 R2 | mov R1 FLAGS
    ans = ""

    if cmd[2][0] == '$':
        ans += "00010" + getRegister(cmd[1])
        s = cmd[2][1:]
        if s.isnumeric():
            if(0<=int(s)<=255):
                ans+=str(f'{int(s):08b}')
            else:
                print(errors['e'])
                quit()
        else:
            print(errors['a'])
            quit()

    else:
        ans += "00011" + "00000" + getRegister(cmd[1]) + getRegister(cmd[2], 'mov')

    print(ans)

def handle_b(cmd):
    ans = ""
    if cmd[2][0] == '$':
        ans += b_commands[cmd[0]] + getRegister(cmd[1])
        s = cmd[2][1:]
        if s.isnumeric():
            if(0<=int(s)<=255):
                ans+=str(f'{int(s):08b}')
            else:
                print(errors['e'])
                quit()
        else:
            print(errors['a'])
            quit()
    else:
        print(errors['j'])
        quit()
    print(ans)

def handle_c(cmd):
    ans = c_commands[cmd[0]] + "00000" + getRegister(cmd[1]) + getRegister(cmd[2], 'mov')
    print(ans)
    
def handle_d(cmd, variables, instructionSize): #st R4 xyz
    ans = ""
    ans += d_commands[cmd[0]] + getRegister(cmd[1])
    if cmd[2] in variables:
        n = variables.index(cmd[2]) + instructionSize
        ans += str(f'{n:08b}')
    else :
        print(errors['b'])
        quit()
    print(ans)

def handle_e(line, labels):
    ans = ''
    ans += e_commands[line[0]] + '000'
    if str(line[1]) in labels.keys():
        ans += str(f'{int(labels[line[1]]):08b}')
    else:
        print(errors['a'])
        quit()
    print(ans)

    

#def setFlag: 
#def getFlag:






# -------------------------------------- VARIABLES ---------------------------------------------------
lines = []
variables = []
labels = {}





# --------------------------------------------- HANDLING INPUT --------------------------------------

for inp in stdin:
    if inp == '':
        break
    lines.append(inp)

# while True:
#     inp = input()
#     if inp == '':
#         break
#     lines.append(inp)
    

for line in lines:
    line = line.split(' ')
    
    if line[0] == 'var':
        if len(line) != 2:
            print(errors['j'])
            quit()
        variables.append(line[1])
    else:
        break
        
#print(variables)

lines = lines[len(variables):]


for i in range(len(lines)):
    lines[i] = list(lines[i].split(' '))
    if lines[i][0][-1] == ':':
        labels[lines[i][0][:-1]] = i
        lines[i] = lines[i][1:]


# ----------------------------------------- MAIN LOOP -------------------------------------
for line in lines:

    # A COMMANDS
    if line[0] in a_commands.keys():
        if len(line) != instruction_length['a']:
            print(errors['j'])
            quit()
            
        handle_a(line)

    
    # MOV COMMAND
    elif line[0] == 'mov':
        if len(line) != instruction_length['b']:
            print(errors['j'])
            quit()
        handle_mov(line)
        
    
    # B COMMANDS
    elif line[0] in b_commands.keys():
        if len(line) != instruction_length['b']:
            print(errors['j'])
            quit()
            
        handle_b(line)
    
    # C COMMANDS
    elif line[0] in c_commands.keys():
        if len(line) != instruction_length['c']:
            print(errors['j'])
            quit()
            
        handle_c(line)
    
    # D COMMANDS
    elif line[0] in d_commands.keys():
        if len(line) != instruction_length['d']:
            print(errors['j'])
            quit()
            
        handle_d(line, variables, len(lines))


    # E COMMANDS
    elif line[0] in e_commands.keys():
        if len(line) != instruction_length['e']:
            print(errors['a'])
            quit()
        handle_e(line, labels)

    

    # F COMMANDS
    elif line[0] in f_commands.keys():
        if lines.index(line) == len(lines) - 1:
            if len(line) != 1:
                print(errors['j'])
                quit()
            
            print(f_commands[line[0]] + "0"*11)
        else:
            print(errors['i'])
            quit()
        
  
    # INVALID COMMAND ERROR
    else:
        print(errors['a'])   
        quit()
        








	






