import random
import copy

class Element: 
    def __init__(self,
                 coefficient = 1,
                 expression = 0,
                 power = 1
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
            return None

    def __mul__(self, other): #Element * Element
        if type(other) is Element and self.expression == other.expression:
            return Element(coefficient=self.coefficient * other.coefficient,
                           expression=self.expression,
                           power = self.power + other.power)
        else:
            return None     
        
    def __add__(self,other):
        if (type(other) is Element and
            self.power == other.power and self.expression == other.expression): #Element + Element 
                return Element(expression=self.expression,
                                      coefficient=self.coefficient+other.coefficient,
                                      power=self.power)
        else:
            return None
        
    def __sub__(self,other):
        if (type(other) is Element and
            self.expression == other.expression and self.power == other.power):
                return Element(coefficient = self.coefficient-other.coefficient,
                               expression=self.expression,
                               power = self.power)
           
        else:
            return None
        
    
        
    
        
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
            return Block(expression=self.expression,
                         coefficient=self.coefficient/other.coefficient,
                         power=self.power-other.power)
        else:
            return None

    def __mul__(self, other):
        if type(other) is Block and self.expression == other.expression:
            return Block(   power=self.power+other.power,
                            coefficient=self.coefficient*other.coefficient,
                            expression = self.expression)
        else:
            return None    
            
    def __add__(self,other):
        if type(other) is Block and self.power == other.power and self.expression == other.expression: 
            return Block(expression=self.expression,
                                  coefficient=self.coefficient+other.coefficient,
                                  power=self.power)
        else:
            return None
        
    def __sub__(self,other):
        if type(other) is Block and self.power == other.power and self.expression == other.expression:    
            if self.coefficient == other.coefficient:
                return Element(coefficient = 0)
            else:
                return Block(coefficient=self.coefficient-other.coefficient,
                                      expression=self.expression,
                                      power=self.power)
        else:
            return None

    
class Equation:
    def __init__(self,left,right):
        self.left = left
        self.right = right
    
                    
class Operator:
    def __eq__(self, other):
        return type(self) is type(other)

    def __hash__(self):
        return hash(type(self))



class Arithmetic_Operator(Operator):
    def operation(self):
        pass

class Add(Arithmetic_Operator):
    string_form = "+"    
    def operation(self,left,right):
        return left + right
    
class Sub(Arithmetic_Operator):
    string_form = "-"
    def operation(self,left,right):
        return left - right
    
class Mul(Arithmetic_Operator):
    string_form = "*"
    def operation(self,left,right):
        return left * right
    
class Div(Arithmetic_Operator):
    string_form = "/"
    def operation(self,left,right):
        return left / right
    


class MathTechnique: # stored as steps
    expression_list = ["x","y","z","w","v"]
    def __init__(self,prev_step = []):
        self.answer = None
        self.question = None
        self.step_list = prev_step 

    def update_answer(self):
        pass

    def update_question(self):
        pass
    
    def generate_and_modify_steps(self):
        pass

        
        

#class Step:
#    def __init__(self):
#        self.part_working_on_before = None # near to the question, is a block
#        self.part_working_on_after = None # near to the answer, is a block
        

class Commutative(MathTechnique): # shuffle the order of the elements inside the block, only when the operator is commutative e.g. +,* 
    def generate_and_modify_steps(self):
        # The answer is the expression in a standard order.
        self.answer = Block(expression=[
            Element(expression="x", coefficient=random.randint(2, 5)), 
            Add(), 
            Element(expression="y", coefficient=random.randint(2, 5))
        ])
        
        # The question is a shuffled version of the answer.
        self.question = copy.deepcopy(self.answer)
        
        # Separate operands and operators
        operands = [item for item in self.question.expression if not isinstance(item, Operator)]
        operators = [item for item in self.question.expression if isinstance(item, Operator)]

        # Shuffle the operands
        if len(operands) > 1:
            random.shuffle(operands)

            # Rebuild the expression
            new_expression = []
            for i in range(len(operands)):
                new_expression.append(operands[i])
                if i < len(operators):
                    new_expression.append(operators[i])
            self.question.expression = new_expression

        self.step_list = [copy.deepcopy(self)]

class Distributive(MathTechnique):
    def generate_and_modify_steps(self):
        # Create the components for a distributive property expression like a * (b + c)
        
        # 'a' term
        term_a = Element(expression=random.choice(self.expression_list), coefficient=random.randint(2, 5))
        
        # 'b' term
        term_b = Element(expression=random.choice([e for e in self.expression_list if e != term_a.expression]), coefficient=random.randint(2, 5))
        
        # 'c' term
        term_c = Element(expression=random.choice([e for e in self.expression_list if e != term_a.expression and e != term_b.expression]), coefficient=random.randint(2, 5))

        # Operator for inside the parenthesis (e.g., + or -)
        inner_op = random.choice([Add(), Sub()])

        # --- Create the Answer (Factored Form) ---
        # This will be in the form: a * (b + c)
        inner_block = Block(expression=[term_b, inner_op, term_c])
        self.answer = Block(expression=[term_a, Mul(), inner_block])

        # --- Create the Question (Expanded Form) ---
        # This will be in the form: a*b + a*c
        
        # First part of the expansion: a * b
        expanded_part1 = term_a * term_b
        if expanded_part1 is None: # Handle cases where multiplication isn't defined (e.g., different variables)
            expanded_part1 = Block(expression=[copy.deepcopy(term_a), Mul(), copy.deepcopy(term_b)])

        # Second part of the expansion: a * c
        expanded_part2 = term_a * term_c
        if expanded_part2 is None:
            expanded_part2 = Block(expression=[copy.deepcopy(term_a), Mul(), copy.deepcopy(term_c)])

        self.question = Block(expression=[expanded_part1, inner_op, expanded_part2])
        
        self.step_list = [copy.deepcopy(self)]
        
            
class Quadratic(MathTechnique): # ax^2 + bx + c = 0
    def generate_and_modify_steps(self):
        # generate two random roots as constant elements
        root1 = random.randint(1, 10)
        root2 = random.randint(1, 10)
        # generate the sum of the roots
        sum = root1 + root2
        # generate the product of the roots
        product = root1 * root2
        # generate the quadratic equation
        self.question = Block(expression = [
                                                    Element(expression="x",power=2),
                                                    Sub() ,
                                                    Element(coefficient=sum,expression="x"),
                                                    Add() ,
                                                    Element(expression = product)])
        self.answer = Block(expression=[Block(expression=[Element(expression="x"), Sub(), Element(expression=int(root1))]),Mul(),
            Block(expression=[Element(expression="x"), Sub(), Element(expression=int(root2))])] )
        self.step_list = [copy.deepcopy(self)]
class BasicPropertyQuestion: # a question that requires the student to apply a basic property of arithmetic
    def __init__(self, num_steps=3):
        self.num_steps = num_steps
        self.current_step = None

    def build(self):
        
        for _ in range(self.num_steps):
            
            
            step = Distributive(prev_step=self.current_step.step_list if _ > 0 else [] )
            step.generate_and_modify_steps()
            step.step_list.append(copy.deepcopy(step))
            self.current_step = step
            
            #step2 = Commutative(prev_step=self.current_step.step_list)
            #step2.generate_and_modify_steps()
            #step.step_list.append(copy.deepcopy(step2))
            #self.current_step = step2
        
       

    
class QuadraticQuestion(MathTechnique): # ax^2 + bx + c = 0
    def __init__(self,num_steps = 3):
        self.question = None
        self.answer = None
        self.current_step = None
        
    def build(self):
        step = Quadratic(prev_step=[])
        step.generate_and_modify_steps()
        self.current_step = step
        
# Reminder for myself

# step 1:
# generate a specific format expression

# step 2:
# apply a technique to the expression

# step 3:
# update the answer 

# step 4:
# previous step is kept as last step

# step 5:
# update the question 

# step 6:
# repeat the process from step 1 to step 5
# until the number of steps is equal to the number of steps in the technique