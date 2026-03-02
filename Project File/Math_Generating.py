#import random
#
#class Element: 
#    def __init__(self,coefficient = None):
#        #constant values (can be used as answer)
#        self.coefficient = coefficient
#        self.variable = None
#        self.power = None
#        self.divider = None
#        
#        
#        
#
#        
#    
#        
#class Elements_Block(Element):
#    def __init__(self):
#        self.elements = None
#        self.operators = None
#        self.coefficent = None
#        self.power = None
#        self.divider = None
#    
#    def __eq__(self, other):
#        if type(other) is Elements_Block:
#            return self.elements == other.elements and self.operators == other.operators
#            
#    
#    def __truediv__(self,other):
#        if type(other) is Elements_Block:
#            return Element(1)
#        
#    def __add__(self,other):
#        if type(other) is Elements_Block:
#            return Advanced_Element(coefficient = self.coefficent+other.coefficent,
#                                    power_expression=self.power,
#                                    divider_expression=self.divider,
#                                    variable_expression=)
#        
#    def __sub__(self,other):
#        if type(other) is Elments_Block:     
#        
#class OperatorBase:
#    def __init__(self):
#        self.operand_left = None
#        self.operand_right = None
#        
#
#        
#class ArithmeticQuestionBuilder:
#    def __init__(self):
#        pass