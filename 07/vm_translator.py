"""
VM Translator

Parses Jack VM code into Hack assembly language.
https://www.nand2tetris.org/project07
"""
import sys

vm_file = sys.argv[0]

def parse_arithmetic_command(vm_command):
  ADD_COMMAND="""
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
  SUBTRACT_COMMAND="""
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
  NEGATE_COMMAND="""
  @SP
  M=M-1
  A=M
  M=-M
  @SP
  M=M+1
  """
  EQUALS_COMMAND="""
  @SP
  M=M-1
  A=M
  D=M
  @SP
  M=M-1
  D=D-M
  @TRUE
  D ; JEQ
  @FALSE
  0 ; JEQ
  
  (TRUE)
  @SP
  M=0
  @END
  0 ; JMP

  (FALSE)
  @SP
  M=-1
  @END
  0 ; JMP
  
  (END)
  @SP
  M=M+1
  """

  GT_COMMAND="""
  @SP
  M=M-1
  A=M
  D=M
  @SP
  M=M-1
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
  M=-1
  @END
  0 ; JMP
  
  (END)
  @SP
  M=M+1
  """
  LT_COMMAND="""
  @SP
  M=M-1
  A=M
  D=M
  @SP
  M=M-1
  D=M-D
  @TRUE
  D ; JLT
  @FALSE
  0 ; JEQ

  (TRUE)
  @SP
  M=0
  @END
  0 ; JMP

  (FALSE)
  @SP
  M=-1
  @END
  0 ; JMP
  
  (END)
  @SP
  M=M+1
  """
  AND_COMMAND="""
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
  OR_COMMAND="""
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
  NOT_COMMAND="""
  @SP
  M=M-1
  A=M
  M=!M
  @SP
  M=M+1
  """
  

def parse(vm_file_lines, output_file):
    
    ARITHMETIC_CMDS = ['ADD', 'SUB', 'NEG', 'EQ', 'GT', 'LT', 'AND', 'OR', 'NOT']
    MEMORY_CMDS = ['PUSH', 'POP']
    BRANCHING_CMDS = ['LABEL', 'GOTO', 'IF-GOTO']
    FUNCTION_CMDS = ['FUNCTION', 'CALL']

    for vm_command in vm_file_lines:
        output_file.write('// ' + vm_command)
        cmd = vm_command.split(' ')[0].upper()
        if cmd in ARITHMETIC_CMDS:
            parse_arithmetic_command(vm_command)
        elif cmd in MEMORY_CMDS:
            parse_memory_command(vm_command)
        elif cmd in BRANCHING_CMDS:
            parse_branching_command(vm_command)
        elif cmd in FUNCTION_CMDS:
            parse_function_command(vm_command)

with open(vm_file, 'r') as input_file, open(vm_file.replace('.vm', '.asm'), 'w') as output_file:
    vm_file_contents = input_file.readlines()
    parse(vm_file_contents, output_file)