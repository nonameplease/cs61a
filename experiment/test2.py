from appJar import gui

app=gui("Grid Demo", "300x300")
app.setSticky("news")
app.setExpand("both")
app.setFont(20)

app.addLabel("l1", "", 0, 0)
app.addLabel("l2", "", 0, 1)
app.addLabel("l3", "", 0, 2)
app.addLabel("l4", "", 1, 0)
app.addLabel("l5", "", 1, 1)
app.addLabel("l6", "", 1, 2)
app.addLabel("l7", "", 2, 0)
app.addLabel("l8", "", 2, 1)
app.addLabel("l9", "", 2, 2)

app.setLabelBg("l1", "black")
app.setLabelBg("l2", "black")
app.setLabelBg("l3", "black")
app.setLabelBg("l4", "white")
app.setLabelBg("l5", "white")
app.setLabelBg("l6", "white")
app.setLabelBg("l7", "black")
app.setLabelBg("l8", "black")
app.setLabelBg("l9", "black")

app.go()
