class RegisterInstructions():
   
    def __init__(self):
        self.instructions = []
        

    def get_assembler(self):
        return self.instructions
  
    def execute(self,instruction):
        self.instructions.append(instruction)

    def executeList(self,instructions):
        for inst in instructions :
            self.execute(inst)

    def RESET(self, reg, execute = True):
        msg = "RESET "+reg
        if execute == True:
            self.execute(msg)
        else :
            return msg
        
    def STORE(self, reg,  reg2, execute = True):
        msg = "STORE "+reg + " " + reg2
        if execute == True:
            self.execute(msg)
        else :
            return msg

    def LOAD(self, register, memory_address,  execute = True):
        msg = "LOAD "+register+" "+str(memory_address)
        if execute == True:
            self.execute(msg)
        else :
            return msg
       
    def PUT(self, register, execute = True):
        msg = "PUT "+str(register)
        if execute == True:
            self.execute(msg)
        else :
            return msg
        
    def GET(self, register, execute = True):
        msg = "GET "+str(register.name)
        if execute == True:
            self.execute(msg)
        else :
            return msg
        
    def SUB(self, register1, register2, execute = True):
        msg = "SUB "+register1+" "+register2
        if execute == True:
            self.execute(msg)
        else :
            return msg
       
    def JUMP(self, j, execute = True):
        msg = "JUMP "+str(j)
        if execute == True:
            self.execute(msg)
        else :
            return msg
    
    def JZERO(self, register, j, execute = True):
        msg = "JZERO "+register+" "+str(j)
        if execute == True:
            self.execute(msg)
        else :
            return msg
       
    def JODD(self, register, j, execute = True):
        msg = "JODD "+register+" "+j
        if execute == True:
            self.execute(msg)
        else :
            return msg
        
    def addLabel(self, label, execute = True):
        
        if execute == True:
            self.execute(label)
        else :
            return label
     
    def INC(self, reg, execute = True):
        msg = "INC "+reg
        if execute == True:
            self.execute(msg)
        else :
            return msg
        

    def SHR(self, r, execute = True):
        msg = "SHR "+r
        if execute == True:
            self.execute(msg)
        else :
            return msg
      
    def SHL(self, reg, execute = True): 
        msg = "SHL "+reg
        if execute == True:
            self.execute(msg)
        else :
            return msg  
       

    def DEC(self, r, execute = True):
        msg = "DEC "+r
        if execute == True:
            self.execute(msg)
        else :
            return msg
       

    def ADD(self, r1, r2, execute = True):
        msg = "ADD "+r1+" "+r2
        if execute == True:
            self.execute(msg)
        else :
            return msg

    def createLabel(self,counter, execute = True):
        msg = "LABEL"+str(counter)
        if execute == True:
            self.execute(msg)
        else :
            return msg
      
    def setLabel(self,label, execute = True):
        
        if execute == True:
            self.execute(label)
        else :
            return label

    def add_const_to_register(self,number,register):
        number = int(number)
        while number > 0 :
            self.INC(reg)
            number -= 1

 
       
        

