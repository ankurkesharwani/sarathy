from Tkinter import *
import os
from time import sleep

#
#	Some Globals we need.
#
navigationDetails = None
messagesDetails = None
frontDetails = None

navigateButton = None
messagesButton = None
backFromNavigationButton = None
messageEntry = None
backFromMessagesButton = None

upImg = None
leftImg = None
rightImg = None
upImgPressed = None
leftImgPressed = None
rightImgPressed = None
frontImage = None
state = 'Neutral'

C_B_AB	= '#E74C3C'
C_B_AF = '#FFFFFF'
C_B_B = '#3A81CC'
C_B_F = '#FFFFFF'
C_B_H = '#E74C3C'
T_B_H = '5'
C_C_B = '#e6e8ea'
C_F_H = '#2ecc71'
T_F_H = '5'
C_I_B = '1C416A'

letters = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
voiceMessages = None
listStatus = 0
selectedWord=None
message = None


def speak(text):
	cmd = 'espeak "{0}" -s 120 2>/dev/null'.format(text)
	os.system(cmd)


def loadWords(letter):
	fin = open(letter, "r")
	words = fin.readline()
	mylist = words.split(', ')
	return mylist
	
def showSplash():
	global navigationDetails,messagesDetails, frontDetails
	navigationDetails.grid_forget()
	messagesDetails.grid_forget()
	#frontDetails.grid(column = 0, row = 0)

def showMessagesModule():
	global navigationDetails,messagesDetails, frontDetails
	navigationDetails.grid_forget()
	#frontDetails.grid_forget()
	messagesDetails.grid(column = 0, row = 0)
	listBox.focus_force()
	speak(voiceMessages[2])

def showNavigateModule():
	global navigationDetails,messagesDetails, frontDetails
	messagesDetails.grid_forget()
	#frontDetails.grid_forget()
	navigationDetails.grid(column = 0, row = 0)
	backFromNavigationButton.focus_force()
	speak(voiceMessages[1])

#
# Navigation Button actions
#
def navActionRight(event):
	messagesButton.focus_force()
	speak(voiceMessages[4])


def navActionDown(event):
	showNavigateModule()

#
# Messages buttons actions
#
def messagesActionLeft(event):
	navigateButton.focus_force()
	speak(voiceMessages[3])

def messagesActionRight(event):
	callForHelpButton.focus_force()

def messagesActionDown(event):
	showMessagesModule()

#
# 
#
def  backActionLeft(event):
	global state
	if(state=='Right'):
		labelTop['image'] = upImg
		labelLeft['image'] = leftImg
		labelRight['image'] = rightImg
		state = 'Neutral'
	else:
		labelTop['image'] = upImg
		labelLeft['image'] = leftImgPressed
		labelRight['image'] = rightImg
		state = 'Left'

def  backActionRight(event):
	global state
	if(state=='Left'):
		labelTop['image'] = upImg
		labelLeft['image'] = leftImg
		labelRight['image'] = rightImg
		state = 'Neutral'
	else:
		labelTop['image'] = upImg
		labelLeft['image'] = leftImg
		labelRight['image'] = rightImgPressed
		state = 'Right'	


def  backActionUp(event):
	global state
	if(state=='Neutral'):
		labelTop['image'] = upImgPressed
		labelLeft['image'] = leftImg
		labelRight['image'] = rightImg
		state = 'Up'

def  backActionDown(event):
	global state
	if(state=='Neutral'):
		navigateButton.focus_force()
		showSplash()
	else:
		labelTop['image'] = upImg
		labelLeft['image'] = leftImg
		labelRight['image'] = rightImg
		state = 'Neutral'

def  backActionDoubleDown(event):
	navigateButton.focus_force()
	showSplash()
	
#
#
#
def listBoxActionLeft(event):
	global listStatus

	if(listStatus==1):
		listBox.delete(first = 0, last = END)
		for letter in letters:
			listBox.insert(END, letter)
		listStatus = 0
	else:
		messageEntry.delete(first = 0, last = END)
		selectedWord = None
		message = None
		backFromMessagesButton.focus_force()

