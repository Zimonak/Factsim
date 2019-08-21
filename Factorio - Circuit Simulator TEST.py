#Generic Combinator class
class Combinator:
    def __init__(self, c_type):
        #Constant, Arithmetic, Decider
        self.c_type = c_type
        if self.c_type != "Constant":
            self.param1 = Signal("A")
            self.param2 = Signal("B")
            self.output_signal = Signal("O")

    def performFunction(self, function):
        try:
            if function == "add" or function == "+":
                self.output_signal.value = self.param1.value + self.param2.value
            if function == "subtract"or function == "/":
                self.output_signal.value = self.param1.value - self.param2.value
            if function == "multiply" or function == "*":
                self.output_signal.value = self.param1.value * self.param2.value
        except NameError:
            print("ERROR: No parameters have been defined")

    def assignInputParameter(self, p_number, signal, value = 0):
        if self.c_type == "Constant":
            return print("ERROR: Can't assign input parameters to Constant Combinator")
        if p_number > 2:
            return print("ERROR: Incorrect parameter number. Choose 1 or 2.")
        if p_number == 1:
            self.param1 = Signal(signal, value)
        else:
            self.param2 = Signal(signal, value)

    def assignOutputSignal(self, signal, value):
        #Reserved for special manipulation only!
        self.output_signal = Signal(signal, value)

    def showInfo(self):
        if self.c_type != "Constant":
            print(f"Type: {self.c_type}| Param1: {self.param1.signal}={self.param1.value}| Param2: {self.param2.signal}={self.param2.value}| Output: {self.output_signal.signal}={self.output_signal.value}")
        else:
            print("Type:",self.c_type)
            
#Generic Signal class
class Signal:
    def __init__(self, signal, value=0):
        self.signal = signal
        self.value = value
        
    def showValues(self):
        print("Signal",self.signal, "Value", self.value)

#Testing only!
a = Combinator("Constant")
b = Combinator("Arithmetic")

#-=Final=-
#ConstantCombinator: A=1      --> ArithmeticCombinator("add","A",10,"X")  --> X=11
#ConstantCombinator: A=1, B=1 --> ArithmeticCombinator("add","A","B","X") --> X=2
