import random

class Element: 
    def __init__(self,
                 coefficient = 1,
                 expression = 0,
                 power = 0
                 ):
        #constant values (can be used as answer)
        self.coefficient = coefficient
        self.expression = expression
        self.power = power
        

    def __hash__(self):
        return hash((self.coefficient, self.expression, self.power))

    def __eq__(self, other):
        return (type(other) is Element and 
                self.coefficient == other.coefficient and 
                self.expression == other.expression and 
                self.power == other.power)

    def __truediv__(self,other):
        if type(other) is Element and self.expression == other.expression:
            return Element(coefficient=self.coefficient/other.coefficient,
                           expression=self.expression,
                           power=self.power-other.power
                           )
        else:
            raise Exception("Invalid division")

    def __mul__(self, other): #Element * Element
        if type(other) is Element and self.expression == other.expression:
            return Element(coefficient=self.coefficient * other.coefficient,
                           expression=self.expression,
                           power = self.power + other.power)
        else:
            raise Exception("Invalid multiplication")        
    def __add__(self,other):
        if type(other) is Element:
            if self.power == other.power and self.expression == other.expression: #Element + Element 
                return Element(expression=self.expression,
                                      coefficient=self.coefficient+other.coefficient,
                                      power=self.power)
        else:
            raise Exception("Invalid addition")
        
    def __sub__(self,other):
        if type(other) is Element and self.power == other.power and self.expression == other.expression:    
            if self.coefficient == other.coefficient:
                return Element(expression = 0)
            else:
                return Block(coefficient=self.coefficient-other.coefficient,
                                      expression=self.expression,
                                      power=self.power)
        else:
            raise Exception("Invalid subtract")    
        
    def simplify(self):
        if check_type([int,float],[self.coefficient,self.expression,self.power]):
            return Element(coefficient=1,
                            expression = self.coefficient*(self.expression**self.power),
                            power=1)
        elif check_type(Element,self.expression):
            return Element(coefficient=self.coefficient*(self.expression.coefficient**self.varible.power),
                           expression = self.expression.expression,
                           power = self.power*self.expression.power)
        elif check_type(Block,self.expression):
            return Block(coefficient=self.coefficient*(self.expression.coefficient**self.expression.power),
                         expression=self.expression.expression,
                         power = self.power * self.expression.power)
        
    
        
class Block(Element):                                                          
    def __init__(self,                                      
                 expression = [],
                 coefficient = 1,
                 power = 1
                 ):
        
        super().__init__(   coefficient=coefficient, #should be a number
                            power=power, #should be an element or block or number
                            expression=expression ) #should be a list of elements or blocks 
    
    def __eq__(self, other):
        return (type(other) is Block and 
                self.expression == other.expression and 
                self.coefficient == other.coefficient and 
                self.power == other.power)

    
    def __hash__(self):
        return hash((
            tuple(self.expression),
            self.coefficient,
            self.power))


    def __truediv__(self,other):
        if type(other) is Block and self.expression == other.expression:
            if self == other:
                return Element(coefficient=1)
            elif self.expression == other.expression:
                return Block(expression=self.expression, 
                                      coefficient= self.coefficient / other.coefficient,
                                      power = self.power-other.power)
        else:
            raise Exception("Invalid division")

    def __mul__(self, other):
        if type(other) is Block and self.expression == other.expression:
            return Block(power=self.power+other.power,
                                  coefficient=1,
                                  expression = self.expression)
        else:
            raise Exception("Invalid multiplication")        
    def __add__(self,other):
        if type(other) is Block and self.power == other.power and self.expression == other.expression: 
            return Block(expression=self.expression,
                                  coefficient=self.coefficient+other.coefficient,
                                  power=self.power)
        else:
            raise Exception("Invalid addition")
        
    def __sub__(self,other):
        if type(other) is Block and self.power == other.power and self.expression == other.expression:    
            if self.coefficient == other.coefficient:
                return Element(coefficient = 0)
            else:
                return Block(coefficient=self.coefficient-other.coefficient,
                                      expression=self.expression,
                                      power=self.power)
        else:
            raise Exception("Invalid subtraction")


        
    def simplify(self):
        if check_type(Element,self.expression): # if all elements are class Element
            if len(self.expression) == 1:
                if type(self.expression[0]) is Element:
                    return Element(coefficient=self.coefficient*(self.expression[0].coefficient**self.expression[0].power),
                                   expression=self.expression[0].expression,
                                   power=self.power*self.expression[0].power)
                elif type(self.expression[0]) is Block:
                    return Block(coefficient=self.coefficient*self.expression[0].coefficient,
                                 expression=self.expression[0].expression,
                                 power=self.power*self.expression[0].power)
            elif (check_type([float,int],[e.expression for e in self.expression if not isinstance(e,Operator)]) or
                all(e.expression == self.expression[0].expression for e in self.expression)):
                step2 = self.expression[:]
                index = 0
                while index<len(step2):
                    if check_type([Mul,Div],step2[index]):
                        step2[index-1:index+1] = step2[index].operation(step2[index-1],step2[index+1])
                        index = 0
                    else:
                        index += 1
                result = step2[0]
                for index,operator in enumerate(step2):
                    if isinstance(operator,(Add,Sub)):
                        result = operator.operation(result,step2[index+1])
                return result
            else:
                if (
                        (   check_type([Add,Sub],[e for e in self.expression if isinstance(e,Operator)]) and
                            all(e.power == self.expression[0].power for e in self.expression if not isinstance(e,Operator))) or
                        (   check_type([Mul,Div],[e for e in self.expression if isinstance(e,Operator)]))
                    ):
                    ans_list = []
                    index = 0
                    while index < len(self.expression):
                        if self.expression[index].variable not in [e.expression for e in ans_list ]:
                            ans_list.append(self.expression[index])
                        else:
                            for var in ans_list:
                                if var.expression == self.expression[index].expression:
                                    var = self.expression[index-1].operation(var,self.expression[index])
                                    break
                        index += 1

                else:
                    return self    
                    
