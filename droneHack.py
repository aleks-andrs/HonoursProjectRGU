#!/usr/bin/python

import tkinter as tk
from tkinter import font  as tkfont
from tkinter import ttk
import os
import sys
import csv
import subprocess
#import pexpect
import _thread
import time

class AccessPoint:
    #access point object
    def __init__(self, connectionArray, counter):
        self.BSSID = connectionArray[0]
        self.channel = connectionArray[3]
        self.privacyType = connectionArray[5]
        self.power = connectionArray[8]
        if connectionArray[13] == " ":
            self.ESSID = " N/A "
        else:
            self.ESSID = connectionArray[13]
        self.c = str(counter)        

    def APtoString(self):
        if self.c != "0":
            return("MAC address: " + self.BSSID + "; channel:" + self.channel +
                  "; power:" + self.power + "; ENC:" + self.privacyType + "; name:" +
                  self.ESSID)
        else:
            return(" ")

class ClientComs:
    #client communications object
    def __init__(self, connectionArray, counter):
        self.power = connectionArray[3]
        self.MAC = connectionArray[0]
        self.packets = connectionArray[4]
        if connectionArray[5] == " ":
            self.BSSID = " N/A "
        else:
            self.BSSID = connectionArray[5]
        self.c = str(counter)

    def CCtoString(self):
        if self.c != "0":
            return("Station MAC:" + self.MAC + "; packets:" + self.packets)
        else:
            return(" ")

class CurrentConfiguration:
    #current device configuration
    def __init__(self, interfacesList):
        self.interfacesNIC = interfacesList
        #default values
        self.NIC = "wlan0"
        self.NICmon = "wlan0mon"

    def setNIC(self, value):
        self.NIC = value
        
    def setNICmon(self, value):
        self.NICmon = value
        
    def getNIC(self):
        return self.NIC
    
    def getNICmon(self):
        return self.NICmon

    def getInterfaces(self):
        return self.interfacesNIC

class DroneHackApp(tk.Tk):

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
                             relief = 'flat')
        self.style.map("TButton",
                       background=[('active', '#191919')])
        self.configure(background = '#000000')

        #display app fullscreen
        self.attributes("-fullscreen", True)

        #calculate screen size
        self.xScreenRes = self.winfo_screenwidth() 
        self.yScreenRes = self.winfo_screenheight()
        self.geometry('+100+100')
        #print(self.xScreenRes) #test output
        #print(self.yScreenRes)

        self.deviceType = ""
        #assign device screen type (small/large)
        if self.xScreenRes < 800 or self.yScreenRes < 500:
            self.deviceType = "small"
        else:
            self.deviceType = "large"

        #set screen view dimensions
        self.screenViewX = 100 #default values
        self.screenViewY = 100
        if self.deviceType == "large":
            self.screenViewX = 830
            self.screenViewY = 560
        else:
            self.screenViewX = self.xScreenRes
            self.screenViewY = self.yScreenRes

        #application default settings
        self.interfaces = []
        self.updateInterfaces()
        self.listOfAP = []
        self.listOfCC = []

        #store frames in container
        container = tk.Frame(self, background = '#000000')
        container.grid(row=1, column=1)
        self.grid_rowconfigure(1, weight = 1)
        self.grid_columnconfigure(1, weight = 1)
        
        self.frames = {}
        self.pages = {MainPage, StartPage,
                      AboutPage, SettingsPage,
                      SelectionPage, ScanNetworkPage,
                      SingleAttackPage, BroadcastAttackPage}
        for P in self.pages:
            page_name = P.__name__
            frame = P(parent=container, controller=self)
            frame.grid(row = 0, column = 0, sticky = 'nsew')
            frame.configure(background = '#990000', width = self.screenViewX, height = self.screenViewY)
            frame.grid_rowconfigure(0, weight = 1)
            frame.grid_columnconfigure(0, weight = 1)
            frame.grid_propagate(False)
            self.frames[page_name] = frame

        #keybord bindings
        self.bind('<Escape>', self.exit_full_screen)
        self.bind('<F11>', self.enter_full_screen)
        self.bind('<Control-q>', self.shut_down)
        
        #display Main page
        self.show_frame("MainPage")

    def show_frame(self, page_name):
            frame = self.frames[page_name]
            frame.tkraise()
            #keyboard button handlers for each frame
            if page_name.__eq__("MainPage"):
                self.bind('2', (lambda event: self.show_frame("SettingsPage")))
                self.bind('3', (lambda event: self.show_frame("AboutPage")))
                self.bind('9', self.shut_down)
            elif page_name.__eq__("AboutPage"):
                self.unbind('3')
            elif page_name.__eq__("SettingsPage"):
                self.unbind('3')


    def exit_full_screen(self, *args):
        if(self.attributes("-fullscreen")):
            self.attributes("-fullscreen", False)


    def enter_full_screen(self, *args):
        if(not self.attributes("-fullscreen")):
            self.attributes("-fullscreen", True)
            

    def readCSV(self, filename):
        #csv file reader
        with open(filename,'r') as f:
            fileContents = f.read()
        parts = fileContents.split('\r\n\r\n')
        entries = parts[0]
        
        if sys.version_info[0] < 3:
            from StringIO import StringIO
        else:
            from io import StringIO
        
        entriesStr = StringIO(entries)
        readerObj = csv.reader(entriesStr)
        entryList = list(readerObj)
        connectionsList = [i for i in entryList if i != []]
        return connectionsList

    def getAllInterfaces(self):
        return os.listdir('/sys/class/net/')

    def updateInterfaces(self):
        self.shortenedInterfaces = []
        self.interfaces = self.getAllInterfaces()
        for interface in self.interfaces:
            if interface.startswith("lo"):
                #do nothing
                True
            elif interface.startswith("eth"):
                #do nothing
                True
            else:
                self.shortenedInterfaces.append(interface)
        self.configurationSettings = CurrentConfiguration(self.shortenedInterfaces)
        
    def shut_down(self, *args):
        self.destroy()







