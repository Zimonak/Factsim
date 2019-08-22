class Combinator:
    # Generic Combinator class
    # Three combinator types supported are: Constant, Arithmetic,Decider|ToDo:tests, tests, finalize
    #
    #   input_signal1->|------------------------|
    #                  | param1;Function;param2 |->output_signal
    #   input_signal2->|------------------------|
    #
    #NB this class is never meant to be called independently!
    
    def __init__(self, function, param1_id, param2_id, out_id):
        if type(self) == Combinator:
            raise Exception("ERROR: Do not refer to this class directly - use subclasses")
        
        self.param1 = Signal(param1_id)
        self.param2 = Signal(param2_id)
        self.function = function
        
        #Input signals are assigned by other objects
        self.input_signal1 = Signal("IN1")
        self.input_signal2 = Signal("IN2")
            
        self.output_signal = Signal(out_id)
        #Unique object's ID
        self.id = id(self)

    def performFunction(self):
        """
        Contains all the functions that Arithmetic and Decider comb. can do.
        List of allowed functions is defined on init.
        This method is only called on request.
        """

        # When it is detected that we have same inputs as parameters, use the input values for calculations
        # Looks ugly, but works...PLEASE REWRITE for MAINTAINABILITY!

        input_signals_list = [self.input_signal1, self.input_signal2]
        input_signals_ids = list(map(lambda x: x.s_id, input_signals_list)) #['IN1', 'IN2']

        if self.param1.s_id in input_signals_ids:
            #wtf, dude, do you even understand...?
            a = input_signals_list[input_signals_ids.index(self.param1.s_id)].value

        # Special signal for param2 ("int",value)| Represents the pure integer or i.e [A + 4]
        if self.param2.s_id == 'int':
            b = self.param2.value
        elif self.param2.s_id in input_signals_ids:
            b = input_signals_list[input_signals_ids.index(self.param2.s_id)].value
            
        #Make sure that we have all the variables
        try:
            a
            b
        except NameError:
            print("WARNING: No inputs matching to parameters were found")
            return
        #---
  
        ops = {"add": (lambda x, y: x + y),
               "+": (lambda x, y: x + y),
               "subtract": (lambda x, y: x - y),
               "-": (lambda x, y: x - y),
               "multiply": (lambda x, y: x * y),
               "*": (lambda x, y: x * y),
               "divide": (lambda x, y: x / y),
               "/": (lambda x, y: x / y),
               "modulo": (lambda x, y: x % y),
               "%": (lambda x, y: x % y),
               "exp": (lambda x, y: x ** y),

               "L bitS": (lambda x, y: x << y),
               "<<": (lambda x, y: x << y),
               "R bitS": (lambda x, y: x >> y),
               " >> ": (lambda x, y: x >> y),
               "AND": (lambda x, y: x & y),
               "&": (lambda x, y: x & y),
               "OR": (lambda x, y: x | y),
               "|": (lambda x, y: x | y),
               "XOR": (lambda x, y: x ^ y),
               "^": (lambda x, y: x ^ y),
               
               ">": (lambda x, y: x > y),
               "<": (lambda x, y: x < y),
               "=": (lambda x, y: x == y),
               ">=": (lambda x, y: x >= y),
               "<=": (lambda x, y: x <= y),
               "!=": (lambda x, y: x != y),
               }
        result = ops[self.function](a, b)
        if result == True:
            self.output_signal.value = 1
        elif result == False:
            self.output_signal.value = 0
        else:
            self.output_signal.value = result

    def assignParameter(self, p_number, s_id, value = 0):
        #Function to change the parameter values     
        if p_number == 1:
            self.param1 = Signal(s_id, value)
        elif p_number == 2:
            self.param2 = Signal(s_id, value)
        else:
            print("ERROR: Incorrect parameter number. Choose 1 or 2.")

    def assignInput(self, input_nr, s_id, value):
        #Function to change the input values 
        if input_nr == 1:
            self.input_signal1 = Signal(s_id, value)
        elif input_nr == 2:
            self.input_signal2 = Signal(s_id, value)
        else:
            print("ERROR: Incorrect input number. Choose 1 or 2.")
            
    def assignOutput(self, s_id, value):
        #Function to change the output values 
        self.output_signal = Signal(s_id, value)

    def showInfo(self):
        print(f"Function: [{self.function}]| Param1: {self.param1.s_id}={self.param1.value}| Param2: {self.param2.s_id}={self.param2.value}")
        print(f"Input1: {self.input_signal1.s_id}={self.input_signal1.value}| Input2: {self.input_signal2.s_id}={self.input_signal2.value}| Output: {self.output_signal.s_id}={self.output_signal.value}")

#----------------------------------------------------------------------------------------------------
# Subclasses of Combinator class
class ArithmeticCombinator(Combinator):
    def __init__(self, function, param1_id, param2_id, out_id):
        super().__init__(function, param1_id, param2_id, out_id)
        
        allowed_functions = ['add', '+', 'subtract', '-', 'multiply', '*', 'divide', '/', 'modulo', '%', 'exp',
                             'L bitS', '<<', 'R bitS', '>>', 'AND', '&', 'OR', '|', 'XOR', '^',]
        if self.function not in allowed_functions:
            raise Exception("ERROR: This Function is not allowed for this combinator")

    def showInfo(self):
        print("Type: Arithmetic combinator")
        super().showInfo()
            
