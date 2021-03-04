class Errors():
    
    def wrong_array_declaration(self,line):
        print("Error: wrong array declaration in line " + str(line))
        exit(0);
    def redeclaration(self,line):
        print("Error: redeclaration in line " +str(line) +", variable already declared in the scope. May use undefined identifier" )
        exit(0);
    def assign_int(self,line):
        print("Error: assign error, unknown assign type in line "+str(line) )
        exit(0);
    def assign_tab(self,line):
        print("Error: assign error, unknown assign type in line "+str(line) )
        exit(0);
    def write_error(self,line):
        print("Error: write error, unknown type suggested to be written in line "+str(line) )
        exit(0);
    def wrong_exp_type(self,line):
        print("Error: expression error, unknown type for calculations in line "+str(line) )
        exit(0);
    def unsupported_operation(self,line):
        print("Error: expression error, unsupported operation in line "+str(line) )
        exit(0);
    def iterator_modification(self,line):
        print("Error: cannot modify iterator  in line "+str(line) )
        exit(0);
    def unknown_variable(self,line):
        print("Error: unknown  variable in line : "+str(line) )
        exit(0);
    def read_error(self,line):
        print("Error: while reading value. Cannot read constant: "+str(line) )
        exit(0);
    def assignment_error(self,line):
        print("Error: while assign operation. Unknown assignment type in line "+str(line) )
        exit(0);
    def error_while_creating_iterator(self,line):
        print("Error: error while creating loop iterator "+str(line) )
        exit(0);
    def run_error(self):
        print("Error: Please make sure u tried to run program like python3 kompilator.py <in> <out>")
        exit(0);
    def unknown_type(self,line):
        print("Error: Unknown variable type in line "+str(line) )
        exit(0);
    def undeclared_variable(self,line):
        print("Error: Undeclared variable  in line "+str(line) )
        exit(0);
    def undeclared_table(self,line):
        print("Error: Undeclared table  in line "+str(line) )
        exit(0);
    def wrong_table_index(self,line):
        print("Error: Trying to  access wrong table index  ")
        exit(0);
    def usage_undeclared_var(self,line):
        print("Error: Trying to access undeclared variable in line "+str(line))
        exit(0);
    def usage_uninitialized_var(self,line):
        print("Error: Trying to use uninitialized variable in line "+str(line))
        exit(0);
    def wrong_syntax(self,line):
        print("Error: Wrong syntax  in line "+str(line))
        exit(0);
    def iterator_in_bounds(self,line):
        print("Error: Cannot use iterator variable as a boundry of loop iterations in line "+str(line))
        exit(0);
    def undeclared_var_in_loop_bounds(self):
        print("Error: Undeclared var in loop bounds ")
        exit(0);
    
    
    