def listBoxActionRight(event):
	global listStatus
	if(listStatus==0):
		file = listBox.get(ACTIVE)
		newWords = loadWords(file)
		listBox.delete(first = 0, last = END)
		for word in newWords:
			listBox.insert(END, word)
		listStatus = 1 
	else:
		message = messageEntry.get()
		selectedWord = listBox.get(ACTIVE)
		messageEntry.delete(first = 0, last = END)
		messageEntry.insert(0, message + ' ' + selectedWord)
		speakButton.focus_force()


def speakActionLeft(event):
	selectedWord = None
	messageEntry.delete(first = 0, last = END)
	#messageEntry.insert(0, message)
	listBox.focus_force()

def speakActionRight(event):
	backFromMessagesButton.focus_force()

def speakActionUp(event):
	selectedWord = None
	message = None
	listBox.focus_force()

def speakActionDown(event):
	print "Speaking ..." + messageEntry.get()
	speak(messageEntry.get())


def backFromMessagesActionLeft(event):
	speakButton.focus_force()

def backFromMessagesActionRight(event):
	listBox.focus_force()

def backFromMessagesActionDown(event):
	showSplash()
	messagesButton.focus_force()


def callForHelpActionLeft(event):
	messagesButton.focus_force()

def callForHelpActionDown(event):
	speak('Help Me. I need some assistance.')	