class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        #scrollable canvas
        areaMPCanvas = tk.Canvas(self, background = '#000000', highlightthickness = 0)
        areaMPCanvas.grid(row = 0, column = 0, sticky = 'nsew')
        
        #initialize vertical scrollbar
        vBarMP = tk.Scrollbar(self, orient = tk.VERTICAL, background = '#00ff41')
        vBarMP.grid(row = 0, column = 1, rowspan = 1, sticky = 'ns')
        vBarMP.config(command=areaMPCanvas.yview)
        areaMPCanvas.configure(yscrollcommand=vBarMP.set)

        #add horizonal bar for smaller devices
        if controller.deviceType == "small":
            hBarMP = tk.Scrollbar(self, orient = tk.HORIZONTAL, background = '#00ff41')
            hBarMP.grid(row = 1, column = 0, rowspan = 1, sticky = 'ew')
            hBarMP.config(command=areaMPCanvas.xview)
            areaMPCanvas.configure(xscrollcommand=hBarMP.set)
        

        #scrollable main page frame
        mainMPFrame = tk.Frame(areaMPCanvas, background = '#000000')
        areaMPCanvas.create_window((0, 0), window=mainMPFrame, anchor = 'nw')
        
        #internal frames
        logoMPFrame = tk.Frame(mainMPFrame, background = '#000000')
        optionsMPFrame = tk.Frame(mainMPFrame, background = '#000000')
        logoMPFrame.grid(row = 0, column = 0, sticky = 'nsew')
        optionsMPFrame.grid(row = 1, column = 0, sticky = 'nsew')

        #display frame containing logo for large screen devices
        if(controller.deviceType == "large"):
            logoEmptyLineMPLabel = tk.Label(optionsMPFrame,
                             text = " ",
                             background = '#000000',
                             foreground = '#00ff41',
                             font=controller.text_font)
            logoEmptyLineMPLabel.grid(row = 0, column = 20, sticky = 'nsew')
         
            
            logo1 = tk.Label(logoMPFrame,
                             text = "==============================================================",
                             background = '#000000',
                             foreground = '#00ff41',
                             font=controller.text_font)
            logo1.grid(row = 1, column = 0, columnspan = 20, sticky = 'nsew')

            logo2 = tk.Label(logoMPFrame,
                             text = "#",
                             background = '#000000',
                             foreground = '#0000ff',
                             font=controller.text_font)
            logo2.grid(row = 2, column = 19, sticky = 'nsew')

            logo3 = tk.Label(logoMPFrame,
                             text = "#",
                             background = '#000000',
                             foreground = '#0000ff',
                             font=controller.text_font)
            logo3.grid(row = 3, column = 0, sticky = 'nsew')

            logo4 = tk.Label(logoMPFrame,
                             text = "#",
                             background = '#000000',
                             foreground = '#0000ff',
                             font=controller.text_font)
            logo4.grid(row = 4, column = 1, sticky = 'nsew')

            logo5 = tk.Label(logoMPFrame,
                             text = "L",
                             background = '#000000',
                             foreground = '#0000ff',
                             font=controller.text_font)
            logo5.grid(row = 5, column = 2, sticky = 'nsew')
            
            logo6 = tk.Label(logoMPFrame,
                             text = "#",
                             background = '#000000',
                             foreground = '#0000ff',
                             font=controller.text_font)
            logo6.grid(row = 6, column = 3, sticky = 'nsew')
            
            logo7 = tk.Label(logoMPFrame,
                             text = "#",
                             background = '#000000',
                             foreground = '#0000ff',
                             font=controller.text_font)
            logo7.grid(row = 7, column = 4, sticky = 'nsew')
            
            logo8 = tk.Label(logoMPFrame,
                             text = "#",
                             background = '#000000',
                             foreground = '#0000ff',
                             font=controller.text_font)
            logo8.grid(row = 8, column = 5, sticky = 'nsew')
            
            logo100 = tk.Label(logoMPFrame,
                             text = "==============================================================",
                             background = '#000000',
                             foreground = '#00ff41',
                             font=controller.text_font)
            logo100.grid(row = 9, column = 0, columnspan = 20, sticky = 'nsew')

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
        optionsEmptyLineMPLabel.grid(row = 0, column = 20)

        startMPButton = ttk.Button(optionsMPFrame,
                                   text = "[ 1 ] Start     ",
                                   style = 'TButton',
                                   command = lambda: controller.show_frame("StartPage"))
        startMPButton.grid(row=1, column = 10, sticky = 'w')

        aboutMPButton = ttk.Button(optionsMPFrame,
                                   text = "[ 2 ] Settings  ",
                                   style = 'TButton',
                                   command = lambda: controller.show_frame("SettingsPage"))
        aboutMPButton.grid(row = 2, column = 10, sticky = 'w')

        settingsMPButton = ttk.Button(optionsMPFrame,
                                   text = "[ 3 ] About     ",
                                   style = 'TButton',
                                   command = lambda: controller.show_frame("AboutPage"))
        settingsMPButton.grid(row = 3, column = 10, sticky = 'w')

        shutDownMPButton = ttk.Button(optionsMPFrame,
                                   text = "[ 9 ] Shut down ",
                                   style = 'TButton',
                                   command = controller.shut_down)
        shutDownMPButton.grid(row = 4, column = 10, sticky = 'w')
        
        
        #options frame dimensions
        col_count, row_count = optionsMPFrame.grid_size()
        for col in range(col_count):
            optionsMPFrame.grid_columnconfigure(col, minsize = 30)

        for row in range(row_count):
            optionsMPFrame.grid_rowconfigure(row, minsize = 50)

        #update widgets
        mainMPFrame.update_idletasks()
        
        #configure scrollable area
        areaMPCanvas.configure(scrollregion=areaMPCanvas.bbox(tk.ALL))
        

class AboutPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        #scrollable canvas
        areaAPCanvas = tk.Canvas(self, background = '#000000', highlightthickness = 0)
        areaAPCanvas.grid(row = 0, column = 0, sticky = 'nsew')
        
        #initialize vertical scrollbar
        vBarAP = tk.Scrollbar(self, orient = tk.VERTICAL, background = '#00ff41')
        vBarAP.grid(row = 0, column = 1, rowspan = 1, sticky = 'ns')
        vBarAP.config(command=areaAPCanvas.yview)
        areaAPCanvas.configure(yscrollcommand=vBarAP.set)

        #add horizonal bar for smaller devices
        if controller.deviceType == "small":
            hBarAP = tk.Scrollbar(self, orient = tk.HORIZONTAL, background = '#00ff41')
            hBarAP.grid(row = 1, column = 0, rowspan = 1, sticky = 'ew')
            hBarAP.config(command=areaAPCanvas.xview)
            areaAPCanvas.configure(xscrollcommand=hBarAP.set)

        #internal scrollable about page frame
        textAPFrame = tk.Frame(areaAPCanvas, background = '#000000')
        areaAPCanvas.create_window((0, 0), window=textAPFrame, anchor = 'nw')

        labelAbout = tk.Label(textAPFrame,
                         text = "This is the info page \n Bla Bla",
                         background = '#000000',
                         foreground = '#ffffff',
                         font=controller.text_font)
    
        exitAPButton = ttk.Button(textAPFrame,
                                    text = "Back to Main Page",
                                    style = 'TButton',
                                    command = lambda: controller.show_frame("MainPage"))

        labelAbout.grid(row = 0, column = 0, padx = (10, 10))
        exitAPButton.grid(row = 1, column = 0, sticky = 'nsew', padx = ((controller.screenViewX/3), 10), pady = (30, 30))
        
        #dynamically update widgets
        textAPFrame.update_idletasks()
        



class SettingsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        #scrollable canvas
        areaSPCanvas = tk.Canvas(self, background = '#000000', highlightthickness = 0)
        areaSPCanvas.grid(row = 0, column = 0, sticky = 'nsew')
        
        #initialize vertical scrollbar
        vBarSP = tk.Scrollbar(self, orient = tk.VERTICAL, background = '#00ff41')
        vBarSP.grid(row = 0, column = 1, rowspan = 1, sticky = 'ns')
        vBarSP.config(command=areaSPCanvas.yview)
        areaSPCanvas.configure(yscrollcommand=vBarSP.set)

        #add horizonal bar for smaller devices
        if controller.deviceType == "small":
            hBarSP = tk.Scrollbar(self, orient = tk.HORIZONTAL, background = '#00ff41')
            hBarSP.grid(row = 1, column = 0, rowspan = 1, sticky = 'ew')
            hBarSP.config(command=areaSPCanvas.xview)
            areaSPCanvas.configure(xscrollcommand=hBarSP.set)

        #internal scrollable settings page frame
        displaySPFrame = tk.Frame(areaSPCanvas, background = '#000000')
        areaSPCanvas.create_window((0, 0), window=displaySPFrame, anchor = 'nw')
        
        #bash command
        bashCommand = "ifconfig"
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        
        #display area
        infoSPText = tk.Text(displaySPFrame, height=12, width=100, background="blue")
        infoSPText.grid(row = 0, column = 0, columnspan = 10, sticky = 'nsew')
        infoSPText.tag_config("here", background="blue", foreground="green")
        infoSPText.insert(1.0, output)
        
        #exit button
        exitSPButton = ttk.Button(displaySPFrame,
                                  text = "Back to Main Page",
                                  style = 'TButton',
                                  command = lambda: controller.show_frame("MainPage"))
        exitSPButton.grid(row = 1, column = 0, sticky = 'nsew', padx = ((controller.screenViewX/3), 10), pady = (30, 30))

        #dynamically update widgets
        displaySPFrame.update_idletasks()
        
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        #get network interfaces
        bashCommand = "ifconfig"
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()

        #text label
        textStPLabel = tk.Label(self,
                                text = "Select a network card to use in monitor mode:",
                                background = '#000000',
                                foreground = '#ffffff',
                                font=controller.text_font)
        textStPLabel.grid(row = 0, column = 0, sticky = 'nsew')

        #display network interfaces
        self.outputStPText = tk.Text(self, height=12, background="blue")
        self.outputStPText.grid(row = 1, column = 0, sticky = 'nsew')
        self.outputStPText.tag_config("here", background="blue", foreground="green")
        self.outputStPText.insert(1.0, output)

        #choose network interfaces
        NICs = controller.configurationSettings.getInterfaces()
        NICcounter = 0;

        #NICs buttons
        for n in NICs:
            interfaceName = str(NICs[NICcounter])
            ttk.Button(self,
                       text=interfaceName,
                       style = 'TButton',
                       command = lambda idx = interfaceName: self.start_monitor_mode(idx)).grid(row = NICcounter+2, column = 0, sticky = 'nsew')
            NICcounter = NICcounter + 1

        #back to main menu button
        backStPButton = ttk.Button(self,
                                  text = "Back to Main Page",
                                  style = 'TButton',
                                  command = lambda: controller.show_frame("MainPage"))
        backStPButton.grid(row = NICcounter+2, column = 0, sticky = 'nsew')
        
    def start_monitor_mode(self, selectedInterface):
        self.outputStPText.delete(1.0, tk.END)
        self.outputStPText.insert(1.0, "Starting monitor mode...")

        #bash command for network process kill (at most 5 processes)
        checkKillCommand = "airmon-ng check kill"
        i = 0
        while i<5:
            process = subprocess.Popen(checkKillCommand.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()
            if len(output)<4:
                break
            i += 1

        #bash command for monitor mode
        startMonitorModeCommand = "airmon-ng start" 
        startMonitorModeCommand = startMonitorModeCommand + " " + selectedInterface

        #start monitor mode on specified NIC
        process = subprocess.Popen(startMonitorModeCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        
        if selectedInterface.endswith("mon"):
            self.controller.configurationSettings.setNICmon(selectedInterface)
        else:
            self.controller.configurationSettings.setNIC(selectedInterface)
            self.controller.configurationSettings.setNICmon(selectedInterface+"mon")
            
        self.controller.show_frame("SelectionPage")

class SelectionPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        scanSePButton = ttk.Button(self,
                                   text = "Scan network",
                                   style = 'TButton',
                                   command = lambda: controller.show_frame("ScanNetworkPage"))
        scanSePButton.grid(row = 1, column = 0, sticky = 'nsew')

        singleAttackSePButton = ttk.Button(self,
                                           text = "Run single attack",
                                           style = 'TButton',
                                           command = lambda: controller.show_frame("SingleAttackPage"))
        singleAttackSePButton.grid(row = 2, column = 0, sticky = 'nsew')

        broadcastSePButton = ttk.Button(self,
                                        text = "Run broadcast attack",
                                        style = 'TButton',
                                        command = lambda: controller.show_frame("BroadcastAttackPage"))
        broadcastSePButton.grid(row = 3, column = 0, sticky = 'nsew')

        mainPageSePButton = ttk.Button(self,
                                       text = "Main page",
                                       style = 'TButton',
                                       command = lambda: controller.show_frame("MainPage"))
        mainPageSePButton.grid(row = 4, column = 0, sticky = 'nsew')



class ScanNetworkPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.scanResults = []

        #display area
        self.netsSNPText = tk.Text(self, height = 20, background = "blue")
        self.netsSNPText.grid(row = 0, column = 0, sticky = 'nsew')
        self.netsSNPText.tag_config("here", background="blue", foreground = "green")
        self.netsSNPText.insert(1.0, "Scan networks")

        #scan button
        startScanSNPButton = ttk.Button(self,
                                        text = "Scan networks",
                                        style = 'TButton',
                                        command = lambda: self.scanNetworks(5))
        startScanSNPButton.grid(row = 1, column = 0, sticky = 'nsew')



        #return button
        returnSNPButton = ttk.Button(self,
                                     text = "Return",
                                     style = 'TButton',
                                     command = lambda: controller.show_frame("SelectionPage"))
        returnSNPButton.grid(row = 2, column = 0, sticky = 'nsew')
        

    def scanNetworks(self, seconds):
        #bash command for network scan
        bashCommand = "timeout 7 airodump-ng -w netOutput --output-format csv wlan1mon"
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        
        #read results from csv file
        try:
            self.scanResults = self.controller.readCSV("netOutput-01.csv")

            try:
                os.remove("netOutput-01.csv")
            except:
                True
        
            #length counters
            counterAP = 0
            counterCC = 0

            #save results as objects
            for connection in self.scanResults:
                #access points
                if len(connection) == 15:
                    newAccessPoint = AccessPoint(connection, counterAP)
                    self.controller.listOfAP.append(newAccessPoint)
                    counterAP += 1
                    
                #connections
                if len(connection)==7:
                    newClientComs = ClientComs(connection, counterCC)
                    self.controller.listOfCC.append(newClientComs)
                    counterCC += 1

            #display results
            self.netsSNPText.delete(1.0, tk.END)
            for AP in self.controller.listOfAP:
                tempStr = AP.APtoString() + "\n\n"
                self.netsSNPText.insert(tk.END, tempStr)
            
            for CC in self.controller.listOfCC:
                tempStr = CC.CCtoString() + "\n\n"
                self.netsSNPText.insert(tk.END, tempStr)

        except:
            self.netsSNPText.delete(1.0, tk.END)
            self.netsSNPText.insert(1.0, "Unable to read CSV file, check your permissions")


class SingleAttackPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        #display area
        self.detailsSAPText = tk.Text(self, height = 20, background = "blue")
        self.detailsSAPText.grid(row = 0, column = 0, sticky = 'nsew')
        self.detailsSAPText.tag_config("here", background="blue", foreground = "green")
        self.detailsSAPText.insert(1.0, "Run single DoS attack\nREFRESH TO UPDATE LIST")

        #refresh button
        refreshSAPButton = ttk.Button(self,
                                      text = "Refresh",
                                      style = 'TButton',
                                      command = lambda: self.refreshSA())
        refreshSAPButton.grid(row = 1, column = 0, sticky = 'nsew')

        #return button
        returnSAPButton = ttk.Button(self,
                                     text = "Return",
                                     style = 'TButton',
                                     command = lambda: controller.show_frame("SelectionPage"))
        returnSAPButton.grid(row = 2, column = 0, sticky = 'nsew')

    def refreshSA(self):
        if len(self.controller.listOfAP) < 1:
            self.detailsSAPText.delete(1.0, tk.END)
            self.detailsSAPText.insert(1.0, "NO ACCESS POINTS FOUND\nPlease perform a network scan")
        else:
            #record a number of access points
            numberOfAP = len(self.controller.listOfAP)
            #display access points
            self.detailsSAPText.delete(1.0, tk.END)
            for AP in self.controller.listOfAP:
                tempStr = AP.APtoString() + "\n\n"
                self.detailsSAPText.insert(tk.END, tempStr)

    def runSingleAttack(self):
        #bash command for broadcast scan
        bashCommand = "aireplay-ng -0 10 -a " + selectedMAC + " -c " + selectedMAC2 + " wlan1mon"
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()

        



class BroadcastAttackPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        #display area
        self.detailsBAPText = tk.Text(self, height = 20, background = "blue")
        self.detailsBAPText.grid(row = 0, column = 0, sticky = 'nsew')
        self.detailsBAPText.tag_config("here", background="blue", foreground = "green")
        self.detailsBAPText.insert(1.0, "Run broadcast DoS attack\nREFRESH TO UPDATE LIST")

        #refresh button
        refreshBAPButton = ttk.Button(self,
                                      text = "Refresh",
                                      style = 'TButton',
                                      command = lambda: self.refreshBA())
        refreshBAPButton.grid(row = 1, column = 0, sticky = 'nsew')

        #return button
        returnBAPButton = ttk.Button(self,
                                     text = "Return",
                                     style = 'TButton',
                                     command = lambda: controller.show_frame("SelectionPage"))
        returnBAPButton.grid(row = 2, column = 0, sticky = 'nsew')

    def refreshBA(self):
        if len(self.controller.listOfCC) < 1:
            self.detailsBAPText.delete(1.0, tk.END)
            self.detailsBAPText.insert(1.0, "NO COMMUNICATIONS FOUND\nPlease perform a network scan")
        else:
            #record a number of client communications
            numberOfCC = len(self.controller.listOfCC)
            #display communications
            self.detailsBAPText.delete(1.0, tk.END)
            for CC in self.controller.listOfCC:
                tempStr = CC.CCtoString() + "\n\n"
                self.detailsBAPText.insert(tk.END, tempStr)

        def runBroadcastAttack(self):
            #bash command for broadcast scan
            bashCommand = "aireplay-ng -0 10 -a " + selectedMAC + " wlan1mon"
            process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()




        #threads and stuff for later use
        '''
        self.outputStPText = tk.Text(self, height=12, width=100, background="blue")
        self.outputStPText.grid(row = 0, column = 0, sticky = 'nsew')
        
        scanStPButton = ttk.Button(self,
                                 text = "Scan for networks",
                                 style = 'TButton',
                                 command = self.start_thread)

        scanStPButton.grid(row = 1, column = 0, sticky = 'nsew')

        testStPButton = ttk.Button(self,
                                 text = "Emergency stop",
                                 style = 'TButton',
                                 command = self.stop_thread)
        testStPButton.grid(row = 2, column = 0, sticky = 'nsew')

    def start_thread(self):
        _thread.start_new_thread(self.start_monitor_mode, ())

    def stop_thread(self):
        _thread.exit()
        
    def start_monitor_mode(self):
        #bash command for network process kill
        #bashCommand = "timeout 5 airodump-ng wlan1"
        #process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        #output, error = process.communicate()
        #x=0
        #print(error)
        #print(output)
        testText = "Application test run"
        self.outputStPText.insert(tk.END, testText)

    def scan_networks(self):
        #bash command for network scan
        
        bashCommand = "timeout 3 airodump-ng wlan1"
        process = subprocess.check_output(["timeout", "3", "airodump-ng", "wlan1"]) #Popen(bashCommand.split(), stdout=subprocess.PIPE)
        #output, error = process.communicate()
        x=0
        #print(error)
        #print(output)
        self.outputStPText.insert(tk.END, process)
        print("Starting up Airodump-ng")
        cmd_airodump = pexpect.spawn('airodump-ng wlan1 --output-format csv -w data')
        cmd_airodump.expect([pexpect.TIMEOUT, pexpect.EOF], 5)
        print("Airodump-ng Stopping...")
        cmd_airodump.close()
        '''
	
if __name__ == "__main__":
    app = DroneHackApp()
    app.mainloop()
