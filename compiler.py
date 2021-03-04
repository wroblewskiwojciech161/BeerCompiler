# Wojciech Wróblewski 250349 kompilator 


import sys
from parser import OneBeerLexer, OneBeerParser
from methods import Methods
from errors import Errors

error = Errors()
argument = sys.argv
length_arguments = len(argument)
if length_arguments < 3:
    error.run_error()

file_in = sys.argv[1]
file_out = sys.argv[2]
lexer = OneBeerLexer()
parser = OneBeerParser()

with open(file_in) as file:
    text = file.read()
    parse_tree = parser.parse(lexer.tokenize(text))
    machine = Methods(parse_tree,file_out)
    machine.get_assembler()




