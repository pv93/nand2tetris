"""
VM Translator

Parses Jack VM code into Hack assembly language.
https://www.nand2tetris.org/project07
"""
import sys
from string import Template

"""
Translates given arithmetic command to its respective assembly command
Possible commands are: 
  'add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not'
"""

### Assembly command strings/templates

# Arithmetic commands

ADD_COMMAND = """
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
M=D+M
@SP
M=M+1
"""

SUBTRACT_COMMAND = """
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
M=M-D
@SP
M=M+1
"""

NEGATE_COMMAND = """
@SP
M=M-1
A=M
M=-M
@SP
M=M+1
"""

EQUALS_COMMAND = """
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=D-M
@TRUE
D ; JEQ
@FALSE
0 ; JEQ

(TRUE)
@SP
A=M
M=0
@END
0 ; JMP

(FALSE)
@SP
A=M
M=-1
@END
0 ; JMP

(END)
@SP
M=M+1
"""

GREATER_THAN_COMMAND = """
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@TRUE
D ; JGT
@FALSE
0 ; JEQ

(TRUE)
@SP
M=0
@END
0 ; JMP

(FALSE)
@SP
A=M
M=-1
@END
0 ; JMP

(END)
@SP
M=M+1
"""

LESS_THAN_COMMAND = """
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@TRUE
D ; JLT
@FALSE
0 ; JEQ

(TRUE)
@SP
A=M
M=0
@END
0 ; JMP

(FALSE)
@SP
A=M
M=-1
@END
0 ; JMP

(END)
@SP
M=M+1
"""

AND_COMMAND = """
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
M=D&M
@SP
M=M+1
"""

OR_COMMAND = """
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
M=D|M
@SP
M=M+1
"""

NOT_COMMAND = """
@SP
M=M-1
A=M
M=!M
@SP
M=M+1
"""

# Memory segment operations

PUSH_CONSTANT_COMMAND_TMPL = Template("""
@$value
D=A
@SP
A=M
M=D
@SP
M=M+1
""")

# "Basic" memory are conceptually interchangeable memory blocks
# They include the blocks LCL, ARG, THIS, THAT
BASIC_MEMORY_COMMAND_TMPL = 

def parse_arithmetic_command(vm_command):
  print('in parse_arithmetic_command with command', vm_command)
  command_dict = {}
  command_dict['add'] = ADD_COMMAND
  command_dict['sub'] = SUBTRACT_COMMAND 
  command_dict['neg'] = NEGATE_COMMAND
  command_dict['eq'] = EQUALS_COMMAND
  command_dict['gt'] = GREATER_THAN_COMMAND
  command_dict['lt'] = LESS_THAN_COMMAND
  command_dict['and'] = AND_COMMAND
  command_dict['or'] = OR_COMMAND
  command_dict['not'] = NOT_COMMAND
  
  return command_dict[vm_command]

"""
Translates a memory command to assembly language
i.e 'push local 5' 'pop argument 2'
"""
def parse_memory_command(vm_command):
    split_command = vm_command.split(' ')
    action = split_command[0]
    segment = split_command[1]
    value = split_command[2]
    command = ""
    if segment == 'constant':
        command = PUSH_CONSTANT_COMMAND_TMPL.substitute(value=value)
    return command
        


  

def parse(vm_file_lines, output_file):
    
    ARITHMETIC_CMDS = ['add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not']
    MEMORY_CMDS = ['push', 'pop']
    BRANCHING_CMDS = ['label', 'goto', 'if-goto']
    FUNCTION_CMDS = ['function', 'call']

    for vm_command in vm_file_lines:
        if vm_command.startswith('//'):
          continue

        output_file.write('// ' + vm_command)
        vm_command = vm_command.rstrip()
        cmd = vm_command.split(' ')[0]
        print('cmd is ', cmd)
        translated_command = ''
        if cmd in ARITHMETIC_CMDS:
            print('arithmetic command in parse fn')
            translated_command = parse_arithmetic_command(vm_command)
        elif cmd in MEMORY_CMDS:
            translated_command = parse_memory_command(vm_command)
        elif cmd in BRANCHING_CMDS:
            translated_command = parse_branching_command(vm_command)
        elif cmd in FUNCTION_CMDS:
            translated_command = parse_function_command(vm_command)
        output_file.write(translated_command)

if __name__ == '__main__':
  vm_file = sys.argv[1]
  with open(vm_file, 'r') as input_file, open(vm_file.replace('.vm', '.asm'), 'w') as output_file:
      vm_file_lines = input_file.readlines()
      parse(vm_file_lines, output_file)