#
#	Execution Starts here. This is the main entry point.
#
if __name__=="__main__":

	root = Tk()
	root.option_readfile('Config')
	
	voiceMessages = loadWords('Voices')


	frame = Frame(root)
	#
	#	Setup Splash Details screen.
	#
	frontImage = PhotoImage(file='image.gif')
	frontDetails = Frame(frame, width = 800, height = 500)
	imageLabel = Label(frontDetails, image = frontImage)
	imageLabel.pack(fill = BOTH, expand = 1)
	
	#
	#	Setup Messages Details screen.
	#
	messagesDetails = Frame(frame, width = 1024, height = 500)
	messageEntry = Entry(messagesDetails)
	messageEntry.grid(row = 0, column = 0, columnspan = 3, sticky = E+W, pady = 10, padx = 10)
	backFromMessagesButton = Button(messagesDetails, text = 'Exit', pady = 10)
	backFromMessagesButton.grid(row = 1, column = 0, pady = 10, padx = 10)	
	listBox = Listbox(messagesDetails)
	for item in letters:
		listBox.insert(END, item)
	listBox.grid(column = 1, row = 1, pady = 10, padx =10)	
	speakButton = Button(messagesDetails, text = 'Speak', pady = 10, padx = 20)
	speakButton.grid(row = 1, column = 2, pady = 10, padx = 10)

	#
	#	Setup Navigation Details screen.
	#
	navigationDetails = Frame(frame, width = 800, height = 500, padx = 10, pady = 10)	
	backFromNavigationButton = Button(navigationDetails, text = 'Exit' , padx = 20 , pady = 10)
	labelTop = Label(navigationDetails)
	labelLeft = Label(navigationDetails)
	labelRight = Label(navigationDetails)

	upImg = PhotoImage(file='up.gif')
	leftImg = PhotoImage(file='left.gif')
	rightImg = PhotoImage(file='right.gif')
	upImgPressed = PhotoImage(file='up_pressed.gif')
	leftImgPressed = PhotoImage(file='left_pressed.gif')
	rightImgPressed = PhotoImage(file='right_pressed.gif')

	labelTop['image'] = upImg
	labelLeft['image'] = leftImg
	labelRight['image'] = rightImg
	backFromNavigationButton.grid(column = 1, row = 1)
	labelTop.grid(column = 1, row = 0)
	labelLeft.grid(column = 0, row = 1)
	labelRight.grid(column = 2, row = 1)
	
	#
	#	Setup controls panel.
	#
	controls = Frame(frame, background = C_C_B)
	navigateButton = Button(controls, text = 'Navigate', command = showNavigateModule, pady = 10)
	messagesButton = Button(controls, text = 'Messages', command = showMessagesModule, pady = 10)
	callForHelpButton = Button(controls, text = 'Call For Help', pady = 10)
	controls.grid(column = 0, row = 1, sticky = E+W)
	navigateButton.pack(side = LEFT, fill = X, expand = 1, padx = 10 , pady = 10)
	messagesButton.pack(side = LEFT, fill = X, expand = 1, padx = 10, pady = 10)
	callForHelpButton.pack(side = LEFT, fill = X, expand = 1, padx = 10, pady = 10)
	
	#
	# Event bindings.
	#
	navigateButton.bind('<KeyPress-Down>', navActionDown)
	navigateButton.bind('<KeyPress-Right>', navActionRight)

	messagesButton.bind('<KeyPress-Left>', messagesActionLeft)
	messagesButton.bind('<KeyPress-Right>', messagesActionRight)
	messagesButton.bind('<KeyPress-Down>', messagesActionDown)

	backFromNavigationButton.bind('<KeyPress-Left>', backActionLeft)
	backFromNavigationButton.bind('<KeyPress-Right>', backActionRight)
	backFromNavigationButton.bind('<KeyPress-Up>', backActionUp)
	backFromNavigationButton.bind('<KeyPress-Down>', backActionDown)
	#backFromNavigationButton.bind('<KeyPress-Down>', backActionDoubleDown)

	listBox.bind('<KeyPress-Left>', listBoxActionLeft)
	listBox.bind('<KeyPress-Right>', listBoxActionRight)

	speakButton.bind('<KeyPress-Left>', speakActionLeft)
	speakButton.bind('<KeyPress-Right>', speakActionRight)
	speakButton.bind('<KeyPress-Up>', speakActionUp)
	speakButton.bind('<KeyPress-Down>', speakActionDown)

	backFromMessagesButton.bind('<KeyPress-Left>', backFromMessagesActionLeft)
	backFromMessagesButton.bind('<KeyPress-Right>', backFromMessagesActionRight)
	backFromMessagesButton.bind('<KeyPress-Down>', backFromMessagesActionDown)

	callForHelpButton.bind('<KeyPress-Left>', callForHelpActionLeft)
	callForHelpButton.bind('<KeyPress-Down>', callForHelpActionDown)

	#
	#	Configure Theme.
	#
	backFromNavigationButton.configure(highlightcolor = C_B_H, highlightthickness = T_B_H, activebackground = C_B_AB, activeforeground = C_B_AF, background = C_B_B, foreground = C_B_F)
	navigateButton.configure(highlightcolor = C_B_H, highlightthickness = T_B_H, activebackground = C_B_AB, activeforeground = C_B_AF, background = C_B_B, foreground = C_B_F)
	messagesButton.configure(highlightcolor = C_B_H, highlightthickness = T_B_H, activebackground = C_B_AB, activeforeground = C_B_AF, background = C_B_B, foreground = C_B_F)
	callForHelpButton.configure(highlightcolor = C_B_H, highlightthickness = T_B_H, activebackground = C_B_AB, activeforeground = C_B_AF, background = C_B_B, foreground = C_B_F)		
	
	backFromMessagesButton.configure(highlightcolor = C_B_H, highlightthickness = T_B_H, activebackground = C_B_AB, activeforeground = C_B_AF, background = C_B_B, foreground = C_B_F)		
	messageEntry.configure(highlightcolor = C_B_H, highlightthickness = T_B_H)		
	listBox.configure(highlightcolor = C_B_H, highlightthickness = T_B_H)		
	speakButton.configure(highlightcolor = C_B_H, highlightthickness = T_B_H, activebackground = C_B_AB, activeforeground = C_B_AF, background = C_B_B, foreground = C_B_F)		
			
	navigateButton.focus_force()
	
	controls.configure(highlightcolor = C_F_H, highlightthickness = T_F_H)
	navigationDetails.configure(highlightcolor = C_F_H, highlightthickness = T_F_H)
	messagesDetails.configure(highlightcolor = C_F_H, highlightthickness = T_F_H)

	frontDetails.grid(column = 0, row = 0)

	frame.pack() 
	root.resizable(0, 0)
	speak(voiceMessages[0])
	
	root.mainloop()
