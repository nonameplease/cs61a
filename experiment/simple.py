from appJar import gui
import time
import random

app = gui()

app.addLabel('title', 'Welcome to Experiment')
app.setLabelBg('title', 'white')
baseline = time.time()
counter = 0

def press(btn):
    global counter
    if btn == 'left':
        print('You have choose', btn)
        timenow = time.time() - baseline
        print('seconds passed: ', timenow)
        counter += 1
        print('it has been click ', counter, ' times')
    elif btn == 'right':
        print('You have choose', btn)
        timenow = time.time() - baseline
        print('seconds passed: ', timenow)
        counter += 1
        print('it has been click ', counter, ' times')
    elif btn == 'exit':
        app.stop()

def refreshTimeLine(btn):
    global baseline
    if btn == 'refresh timeline':
        baseline = time.time()

def pressImage(btn):
    if btn == 'header':
        print('image pressed!')

def generatePicLst():
    pic1 = '2.gif'
    pic2 = '3.gif'
    pic3 = '4.gif'
    pic_lst = [pic1, pic2, pic3]
    return pic_lst

def randomdisplay(lst, num):
    choice = random.randint(0, num)
    return lst[choice]

def pin():
    return randomdisplay(generatePicLst(), 2)


app.setTitle('Experiment')
app.setGeometry(800,800)
app.setResizable(True)
app.setBg('black')
app.addButtons(['refresh timeline'], refreshTimeLine, 0,1)
app.addButtons(['left','right'], press, 1, 1, 3, 1)
app.addButtons(['exit'], press, 2,1)
#app.addImage('header', '1.gif')
#app.setImageSubmitFunction('header', pressImage)
app.addLabel('l', '', 3, 0)
app.addLabel('m', '', 3, 1)
app.addLabel('r', '', 3, 2)
app.setLabelBg('l', 'white')
app.setLabelBg('m', 'white')
app.setLabelBg('r', 'white')
app.setPadding([20, 20])
#app.addImage('pic', pin())
#app.addImage('1', '2.gif')
#app.addImage('2', '3.gif')
#app.addImage('3', '4.gif')

app.go()
