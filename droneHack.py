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
        #print(self.x0) #test output
        #print(self.y0)

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
        self.bind('<Escape>', self.exit_full_screen)
        self.bind('<F11>', self.enter_full_screen)
        self.bind('<Control-q>', self.shut_down)

        #display Main page
        self.show_frame("MainPage")

    def show_frame(self, page_name):
            frame = self.frames[page_name]
            frame.tkraise()
            #various keyboard button handlers for each frame
            if (page_name.__eq__("MainPage")):
                self.bind('2', (lambda event: self.show_frame("SettingsPage")))
                self.bind('3', (lambda event: self.show_frame("AboutPage")))
                self.bind('4', self.shut_down)
            elif (page_name.__eq__("AboutPage")):
                self.unbind('3')
            elif (page_name.__eq__("SettingsPage")):
                self.unbind('3')


    def exit_full_screen(self, *args):
        if(self.attributes("-fullscreen")):
            self.attributes("-fullscreen", False)
            for P in self.pages:
                frame = self.frames[P.__name__]
                frame.configure(background = '#000000',
                            padx = 10,
                            pady = 10)

    def enter_full_screen(self, *args):
        if(not self.attributes("-fullscreen")):
            self.attributes("-fullscreen", True)
            for P in self.pages:
                frame = self.frames[P.__name__]
                frame.configure(background = '#000000',
                            padx = self.x0,
                            pady = 100)
            
    def shut_down(self, *args):
        self.destroy()








class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background = '#000000',
                       padx = controller.x0,
                       pady = 100)
        
        #internal frames
        logoMPFrame = tk.Frame(self, background = '#000000')
        optionsMPFrame = tk.Frame(self, background = '#000000')
        logoMPFrame.grid(row = 0, column = 0, sticky='nsew')
        optionsMPFrame.grid(row = 1, column = 0, sticky='nsew')

        #frame containing logo
        logoEmptyLineMPLabel = tk.Label(optionsMPFrame,
                         text = " ",
                         background = '#000000',
                         foreground = '#00ff41',
                         font=controller.text_font)
        logoEmptyLineMPLabel.grid(row = 0, column = 20, sticky='nsew')
     
        
        logo1 = tk.Label(logoMPFrame,
                         text = "==============================================================",
                         background = '#000000',
                         foreground = '#00ff41',
                         font=controller.text_font)
        logo1.grid(row = 1, column = 0, columnspan = 20, sticky='nsew')

        logo2 = tk.Label(logoMPFrame,
                         text = "#",
                         background = '#000000',
                         foreground = '#0000ff',
                         font=controller.text_font)
        logo2.grid(row = 2, column = 19, sticky='nsew')

        logo3 = tk.Label(logoMPFrame,
                         text = "#",
                         background = '#000000',
                         foreground = '#0000ff',
                         font=controller.text_font)
        logo3.grid(row = 3, column = 0, sticky='nsew')

        logo4 = tk.Label(logoMPFrame,
                         text = "#",
                         background = '#000000',
                         foreground = '#0000ff',
                         font=controller.text_font)
        logo4.grid(row = 4, column = 1, sticky='nsew')

        logo5 = tk.Label(logoMPFrame,
                         text = "L",
                         background = '#000000',
                         foreground = '#0000ff',
                         font=controller.text_font)
        logo5.grid(row = 5, column = 2, sticky='nsew')
        
        logo6 = tk.Label(logoMPFrame,
                         text = "#",
                         background = '#000000',
                         foreground = '#0000ff',
                         font=controller.text_font)
        logo6.grid(row = 6, column = 3, sticky='nsew')
        
        logo7 = tk.Label(logoMPFrame,
                         text = "#",
                         background = '#000000',
                         foreground = '#0000ff',
                         font=controller.text_font)
        logo7.grid(row = 7, column = 4, sticky='nsew')
        
        logo8 = tk.Label(logoMPFrame,
                         text = "#",
                         background = '#000000',
                         foreground = '#0000ff',
                         font=controller.text_font)
        logo8.grid(row = 8, column = 5, sticky='nsew')
        
        logo100 = tk.Label(logoMPFrame,
                         text = "==============================================================",
                         background = '#000000',
                         foreground = '#00ff41',
                         font=controller.text_font)
        logo100.grid(row = 9, column = 0, columnspan = 20, sticky='nsew')

        #logo frame dimensions set up
        col_count, row_count = logoMPFrame.grid_size()
        for col in range(col_count):
            logoMPFrame.grid_columnconfigure(col, minsize = 20)

        for row in range(row_count):
            logoMPFrame.grid_rowconfigure(row, minsize = 20)


        #options menu frame
        optionsEmptyLineMPLabel = tk.Label(optionsMPFrame,
                         text = " ",
                         background = '#000000',
                         foreground = '#00ff41',
                         font=controller.text_font)
        optionsEmptyLineMPLabel.grid(row = 0, column = 20, sticky='nsew')

        startMPButton = ttk.Button(optionsMPFrame,
                                 text = "[ 1 ] Start     ",
                                 style = 'TButton')
        startMPButton.grid(row=1, column = 10, sticky='w')

        aboutMPButton = ttk.Button(optionsMPFrame,
                                   text = "[ 2 ] Settings  ",
                                   style = 'TButton',
                                   command = lambda: controller.show_frame("SettingsPage"))
        aboutMPButton.grid(row = 2, column = 10, sticky='w')

        settingsMPButton = ttk.Button(optionsMPFrame,
                                   text = "[ 3 ] About     ",
                                   style = 'TButton',
                                   command = lambda: controller.show_frame("AboutPage"))
        settingsMPButton.grid(row = 3, column = 10, sticky='w')

        shutDownMPButton = ttk.Button(optionsMPFrame,
                                   text = "[ 4 ] Shut down ",
                                   style = 'TButton',
                                   command = controller.shut_down)
        shutDownMPButton.grid(row = 4, column = 10, sticky='w')
        
            
        #options frame dimensions
        col_count, row_count = optionsMPFrame.grid_size()
        for col in range(col_count):
            optionsMPFrame.grid_columnconfigure(col, minsize = 30)

        for row in range(row_count):
            optionsMPFrame.grid_rowconfigure(row, minsize = 50)
        

class AboutPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background = '#000000',
                       padx = controller.x0,
                       pady = 100)

        #internal frames for text and buttons
        textAPFrame = tk.Frame(self, background = '#000000')

        label = tk.Label(self,
                         text = "This is the info page \n Bla Bla",
                         background = '#000000',
                         foreground = '#ffffff',
                         font=controller.text_font)
        emptyLineAPLabel = tk.Label(textAPFrame,
                                           text = " ",
                                           background = '#000000',
                                           foreground = '#00ff41',
                                           font=controller.text_font)
    
        exitAPButton = ttk.Button(textAPFrame,
                                    text = "Back to main page",
                                    style = 'TButton',
                                    command = lambda: controller.show_frame("MainPage"))

        label.grid(row = 0, column = 0, sticky = 'w')
        emptyLineAPLabel.grid(row = 0, column = 20, sticky='nsew')
        exitAPButton.grid(row = 1, column = 10, sticky = 'w')

##        col_count, row_count = textAPFrame.grid_size()
##        for col in range(col_count):
##            textAPFrame.grid_columnconfigure(col, minsize = 30)
##
##        for row in range(row_count):
##            textAPFrame.grid_rowconfigure(row, minsize = 50)
            
        textAPFrame.grid(row = 1, column = 0, sticky = 'nsew')



class SettingsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background = '#000000',
                       padx = controller.x0,
                       pady = 100)
        
        #bash code
        bashCommand = "ifconfig"
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        
        #display area
        infoSPText = tk.Text(self, height=12, width=100, background="blue")
        infoSPText.grid(row = 0, column = 0, columnspan = 10, sticky = 'nsew')
        infoSPText.tag_config("here", background="blue", foreground="green")
        infoSPText.insert(1.0, output)
        
        #exit button
        exitSPButton = ttk.Button(self,
                                            text = "Back to main page",
                                            style = 'TButton',
                                            command = lambda: controller.show_frame("MainPage"))
        exitSPButton.grid(row = 1, column = 0, sticky = 'nsew')

        

if __name__ == "__main__":
    app = DroneHack()
    app.mainloop()