class DeciderCombinator(Combinator):
    def __init__(self, function, param1_id, param2_id, out_id):
        super().__init__(function, param1_id, param2_id, out_id)
        
        allowed_functions = ['>', '<', '=', '>=', '<=', '!=']
        if self.function not in allowed_functions:
            raise Exception("ERROR: This Function is not allowed for this combinator")

    def showInfo(self):
        print("Type: Decider combinator")
        super().showInfo()
    pass

class ConstantCombinator(Combinator):
    def __init__(self, param1_id, out_id_value = 100):
        # Initialise parent's __init__ with function and param2 = None (Ps. None might create issues?)
        # For Constant Combinator the param1_id = output_id
        super().__init__(None, param1_id, None, param1_id)
        self.input_signal1 = None
        self.input_signal2 = None
        self.out_id_value = out_id_value
        
    def performFunction(self):
        print("ERROR: Not allowed for Constant combinator.")

    def assignInput(self):
        print("ERROR: Not allowed for Constant combinator.")

    def showInfo(self):
        print("Type: Constant combinator")
        print(f"Param1: {self.param1.s_id}={self.param1.value}")
        print(f"Output: {self.output_signal.s_id}={self.output_signal.value}")   
#----------------------------------------------------------------------------------------------------
        
class Signal:
    # Generic Signal class
    # Signal object is defined by it's id - i.e "iron-plates", "A", etc
    # And it's value - 32bit Integer| ToDo: Add check whether the value is within limits
    def __init__(self, s_id, value=0):
        self.s_id = s_id
        self.value = value
        
    def showInfo(self):
        print("Signal",self.signal, "Value", self.value)


class Network:
    #Holds all the inputs and outputs of the objects
    #Basically the same as highlighting the same color wires in the Factorio
    #
    # NB! Combinators/Objects OUTput = Networks's INput!!
    def __init__(self):
        self.data = {'input':{}, 'output':{}}    
        #  data = {'input':{'A': [10, 5, 8], 'B': [1, 2, 3]},'output':{}}
        #  ref: network1["input"]["A"]
        #  sum: sum(network1["input"]["A"])              :)

        #Unique object's ID
        self.id = id(self)
        
    def addInput(self, s_id, value):
        #s_id: signal's id, value: signals value
        if s_id in self.data["input"]: #if key exists (output keys, can't exist without input)
            self.data["input"][s_id].append(value)
            self.data["output"][s_id].append(value)
        else:
            self.data["input"][s_id] = [value]
            self.data["output"][s_id] = [value]
            
        #Update output: sum up
        for key in self.data["output"]:
            self.data["output"][key] = [sum(self.data["output"][key])]
            
    def delete(self):
        # Removes node (input/output from the network (for special manipulation)
        # Meant for future GUI when removing/adding combinators
        pass
    
    def showInfo(self):
        print(f"Network id: xxxx \nInput: {n.data['input']} \nOutput: {n.data['output']}")
        pass

#Testing only! <<<< move to pytests folder
print("Original Arithmetic:")
a = ArithmeticCombinator("add","L","B","X")
a.showInfo()
print()
a.assignInput(1,"A",200)
a.assignInput(2,"L",25)
a.assignParameter(2, "int", 99)
a.performFunction()
a.showInfo()
print()
a.assignInput(1,"L",11)
a.assignInput(2,"C",21)
a.assignParameter(2, "int", 10)
a.performFunction()
a.showInfo()
print()
a.assignInput(1,"R",333)
a.assignInput(2,"T",222)
a.assignParameter(1, "T")
a.assignParameter(2, "R")
a.performFunction()
a.showInfo()

print()
print("Original Decider:")
b = DeciderCombinator(">","D","L","Ö")
b.showInfo()
print()
b.assignInput(1,"A",200)
b.assignInput(2,"D",25)
b.assignParameter(2, "int", 99)
b.performFunction()
b.showInfo()
print()
b.assignInput(1,"D",11)
b.assignInput(2,"C",21)
b.assignParameter(2, "int", 10)
b.performFunction()
b.showInfo()
print()
b.assignInput(1,"R",333)
b.assignInput(2,"T",222)
b.assignParameter(1, "T")
b.assignParameter(2, "R")
b.performFunction()
b.showInfo()
    
#n = Network()

#n.addInput(b.output_signal.s_id,b.output_signal.value)
#n.addInput(c.output_signal.s_id,c.output_signal.value)

#n.showInfo()

#-=Final=-
#ConstantCombinator: A=1      --> ArithmeticCombinator("add","A",10,"X")  --> X=11
#ConstantCombinator: A=1, B=1 --> ArithmeticCombinator("add","A","B","X") --> X=2
