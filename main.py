# TODO move defs and imports into own scripts
import tkinter as tk
from tkinter import *   # generate window for the user to interact with
from tkinter import messagebox
from fpdf import FPDF   # generate pdf with the prompt used and your response
import pickle   # for saving nouns and adjectives to use as
import random


# region pdf, tkinter, and global variable setup


pdf = FPDF()    # initialize pdf information

root = Tk()
root.title('Creature Design Prompts')
root.geometry("400x600")

nounSet = {"school", "field", "t-rex"}
adjSet = {"heroic", "comfy", "educated"}


pdfName = StringVar()
pdfName.set("New Pdf")
prompt = StringVar()
prompt.set("Santa fighting Global Warming")
usersResponse = StringVar()
usersResponse.set("Something went Wrong")
#endregion

typingText = Text() # todo this is here for testing purposes


# region timer ui
time = 0

hour = StringVar()
minute = StringVar()
second = StringVar()

# setting the default value as 0
hour.set("00")
minute.set("00")
second.set("00")

# Use of Entry class to take input from the user
hourLabel = Label(root, text="Hours")
hourLabel.grid(row=3, column=1)

hourEntry = Entry(root, width=3, font=("Arial", 18, ""), textvariable=hour)
hourEntry.grid(row=4, column=1)

minuteLabel = Label(root, text="Minutes")
minuteLabel.grid(row=3, column=2)

minuteEntry = Entry(root, width=3, font=("Arial", 18, ""), textvariable=minute)
minuteEntry.grid(row=4, column=2)

secondLabel = Label(root, text="Seconds")
secondLabel.grid(row=3, column=3)

secondEntry = Entry(root, width=3, font=("Arial", 18, ""), textvariable=second)
secondEntry.grid(row=4, column=3)
#endregion


# region working functions

def generatePrompt():
    nouns = pickle.load(open("nouns.dat", "rb"))
    nounOnePrompt = str(random.sample(set(nouns), 1))[2:-2]
    nounTwoPrompt = str(random.sample(set(nouns), 1))[2:-2]
    adjs = pickle.load(open("adjs.dat", "rb"))
    adjPrompt = str(random.sample(set(adjs), 1))[2:-2]
    return " Please design a {} {} that is {}.".format(nounOnePrompt, nounTwoPrompt, adjPrompt)


def addAdjuctive():
    try:  # if dictionary already saved
        adjs = pickle.load(open("adjs.dat", "rb"))
        adjs.add(newAdjEntry.get().lower())
        pickle.dump(adjs, open("adjs.dat", "wb"))
        print(adjs)
    except:  # if first time using dictionary
        adjSet.add(newAdjEntry.get().lower())
        pickle.dump(adjSet, open("adjs.dat", "wb"))
        print("adj: first entry")


def addNoun():
    try:    # if dictionary already saved
        nouns = pickle.load(open("nouns.dat", "rb"))
        nouns.add(newNounEntry.get().lower())
        pickle.dump(nouns, open("nouns.dat", "wb"))
        print(nouns)
    except:  # if first time using dictionary
        nounSet.add(newNounEntry.get().lower())
        pickle.dump(nounSet, open("nouns.dat", "wb"))
        print("noun: first entry")


def earlyEnd():
    global time
    time = 0


def setupTimer():
    try:
        # the input provided by the user is
        global time
        time = int(hour.get()) * 3600 + int(minute.get()) * 60 + int(second.get())
        print("in setup time, success")
        openSecondWindow()
        startWriting()
    except:
        print("Please input the right value")


#endregion


def openSecondWindow():
    typingWindow = Toplevel()

    global prompt
    prompt = generatePrompt()
    promptText = Label(typingWindow, text=prompt)
    promptText.pack()

    global typingText
    typingText = Text(typingWindow, width=40, height=10)#, textvariable=usersResponse )  #todo on this

    typingText.pack()
    endTypingButton = Button(typingWindow, text="Finish", command=earlyEnd)
    endTypingButton.pack()

    # global pdfName
    # pdfTitle = Entry(newWindow, width=3, font=("Arial", 18, ""), textvariable=pdfName)
    # pdfTitle.pack()


#  todo add user input functionality, bug inside
def startWriting():
    global time
    # time now working as intended
    if time > 0:

        # divmod(firstvalue = timeInSec//60, secondvalue = timeInSec%60)
        mins, secs = divmod(time, 60)

        hours = 0
        if mins > 60:
            # divmod(firstvalue = timeInSec//60, secondvalue
            # = timeInSec%60)
            hours, mins = divmod(mins, 60)


        hour.set("{0:2d}".format(hours))
        minute.set("{0:2d}".format(mins))
        second.set("{0:2d}".format(secs))

        time -= 1
        root.after(1000, startWriting)
    elif time == 0:
        global typingText  # todo working on this also
        print(typingText.get(1.0, tk.END+"-1c"))     #todo this is a test variable
        response = messagebox.askyesno("Time Countdown", "Would you like to save?")
        if response:
            newWindow = Toplevel()
            newWindow.title("save?")
            global pdfName
            pdfTitle = Entry(newWindow, width=3, font=("Arial", 18, ""), textvariable=pdfName)
            pdfTitle.pack()
            savePdfButton = Button(newWindow, text="whatever", command=savePDF)
            savePdfButton.pack()



# todo fix accepting user input from different script
def savePDF():
    global typingText

    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=prompt, ln=1, align='C')
    pdf.line(10, 20, 200, 20)
    pdf.cell(200, 10, txt=typingText.get(1.0, tk.END+"-1c"), ln=2)
    pdf.output("{}.pdf".format(pdfName.get()))
    print("File Saved!")

myButtonStart = Button(root, text="Begin!", command=setupTimer)
myButtonStart.grid(row=5, column=2)


# region adding words ui
newNounLabel = Label(root, text="Noun to add to options")
newNounLabel.grid(row=0, column=3)

newNounEntry = Entry(root, width=3, font=("Arial", 12, ""), textvariable='newNoun')
newNounEntry.grid(row=1, column=3)

nounButton = Button(root, text="Add Noun", command=addNoun)
nounButton.grid(row=1, column=4)

newAdjLabel = Label(root, text="Adjective to add to options")
newAdjLabel.grid(row=0, column=1)

newAdjEntry = Entry(root, width=3, font=("Arial", 12, ""), textvariable='newAdj')
newAdjEntry.grid(row=1, column=1)

adjButton = Button(root, text="Add Adjective", command=addAdjuctive)
adjButton.grid(row=1, column=2)
# endregion

root.mainloop()
