from instructions import RegisterInstructions
from register import Register
from objects import Variable,Table,Number
from errors import Errors
import string 
import random

"""
Main class with implementation of all commands and 
expressions defined in grammar. Based on instructions
from instructions file, generates output code into file
"""

class Methods():

    def __init__(self, ast,output_name):
        self.output_name =output_name
        #if set to true, remains labels 
        self.debug = False

        self.a = None
        self.b = None
        self.c = None
        self.d = None
        self.e = None
        self.f = None

        self.types={}
        self.types['var']='int'
        self.types['number']='number'
        self.types['table'] = 'table'
        self.counter = 0
        
        #access to errors
        self.error = Errors()
        self.iterators ={}
        # indicates next address to assign
        self.ptr = 4
        self.load_registers()
        self.parse_tree = ast
        self.variables = self.get_variables()
        self.declarations = self.variables.keys()
        self.decoder = RegisterInstructions()
        self.assembler = self.decoder.get_assembler()
        self.commands = ast[2]
        # help addresses to swap or for temporary storage
        self.help1 = 0
        self.help2 = 1
        self.help3 = 2
        self.help4 = 3
        ##############
        self.storeNumberInVariables('1','')
      
    
 
    def load_registers(self):
        self.a = Register("a", self.ptr)
        self.ptr += 1
        self.b = Register("b", self.ptr)
        self.ptr += 1
        self.c = Register("c", self.ptr)
        self.ptr += 1
        self.d = Register("d", self.ptr)
        self.ptr += 1
        self.e = Register("e", self.ptr)
        self.ptr += 1
        self.f = Register("f", self.ptr)
        self.ptr += 1
   

    ############################################33
    # load declarations / arrays/ variables
    ##############################################3
    def get_variables(self):
        declarations = []
        dict = {}
        def get_arr(t):
            arr = list(t)
            if isinstance(arr[0], str) == False:
                del arr[0]
            return arr

        def go_rec(tree):
            copy = tree
            declarations.append(get_arr(tree))
            if isinstance(tree[0], tuple):
                go_rec(tree[0])

        go_rec(self.parse_tree[1])

        for declaration in declarations:
           
            declaration_id = declaration[1]
            if declaration_id in dict.keys():
                if declaration[0] ==  self.types['table']:
                     line = declaration[4]
                else :
                     line = declaration[2]
                self.error.redeclaration(line)
            else:
                # array declaration
                if declaration[0] ==  self.types['table']:
                    line = declaration[4]
                    # wrong table declaration
                    if int(declaration[2]) > int(declaration[3]):
                       
                        self.error.wrong_array_declaration(line)
                    else:
                       
                        first = int(declaration[2])
                        last = int(declaration[3])
                        table = Table(declaration_id,first,last)

                        table.first_address_id = self.ptr
                        self.ptr += table.length - 1
                        table.last_address_id = self.ptr
                        self.ptr = self.ptr + 1
                        dict[table.name] = table
                       
                else:
                    variable = Variable(declaration_id)
                    variable.address = self.ptr
                    self.ptr += 1
                    dict[variable.name] = variable
        return dict

    def compile(self):
        self.assembly()

    #############################################33
    # UTILS methods
    ##############################################3


    def get_assembler(self):

        commands = self.parse_tree[2:][0]
        for command in commands:
            self.match_action(command)
       
        self.assembler.append("HALT")
        self.clear_assembly_code(self.assembler,self.debug)
        f = open(self.output_name, "w")
        for a in self.assembler:
            f.write(str(a)+'\n')
        f.close()
    
    def add_var_to_variables(self,name):
        variable = Variable(name)
        self.ptr += 1
        variable.address = self.ptr
        self.variables[variable.name] = variable

    def check_if_correct_tab_index(self,tab_name,idx):
        obj = self.variables[tab_name]
        start = obj.first
        end   = obj.last
        if not int(start) <= idx <= int(end):
            self.error.wrong_table_index("")
            
    def remove_variable_from_variables(self,name):
        self.variables.pop(name,None)

    def setValueInRegister(self,register,value):
        self.set_number_in_register(register.name,value)
        #self.decoder.STORE(register.name,register.name)

    
    def setAddressInRegister(self,register,memory_cell):
        register.address = memory_cell
        self.set_number_in_register(register.name,memory_cell)

    def getVarAddress(self,name):
        obj = self.variables[str(name)]
        return obj.address

    def getNumberAddress(self,name):
        obj = self.variables[str(name)]
        return obj.get_address()

    def set_number_in_register(self, reg, number, bound = 5):
            
        self.decoder.RESET(reg)
        temp = []
        number = int(number)
        while number > bound:
            if number % 2:
                number -= 1
                temp.append(self.decoder.INC(reg,False))
            else:
                number = number // 2
                temp.append(self.decoder.SHL(reg,False))

        while number > 0 :
            number -= 1
            temp.append(self.decoder.INC(reg,False))

        temp.reverse()
        self.decoder.executeList(temp)

    def loadValueOfAddressToRegister(self,address,register):
        self.setValueInRegister(self.f,int(address))
        self.decoder.LOAD(register,self.f.name)

    def printValueOfAddress(self,address):
        self.loadValueOfAddressToRegister(address,self.a)
        self.decoder.STORE(self.a.name,self.f.name)
        self.decoder.PUT(self.f.name)

    def storeNumberInVariables(self, value,line):
        if value in self.variables.keys():
            self.error.redeclaration(str(line))

        self.ptr = self.ptr + 1
        addr = self.ptr
        obj = Number(value)
        obj.value = int(value)
        obj.address = addr
        self.variables[value] =obj
        self.setValueInRegister(self.b,int(value))
        self.setValueInRegister(self.c,addr)
        self.decoder.STORE(self.b.name,self.c.name)

    
    # based on index  number or variable  return its addr in b register
    def set_table_address_in_B(self,tab_name,value):

        obj = self.variables[tab_name]
        # get the address of fires tab value
        first_address = obj.get_first_address()
        first_idx = obj.first
        variable_address = self.getVarAddress(value)
        self.setValueInRegister(self.e,first_idx)
        self.loadValueOfAddressToRegister(variable_address,self.d.name)
        #off set
        self.decoder.SUB(self.d.name,self.e.name)
        # add offset and strign address for particular array
        # store res in b
        self.setValueInRegister(self.b,first_address)
        self.decoder.ADD(self.b.name,self.d.name)
   

    ################################################
    # READ
    ################################################

    def read(self,command):
        self.decoder.RESET(self.b.name)
        self.decoder.RESET(self.c.name)
        self.decoder.RESET(self.d.name)
        self.decoder.RESET(self.f.name)
        self.decoder.RESET(self.e.name)
        self.decoder.RESET(self.a.name)
        # read to a
        line = command[2]
        type = command[1][0]
        self.set_var_declared(command[1][1],line)
        if type == self.types['var']:
      
            variable_name = command[1][1]
            if variable_name not in self.variables.keys():
                self.error.undeclared_variable(line)
            # ustawiam rejest a na wartosc adresu int var
            addr = self.getVarAddress(variable_name)
            self.setAddressInRegister(self.a,addr)
            # czytam do tego adresu
            self.decoder.GET(self.a)

        # tab
        elif type == self.types['table'] :
            tab_name = command[1][1]
            if command[1][2][0] ==  self.types['number']:
            
                value = command[1][2][1]
                tab_name = command[1][1]

                if tab_name not in self.variables.keys():
                    self.error.undeclared_table(line)

                self.check_if_correct_tab_index(tab_name,int(value))

                if value not in self.variables.keys():
                    self.storeNumberInVariables(value,line)
                self.set_table_address_in_B(tab_name,value)
                # now in b we got proper tab(n) address 
                # so we can GET into it
                self.decoder.GET(self.b)
                self.decoder.RESET(self.b.name)

            #int
            else :
                
                line = command[2]
                variable_name = command[1][2][1]
                tab_name = command[1][1]

                if tab_name not in self.variables.keys():
                    self.error.undeclared_table(line)

                if variable_name not in self.variables.keys():
                    self.error.unknown_variable(line)

                self.set_table_address_in_B(tab_name,variable_name)
                # now in b we got proper tab(n) address 
                # so we can GET into it
                self.decoder.GET(self.b)
                self.decoder.RESET(self.b.name)

        else :
            self.error.read_error(line)

    #############################################33
    # WRITE 
    ##############################################3

    def write(self,command):
        line = int(command[2])
        type = command[1][0]
        id = command[1][1]
        self.decoder.RESET(self.b.name)
        self.decoder.RESET(self.c.name)
        self.decoder.RESET(self.d.name)
        self.decoder.RESET(self.f.name)
        self.decoder.RESET(self.e.name)
        self.decoder.RESET(self.a.name)
        
        # int var
        if type ==self.types['var']:

            self.check_var_declared(id,line)
        
            # get address of a variavle
            addr = self.getVarAddress(id)
            # set address as a value of register a
            self.setValueInRegister(self.a,addr)
            self.decoder.LOAD(self.b.name,self.a.name)
            # store in b
            self.decoder.STORE(self.b.name,self.f.name)
            # write
            self.decoder.PUT(self.f.name)
        #tab
        elif type ==  self.types['table']:
            tab_name = command[1][1]
            line = command[2]

            
            #  tab with int variable alike tab(n)
            if command[1][2][0] == self.types['var']:
                variable_name = command[1][2][1]
                if variable_name not in self.variables.keys():
                    self.error.unknown_variable(line)
                #get address of particual element
                self.set_table_address_in_B(tab_name,variable_name)
                self.decoder.LOAD(self.d.name,self.b.name)
                self.decoder.STORE(self.d.name,self.c.name)
                self.decoder.PUT(self.c.name)
            
            else :
                index_value = command[1][2][1]
                if index_value not in self.variables.keys():
                    self.storeNumberInVariables(index_value,line)
                self.check_if_correct_tab_index(tab_name,int(index_value))
                #get address of particual element
                self.set_table_address_in_B(tab_name,index_value)
                self.decoder.LOAD(self.d.name,self.b.name)
                self.decoder.STORE(self.d.name,self.c.name)
                self.decoder.PUT(self.c.name)

                
        elif type ==  self.types['number']:
            # set numeric value in a register b
            self.setValueInRegister(self.b,int(command[1][1]))
            # do write we have to store it in helper memory slot and then
            # invoke by its address
            # load value of helper addres into c
            self.setValueInRegister(self.c,self.help1)
            # store numeric value in help addres
            self.decoder.STORE(self.b.name,self.c.name)
            # now we can invoke put on helper address to write number
            self.decoder.PUT(self.c.name)
            self.decoder.RESET(self.b.name)
        else :
            self.error.write_error(line)

    #######################################################
    # Expressions
    #######################################################
    def addition(self):
        # left ->  a register
        # right -> c register

        self.decoder.RESET(self.b.name)
        self.decoder.LOAD(self.b.name,self.a.name)
        self.decoder.LOAD(self.a.name,self.c.name)
        self.decoder.ADD(self.b.name,self.a.name)
    
    def exp_subtraction(self):
       
        self.decoder.RESET(self.b.name)
        self.decoder.LOAD(self.b.name,self.a.name)
        self.decoder.LOAD(self.a.name,self.c.name)
        self.decoder.SUB(self.b.name,self.a.name)
    
    def multiplication(self): 
        labels = self.get_label_dict(4)
        self.decoder.LOAD(self.a.name,self.a.name)
        self.decoder.LOAD(self.c.name,self.c.name)
        self.decoder.RESET(self.b.name)
        self.decoder.setLabel(labels[1])
        self.decoder.JZERO(self.c.name,labels[4])
        self.decoder.JODD(self.c.name,labels[3])
        self.decoder.setLabel(labels[2])
        self.decoder.SHR(self.c.name)
        self.decoder.ADD(self.a.name,self.a.name)
        self.decoder.JUMP(labels[1])
        self.decoder.setLabel(labels[3])
        self.decoder.ADD(self.b.name,self.a.name)
        self.decoder.JUMP(labels[2])
        self.decoder.setLabel(labels[4])
                     
    def division(self,register):
          
        labels = self.get_label_dict(7)
        self.decoder.LOAD(self.d.name,self.a.name)
        self.decoder.LOAD(self.c.name,self.c.name)
        self.decoder.RESET(register.name)
        self.decoder.JZERO(self.c.name,labels[7])
        self.decoder.RESET(self.e.name)
        self.decoder.ADD(self.e.name,self.c.name)
        self.decoder.RESET(register.name)
        self.decoder.addLabel(labels[2])
        self.decoder.ADD(register.name,self.e.name)
        self.decoder.SUB(register.name,self.d.name)
        self.decoder.JZERO(register.name,2)
        self.decoder.JUMP(labels[3])
        self.decoder.SHL(self.e.name)
        self.decoder.JUMP(labels[2])
        self.decoder.addLabel(labels[3])
        self.decoder.RESET(register.name)
        self.decoder.addLabel(labels[1])
        self.decoder.RESET(self.f.name)
        self.decoder.ADD(self.f.name,self.e.name)
        self.decoder.SUB(self.f.name,self.d.name)
        self.decoder.JZERO(self.f.name,labels[6])
        self.decoder.SHL(register.name)
        self.decoder.SHR(self.e.name)
        self.decoder.JUMP(labels[5])
        self.decoder.addLabel(labels[6])
        self.decoder.SHL(register.name)
        self.decoder.INC(register.name)
        self.decoder.SUB(self.d.name,self.e.name)
        self.decoder.SHR(self.e.name)
        self.decoder.addLabel(labels[5])
        self.decoder.RESET(self.f.name)
        self.decoder.ADD(self.f.name,self.c.name)
        self.decoder.SUB(self.f.name,self.e.name)
        self.decoder.JZERO(self.f.name,labels[1])
        self.decoder.addLabel(labels[7])

    # returns dict of labels
    # predefined number of labels needed
    def get_label_dict(self,amount):
        labels = {}
        for i in range(1,amount+1):
            labels[i] = self.injectAsmLabel()

        return labels

    def modulo(self):

        labels = self.get_label_dict(4)

        # by default operating data stored in a,c addresses
        # load them into b and d
        self.decoder.LOAD(self.d.name,self.a.name)
        self.decoder.LOAD(self.c.name,self.c.name)
        # by rules mod 0 is zero if right side value
        # is zero then jump and return 0
        self.decoder.JZERO(self.c.name,labels[4])
        self.decoder.RESET(self.e.name)
        self.decoder.ADD(self.e.name,self.c.name)
        self.decoder.addLabel(labels[1])
        self.decoder.RESET(self.b.name)
        self.decoder.ADD(self.b.name,self.e.name)
        self.decoder.SUB(self.b.name,self.d.name)
        self.decoder.JZERO(self.b.name,2)
        self.decoder.JUMP(3)
        self.decoder.ADD(self.e.name,self.e.name)
        self.decoder.JUMP(labels[1])
        self.decoder.RESET(self.b.name)
        self.decoder.RESET(self.f.name)
        self.decoder.addLabel(labels[3])
        self.decoder.ADD(self.f.name,self.e.name)
        self.decoder.SUB(self.f.name,self.d.name)
        self.decoder.JZERO(self.f.name,4)
        self.decoder.ADD(self.b.name,self.b.name)
        self.decoder.SHR(self.e.name)
        self.decoder.JUMP(labels[2])
        self.decoder.ADD(self.b.name,self.b.name)
        self.decoder.INC(self.b.name)
        self.decoder.SUB(self.d.name,self.e.name)
        self.decoder.SHR(self.e.name)
        self.decoder.addLabel(labels[2])
        self.decoder.RESET(self.f.name)
        self.decoder.ADD(self.f.name,self.c.name)
        self.decoder.SUB(self.f.name,self.e.name)
        self.decoder.JZERO(self.f.name,labels[3])
        self.decoder.JUMP(2)
        self.decoder.addLabel(labels[4])
        self.decoder.RESET(self.d.name)
        self.decoder.RESET(self.b.name)
        self.decoder.ADD(self.b.name,self.d.name)


    def undeclared_check(self,data,register,setbound = False):
           
        type = data[0]
        if type ==  self.types['number']:
            line = data[2]
            value = data[1]
            if value not in self.variables.keys():
                self.storeNumberInVariables(value,line)
        elif type == self.types['var']:
            line = data[2]
            value = data[1]
            self.check_var_declared(value,line)

        elif type ==  self.types['table']:
            line = data[3]
            tab_name = data[1]
            index_value = data[2][1]
            index_type = data[2][0]
            # check if index in variables
            if index_type ==  self.types['number'] :
                if index_value not in self.variables.keys():
                    self.storeNumberInVariables(index_value,line)
                self.check_if_correct_tab_index(tab_name,int(index_value))
            elif index_type == self.types['var'] :
                self.check_var_declared(index_value,line)
                
            else:
                self.error.unknown_type(line)


           

    def store_address_in_register(self,data,register,setbound = False):
        self.decoder.RESET(register.name)
       
        type = data[0]
        if type ==  self.types['number']:
            value = data[1]
            line = data[2]
            if value not in self.variables.keys():
                self.storeNumberInVariables(value,line)

            address =  self.getNumberAddress(value)
            self.setValueInRegister(register,address)
        elif type == self.types['var']:
            line = data[2]
            value = data[1]
            self.check_var_declared(value,line)


            address =  self.getVarAddress(value)
            self.setValueInRegister(register,address)

        elif type ==  self.types['table']:
            line = data[3]
            tab_name = data[1]
            index_value = data[2][1]
            index_type = data[2][0]
            # check if index in variables
            if index_type ==  self.types['number'] :
                if index_value not in self.variables.keys():
                    self.storeNumberInVariables(index_value,line)
                self.check_if_correct_tab_index(tab_name,int(index_value))
            elif index_type == self.types['var'] :
                self.check_var_declared(index_value,line)
                
            else:
                self.error.unknown_type(line)


            # get  object of array from variables
            obj = self.variables[tab_name]
            # get the address of fires tab value
            first_address = obj.get_first_address()
            first_idx = obj.first
            variable_address = self.getVarAddress(index_value)
            self.setValueInRegister(self.e,first_idx)
            self.loadValueOfAddressToRegister(variable_address,self.d.name)
            #off set
            self.decoder.SUB(self.d.name,self.e.name)
            # add offset and strign address for particular array
            # store res in b
            self.setValueInRegister(register,first_address)
            self.decoder.ADD(register.name,self.d.name)

      
    def calculate_expression(self,command):
 
        # set left side address in a register avlue 
        # set right side address in c register value
        operator = command[0]
        line = command[3]
        left = command[1]
        right = command[2]
        # store numer as variable to have access later
     
        self.store_address_in_register(command[1],self.a)
        self.store_address_in_register( command[2],self.c)
        if operator == '+':
            self.addition()
        elif operator == '-':
            self.exp_subtraction()
        elif operator == '*':
            self.multiplication()
        elif operator == '/':
            self.division(self.b)
        elif operator == '%':
            self.modulo()
        else :
            self.error.unsupported_operation(line)

    def check_var_declared(self,name,line):
        if name not in self.variables.keys():
            self.error.usage_undeclared_var(line)

        var_obj = self.variables[name]
        if var_obj.declared == False:
            self.error.usage_uninitialized_var(line)
   

    def set_var_declared(self,name,line):
        if name not in self.variables.keys():
            self.error.usage_undeclared_var(line)

        var_obj = self.variables[name]
        var_obj.declared = True

    def type_check(self,name,type,line):
        if name not in self.variables.keys():
            self.error.usage_undeclared_var(line)
        obj = self.variables[name]
        if obj.type != type:
            self.error.wrong_syntax(line)
        

    def assign(self, command):
        self.decoder.RESET(self.b.name)
        self.decoder.RESET(self.c.name)
        self.decoder.RESET(self.d.name)
        self.decoder.RESET(self.f.name)
        self.decoder.RESET(self.e.name)
        self.decoder.RESET(self.a.name)
        line = command[3]
        left_id = command[1][1]
        left_type = command[1][0]
        right_id = command[2][1]
        right_type = command[2][0]
        self.type_check(left_id,left_type,line)
           
        if left_type == self.types['var']:

            self.set_var_declared(left_id,line)
         
            # check if it is iterator if not u can try modyfying
            if self.variables[left_id].iterator == False :
                if right_type == self.types['number']:
                    #get value to assign
                    value = command[2][1]
                    # get variable addres from memory
                    addr = self.getVarAddress(left_id)
                    # set value in b register
                    self.setValueInRegister(self.b,value)
                    # set address as value of c register 
                    self.setValueInRegister(self.c,addr)
                    # store value in memory addres of variable
                    self.decoder.STORE(self.b.name,self.c.name)
                    
                elif right_type == self.types['var']:
                    #error
                    self.type_check(right_id,right_type,line)
                    self.check_var_declared(right_id,line)
                     
                    addr = self.getVarAddress(right_id)
                    addl = self.getVarAddress(left_id)
                    # set value of right side  addres in b register
                    self.setValueInRegister(self.b,addr)
                    # set value of  left side addres in d register
                    self.setValueInRegister(self.d,addl)
                    # load right side variable value to c register
                    self.decoder.LOAD(self.c.name,self.b.name)
                    # store upper right side value in adres of left side stored in d
                    self.decoder.STORE(self.c.name, self.d.name)
                
                elif right_type == self.types['table']:
                    #2 cases  first table(number)
                    self.type_check(right_id,right_type,line)

                    if command[2][2][0] ==  self.types['number']:
                        tab_name = command[2][1]
                        value = command[2][2][1]
                     
                        if value not in self.variables.keys():
                            self.storeNumberInVariables(value,line)
                        variable_addr = self.getNumberAddress(value)
                        addl = self.getVarAddress(left_id)
                        self.set_table_address_in_B(tab_name,value)
                        self.decoder.LOAD(self.c.name,self.b.name)
                        self.setValueInRegister(self.d,addl)
                        self.decoder.STORE(self.c.name,self.d.name)
            
                    # case tab(n) -> tab with int variable 
                    elif command[2][2][0] == self.types['var']:

                        variable_name = command[2][2][1]
                        tab_name = command[2][1]
                        self.check_var_declared(variable_name,line)

                        addl = self.getVarAddress(left_id)
                        # set value of  left side addres in d register
                        self.setValueInRegister(self.c,addl)
                        self.set_table_address_in_B(tab_name,variable_name)
                        self.decoder.LOAD(self.d.name,self.b.name)
                        # store upper right side value in adres of left side stored in d
                        self.decoder.STORE(self.d.name, self.c.name)
                    else:
                        self.error.unknown_type(line)
                else :
                    addl = self.getVarAddress(left_id)
                    self.calculate_expression(command[2])
                    self.setValueInRegister(self.c,addl)
                    self.decoder.STORE(self.b.name,self.c.name)
            else :
                self.error.iterator_modification(line)
            
        elif left_type ==  self.types['table']:

            tab_name = command[1][1]
            index_type = command[1][2][0]
            index_value = command[1][2][1]
            line = command[3]

            self.type_check(left_id,left_type,line)
            
            # check if index in variables
            if index_type ==  self.types['number'] :
                if index_value not in self.variables.keys():
                    self.storeNumberInVariables(index_value,line)
                self.check_if_correct_tab_index(tab_name,int(index_value))
            elif index_type == self.types['var'] :
                if index_value not in self.variables.keys():
                    self.error.unknown_type(line)
            else:
                self.error.unknown_type(line)

            if right_type ==  self.types['number']:
                num_value = command[2][1]
                # get left side address in b register
                self.set_table_address_in_B(tab_name,index_value)
                #set value in d register
                self.setValueInRegister(self.d,num_value)
                self.decoder.STORE(self.d.name,self.b.name)
               
            elif right_type == self.types['var']:
                self.type_check(right_id,right_type,line)

                var_value = command[2][1]
                # check if declared and initialized 
                self.check_var_declared(var_value,line)

                var_address = self.getVarAddress(var_value)
                # get left side address in b register
                self.set_table_address_in_B(tab_name,index_value)
                #set value in d register
                self.loadValueOfAddressToRegister(var_address,self.d.name)
                self.decoder.STORE(self.d.name,self.b.name)
                
            elif right_type ==  self.types['table']:
                self.type_check(right_id,right_type,line)
                line =command[3]
             
                right_tab_name = command[2][1]
                right_type = command[2][2][0]
                right_index = command[2][2][1]
                if right_type ==self.types['var']:
                    if right_index not in self.variables.keys():
                        self.error.unknown_variable(line)
                elif right_type ==  self.types['number']:
                    if right_index not in self.variables.keys():
                        self.storeNumberInVariables(right_index,line)
                    self.check_if_correct_tab_index(right_tab_name,int(right_index))
                else :
                     self.error.unknown_variable(line)

                # get LEFT side address in b register
                self.set_table_address_in_B(tab_name,index_value)
                self.setValueInRegister(self.f,1)
                self.decoder.STORE(self.b.name,self.f.name)
                # get RIGHT side address in b register
                self.set_table_address_in_B(right_tab_name,right_index)
                self.decoder.LOAD(self.c.name,self.b.name)
                self.setValueInRegister(self.f,1)
                self.decoder.LOAD(self.d.name,self.f.name)
                self.decoder.STORE(self.c.name,self.d.name)

            else : 
                # get LEFT side address in b register
                self.set_table_address_in_B(tab_name,index_value)
                self.setValueInRegister(self.f,1)
                self.decoder.STORE(self.b.name,self.f.name)
                expression = command[2]
                # store result of expression in b 
                self.calculate_expression(expression)
                self.setValueInRegister(self.f,1)
                #we got left addres in c 
                self.decoder.LOAD(self.c.name,self.f.name)
                # store result of expression in  left assign address
                self.decoder.STORE(self.b.name,self.c.name)
    
        else:
            self.error.assignment_error(line)
 
                
    # conditions evaluated at addresses stored in a and c
    def conditions(self,operand):
            # store in B
            if operand == '>=':
                # if sub(b + 1, d) != 0 , then b >= d
                self.decoder.LOAD(self.b.name,self.a.name)
                self.decoder.LOAD(self.d.name,self.c.name)
             
                self.decoder.INC(self.b.name)
                self.decoder.SUB(self.b.name,self.d.name)

            elif operand == '>':
                # if sub(b, d) != 0 , then b > d

                self.decoder.LOAD(self.b.name,self.a.name)
                self.decoder.LOAD(self.d.name,self.c.name)
                self.decoder.SUB(self.b.name,self.d.name)

            elif operand == '<=':
                # reverse greater or equal
                self.decoder.LOAD(self.b.name,self.a.name)
                self.decoder.LOAD(self.d.name,self.c.name)
                self.decoder.INC(self.d.name)
                self.decoder.SUB(self.d.name,self.b.name)
                self.decoder.STORE(self.d.name,self.f.name)
                self.decoder.LOAD(self.b.name,self.f.name)

            elif operand == '<':
                # reverse reverse greater
                self.decoder.LOAD(self.b.name,self.a.name)
                self.decoder.LOAD(self.d.name,self.c.name)
                self.decoder.SUB(self.d.name,self.b.name)
                self.decoder.STORE(self.d.name,self.f.name)
                self.decoder.LOAD(self.b.name,self.f.name)

            elif operand == '!=':
                # if sub(b,d) + sub(d,b) != 0 then b != d
                self.decoder.LOAD(self.b.name,self.a.name)
                self.decoder.LOAD(self.d.name,self.c.name)
                self.decoder.LOAD(self.e.name,self.a.name)

                self.decoder.SUB(self.b.name,self.d.name)
                self.decoder.SUB(self.d.name,self.e.name)
                self.decoder.ADD(self.b.name,self.d.name)

            elif operand == '=':
                labels = self.get_label_dict(2)
                self.decoder.LOAD(self.b.name,self.a.name)
                self.decoder.LOAD(self.d.name,self.c.name)
                self.decoder.STORE(self.d.name,self.e.name)
                self.decoder.LOAD(self.f.name,self.e.name)
                self.decoder.SUB(self.f.name,self.b.name)
                self.decoder.SUB(self.b.name,self.d.name)
                self.decoder.ADD(self.b.name,self.f.name)
                self.decoder.JZERO(self.b.name,labels[1])
                self.decoder.RESET(self.b.name)
                self.decoder.JUMP(labels[2])
                self.decoder.setLabel(labels[1])
                self.decoder.INC(self.b.name)
                self.decoder.addLabel(labels[2])

    def clear_assembly_code(self, asembler , debug = False):
            
            if debug == False :

                base = "LABEL"
                l = len(base)
                storage = {}

                def check_if_label(instruct):
                    #this is label
                    if instruct[:l] == base:
                        return True
                    else :
                        return False

                def get_label(instruct):
                
                    first_idx = instruct.index(base)
                    return instruct[first_idx :]

                def label_into_lineidx(instruct,label,current):
                    return  instruct.replace(label, str(storage[label]-current)).strip()
                    
                k = 0
                j = 0
        
                while len(asembler) > k:  
                    if check_if_label(asembler[k]):
            
                        storage[asembler[k]] = k
                        asembler.remove(asembler[k])
                    else:
                        k += 1
                m = len(asembler)
                n = 0
                while n < m:
                    instruct = asembler[n]
                    if base in instruct:
                        label = get_label(instruct)
                        asembler[j] = label_into_lineidx(instruct,label,j)
                    j += 1
                    n += 1
            else :
                print(">DEBUG")

            
    def injectAsmLabel(self):
        self.counter += 1
        self.decoder.createLabel(self.counter)
        return "LABEL"+str(self.counter)

    def if_statement(self, command):
        
        cond = command[1]
        actions = command[2]
        op = cond[0]
        labels = self.get_label_dict(1)
        line = cond[3]
        left = cond[1]
        right = cond[2]
        self.store_address_in_register(left,self.a)
        self.store_address_in_register(right,self.c)
        self.conditions(op)
        self.decoder.JZERO(self.b.name, labels[1])
        for a in actions:
            self.match_action(a)
        
        self.decoder.addLabel(labels[1])


    def if_else_statement(self, command):

        line = command[4]
        else_inner_operations = command[3]
        if_inner_operations = command[2]
        condition_statement = command[1]
        labels = self.get_label_dict(2)
        left = condition_statement[1]
        right = condition_statement[2]
        self.store_address_in_register(left,self.a)
        self.store_address_in_register(right,self.c)
        # result of condition stored in b 
        self.conditions(condition_statement[0])
        # if condition is false  jummp to label 2 and do else command
        # if condition is true do id command and jump to end label
        self.decoder.JZERO(self.b.name, labels[2])
        for a in if_inner_operations:
            self.match_action(a)
        self.decoder.JUMP(labels[1])
        self.decoder.addLabel(labels[2])
        for a in else_inner_operations:
            self.match_action(a)
        self.decoder.addLabel(labels[1])


    # generatues special variable name that will be used for
    # storing upper or lower bound of iterations  in LOOPS
    def generate_bound_var_id(self,iterator_object,type,line):
        if type == "upper":
            base = str(iterator_object.name)+"_upper"
            while base in self.variables.keys():
                base += random.choice(string.ascii_letters)
        elif type == "lower":
            base = str(iterator_object.name)+"lower"
            while base in self.variables.keys():
                base += random.choice(string.ascii_letters)

        else :
            self.error.error_while_creating_iterator(line)
        return base
                


    def for_loop_with_to(self,command):
       
        line = command[5]
        iterator = command[1]
        inner_commands = command[4]
        labels = self.get_label_dict(2)
       
        start_value_address = command[2]
        end_value_address = command[3]

        # check declarations, case when current bounds are undeclared
        # or bound is the same as current iterator
        self.undeclared_check(end_value_address,self.a,True)
        self.undeclared_check(start_value_address,self.c,True)

        # define iterator in varialbes as long as for executes if possible
        if iterator in self.variables.keys():
            self.error.redeclaration(line)

        self.add_var_to_variables(iterator)
        self.set_var_declared(iterator,line)
        iterator_address = self.getVarAddress(iterator)
        obj = self.variables[iterator]
        obj.iterator = True

        #to ensure that upper bound won't change define 
        #upper fild in iterator that have same value as upper
        # bound of iterations in loop
        upper_var_id=self.generate_bound_var_id(obj,"upper",line)
        #we are sure that upper_ver_id not in self.vars so
        self.add_var_to_variables(upper_var_id)
        upper_var_address = self.getVarAddress(upper_var_id)
       

        # set start value to iterator
        self.store_address_in_register(start_value_address,self.a)
        self.decoder.LOAD(self.d.name, self.a.name)
        self.setValueInRegister(self.c,iterator_address)
        self.decoder.STORE(self.d.name,self.c.name)
        #self.decoder.PUT(self.c.name)
        #set lower boud value to  number of iterations
        self.store_address_in_register(end_value_address,self.a,True)
        self.store_address_in_register(start_value_address,self.c,True)


        # condtiion to  proper start the loop start fulfilled ( condition on bounds)
        self.decoder.LOAD(self.b.name,self.a.name)
        self.decoder.LOAD(self.d.name,self.c.name)
        self.decoder.INC(self.b.name)
        self.decoder.SUB(self.b.name,self.d.name)
        self.decoder.JZERO(self.b.name, labels[2])

        self.decoder.RESET(self.d.name)
        self.decoder.LOAD(self.d.name,self.a.name)
        self.decoder.LOAD(self.a.name,self.c.name)
        self.decoder.SUB(self.d.name,self.a.name)
        self.decoder.INC(self.d.name)
        self.setValueInRegister(self.c,upper_var_address)
        self.decoder.STORE(self.d.name,self.c.name)
        #self.decoder.PUT(self.c.name)

        ######################################## START 
        self.decoder.addLabel(labels[1])
         
        self.loadValueOfAddressToRegister(upper_var_address,self.b.name)
 

        # IF HAVE STOP ITERATING JUMP TO END
        self.decoder.JZERO(self.b.name, labels[2])
        self.decoder.RESET(self.b.name)
        # make loop's inner commands
        for command in inner_commands :
            self.match_action(command)

        # inc iterator
        self.loadValueOfAddressToRegister(iterator_address,self.f.name)
        self.decoder.INC(self.f.name)
        self.setValueInRegister(self.c,iterator_address)
        self.decoder.STORE(self.f.name,self.c.name)
        #self.decoder.PUT(self.c.name)

        # dec couter
        self.loadValueOfAddressToRegister(upper_var_address,self.f.name)
        self.decoder.DEC(self.f.name)
        self.setValueInRegister(self.c,upper_var_address)
        self.decoder.STORE(self.f.name,self.c.name)
        #self.decoder.PUT(self.c.name)
        

        # JUMP TO START
        self.decoder.JUMP(labels[1])

        ######################################## END

        # END LABEL
        self.decoder.addLabel(labels[2])
        #==============
        # at the end remove  temporary iterator variable 
        self.remove_variable_from_variables(iterator)
        self.remove_variable_from_variables(upper_var_id)


    def while_loop(self,command):

        self.decoder.RESET(self.b.name)
        self.decoder.RESET(self.a.name)
        self.decoder.RESET(self.c.name)
        self.decoder.RESET(self.d.name)
        self.decoder.RESET(self.e.name)
        self.decoder.RESET(self.f.name)

        condition_statement = command[1]
        line = command[3]
        inner_actions = command[2]
        labels = self.get_label_dict(2)
        

        self.decoder.addLabel(labels[1])
        left = condition_statement[1]
        right = condition_statement[2]
        self.store_address_in_register(left,self.a)
        self.store_address_in_register(right,self.c)

        #if condition ok then resolve inner commands
        self.conditions(condition_statement[0])
        self.decoder.JZERO(self.b.name, labels[2])

        for actions in inner_actions:
            self.match_action(actions)

        self.decoder.JUMP(labels[1])
        self.decoder.addLabel(labels[2])


    def repeat_until_loop(self,command):
        inner_commands = command[1]
        condition_statement = command[2]
        line = command[3]
        labels = self.get_label_dict(2)


        self.decoder.addLabel(labels[1])
        # do inner commands
        for c in inner_commands:
            self.match_action(c)

        left = condition_statement[1]
        right = condition_statement[2]
        self.store_address_in_register(left,self.a)
        self.store_address_in_register(right,self.c)
       
        self.conditions(condition_statement[0])
        self.decoder.JZERO(self.b.name, labels[1])
        self.decoder.JUMP(labels[2])
        self.decoder.addLabel(labels[2])

    def for_loop_with_downto(self,command):
        
       
        line = command[5]
        iterator = command[1]
        inner_commands = command[4]
        labels = self.get_label_dict(2)
        start_value_address = command[2]
        end_value_address = command[3]

        # check declarations ic case when bounds are uncedlared
        # or bound is the same as current iterator
        self.undeclared_check(end_value_address,self.a,True)
        self.undeclared_check(start_value_address,self.c,True)


        # define iterator in varialbes as long as for executes if possible
        if iterator in self.variables.keys():
            self.error.redeclaration(line)

        self.add_var_to_variables(iterator)
        self.set_var_declared(iterator,line)
        iterator_address = self.getVarAddress(iterator)


        #to ensure that lower bound won't change define 
        #lower field in iterator that have same value as lower
        # bound of iterations in loop
        obj = self.variables[iterator]
        lower_var_id=self.generate_bound_var_id(obj,"lower",line)
        #we are sure that lower_ver_id not in self.vars so
        self.add_var_to_variables(lower_var_id)
        lower_var_address = self.getVarAddress(lower_var_id)
        

     
        # set start value to iterator
        self.store_address_in_register(start_value_address,self.a)
        self.decoder.LOAD(self.d.name, self.a.name)
        self.setValueInRegister(self.c,iterator_address)
        self.decoder.STORE(self.d.name,self.c.name)
        #self.decoder.PUT(self.c.name)


        # condtiion to  proper start the loop start fulfilled ( condition on bounds)
        self.store_address_in_register(start_value_address,self.a)
        self.store_address_in_register(end_value_address,self.c)
        self.decoder.LOAD(self.b.name,self.a.name)
        self.decoder.LOAD(self.d.name,self.c.name)
             
        self.decoder.INC(self.b.name)
        self.decoder.SUB(self.b.name,self.d.name)
        self.decoder.JZERO(self.b.name,labels[2])



        #set lower boud value to  number of iterations
        self.store_address_in_register(start_value_address,self.a)
        self.store_address_in_register(end_value_address,self.c)
        self.decoder.RESET(self.d.name)
        self.decoder.LOAD(self.d.name,self.a.name)
        self.decoder.LOAD(self.a.name,self.c.name)
        self.decoder.SUB(self.d.name,self.a.name)
        self.decoder.INC(self.d.name)
        self.setValueInRegister(self.c,lower_var_address)
        self.decoder.STORE(self.d.name,self.c.name)
        #self.decoder.PUT(self.c.name)

        ######################################## START 
        self.decoder.addLabel(labels[1])
         
        self.loadValueOfAddressToRegister(lower_var_address,self.b.name)

        # IF HAVE REACHED STOP OF ITERATING JUMP TO END
        self.decoder.JZERO(self.b.name, labels[2])
        self.decoder.RESET(self.b.name)
        # make loop's inner commands
        for command in inner_commands :
            self.match_action(command)

        # decrement iterator
        self.loadValueOfAddressToRegister(iterator_address,self.f.name)
        self.decoder.DEC(self.f.name)
        self.setValueInRegister(self.c,iterator_address)
        self.decoder.STORE(self.f.name,self.c.name)
        #self.decoder.PUT(self.c.name)

        # decrement counter
        self.loadValueOfAddressToRegister(lower_var_address,self.f.name)
        self.decoder.DEC(self.f.name)
        self.setValueInRegister(self.c,lower_var_address)
        self.decoder.STORE(self.f.name,self.c.name)
        #self.decoder.PUT(self.c.name)
        
        # JUMP TO START
        self.decoder.JUMP(labels[1])

  
        # END LABEL
        self.decoder.addLabel(labels[2])

        #==============
        # at the end remove  temporary iterator variable 
        self.remove_variable_from_variables(iterator)
        self.remove_variable_from_variables(lower_var_id)
        

    def match_action(self, command):
        
            command_id = command[0]
            if command_id == "ASSIGN":
                self.assign(command)
            elif command_id =="WRITE":
                self.write(command)
            elif command_id =="READ":
                self.read(command)
            elif command_id == "IF_STATEMENT":
                self.if_statement(command)
            elif command_id == "IF_ELSE_STATEMENT":
                self.if_else_statement(command)
            elif command_id == "FOR_LOOP_WITH_TO":
                self.for_loop_with_to(command)
            elif command_id == "WHILE_LOOP":
                self.while_loop(command)
            elif command_id == "FOR_LOOP_WITH_DOWNTO":
                self.for_loop_with_downto(command)
            elif command_id == "REPEAT_UNTIL_LOOP":
                self.repeat_until_loop(command)
