from appJar import gui

app=gui("Experiment", "500x300")
app.setSticky("news")
app.setExpand("both")
app.setFont(20)
app.setBg('black')

app.addImage('1', '1.gif', 1, 0)
app.setImageSize('1', 100, 100)
app.addImage('2', '2.gif', 1, 1)
app.setImageSize('2', 100, 100)
app.addImage('3', '3.gif', 1, 2)
app.setImageSize('3', 100, 100)

def displayEntry(string):
    print(string)

def chooseLeft():
    displayEntry('left')

def chooseRight():
    displayEntry('right')

def detectEntry():
    app.bindKey('q', chooseLeft)
    app.bindKey('p', chooseRight)

app.registerEvent(detectEntry)

app.go()