class Equation():
    def __init__(self,left=Element(variable="x"),right=Element(variable=1)):
        self.left = left #should be a block or a element
        self.right = right #same type as left
        
    def __eq__(self, other):
        return type(self) is type(other) and self.left == other.left and self.right == other.right
        
    
    
    
    
class Operator:
    def __eq__(self, other):
        return type(self) is type(other)

    def __hash__(self):
        return hash(type(self))
    pass

class Arithmetic_Operator(Operator):
    def alt_operator(self):
        
        if isinstance(self, Add):
            return Sub()
        if isinstance(self, Sub):
            return Add()
        if isinstance(self, Mul):
            return Div()
        if isinstance(self, Div):
            return Mul()

        
    def operation(self):
        pass

class Add(Arithmetic_Operator):
    symbol = "+"    
    def operation(self,left,right):
        return left + right
    
class Sub(Arithmetic_Operator):
    symbol = "-"
    def operation(self,left,right):
        return left - right
    
class Mul(Arithmetic_Operator):
    symbol = "*"
    def operation(self,left,right):
        return left * right
    
class Div(Arithmetic_Operator):
    symbol = "/"
    def operation(self,left,right):
        return left / right
    
class Basic_Properties:
    def __init__(self):
        pass
# An abstract class of Math Techniques
class MathTechnique:
    def __init__(self,equation,mode):
        self.steps = []
        self.equation = equation
        self.mode = mode
    def generate_problem(self):
        pass

    def generate_answer(self):
        pass
    
        
    def get_steps(self):
        return tuple(self.steps)
    
class Step:
    def __init__(self,technique,describtions,previous_equation=None,next_equation = None):
        self.technique = technique
        self.describtions = describtions
        self.previous_equation = previous_equation
        self.next_equation = next_equation
        
    

def check_type(types, objs):
        if isinstance(types,list):
            if not all(isinstance(t,type) for t in types):
                raise TypeError("invalid types")
        else:
            if not isinstance(types,type):
                raise TypeError("invalid types")
            
        if type(objs) is list and type(types) is list:
            return all(type(obj) in types  for obj in objs) 
        elif type(objs) is list and type(types) is not list:
            return all(type(obj) is types for obj in objs)
        elif type(objs) is not list and type(types) is list:
            return objs in types
        else:
            return type(objs) is types
        
