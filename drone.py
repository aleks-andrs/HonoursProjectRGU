#!/usr/bin/python

from tkinter import *

def exitFullScreen(event):
    if(root.attributes("-fullscreen")):
        b3.configure(text="Enter Full Screen")
        root.attributes("-fullscreen", False)
        root.configure(background='black', padx=100)

def enterFullScreen(event):
    if(not root.attributes("-fullscreen")):
        b3.configure(text="Exit Full Screen")
        root.attributes("-fullscreen", True)
        root.configure(background='black', padx=x0)

def switchWindowSize():
    if(not root.attributes("-fullscreen")):
        enterFullScreen(True)
    else:
        exitFullScreen(True)

def shutDown():
    root.destroy()

if __name__ == '__main__':
    root = Tk()
    root.title("Drone Hack")
    root.geometry("+100+100")
    
    #Calculate screen size
    x0 = root.winfo_screenwidth()/2-300
    y0 = root.winfo_screenheight()/2
    print(x0)
    print(y0)

    #Display app fullscreen
    root.attributes("-fullscreen", True)

    #Frame colour&size
    root.configure(background='black', padx=x0)
    #Generate frames
    logo_frame = Frame(root, background='green')
    options_frame = Frame(root, background='red')

    #Key bindings
    #Escape to exit fullscreen
    root.bind("<Escape>", exitFullScreen)
    #F11 to enter fullscreen
    root.bind("<F11>", enterFullScreen)


    l1 = Label(logo_frame, text = "==================================================")
    l2 = Label(logo_frame, text = " ", background='green')
    l3 = Label(logo_frame, text = "H")
    l4 = Label(logo_frame, text = "H")
    l5 = Label(logo_frame, text = "H")
    l6 = Label(logo_frame, text = "H")
    l7 = Label(logo_frame, text = "H")
    l8 = Label(logo_frame, text = "H")
    l9 = Label(logo_frame, text = "H")
    l10 = Label(logo_frame, text = "H")
    l11 = Label(logo_frame, text = "H")
    l12 = Label(logo_frame, text = "H")
    l13 = Label(logo_frame, text = "H", font='consolas 14 bold')
    l14 = Label(logo_frame, text = "H")
    l15 = Label(logo_frame, text = "H")
    l16 = Label(logo_frame, text = "H")
    l17 = Label(logo_frame, text = "H")
    l18 = Label(logo_frame, text = "H")

    l1.grid(row=0, column=0, columnspan = 50)
    l2.grid(row=1, column=1)
    l3.grid(row=2, column=2)
    l4.grid(row=3, column=3)
    l5.grid(row=4, column=4)
    l6.grid(row=5, column=5)
    l7.grid(row=6, column=6)
    l8.grid(row=7, column=7)
    l9.grid(row=8, column=8)
    l10.grid(row=9, column=9)
    l11.grid(row=10, column=10)
    l12.grid(row=11, column=11)
    l13.grid(row=12, column=12)
    l14.grid(row=13, column=13)
    l15.grid(row=14, column=14)
    l16.grid(row=15, column=15)
    l17.grid(row=16, column=16)
    l18.grid(row=17, column=17)

    b1 = Button(options_frame, text = "Button 1", font='consolas 14 bold')
    #b2 = Button(options_frame, text = "Buttooooooon 2", command = exitFullScreen)
    b3 = Button(options_frame, text = "Exit Full Screen", command = switchWindowSize, font='consolas 14 bold')
    b4 = Button(options_frame, text = "Shut down", command = shutDown, font='consolas 14 bold')
    
    b1.grid(row=1, column=1)
    #b2.grid(row=2, column=1)
    b3.grid(row=2, column=1)
    b4.grid(row=3, column=1)

    logo_frame.grid(row=0,column=0, sticky="")
    options_frame.grid(row=1,column=0, sticky="")
    

    root.mainloop()
