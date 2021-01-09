# TODO move defs and imports into own scripts
from tkinter import *   # generate window for the user to interact with
from tkinter import messagebox
from fpdf import FPDF   # generate pdf with the prompt used and your response
import time
import pickle   # for saving nouns and adjectives to use as prompts

pdf = FPDF()    # initialize pdf information
pdf.add_page()
pdf.set_font("Arial", size=14)

root = Tk()
root.title('Creature Design Prompts')
root.geometry("400x600")

nounDict = {}
adjDict = {}

# region timer ui
# todo move into own script
# code for the timer
# Declaration of variables
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

def savePDF(name):
    pdf.output("{}.pdf".format(name))
    print("File Saved!")


def addAdjuctive():  # TODO: add functionality to button
    print("adding an adjective")


def addNoun():  # TODO: add functionality to button
    #adds info to save
    #add new variables
    #pickleOut = open("dict.pickle", "wb")
    #pickle.dump(nounDict, pickleOut)
    #pickleOut.close()

    #move after
    #open saved data
    #pickleIn = open("dict.pickle", "rb")
    #nounDict = pickle.load(pickleIn)
    print("adding a noun")



#  todo add user input functionality, bug inside
def startWriting():
    try:
        # the input provided by the user is
        # stored in here :temp
        temp = int(hour.get()) * 3600 + int(minute.get()) * 60 + int(second.get())
    except:
        print("Please input the right value")
    while temp > -1:

        # divmod(firstvalue = temp//60, secondvalue = temp%60)
        mins, secs = divmod(temp, 60)

        # Converting the input entered in mins or secs to hours,
        # mins ,secs(input = 110 min --> 120*60 = 6600 => 1hr :
        # 50min: 0sec)
        hours = 0
        if mins > 60:
            # divmod(firstvalue = temp//60, secondvalue
            # = temp%60)
            hours, mins = divmod(mins, 60)

        # using format () method to store the value up to
        # two decimal places
        hour.set("{0:2d}".format(hours))
        minute.set("{0:2d}".format(mins))
        second.set("{0:2d}".format(secs))

        # updating the GUI window after decrementing the
        # temp value every time
        root.update()
        time.sleep(1)

        # when temp value = 0; then a messagebox pop's up
        # with a message:"Time's up"
        if temp == 0:
            response = messagebox.askyesno("Time Countdown", "Would you like to save?")
            if response:
                newWindow = Toplevel()
                newWindow.title("save?")

                pdfTitle = Entry(newWindow, width=3, font=("Arial", 18, ""))
                pdfTitle.pack()

                savePdfButton = Button(newWindow, text="whatever", command=savePdfButton)  # todo fix functionality
                savePdfButton.pack()

        # after every one sec the value of temp will be decremented
        # by one
        temp -= 1


myButtonStart = Button(root, text="Begin!", command=startWriting)
myButtonStart.grid(row=5, column=2)


# region adding words ui
newNounLabel = Label(root, text="Noun to add to options")
newNounLabel.grid(row=0, column=3)

newNounEntry = Entry(root, width=3, font=("Arial", 12, ""))
newNounEntry.grid(row=1, column=3)

nounButton = Button(root, text="Add Noun", command=addNoun)
nounButton.grid(row=1, column=4)

newAdjLabel = Label(root, text="Adjective to add to options")
newAdjLabel.grid(row=0, column=1)

newAdjEntry = Entry(root, width=3, font=("Arial", 12, ""))
newAdjEntry.grid(row=1, column=1)

adjButton = Button(root, text="Add Adjective", command=addAdjuctive)
adjButton.grid(row=1, column=2)
# endregion

root.mainloop()
