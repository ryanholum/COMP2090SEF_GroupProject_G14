import tkinter as tk
import new_Math_Generating as MG
import random
import copy

class Quiz_Pages:
    def __init__(self, root, question_number = None,difficulty_level=None,change_page=None):
        self.root = root
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.font_size = 20
        self.question_number = question_number
        self.difficulty_level = difficulty_level
        self.quiz_set = []
        self.pages = []
        self.main_frame = tk.Frame(self.root)
        self.main_frame.grid(row=0,column=0,sticky="nsew")
        self.main_frame.rowconfigure(0, weight=1)
        self.main_frame.rowconfigure(1, weight=10)
        self.main_frame.columnconfigure(0, weight=1)
        self.second_frame = tk.Frame(self.main_frame)
        self.second_frame.grid(row=1,column=0,sticky="nsew")
        self.second_frame.rowconfigure(0, weight=1)
        self.second_frame.columnconfigure(0, weight=1)
        self.second_frame.rowconfigure(0, weight=1)
        self.second_frame.columnconfigure(0, weight=1)
        self.change_page = change_page
        self.initialize_questions()
        self.finished = False
        self.time_limit = self.question_number  * 3
        self.remaining_time = self.time_limit
        
        self.score = 0
        
        # display 
        
        
    def grid(self):
        self.pages[0].grid()    
    
    def display_correct_answers(self):
        for page in self.pages:
            page.show_ans()
    def count_score(self):
        self.score = 0
        for i in range(len(self.pages)):
            if self.pages[i].selected_answer.get() == str(self.pages[i].correct_ans_pos):
                self.score += 1
        
    # generate Question Pages
    def initialize_questions(self):
        num = 0
        match self.difficulty_level:
            case "Easy":
                self.question_number = 5
            case "Hard":    
                self.question_number = 10
        for i in range(self.question_number):
            # Use the correct classes from new_Math_Generating
            question_technique = random.choice([MG.QuadraticQuestion, MG.BasicPropertyQuestion])
            technique_instance = question_technique()
            technique_instance.build()
            
            self.quiz_set.append(technique_instance)
          
        for i in range(self.question_number):
             _ = Question_Page(self.second_frame,self.quiz_set[i],(i+1,self.question_number))
             self.pages.append(_)
        for i in range(self.question_number):
            if i < self.question_number - 1:
                self.pages[i].setbutton_next(lambda i=i: self.change_question_next(i, i + 1))
            else:
                self.pages[i].setbutton_next(self.finish_quiz)
                self.pages[i].setbutton_return_to_main(self, change_page=self.change_page)
                

            if i > 0:
                self.pages[i].setbutton_prev(lambda i=i: self.change_question_prev(i, i - 1))

    
    def change_question_next(self, current_page, destination_page):
        self.pages[current_page].main_frame.grid_forget()
        self.pages[destination_page].grid()

    def change_question_prev(self, current_page, destination_page):
        self.pages[current_page].main_frame.grid_forget()
        self.pages[destination_page].grid()

    def finish_quiz(self):
        # This function is called when the 'Next' button on the last question is clicked.
        
        print("Quiz has been completed!")
       
        if self.finished:
            return
        else:
            self.finished = True
            self.count_score()
            self.second_frame.rowconfigure(1, weight=1)
            frame_score = tk.Frame(self.second_frame)
            
            frame_score.rowconfigure(0, weight=1)
            frame_score.columnconfigure(0, weight=1)
            frame_score.grid(row=1, column=0, sticky="nsew")
            score_label = tk.Label(frame_score, text=f"Your Score: {self.score}/{self.question_number}", font=("Arial", self.font_size * 2))
            score_label.grid(row=0, column=0, sticky="")
            self.display_correct_answers()
        
   

