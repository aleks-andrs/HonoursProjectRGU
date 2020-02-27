#!/usr/bin/python

import subprocess
import tkinter as tk
from tkinter import font  as tkfont
from tkinter import ttk

class DroneHack(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Drone Hack")
        
        #set up application style
        self.text_font = tkfont.Font(family = 'Consolas',
                                     size = 16,
                                     weight = "bold")
        self.style = ttk.Style()
        self.style.configure("TButton",
                             font = ('Consolas',
                                     16,
                                     'bold'),
                             background = '#000000',
                             foreground = '#00ff41',
                             relief='flat')
        self.style.map("TButton",
                       background=[('active', '#191919')])

        #display app fullscreen
        self.attributes("-fullscreen", True)

        #calculate screen size
        self.x0 = self.winfo_screenwidth()/2 - 410
        self.y0 = self.winfo_screenheight()/2
        self.geometry("+100+100")
        print(self.x0)
        print(self.y0)

        #store frames in container
        container = tk.Frame(self)
        container.pack(side = "top", fill = "both", expand=True)
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
        self.frames = {}
        self.pages = {MainPage, AboutPage, SettingsPage}
        for F in self.pages:
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row = 0, column = 0, sticky = 'nsew')

        #keybord bindings
        self.bind("<Escape>", self.exit_full_screen)
        self.bind("<F11>", self.enter_full_screen)

        #display Main page
        self.show_frame("MainPage")

    def show_frame(self, page_name):
            frame = self.frames[page_name]
            frame.tkraise()

    def exit_full_screen(self, page_name):
        if(self.attributes("-fullscreen")):
            self.attributes("-fullscreen", False)
            for P in self.pages:
                frame = self.frames[P.__name__]
                frame.configure(background = '#000000',
                            padx = 10,
                            pady = 10)

    def enter_full_screen(self, page_name):
        if(not self.attributes("-fullscreen")):
            self.attributes("-fullscreen", True)
            for P in self.pages:
                frame = self.frames[P.__name__]
                frame.configure(background = '#000000',
                            padx = self.x0,
                            pady = 100)

            
    def shut_down(self):
        self.destroy()








class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background = '#000000',
                       padx = controller.x0,
                       pady = 100)
        
        #internal frames
        logoFrame = tk.Frame(self, background = '#000000')
        optionsFrame = tk.Frame(self, background = '#000000')

        #frame containing logo
        labelLogoEmptyLine = tk.Label(optionsFrame,
                         text = " ",
                         background = '#000000',
                         foreground = '#00ff41',
                         font=controller.text_font)
        
        logo1 = tk.Label(logoFrame,
                         text = "==============================================================",
                         background = '#000000',
                         foreground = '#00ff41',
                         font=controller.text_font)
        logo2 = tk.Label(logoFrame,
                         text = "#",
                         background = '#000000',
                         foreground = '#0000ff',
                         font=controller.text_font)
        logo3 = tk.Label(logoFrame,
                         text = "#",
                         background = '#000000',
                         foreground = '#0000ff',
                         font=controller.text_font)
        logo4 = tk.Label(logoFrame,
                         text = "#",
                         background = '#000000',
                         foreground = '#0000ff',
                         font=controller.text_font)
        logo5 = tk.Label(logoFrame,
                         text = "L",
                         background = '#000000',
                         foreground = '#0000ff',
                         font=controller.text_font)
        logo6 = tk.Label(logoFrame,
                         text = "#",
                         background = '#000000',
                         foreground = '#0000ff',
                         font=controller.text_font)
        logo7 = tk.Label(logoFrame,
                         text = "#",
                         background = '#000000',
                         foreground = '#0000ff',
                         font=controller.text_font)
        logo8 = tk.Label(logoFrame,
                         text = "#",
                         background = '#000000',
                         foreground = '#0000ff',
                         font=controller.text_font)
        logo100 = tk.Label(logoFrame,
                         text = "==============================================================",
                         background = '#000000',
                         foreground = '#00ff41',
                         font=controller.text_font)
        
        labelLogoEmptyLine.grid(row = 0, column = 20, sticky='nsew')
        logo1.grid(row = 1, column = 0, columnspan = 20, sticky='nsew')
        logo2.grid(row = 2, column = 19, sticky='nsew')
        logo3.grid(row = 3, column = 0, sticky='nsew')
        logo4.grid(row = 4, column = 1, sticky='nsew')
        logo5.grid(row = 5, column = 2, sticky='nsew')
        logo6.grid(row = 6, column = 3, sticky='nsew')
        logo7.grid(row = 7, column = 4, sticky='nsew')
        logo8.grid(row = 8, column = 5, sticky='nsew')
        logo100.grid(row = 9, column = 0, columnspan = 20, sticky='nsew')
        
        col_count, row_count = logoFrame.grid_size()
        for col in range(col_count):
            logoFrame.grid_columnconfigure(col, minsize = 20)

        for row in range(row_count):
            logoFrame.grid_rowconfigure(row, minsize = 20)

        logoFrame.grid(row = 0, column = 0, sticky='nsew')

        #options menu
        labelEmptyLine = tk.Label(optionsFrame,
                         text = " ",
                         background = '#000000',
                         foreground = '#00ff41',
                         font=controller.text_font)
        buttonStart = ttk.Button(optionsFrame,
                                 text = "[ 1 ] Start     ",
                                 style = 'TButton')
        buttonAboutPage = ttk.Button(optionsFrame,
                                   text = "[ 2 ] Settings  ",
                                   style = 'TButton',
                                   command = lambda: controller.show_frame("SettingsPage"))
        buttonSettings = ttk.Button(optionsFrame,
                                   text = "[ 3 ] About     ",
                                   style = 'TButton',
                                   command = lambda: controller.show_frame("AboutPage"))
        buttonShutDown = ttk.Button(optionsFrame,
                                   text = "[ 4 ] Shut down ",
                                   style = 'TButton',
                                   command = controller.shut_down)
        
        labelEmptyLine.grid(row = 0, column = 20, sticky='nsew')
            
        buttonStart.grid(row=1, column = 10, sticky='w')
        buttonAboutPage.grid(row = 2, column = 10, sticky='w')
        buttonSettings.grid(row = 3, column = 10, sticky='w')
        buttonShutDown.grid(row = 4, column = 10, sticky='w')

        col_count, row_count = optionsFrame.grid_size()
        for col in range(col_count):
            optionsFrame.grid_columnconfigure(col, minsize = 30)

        for row in range(row_count):
            optionsFrame.grid_rowconfigure(row, minsize = 50)

        optionsFrame.grid(row = 1, column = 0, sticky='nsew')



        def clickBut(self):
            buttonShutDown.invoke()

        controller.bind("1", clickBut)
        

class AboutPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background = '#000000',
                       padx = controller.x0,
                       pady = 100)

        aboutPageFrame = tk.Frame(self, background = '#000000')

        label = tk.Label(self,
                         text = "This is the info page \n Bla Bla",
                         background = '#000000',
                         foreground = '#ffffff',
                         font=controller.text_font)
        labelEmptyLineAboutPage = tk.Label(aboutPageFrame,
                                           text = " ",
                                           background = '#000000',
                                           foreground = '#00ff41',
                                           font=controller.text_font)
    
        buttonExitAboutPage = ttk.Button(aboutPageFrame,
                                    text = "Back to main page",
                                    style = 'TButton',
                                    command = lambda: controller.show_frame("MainPage"))

        label.grid(row = 0, column = 0, sticky = 'w')
        labelEmptyLineAboutPage.grid(row = 0, column = 20, sticky='nsew')
        buttonExitAboutPage.grid(row = 1, column = 10, sticky = 'w')

##        col_count, row_count = aboutPageFrame.grid_size()
##        for col in range(col_count):
##            aboutPageFrame.grid_columnconfigure(col, minsize = 30)
##
##        for row in range(row_count):
##            aboutPageFrame.grid_rowconfigure(row, minsize = 50)
            
        aboutPageFrame.grid(row = 1, column = 0, sticky = 'nsew')

class SettingsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background = '#000000',
                       padx = controller.x0,
                       pady = 100)
        
        #bash code
        bashCommand = "airmon-ng start wlan1"
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        
        #display area
        textAreaSettingsPage = tk.Text(self, height=12, width=100, background="blue")
        textAreaSettingsPage.grid(row = 0, column = 0, columnspan = 10, sticky = 'nsew')
        textAreaSettingsPage.tag_config("here", background="blue", foreground="green")
        textAreaSettingsPage.insert(1.0, output)
        
        #exit button
        buttonExitSettingsPage = ttk.Button(self,
                                            text = "Back to main page",
                                            style = 'TButton',
                                            command = lambda: controller.show_frame("MainPage"))
        buttonExitSettingsPage.grid(row = 1, column = 0, sticky = 'nsew')

        

if __name__ == "__main__":
    app = DroneHack()
    app.mainloop()
