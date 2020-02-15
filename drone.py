#!/usr/bin/python

from tkinter import *

def closeFullScreen():
    root.attributes("-fullscreen", False)
    root.configure(background='black', padx=100)

if __name__ == '__main__':
    root = Tk()
    root.title("Drone Hack")
    
    #Initial screen location
    root.geometry("+100+100")
    
    #Calculate screen size
    x0 = root.winfo_screenwidth()/2
    y0 = root.winfo_screenheight()/2
    print(x0)
    print(y0)

    #Display app fullscreen
    root.attributes("-fullscreen", True)

    #Escape to exit fullscreen
    root.bind("<Escape>", lambda event: root.attributes("-fullscreen", False))
    #F11 to enter fullscreen
    root.bind("<F11>", lambda event: root.attributes("-fullscreen", not root.attributes("-fullscreen")))

    #Frame colour
    root.configure(background='black', padx=x0)
    #Generate frames
    logo_frame = Frame(root, background='green')
    options_frame = Frame(root,background='red')    


    l1 = Label(logo_frame, text = "H")
    l2 = Label(logo_frame, text = "H")
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
    l13 = Label(logo_frame, text = "H")
    l14 = Label(logo_frame, text = "H")
    l15 = Label(logo_frame, text = "H")
    l16 = Label(logo_frame, text = "H")
    l17 = Label(logo_frame, text = "H")
    l18 = Label(logo_frame, text = "H")

    l1.grid(row=0,column=0)
    l2.grid(row=1,column=1)
    l3.grid(row=2,column=2)
    l4.grid(row=3,column=3)
    l5.grid(row=4,column=4)
    l6.grid(row=5,column=5)
    l7.grid(row=6,column=6)
    l8.grid(row=7,column=7)
    l9.grid(row=8,column=8)
    l10.grid(row=9,column=9)
    l11.grid(row=10,column=10)
    l12.grid(row=11,column=11)
    l13.grid(row=12,column=12)
    l14.grid(row=13,column=13)
    l15.grid(row=14,column=14)
    l16.grid(row=15,column=15)
    l17.grid(row=16,column=16)
    l18.grid(row=17,column=17)

    b1 = Button(options_frame, text = "Button 1")
    b2 = Button(options_frame, text = "Buttooooooon 2", command = closeFullScreen)

    b1.grid(row=1,column=1)
    b2.grid(row=2,column=1)


    logo_frame.grid(row=0,column=0, sticky="")
    options_frame.grid(row=1,column=0, sticky="")
     

    root.mainloop()
