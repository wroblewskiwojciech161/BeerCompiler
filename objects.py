
class Variable():
    def __init__(self, name):
        self.name = str(name)
        self.value = None
        self.address = None
        self.declared = False
        self.iterator = False
        # if iterator stre the addresses of iteration
        self.lowerBound = None
        self.upperBound = None
        self.type = 'int'

    def get_address(self):
        return self.address

class Table():

    def __init__(self, name, first_idx, last_idx):
        self.name = str(name)
        self.first = int(first_idx)
        self.last = int(last_idx)
        self.offset = int(self.first)
        self.length = int(self.last - self.first) + 1
        self.first_address_id = None
        self.last_address_id = None
        self.declared = False
        self.ids = []
        self.addresses = {}
        self.type = "table"
    
    def get_first_address(self):
        return self.first_address_id
    
class Number():
    def __init__(self, name):
        self.name = str(name)
        self.value = None
        self.address = None
        self.type = 'number'
     
    def get_address(self):
        return self.address
 