class Question_Page:
    def __init__(self,parent,question,question_number,prev_page=None,next_page=None): # question number is a tuple of (question_number,total_question_number) 
        self.question_steps = question.current_step.step_list
        self.answer = self.question_steps[-1].answer
        self.question = self.question_steps[-1].question
        self.selected_answer = tk.StringVar()
        self.selected_answer.set("0")
        self.font_size = 20
        self.main_frame = tk.Frame(parent)
        [self.main_frame.rowconfigure(i, weight=1) for i in range(5)]
        self.main_frame.columnconfigure(0, weight=1)
        self.point_get = 0
        self.question_number = question_number
        self.prev_page = prev_page
        self.next_page = next_page
        self.display_question()
        # self.generate_answers()
        self.gernerate_change_question_button()
    # display question
    def display_question(self):
        question_frame = tk.Frame(self.main_frame)
        question_frame.grid(row=0,column=0)
        question_frame.rowconfigure(0, weight=1)
        question_frame.rowconfigure(1, weight=1)
        
        question_frame.columnconfigure(0, weight=1)
        question_frame.columnconfigure(1, weight=1)
        question_frame.columnconfigure(2, weight=1)
       
        
        frame_question = tk.Frame(question_frame)
        frame_question.grid(row=0,column=1,sticky="")
        frame_question.rowconfigure(0, weight=1)
        frame_question.columnconfigure(0, weight=1)
        question_string = "Factorize: "
        self.question_label1 = tk.Label(frame_question,text="Question "+str(self.question_number[0])+"/"+str(self.question_number[1]))
        self.question_label1.grid(row=0,column=0,sticky="")
        self.question_label1.config(font=("Arial",self.font_size))
        self.question_label2_frame = tk.Frame(frame_question)
        self.question_label2_frame.grid(row=1,column=0,sticky="")
        self.question_label2_frame.rowconfigure(0, weight=1)
        self.question_label2_frame.columnconfigure(0, weight=1)
        self.question_label2 = tk.Label(self.question_label2_frame,text=question_string)
        self.question_label2.grid(row=0,column=0,sticky="") 
        self.question_label2.config(font=("Arial",self.font_size))
        # display question equation
        self.question_block_frame = tk.Frame(question_frame)
        self.question_block_frame.grid(row=2,column=1,sticky="")
        self.question_block_frame.rowconfigure(0, weight=1)
        self.question_block_frame.columnconfigure(0, weight=1)
        _ = Block_Frame(self.question,self.question_block_frame,self.font_size)

       
       
        # display 4 answer choices with radio buttons vertically
        self.ans_table_frame = tk.Frame(self.main_frame)
        self.ans_table_frame.grid(row=1,column=0)
        [self.ans_table_frame.rowconfigure(i, weight=1) for i in range(4)]
        self.ans_table_frame.columnconfigure(0, weight=0) # Radio button column
        self.ans_table_frame.columnconfigure(1, weight=1) # Answer content column

        self.build_answer_choices()

        # other answer choices
       
    def build_answer_choices(self):
        answers = [self.answer]
        distractors = []

        # Generate 3 unique distractors
        for _ in range(3):
            appended = False
            for attempt in range(20):
                candidate_expr = self.modify_answer(
                    copy.deepcopy(self.answer.expression),
                    existing_distractors=answers + distractors
                )
                candidate = MG.Block(expression=candidate_expr)
                if candidate not in answers and candidate not in distractors:
                    distractors.append(candidate)
                    appended = True
                    break

            if not appended:
                # fallback: force one variable coefficient to change so the answer is not duplicated
                fallback_expr = copy.deepcopy(self.answer.expression)

                def force_change(expr):
                    for element in expr:
                        if isinstance(element, MG.Element) and isinstance(element.expression, str) and element.expression in ["x", "y", "z", "w", "v"]:
                            coeff_choices = [e2 for e2 in range(1, 15) if e2 != element.coefficient]
                            if coeff_choices:
                                element.coefficient = random.choice(coeff_choices)
                                return True
                        elif isinstance(element, MG.Block):
                            if force_change(element.expression):
                                return True
                    return False

                force_change(fallback_expr)
                fallback = MG.Block(expression=fallback_expr)
                if fallback not in answers and fallback not in distractors:
                    distractors.append(fallback)
                else:
                    # if forced change still did not produce a unique distractor, keep the best candidate
                    if candidate is not None and candidate not in answers and candidate not in distractors:
                        distractors.append(candidate)

        # Combine correct + distractors
        answers.extend(distractors)

        # Shuffle
       
        random.shuffle(answers)

        # Update correct answer position as string
        for i, ans in enumerate(answers):
            if ans.expression == self.answer.expression:
                self.correct_ans_pos = str(i)   # <-- stored as string
                break

        # Render radio buttons + answer blocks
        for i, ans in enumerate(answers):
            rb = tk.Radiobutton(
                self.ans_table_frame,
                font=self.font_size,
                variable=self.selected_answer,
                value=str(i)
            )
            rb.grid(row=i, column=0, padx=10)

            b_frame = tk.Frame(self.ans_table_frame)
            b_frame.grid(row=i, column=1, sticky="w")
            Block_Frame(ans, b_frame, self.font_size)



    def show_ans(self):
        self.main_frame.rowconfigure(5, weight=1)
        tk.Label(self.main_frame, text=f"Correct Answer: ", font=("Arial", self.font_size)).grid(row=5, column=0, sticky="w")
        self.correct_answer_frame = tk.Frame(self.main_frame)
        self.correct_answer_frame.grid(row=6,column=0,sticky="")
        self.main_frame.rowconfigure(6, weight=1)
        _ = Block_Frame(self.answer,self.correct_answer_frame,self.font_size)

        
    def modify_answer(self, answer, existing_distractors=None):
        if existing_distractors is None:
            existing_distractors = []
        if answer is None:
            return []

        def is_linear_factor(block):
            if not isinstance(block, MG.Block):
                return False
            if len(block.expression) != 3:
                return False
            first, op, second = block.expression
            return (
                isinstance(first, MG.Element)
                and isinstance(first.expression, str)
                and first.expression in ["x", "y", "z", "w", "v"]
                and isinstance(op, MG.Operator)
                and isinstance(second, MG.Element)
                and isinstance(second.expression, (int, float))
            )

        def mutate_linear_factor(block):
            first, op, second = block.expression
            new_op = op
            if random.random() < 0.35:
                new_op = random.choice([MG.Add(), MG.Sub()])

            coeff_choices = [c for c in range(1, 11) if c != first.coefficient]
            new_coeff = random.choice(coeff_choices) if coeff_choices else first.coefficient

            constant_choices = [n for n in range(1, 15) if n != second.expression]
            new_constant = random.choice(constant_choices) if constant_choices else second.expression

            return MG.Block(expression=[
                MG.Element(coefficient=new_coeff, expression=first.expression, power=first.power),
                new_op,
                MG.Element(expression=new_constant, coefficient=second.coefficient, power=second.power)
            ])

        def is_quadratic_pair(expr):
            return (
                isinstance(expr, list)
                and len(expr) == 3
                and isinstance(expr[0], MG.Block)
                and isinstance(expr[1], MG.Mul)
                and isinstance(expr[2], MG.Block)
                and is_linear_factor(expr[0])
                and is_linear_factor(expr[2])
            )

        def build_quadratic(expr):
            factor1, mulop, factor2 = expr
            return [mutate_linear_factor(factor1), mulop, mutate_linear_factor(factor2)]

        def build_expression(expr):
            if is_quadratic_pair(expr):
                return build_quadratic(expr)

            new_expr = []
            for element in expr:
                if isinstance(element, MG.Element):
                    if isinstance(element.expression, (int, float)):
                        new_expr.append(MG.Element(
                            coefficient=element.coefficient,
                            expression=random.choice([e2 for e2 in range(1, 15) if e2 != element.expression]),
                            power=element.power
                        ))
                    elif isinstance(element.expression, str) and element.expression in ["x", "y", "z", "w", "v"]:
                        coeff_choices = [e2 for e2 in range(1, 15) if e2 != element.coefficient]
                        new_expr.append(MG.Element(
                            coefficient=random.choice(coeff_choices) if coeff_choices else element.coefficient,
                            expression=element.expression,
                            power=element.power
                        ))
                    else:
                        new_expr.append(copy.deepcopy(element))
                elif isinstance(element, MG.Block):
                    new_expr.append(MG.Block(
                        expression=build_expression(copy.deepcopy(element.expression)),
                        coefficient=element.coefficient,
                        power=element.power
                    ))
                elif isinstance(element, MG.Operator):
                    new_expr.append(element)
                else:
                    new_expr.append(copy.deepcopy(element))
            return new_expr

        attempt = 0
        while True:
            new_answer = build_expression(copy.deepcopy(answer))
            candidate = MG.Block(expression=new_answer)
            if candidate not in existing_distractors:
                return new_answer
            attempt += 1
            if attempt >= 20:
                return new_answer

    # generate answers steps
    







    def gernerate_change_question_button(self):

        # frame for buttons
        self.button_frame = tk.Frame(self.main_frame)
        self.button_frame.grid(row=4,column=0, sticky="ew")
        self.button_frame.rowconfigure(0, weight=1)
        self.button_frame.columnconfigure(0, weight=1) # Spacer
        self.button_frame.columnconfigure(1, weight=0) # Prev
        self.button_frame.columnconfigure(2, weight=0) # Next
        self.button_frame.columnconfigure(3, weight=1) # Spacer


        # create prev button
        self.prev_button = tk.Button(self.button_frame,text="Prev",font=("Arial",self.font_size))
        self.prev_button.grid(row=0,column=1)
        #create next button
        self.next_button = tk.Button(self.button_frame,text="Next" if self.question_number[0] != self.question_number[-1] else "Submit",font=("Arial",self.font_size))
        #grid next button to the right
        self.next_button.grid(row=0,column=2)

        # if last page
        if self.question_number[0] == self.question_number[-1]:
            self.return_to_main_button = tk.Button(self.button_frame,text="Quit",font=("Arial",self.font_size))
            self.return_to_main_button.grid(row=0,column=3)
            

    def setbutton_next(self,thefunction):
        self.next_button.config(command=thefunction)
    def setbutton_prev(self,thefunction):
        self.prev_button.config(command=thefunction)
    def setbutton_return_to_main(self,destroy_obj,change_page=None):
        self.return_to_main_button.config(command=lambda: self.return_to_main(destroy_obj,change_page=change_page))
    def return_to_main(self,destroy_obj,change_page=None):          
        destroy_obj.main_frame.destroy()
        if change_page:
            change_page.grid()
    def grid(self):
        self.main_frame.grid(row=0,column=0,sticky="")
