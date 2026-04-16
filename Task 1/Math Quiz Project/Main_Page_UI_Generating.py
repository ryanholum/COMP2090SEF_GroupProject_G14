import tkinter as tk

#############
# Main Page #
#############


class Main_Page:
    def __init__(self, window):
        self.window = window
        self.main_frame = tk.Frame(self.window, bg="lightblue")
        self.font_size = 24
    
        self.next_page = None
        self.difficulty = tk.StringVar(value="Easy")
        self.main_page_layout()
        self.set_color(self.main_frame)

        
        
    def get_difficulty(self):
        return self.difficulty.get()
    def set_next_page(self,next_page):
        self.next_page = next_page
    def set_start_button(self):
        self.main_frame.grid_forget()
        q = self.next_page
        question =q(root=self.window,difficulty_level = self.difficulty.get(),change_page = self)
        
        question.grid()
    def update_start_button(self):
        self.start_button.config(command=self.set_start_button)
    def main_page_layout(self):
        # main frame
        [self.main_frame.rowconfigure(i, weight=w) for i, w in enumerate([3, 4, 2])]
        [self.main_frame.columnconfigure(i, weight=w) for i, w in enumerate([1, 8, 1])]

        # title frame
        self.title_frame = tk.Frame(self.main_frame)
        self.title_frame.grid(row=0, column=1, sticky="nsew")
        self.title_frame.rowconfigure(0, weight=1)
        self.title_frame.columnconfigure(0, weight=1)
        self.title_label = tk.Label(self.title_frame, text="Math Quiz", font=("Arial", self.font_size * 2))
        self.title_label.grid(row=0, column=0, sticky="nsew")

        # start button frame
        self.start_button_frame = tk.Frame(self.main_frame)
        self.start_button_frame.grid(row=1, column=1, sticky="nsew")
        self.start_button_frame.rowconfigure(0, weight=1)
        self.start_button_frame.columnconfigure(0, weight=1)
        self.start_button = tk.Button(self.start_button_frame, text="Start", font=("Arial", self.font_size), width=10,height=2,command=None)
        self.start_button.grid(row=0, column=0, sticky="")

        # lower frame
        self.lower_frame = tk.Frame(self.main_frame)
        self.lower_frame.grid(row=2, column=1, sticky="nsew")
        self.lower_frame.rowconfigure(0, weight=1)
        [self.lower_frame.columnconfigure(i, weight=w) for i, w in enumerate([1, 1, 1])]

        # Exit Button
        self.exit_button_frame = tk.Frame(self.lower_frame)
        self.exit_button_frame.grid(row=0, column=2, sticky="nsew")
        self.exit_button_frame.rowconfigure(0, weight=1)
        self.exit_button_frame.columnconfigure(0, weight=1)
        self.exit_button = tk.Button(self.exit_button_frame, text="Exit", font=("Arial", int(self.font_size//2)),command=self.window.destroy, width=6,height=1)
        self.exit_button.grid(row=0, column=0, sticky="")
        # difficulty radio buttons with difficulty "easy" and "hard"
        

        self.difficulty_radio_frame = tk.Frame(self.lower_frame)
        self.difficulty_radio_frame.grid(row=0, column=1, sticky="nsew")
        self.difficulty_radio_frame.rowconfigure(0, weight=1)
        self.difficulty_radio_frame.columnconfigure(0, weight=1)
        self.difficulty_radio_frame.columnconfigure(1, weight=1)
        
        
        self.easy_radio = tk.Radiobutton(self.difficulty_radio_frame, text="Easy", font=("Arial", int(self.font_size//1.7)), variable=self.difficulty, value="Easy", command=self.update_start_button)
        self.easy_radio.grid(row=0, column=0, sticky="nsew")
        self.hard_radio = tk.Radiobutton(self.difficulty_radio_frame, text="Hard", font=("Arial", int(self.font_size//1.7)), variable=self.difficulty, value="Hard", command=self.update_start_button)
        self.hard_radio.grid(row=0, column=1, sticky="nsew")    
        
        # label indicating difficulty level selection
        self.difficulty_label = tk.Label(self.lower_frame, text="Difficulty:", font=("Arial", self.font_size))
        self.difficulty_label.grid(row=0, column=0, sticky="nsew")

            

    def set_color(self,widget):
        widget.config(bg="lightblue")
        for child_widget in widget.winfo_children():
            self.set_color(child_widget)
            

    def grid(self): # make sure all the widgets are in the correct order
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        
        
        
        
        
        
        
        
        
        
        
   


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Math Quiz")
    root.geometry("800x600")
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    main_page = Main_Page(root)
    main_page.main_page_grid()
    root.mainloop()