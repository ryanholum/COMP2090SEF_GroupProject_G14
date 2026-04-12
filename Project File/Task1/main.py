import Main_Page_UI_Generating as Main_Page
import Quiz_Page_UI_Generating as Quiz_Page
import new_Math_Generating as Math
import tkinter as tk


    

    


if  __name__ == '__main__':
    root = tk.Tk()
    root.geometry("800x600")
    root.rowconfigure(0,weight=1)
    root.columnconfigure(0,weight=1)
    root.title("Math Quiz")
    main_page = Main_Page.Main_Page(root)
    main_page.set_next_page(Quiz_Page.Quiz_Pages)
    main_page.grid()
   
    
    
    
    root.mainloop()