class Element_Frame:
    def __init__(self,element,parent,font_size=20):
        self.element = element
        self.parent_frame = parent
        self.font_size = font_size
        self.main_frame = tk.Frame(parent)
        
        self.main_frame.rowconfigure(0,weight=1)
        
      
        self.main_frame.grid(row=0,column=0,sticky="")
        self.format_element()


    def format_element(self):
        
        # Base string for coefficient + expression
        text_parts = ""
        if self.element.coefficient != 1:
            text_parts += str(self.element.coefficient)
    
        text_parts += str(self.element.expression)
    
        # Create one label for coefficient + expression
        self.base_label = tk.Label(
            self.main_frame,
            text=text_parts,
            font=("Arial", self.font_size),
            compound="left"   # ensures text is treated as one continuous unit
        )
        self.base_label.grid(row=0, column=0, sticky="w", padx=0, pady=0)
    
        # --- Power handling ---
        if self.element.power != 1:
            self.power_frame = tk.Frame(self.main_frame)
            self.power_frame.grid(row=0, column=1, sticky="nw")
    
            if isinstance(self.element.power, (int, float)):
                self.power_label = tk.Label(
                    self.power_frame,
                    text=str(self.element.power),
                    font=("Arial", int(self.font_size // 2))
                )
                self.power_label.grid(row=0, column=0, sticky="nw")
            elif isinstance(self.element.power, MG.Element):
                frame = Element_Frame(self.element.power, self.power_frame, font_size=int(self.font_size // 2))
                frame.main_frame.grid(row=0, column=0, sticky="nw")
            elif isinstance(self.element.power, MG.Block):
                frame = Block_Frame(self.element.power, self.power_frame, font_size=int(self.font_size // 2))
                frame.main_frame.grid(row=0, column=0, sticky="nw")



              

class Block_Frame:
    def __init__(self,element,parent,font_size=20):
        self.element = element
        self.parent_frame = parent
        self.font_size = font_size
        self.main_frame = tk.Frame(self.parent_frame)
        self.main_frame.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.grid(row=0,column=0,sticky="")
        self.format_block()

    def format_block(self):
        
        if self.element.coefficient != 1 and self.element.power != 1:
            [self.main_frame.columnconfigure(i, weight=w) for i,w in enumerate([1,1,1])]
        elif self.element.coefficient != 1 or self.element.power != 1:
            [self.main_frame.columnconfigure(i, weight=w) for i,w in enumerate([1,1])]
        else:
            [self.main_frame.columnconfigure(i, weight=w) for i,w in enumerate([1])]

        
        if self.element.coefficient != 1:
            self.coefficient_frame = tk.Frame(self.main_frame)
            self.coefficient_frame.rowconfigure(0, weight=1)
            self.coefficient_frame.columnconfigure(0, weight=1)
            self.coefficient_frame.grid(row=0,column=0,sticky="s")
            self.coefficient_label = tk.Label(self.coefficient_frame,text=str(self.element.coefficient),font=("Arial",self.font_size))
            self.coefficient_label.grid(row=0,column=0,sticky="")
        
        formatted_expression = []
        current_expression = []
        if len(self.element.expression) > 1:
            for element in self.element.expression:
                if type(element) == MG.Add or type(element) == MG.Sub:
                    formatted_expression.append(current_expression)
                    formatted_expression.append(element)
                    current_expression = []

                else:
                    current_expression.append(element)
            formatted_expression.append(current_expression)
        else:
            formatted_expression =[self.element.expression]
        
        self.expression_frame = tk.Frame(self.main_frame)
        self.expression_frame.rowconfigure(0, weight=1)
        self.expression_frame.columnconfigure(0, weight=1)
        self.expression_frame.grid(row=0,column=1 if self.element.coefficient != 1 else 0,sticky="")
        if len(self.element.expression) > 1:
            open_bracket_frame = tk.Frame(self.expression_frame)
            open_bracket_frame.grid(row=0,column=0,sticky="")
        
            label = tk.Label(open_bracket_frame,text="(",font=("Arial",self.font_size))
            label.grid(row=0,column=0,sticky="")
        for i,e in enumerate(formatted_expression):
            
            self.small_frame = tk.Frame(self.expression_frame)
            self.small_frame.grid(row=0,column=i+1,sticky="")
            self.small_frame.rowconfigure(0, weight=1)
            
            if type(e) is list and len(e) > 0:
                if MG.Div in [type(element) for element in e]:
                    
                    element_frame = tk.Frame(self.small_frame)
                    [element_frame.rowconfigure(i2, weight=w) for i2,w in enumerate([100,1,100])]
                    
                    element_frame.grid(row=0,column=0,sticky="")
                    upper_frame = tk.Frame(element_frame)
                    upper_frame.rowconfigure(0, weight=1)
                    upper_frame.columnconfigure(0, weight=1)
                    upper_frame.grid(row=0,column=0,sticky="")

                    middle_frame = tk.Frame(element_frame,bg="black")
                    middle_frame.rowconfigure(0, weight=1)
                    middle_frame.columnconfigure(0, weight=1)
                    middle_frame.grid(row=1,column=0,sticky="ewsn")

                    lower_frame = tk.Frame(element_frame)
                    lower_frame.rowconfigure(0, weight=1)
                    lower_frame.columnconfigure(0, weight=1)
                    lower_frame.grid(row=2,column=0,sticky="")
                    
                    no_of_mul = [a for a,b in enumerate(e) if type(b) is MG.Mul ]
                    no_of_div = [a for a,b in enumerate(e) if type(b) is MG.Div ]
                    [element_frame.columnconfigure(a, weight=1) for a in range(len(no_of_mul) if len(no_of_mul) > len(no_of_div) else len(no_of_div))]
                    upper_small_frame = tk.Frame(upper_frame)
                    if type(e[0]) == MG.Element:
                        first = Element_Frame(e[0],upper_small_frame,font_size=self.font_size)
                    elif type(e[0]) == MG.Block:
                        first = Block_Frame(e[0],upper_small_frame,font_size=self.font_size)
                    upper_small_frame.grid(row=0,column=0,sticky="")

                    for i,k in enumerate(no_of_mul):
                        upper_frame.columnconfigure(i, weight=1)
                        upper_small_frame = tk.Frame(upper_frame)
                        if type(e[k+1]) == MG.Element:
                            frame = Element_Frame(e[k+1],upper_small_frame,font_size=self.font_size)
                        elif type(e[k+1]) == MG.Block:
                            frame = Block_Frame(e[k+1],upper_small_frame,font_size=self.font_size)
                        upper_small_frame.grid(row=0,column=i+1,sticky="")

                    for i,k in enumerate(no_of_div):
                        lower_small_frame = tk.Frame(lower_frame)
                        lower_small_frame.columnconfigure(i, weight=1)
                        if type(e[k+1]) == MG.Element:
                            frame = Element_Frame(e[k+1],lower_small_frame,font_size=self.font_size)
                        elif type(e[k+1]) == MG.Block:
                            frame = Block_Frame(e[k+1],lower_small_frame,font_size=self.font_size)
                        lower_small_frame.grid(row=0,column=i+1,sticky="")

                else: # for mul only
                    
                    self.small_frame.columnconfigure(0, weight=1)
                    first_frame = tk.Frame(self.small_frame)
                    if type(e[0]) is MG.Element:
                        first = Element_Frame(e[0],first_frame,font_size=self.font_size)
                    elif type(e[0]) is MG.Block:
                        first = Block_Frame(e[0],first_frame,font_size=self.font_size)
                    first_frame.grid(row=0,column=0,sticky="")
                    if len(e) > 1:
                        no_of_mul = [a for a,b in enumerate(e) if type(b) is MG.Mul ]
                        for i,k in enumerate(no_of_mul):
                            other_frame = tk.Frame(self.small_frame)
                            self.small_frame.columnconfigure(i+1, weight=1)
                            if type(e[k+1]) == MG.Element:
                                frame = Element_Frame(e[k+1],other_frame,font_size=self.font_size)
                            elif type(e[k+1]) == MG.Block:
                                frame = Block_Frame(e[k+1],other_frame,font_size=self.font_size)
                            other_frame.grid(row=0,column=i+1,sticky="")
            if type(e) == MG.Add or type(e) == MG.Sub:
                frame = tk.Frame(self.small_frame)
                frame.rowconfigure(0, weight=1)
                frame.columnconfigure(0, weight=1)
                frame.grid(row=0,column=i,sticky="")    
                label = tk.Label(frame,text=e.string_form,font=("Arial",self.font_size))
                label.grid(row=0,column=0,sticky="")
        if len(self.element.expression) > 1:
            close_bracket_frame = tk.Frame(self.expression_frame)
            close_bracket_frame.grid(row=0,column=len(formatted_expression)+1,sticky="")
            label = tk.Label(close_bracket_frame,text=")",font=("Arial",self.font_size))
            label.grid(row=0,column=0,sticky="")
                
        if self.element.power != 1:
            self.power_frame = tk.Frame(self.main_frame)
            self.power_frame.rowconfigure(0, weight=1)
            self.power_frame.columnconfigure(0, weight=1)
            self.power_frame.grid(row=0,column=len(formatted_expression)+2,sticky="n")
            if type(self.element.power) is int or type(self.element.power) is float:
                self.power_label = tk.Label(self.power_frame,text=str(self.element.power),font=("Arial",int(self.font_size//2)))
                self.power_label.grid(row=0,column=0,sticky="")
            else:
                if type(self.element.power) is MG.Element:
                    element_frame = tk.Frame(self.power_frame)
                    element_frame.grid(row=0,column=0,sticky="n")
                    element_frame.rowconfigure(0, weight=1)
                    element_frame.columnconfigure(0, weight=1)
                    frame = Element_Frame(self.element.power,element_frame,font_size=int(self.font_size//2))
                elif type(self.element.power) is MG.Block:
                    block_frame = tk.Frame(self.power_frame)
                    block_frame.grid(row=0,column=0,sticky="n")
                    block_frame.rowconfigure(0, weight=1)
                    block_frame.columnconfigure(0, weight=1)
                    frame = Block_Frame(self.element.power,block_frame,font_size=int(self.font_size//2))
    
        
                
if __name__ == "__main__":
    print("Hello World")
    root = tk.Tk()
    root.title("Math Quiz")
    root.geometry("800x600")
    root.resizable(False,False)


    _ = Quiz_Pages(root)
    print("Quiz_Pages created")
    root.mainloop()
    print("end")