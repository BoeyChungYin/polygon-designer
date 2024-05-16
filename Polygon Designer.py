import turtle
from math import *

shape = 1               #keeping track of the shape number
point = 1               #keeping track of the point number
dataList = []           #holds data of points being added when creating a new shape
displayShapes = []      #holds data of the currently displayed shapes {'shape', 'penColour', 'fillColour', 'points'}
addingPt = False        #check whether current adding points
multiplyShape = False   #check whether multiplying shapes is active or not
ans2 = 2                #defaults the input method to clicking
isPanning = False       #checks whether panning is activated
isRotating = False      #check whether rotation is activated
showArea = False        #toggle showing the area
showPeri = False        #toggle showing the perimeter
selectedShapes = []     #list of shapes selected
isSelecting = False     #checking whether currently selecting shape

#Buttons that are not always on screen
panUpButton = 0
panDownButton = 0
panLeftButton = 0
panRightButton = 0
ccwButton = 0
cwButton = 0

#increments to x and y when panning
panIncrement = 5

#for rotation of shapes
addCentre = False
centre = (0,0)
theta = radians(5)

#return the x,y coordinates of a click
def click(x,y):
    global addingPt
    global addCentre
    global centre
    global multiplyShape
    global panUpButton
    global panDownButton
    global panLeftButton
    global panRightButton
    global ccwButton
    global cwButton
    global shape
    global point
    global isSelecting
        
    #clicking on the new file button
    if x >= newFile[0][0] and x <= newFile[1][0] and y >= newFile[1][1] and y <= newFile[2][1]:
        shape = 1
        point = 1

        clearBindings() #reset key bindings
        clearAll()
        
        #creating the data file
        with open("shapes.txt", 'w') as myFile:
            #creating the headers for the file
            header = "shape,point,x,y\n"
            myFile.write(header)

        newShape()
    
    #clicking on the finishDraw button
    elif addingPt and x >= finishDraw[0][0] and x <= finishDraw[1][0] and y >= finishDraw[1][1] and y <= finishDraw[2][1]:

        clearBindings() #reset key bindings
        addToFile()
        clearAll()
        sheldon.hideturtle()
        addingPt = False

    #clicking on the nextShape button
    elif addingPt and x >= nextSp[0][0] and x <= nextSp[1][0] and y >= nextSp[1][1] and y <= nextSp[2][1]:

        clearBindings() #reset key bindings
        nextShape()

    #clicking on the display button
    elif x >= display[0][0] and x <= display[1][0] and y >= display[1][1] and y <= display[2][1]:
        clearBindings() #reset key bindings
        selectedShapes.clear()
        tSelect.clear()
        
        writeLabel()
        getShapePara()
        draw()

    #clicking on the modify button
    elif x >= mod[0][0] and x <= mod[1][0] and y >= mod[1][1] and y <= mod[2][1]:
        clearBindings() #reset key bindings
        clearAll()
        modify()

    #clicking the pan button
    elif x >= pan[0][0] and x <= pan[1][0] and y >= pan[1][1] and y <= pan[2][1]:
        
        clearBindings() #reset key bindings
        
        #write label for panning
        if multiplyShape == True:
            writeLabel("Use arrow keys to pan\nMultiply shapes activated")
        else:
            writeLabel("Use arrow keys to pan")

        #[Left, Down, Right, Up]
        coordinates = drawArrows()
        panning()

        panLeftButton = coordinates[0]
        panDownButton = coordinates[1]
        panRightButton = coordinates[2]
        panUpButton = coordinates[3]

    #After activating panning
    elif isPanning and x >= panLeftButton[0][0] and x <= panLeftButton[1][0] and y >= panLeftButton[1][1] and y <= panLeftButton[2][1]:
        panLeft()

    elif isPanning and x >= panDownButton[0][0] and x <= panDownButton[1][0] and y >= panDownButton[1][1] and y <= panDownButton[2][1]:
        panDown()

    elif isPanning and x >= panRightButton[0][0] and x <= panRightButton[1][0] and y >= panRightButton[1][1] and y <= panRightButton[2][1]:
        panRight()

    elif isPanning and x >= panUpButton[0][0] and x <= panUpButton[1][0] and y >= panUpButton[1][1] and y <= panUpButton[2][1]:
        panUp()
        
    #clicking the rotate button
    elif x >= rotate[0][0] and x <= rotate[1][0] and y >= rotate[1][1] and y <= rotate[2][1]:

        #reset key bindings
        clearBindings()
        
        addCentre = True
        
        #write label for rotating
        writeLabel("Click the centre point of rotation")

        coordinates = drawRotateArrows()

        ccwButton = coordinates[0]
        cwButton = coordinates[1]

    #center of rotation for rotating shapes after clicking rotate button
    elif addCentre:
        
        centre = (x,y)
        addCentre = False

        tcross.goto(x+0.5,y-9)
        tcross.write('x', align='center', font=('Arial', 14, 'normal'))

        #write label for rotation instructions
        if multiplyShape == True:
            writeLabel("LEFT arrow key to rotate CCW\nRIGHT arrow key to rotate CW\nMultiply Shapes activated")
        else:
            writeLabel("LEFT arrow key to rotate CCW\nRIGHT arrow key to rotate CW")
        
        rotateShape()

    #After activating rotation
    elif isRotating and x >= ccwButton[0][0] and x <= ccwButton[1][0] and y >= ccwButton[1][1] and y <= ccwButton[2][1]:
        rotCCW()

    elif isRotating and x >= cwButton[0][0] and x <= cwButton[1][0] and y >= cwButton[1][1] and y <= cwButton[2][1]:
        rotCW()

    #clicking the zoom out button
    elif x >= scaleDown[0][0] and x <= scaleDown[1][0] and y >= scaleDown[1][1] and y <= scaleDown[2][1]:
        tcross.clear()
        zoom(0.9)

    #clicking the zoom in button
    elif x >= scaleUp[0][0] and x <= scaleUp[1][0] and y >= scaleUp[1][1] and y <= scaleUp[2][1]:
        tcross.clear()
        zoom(1.1)

    #clicking the custom zoom button
    elif x >= customScale[0][0] and x <= customScale[1][0] and y >= customScale[1][1] and y <= customScale[2][1]:
        tcross.clear()
        writeLabel("Enter custom scaling factor")
        scale = s.numinput("Scale", "Enter custom scaling factor", minval=0)
        zoom(scale)

    #clicking the Multiply button
    elif x >= multiply[0][0] and x <= multiply[1][0] and y >= multiply[1][1] and y <= multiply[2][1]:
        clearBindings() #reset key bindings

        #multiply shape currently OFF
        if multiplyShape == False:
            print("Multiply shapes activated")
            writeLabel("Multiplying shapes activated\nUse the Pan or rotate buttons to multiply currently displayed shapes")
            multiplyShape = True

        #multiply shape current ON
        else:
            print("Multiply shapes deactivated")
            writeLabel("Multiplying shapes deactivated")
            multiplyShape = False

    #clicking the Perimeter button
    elif x >= perimeter[0][0] and x <= perimeter[1][0] and y >= perimeter[1][1] and y <= perimeter[2][1]:
        clearBindings() #reset key bindings
        getPerimeter()

    #clicking the Area button
    elif x >= area[0][0] and x <= area[1][0] and y >= area[1][1] and y <= area[2][1]:
        clearBindings() #reset key bindings
        getArea()

    #clicking the Check point button
    elif x >= checkPt[0][0] and x <= checkPt[1][0] and y >= checkPt[1][1] and y <= checkPt[2][1]:
        clearBindings() #reset key bindings
        selectedShapes.clear()
        tSelect.clear()
        checkLiesWithin()

    #clicking the Select button
    elif x >= selectButton[0][0] and x <= selectButton[1][0] and y >= selectButton[1][1] and y <= selectButton[2][1]:
        selectedShapes.clear()

        writeLabel("Click on the shape you wish to interact with\nClick on overlapping shapes to select Multiple shapes")
        isSelecting = True
        s.onclick(countIntersects)

    #clicking the Unselect button
    elif x >= unselectButton[0][0] and x <= unselectButton[1][0] and y >= unselectButton[1][1] and y <= unselectButton[2][1]:
        isSelecting = False
        selectedShapes.clear()
        tSelect.clear()
    
    #clicking the Clear button
    elif x >= clearButton[0][0] and x <= clearButton[1][0] and y >= clearButton[1][1] and y <= clearButton[2][1]:
        clearBindings() #reset key bindings
        clearAll()
    
    #clicking to add point to the polygon
    else:
        if addingPt == True:
            addPoint(x,y)

#write labels (turtle 't')
def writeLabel(label="", header=""):
    
    t.clear()

    t.goto(0, s.window_height()*2/5)
    t.write(header, align='center', font=('Arial', 16, 'normal'))
    
    t.goto(0, -s.window_height()*2/5)
    t.write(label, align='center', font=('Arial', 16, 'normal'))

#create new shape
def newShape():
    global ans2
    global addingPt

    sheldon.color('black', 'black')
    
    #add new shape into displayShape list
    displayShapes.append({'shape': shape, 'points': []})
    
    #ask for method of input
    ans2 = s.numinput("Choose method of input", "Choose method of input\nEnter \'1\' to type\nEnter \'2\' to click", minval=1, maxval=2)

    #choose to input by typing coordinates
    if ans2 == 1:

        #prompt for polygon information
        numShapes = int(s.numinput("How many shapes?", "How many shapes?\nEnter number of shapes"))
        for sp in range(1, numShapes+1):
            
            #prompt for individual point information
            numPoints = int(s.numinput("How many points?", f"Shape {shape}\nHow many points?\nEnter number of points"))
            for pt in range(1, numPoints+1):
                
                writeLabel(f"Enter X-coordinate for Point {pt}", f"Shape {shape}")
                x = s.numinput(f"Shape {sp} Point {pt}", f"Shape {sp} Point {pt}\nType in X-coordinate")
                writeLabel(f"Enter Y-coordinate for Point {pt}", f"Shape {shape}")
                y = s.numinput(f"Shape {sp} Point {pt}", f"Shape {sp} Point {pt}\nType in Y-coordinate")
                
                addPoint(x,y,ans2)
                
            nextShape(ans2)

        #clear screen and clear displayShapes
        t.clear()
        sheldon.clear()
        sheldon.hideturtle()
        displayShapes.clear()

    #choose to input by clicking on screen
    elif ans2 == 2:
        addingPt = True
        writeLabel("Click anywhere to add points\nClick 'Next Shape' button to create the next shape\nClick 'Finish Draw' button to complete", f"Shape {shape}")

#click to add new point data to the polygon
def addPoint(x,y,ans2=2):
    global point

    #start drawing from 2nd point onwards
    if point == 2:
        sheldon.pd()

    #starting from 3rd point, check for intersection
    if point > 2:
        if checkIntersect(x,y):
            if ans2 == 1:
                x,y = intersectError()
            elif ans2 == 2:
                print("Line intersect ERROR")
                return

    sheldon.goto(x,y)
    sheldon.showturtle()

    displayShapes[0]['points'].append([point,x,y])
        
    point += 1

#complete the current polygon and move on to the next
def nextShape(ans2=2):
    global shape
    global point

    if checkIntersect(displayShapes[0]['points'][0][1], displayShapes[0]['points'][0][2]):
        while True:
            displayShapes[0]['points'].pop(-1)
            point -= 1
            sheldon.pencolor("white")
            sheldon.goto(displayShapes[0]['points'][-1][1], displayShapes[0]['points'][-1][2])
            sheldon.pencolor("black")
            if ans2 == 1:
                x,y = intersectError()
                addPoint(x,y,ans2)
                if checkIntersect(displayShapes[0]['points'][0][1], displayShapes[0]['points'][0][2]):
                    continue
                break
            elif ans2 == 2:
                print("Line intersect ERROR")
                return

    addToFile()

    shape += 1
    point = 1

    #add new shape into displayShape list
    displayShapes.append({'shape': shape, 'points': []})
    
    sheldon.clear()
    sheldon.pu()

    if ans2 == 2:
        writeLabel("Click anywhere to add points\nClick 'Next Shape' button to create the next shape\nClick 'Finish Draw' button to complete", f"Shape {shape}")
    elif ans2 == 1:
        writeLabel(f"Enter number of points for shape {shape}", f"Shape {shape}")

#check whether collinear points intersect
def collinearIntersect(a,b,c):

    if b[0] <= max(a[0], c[0]) and b[0] >= min(a[0], c[0]) and b[1] <= max(a[1], c[1]) and b[1] >= min(a[1], c[1]):
        return True
    return False

#check the orientation of 3 points
def checkOrientation(a,b,c):
    #0: collinear
    #1: clockwise
    #2: counterclockwise
    #3: same point

    #if any 2 of the points are the same
    if a == b or a == c or b == c:
        return 3
    
    val = ((b[1]-a[1])*(c[0]-b[0])) - ((b[0]-a[0])*(c[1]-b[1]))
    if val > 0:     #clockwise
        return 1
    elif val < 0:   #counterclockwise
        return 2
    else:           #collinear (but not same point)
        return 0

#run checks and determine whether they intersect
def checks(p1,q1,p2,q2):
    #Find the 4 orientations required for
    #the general and special cases
    o1 = checkOrientation(p1, q1, p2)
    o2 = checkOrientation(p1, q1, q2)
    o3 = checkOrientation(p2, q2, p1)
    o4 = checkOrientation(p2, q2, q1)

    #if both points are the same
    if o1 == 3 and o2 == 3 and o3 == 3 and o4 == 3:
        return True

    #Special Cases (if they are collinear but not the same point)
    if (o1 in (0,3)) or (o2 in (0,3)) or (o3 in (0,3)) or (o4 in (0,3)):
     
        #p1 , q1 and p2 are collinear and p2 lies on segment p1q1
        if (o1 == 0) and collinearIntersect(p1, p2, q1):
            return True
     
        #p1 , q1 and q2 are collinear and q2 lies on segment p1q1
        if (o2 == 0) and collinearIntersect(p1, q2, q1):
            return True
     
        #p2 , q2 and p1 are collinear and p1 lies on segment p2q2
        if (o3 == 0) and collinearIntersect(p2, p1, q2):
            return True
     
        #p2 , q2 and q1 are collinear and q1 lies on segment p2q2
        if (o4 == 0) and collinearIntersect(p2, q1, q2):
            return True

    else:
        
        #General case
        if o1 != o2 and o3 != o4:
            return True
 
    #If none of the cases (does not intersect)
    return False

#get the points of 2 lines to check and run the checks
def checkIntersect(x,y,index=None):

    p1 = (x,y)

    #checking after using Modify
    if index:

        #if new point is in between first and last point
        if index == len(displayShapes[0]['points']):
            
            #loops 2 times for the 2 new lines
            for i in range(0,index,index-1):
                q1 = (displayShapes[0]['points'][i][1], displayShapes[0]['points'][i][2])

                for i in range(len(displayShapes[0]['points'])):

                    #for last and first point
                    if i == len(displayShapes[0]['points'])-1:
                        p2 = (displayShapes[0]['points'][i][1], displayShapes[0]['points'][i][2])
                        q2 = (displayShapes[0]['points'][0][1], displayShapes[0]['points'][0][2])

                    else:
                        p2 = (displayShapes[0]['points'][i][1], displayShapes[0]['points'][i][2])
                        q2 = (displayShapes[0]['points'][i+1][1], displayShapes[0]['points'][i+1][2])
                    
                    if checks(p1,q1,p2,q2):
                        print("intersects")
                        return True

        else:

            #loops 2 times for the 2 new lines
            for i in range(index-1,index+1):
                q1 = (displayShapes[0]['points'][i][1], displayShapes[0]['points'][i][2])

                for i in range(len(displayShapes[0]['points'])):

                    #for last and first point
                    if i == len(displayShapes[0]['points'])-1:
                        p2 = (displayShapes[0]['points'][i][1], displayShapes[0]['points'][i][2])
                        q2 = (displayShapes[0]['points'][0][1], displayShapes[0]['points'][0][2])

                    else:
                        p2 = (displayShapes[0]['points'][i][1], displayShapes[0]['points'][i][2])
                        q2 = (displayShapes[0]['points'][i+1][1], displayShapes[0]['points'][i+1][2])
                    
                    if checks(p1,q1,p2,q2):
                        print("intersects")
                        return True
            
    #checking for applications
    else:
        q1 = (displayShapes[0]['points'][-1][1], displayShapes[0]['points'][-1][2])
        
        for i in range(len(displayShapes[0]['points'])-1):
            p2 = (displayShapes[0]['points'][i][1], displayShapes[0]['points'][i][2])
            q2 = (displayShapes[0]['points'][i+1][1], displayShapes[0]['points'][i+1][2])
            
            if checks(p1,q1,p2,q2):
                print("intersects")
                return True

def intersectError():
    
    #Prompt user until a valid point is entered
    while True:
        print("Line intersect ERROR")
        s.listen()
        x = s.numinput(f"Shape {shape} Point {point}", f"Intersect ERROR\nShape {shape} Point {point}\nType in new X-coordinate")
        y = s.numinput(f"Shape {shape} Point {point}", f"Intersect ERROR\nShape {shape} Point {point}\nType in new Y-coordinate")
            
        if checkIntersect(x,y):
            continue
        else:
            break

    return x,y


#returns a list of the points in that shape
def getShapePoints(shapeNum):
    ptList = []   #list to hold the points data

    #check for existing file
    try:
        with open("shapes.txt") as myFile:
            myFile.readline()   #read past the header
            for line in myFile:
                data = [float(i) for i in line[:-2].split(',')] #[shape,point number,x,y]
                if int(data[0]) == shapeNum:            #filter current shape points
                    ptList.append(data[1:])    #appending only point information

    except FileNotFoundError:
        writeLabel("ERROR File does not exist\nPlease click on 'New File' to create a new file")
        return

    return ptList #list[point number, x,y] within a list[pt1,pt2,pt3,...]

#get the total number of shapes in the data file
def getMaxShape():
    ptList = []

    #check for existing file
    try:
        with open("shapes.txt") as myFile:
            myFile.readline()
            for line in myFile:
                point = line.split(',')
                ptList.append(point)
                
    except FileNotFoundError:
        writeLabel("ERROR File does not exist\nPlease click on 'New File' to create a new file")
        return
            
    ptList = [int(pt[0]) for pt in ptList]
    return max(ptList)

#get shape parameters from the user
def getShapePara():

    maxSp = getMaxShape()

    #if file does not exist
    if maxSp == None:
        return
    
    #get shape to display
    shapeNum = int(s.numinput("Choose shape", "Enter shape number to display", minval=1, maxval=maxSp))

    #get the pen colour
    while True:
        try:
            penColour = s.textinput("Pen colour", "Choose the pen colour")
            sheldon.pencolor(penColour)
            break
        except:
            writeLabel("ERROR Invalid colour name\nEnter a valid colour name (e.g. 'blue', 'red', etc.)")

    #get fill colour
    while True:
        try:
            fillColour = s.textinput("Fill colour", "Choose the fill colour")
            sheldon.fillcolor(fillColour)
            break
        except:
            writeLabel("ERROR Invalid colour name\nEnter a valid colour name (e.g. 'blue', 'red', etc.)")

    ptList = getShapePoints(shapeNum)
    displayShapes.append({'shape': shapeNum, 'penColour': penColour, 'fillColour': fillColour, 'points': ptList})

#add all the points of the shape to the file
def addToFile():
    tempList = []
    
    #process dataList before adding to file
    for point in displayShapes[0]['points']:
        data = [displayShapes[0]['shape']] + point
        data = [int(data[0]), int(data[1]), float(data[2]), float(data[3])]
        tempList.append([str(val) for val in data])

    fileList = [','.join(data) + '\n' for data in tempList]
    
    #add x,y coordinates to the file
    with open("shapes.txt", 'a') as myFile:
        myFile.writelines(fileList)

    displayShapes.clear()

#clear key bindings
def clearBindings():

    global isPanning
    global isRotating
    global isSelecting

    s.onkeypress(None, "Up")
    s.onkeypress(None, "Down")
    s.onkeypress(None, "Left")
    s.onkeypress(None, "Right")
    isPanning = False
    isRotating = False
    arrow.clear()
    tmod.clear()
    tcross.clear()

#draw the polygon
def draw():

    if multiplyShape == False:
        sheldon.clear()

    for i in range(len(displayShapes)):

        sheldon.pu()
        sheldon.color(displayShapes[i]['penColour'], displayShapes[i]['fillColour'])
        sheldon.begin_fill()
        
        for pt in displayShapes[i]['points']:
            sheldon.goto(pt[1], pt[2])

            #start drawing after moving to first point
            if pt[0] == 1:
                sheldon.pd()

        #go back to the first point to close the polygon
        sheldon.goto(displayShapes[i]['points'][0][1], displayShapes[i]['points'][0][2])
        sheldon.end_fill()

    #reset turtle colour
        sheldon.color("black", "black")
    
#modify the current shape
def modify():

    maxSp = getMaxShape()

    #if file does not exist
    if maxSp == None:
        return
    
    #selecting which shape to modify
    writeLabel("Select shape to modify")
    modShape = int(s.numinput("Select shape", "Select shape to modify\nEnter shape number", minval=1, maxval=maxSp))

    #clearing the displayShapes list and leaving the shape being modified
    ptList = getShapePoints(modShape)
    displayShapes.append({'shape': modShape, 'penColour': 'black', 'fillColour': None, 'points': ptList})

    #draw out the shape to be modified for reference
    modDraw()

    #selecting the type of modification (remove or insert point)
    writeLabel("Select type of modification, Remove point(1) or insert point(2)\nEnter '1' to remove or '2' to insert")
    modType = s.numinput("Modification", "Select type of modification\nRemove(1) or insert point(2)?\n'1' to Remove\n'2' to Insert", minval=1, maxval=2)

    #removing point
    if modType == 1:
        writeLabel("Enter point number that you wish to remove", f"Shape {displayShapes[0]['shape']}")
        modPt = int(s.numinput("Removing point", "Select point to remove\nEnter the point number", minval=1, maxval=len(displayShapes[0]['points'])))
        displayShapes[0]['points'].pop(modPt-1)
        reOrder()
        modDraw()
        writeLabel("Modification saved", f"Shape {displayShapes[0]['shape']}")
        editFile()
        

    #inserting new point (modType == 2)
    else:
        writeLabel("Choose method of input for new point\nEnter '1' to Type in or '2' to Click")
        modInput = s.numinput("Method of input", "Choose method of input for new point\n'1' to Type\n'2' to Click", minval=1, maxval=2)

        #Typing in new point
        if modInput == 1:
            writeLabel("Type in the x & y coordinates of the new point", f"Shape {displayShapes[0]['shape']}")
            x = s.numinput("X coordinate", "Type in X coordinate")
            y = s.numinput("Y coordinate", "Type in Y coordinate")
            newPtPos(x,y)

        #Clicking new point (modInput == 2)
        else:
            writeLabel("Click new point to insert", f"Shape {displayShapes[0]['shape']}")
            s.onclick(newPtPos)

#drawing for modifications
def modDraw():

    tmod.clear()
    tmod.pu()

    for pt in displayShapes[0]['points']:
        tmod.goto(pt[1], pt[2])
        tmod.write(str(int(pt[0])), align='right', font=('Arial', 10, 'normal'))

        #for the first point
        if pt[0] == 1:
            tmod.pd()

    #go back to the first point to close the shape
    tmod.goto(displayShapes[0]['points'][0][1], displayShapes[0]['points'][0][2])

#checking the correct position of the new point
def newPtPos(x,y):

    #distance of new point from each existing point in order
    distList = []

    #create the list of distances
    for pt in displayShapes[0]['points']:
        dist = sqrt((pt[1]-x)**2 + (pt[2]-y)**2)
        distList.append(dist)
    
    #get index of closest and second closest point
    pt1 = distList.index(min(distList))
    distList.pop(distList.index(min(distList)))

    #adjust the index for the shift
    if distList.index(min(distList)) >= pt1:
        pt2 = distList.index(min(distList)) + 1
    else:
        pt2 = distList.index(min(distList))

    #index of new point is in between closest and second closest
    index =  max(pt1,pt2)

    #checks if new point is in between first and last point
    if min(pt1,pt2) == 0 and max(pt1,pt2) == len(displayShapes[0]['points'])-1:
        newPtIndex = index + 1
    else:
        newPtIndex = index

    #run checks for intersection with the new point added
    if checkIntersect(x,y,newPtIndex):
        writeLabel("Intersection ERROR\nUnable to add point at that location\nPlease click a new point", f"Shape {displayShapes[0]['shape']}")
        
    else:

        #insert new point into displayShapes list
        displayShapes[0]['points'].insert(newPtIndex,[newPtIndex+1,x,y])

        #rearrange the points in displayShapes and display
        reOrder()
        modDraw()
        writeLabel("Modification saved", f"Shape {displayShapes[0]['shape']}")
        editFile()
        s.onclick(click)

#Edit the existing file
def editFile():
    ptList = []   #list to hold the points data

    #read in existing data in the file
    with open("shapes.txt") as myFile:
        myFile.readline()   #read past the header

        #add currently existing points into ptList
        for line in myFile:
            dataList = [data for data in line[:-2].split(',')] #[shape,point number,x,y]
            dataList = [int(dataList[0]), int(dataList[1]), float(dataList[2]), float(dataList[3])]
            ptList.append(dataList)

    index = None
    i = 0
    #Remove old points from ptList
    while i < len(ptList):
        if ptList[i][0] == displayShapes[0]['shape']:
            index = i
            ptList.pop(i)
        else:
            i += 1
    
    tempList = []
    #create a tempList to hold new points
    for point in displayShapes[0]['points']:
        data = [displayShapes[0]['shape']] + point
        tempList.append(data)

    #add the new points in tempList to ptList at the index
    ptList = ptList[:index] + tempList + ptList[index:]
    
    #process ptList before adding to file
    for i in range(len(ptList)):
        for j in range(len(ptList[i])):
            ptList[i][j] = str(ptList[i][j])

    fileList = [','.join(data) + '\n' for data in ptList]
    
    #write data to the file
    with open("shapes.txt", 'w') as myFile:
        myFile.write("shape,point,x,y\n")
        myFile.writelines(fileList)

    displayShapes.clear()

#reorder the point numbers after removing or inserting one point
def reOrder():
    for i in range(len(displayShapes[0]['points'])):
        displayShapes[0]['points'][i][0] = i + 1

#draw the arrow keys on screen for panning
def drawArrows():

    #[Left, Down, Right, Up]
    coordinates = []

    #button width, height and spacing
    width = s.window_width()*5/100
    spacing = s.window_width()*6/100

    #starting position
    arrow.goto(s.window_width()*25/100 ,-s.window_height()*35/100)

    #drawing the perimeter of the button and saving corner coordinates
    for i in range(4):
        
        #drawing the box
        a = arrow.pos()
        arrow.pd()
        arrow.seth(0)
        arrow.fd(width)
        b = arrow.pos()
        arrow.seth(90)
        arrow.fd(width)
        c = arrow.pos()
        arrow.seth(180)
        arrow.fd(width)
        d = arrow.pos()
        arrow.seth(270)
        arrow.fd(width)
        arrow.pu()

        #append corner coordinates of the buttons
        coordinates.append([a,b,c,d])

        if i == 2:
            arrow.goto(coordinates[1][0][0], coordinates[1][0][1]+spacing)
        else:
            arrow.setx(a[0]+spacing)
    
    #drawing the arrows

    #Left arrow
    arrow.goto(coordinates[0][1][0]-width/10, coordinates[0][0][1]+width/2,)
    arrow.pd()
    arrow.seth(180)
    arrow.fd(width*8/10)
    arrow.right(135)
    arrow.fd(width*4/10)
    arrow.bk(width*4/10)
    arrow.right(90)
    arrow.fd(width*4/10)
    arrow.pu()

    #Down arrow
    arrow.goto(coordinates[1][0][0]+width/2, coordinates[1][2][1]-width/10,)
    arrow.pd()
    arrow.seth(270)
    arrow.fd(width*8/10)
    arrow.right(135)
    arrow.fd(width*4/10)
    arrow.bk(width*4/10)
    arrow.right(90)
    arrow.fd(width*4/10)
    arrow.pu()

    #Right arrow
    arrow.goto(coordinates[2][0][0]+width/10, coordinates[2][0][1]+width/2,)
    arrow.pd()
    arrow.seth(0)
    arrow.fd(width*8/10)
    arrow.right(135)
    arrow.fd(width*4/10)
    arrow.bk(width*4/10)
    arrow.right(90)
    arrow.fd(width*4/10)
    arrow.pu()

    #Up arrow
    arrow.goto(coordinates[3][0][0]+width/2, coordinates[3][0][1]+width/10,)
    arrow.pd()
    arrow.seth(90)
    arrow.fd(width*8/10)
    arrow.right(135)
    arrow.fd(width*4/10)
    arrow.bk(width*4/10)
    arrow.right(90)
    arrow.fd(width*4/10)
    arrow.pu()

    return coordinates

#pan the current shape
def panning():
    global isPanning
    
    isPanning = True

    print("Panning activated")
    
    #activate the arrow keys to pan the current shapes
    s.onkeypress(panUp, "Up")
    s.onkeypress(panDown, "Down")
    s.onkeypress(panLeft, "Left")
    s.onkeypress(panRight, "Right")

#pan up
def panUp():    

    for i in range(len(displayShapes)):

        #if certain shapes are selected
        if selectedShapes:

            #check if the current shape is one of the selected
            if displayShapes[i]['shape'] in selectedShapes:
                
                for j in range(len(displayShapes[i]['points'])):
                    displayShapes[i]['points'][j][2] += panIncrement

        #else pan all the currently displayed shapes
        else:
            for j in range(len(displayShapes[i]['points'])):
                displayShapes[i]['points'][j][2] += panIncrement
    draw()

#pan down
def panDown():
    
    for i in range(len(displayShapes)):
        
        #if certain shapes are selected
        if selectedShapes:

            #check if the current shape is one of the selected
            if displayShapes[i]['shape'] in selectedShapes:
                
                for j in range(len(displayShapes[i]['points'])):
                    displayShapes[i]['points'][j][2] -= panIncrement

        #else pan all the currently displayed shapes
        else:
            for j in range(len(displayShapes[i]['points'])):
                displayShapes[i]['points'][j][2] -= panIncrement
    draw()

#pan left
def panLeft():
    
    for i in range(len(displayShapes)):

        #if certain shapes are selected
        if selectedShapes:

            #check if the current shape is one of the selected
            if displayShapes[i]['shape'] in selectedShapes:
                
                for j in range(len(displayShapes[i]['points'])):
                    displayShapes[i]['points'][j][1] -= panIncrement

        #else pan all the currently displayed shapes
        else:
            for j in range(len(displayShapes[i]['points'])):
                displayShapes[i]['points'][j][1] -= panIncrement
    draw()

#pan right
def panRight():
    
    for i in range(len(displayShapes)):

        #if certain shapes are selected
        if selectedShapes:

            #check if the current shape is one of the selected
            if displayShapes[i]['shape'] in selectedShapes:
                
                for j in range(len(displayShapes[i]['points'])):
                    displayShapes[i]['points'][j][1] += panIncrement

        #else pan all the currently displayed shapes
        else:
            for j in range(len(displayShapes[i]['points'])):
                displayShapes[i]['points'][j][1] += panIncrement
    draw()

#draw rotation buttons
def drawRotateArrows():

    #[counter clock wise, clock wise]
    coordinates = []

    #button width, height and spacing
    width = s.window_width()*5/100
    spacing = s.window_width()*6/100

    #starting position
    arrow.goto(s.window_width()*25/100 ,-s.window_height()*35/100)

    #drawing the perimeter of the button and saving corner coordinates
    for i in range(2):
        
        #drawing the box
        a = arrow.pos()
        arrow.pd()
        arrow.seth(0)
        arrow.fd(width)
        b = arrow.pos()
        arrow.seth(90)
        arrow.fd(width)
        c = arrow.pos()
        arrow.seth(180)
        arrow.fd(width)
        d = arrow.pos()
        arrow.seth(270)
        arrow.fd(width)
        arrow.pu()
        arrow.setx(a[0]+spacing)

        #append corner coordinates of the buttons
        coordinates.append([a,b,c,d])
    
    #drawing the arrows

    #CCW arrow
    arrow.goto(coordinates[0][1][0]-width/4, coordinates[0][1][1]+width/4,)
    arrow.pd()
    arrow.seth(45)
    arrow.circle(width/3, 280)
    arrow.right(135)
    arrow.fd(width*2/10)
    arrow.bk(width*2/10)
    arrow.right(90)
    arrow.fd(width*2/10)
    arrow.pu()

    #CW arrow
    arrow.goto(coordinates[1][0][0]+width/4, coordinates[1][0][1]+width/4,)
    arrow.pd()
    arrow.seth(-45)
    arrow.circle(width/3, -280)
    arrow.right(45)
    arrow.fd(width*2/10)
    arrow.bk(width*2/10)
    arrow.left(90)
    arrow.fd(width*2/10)
    arrow.pu()

    return coordinates

#rotate current shapes
def rotateShape():
    global isRotating

    isRotating = True
    
    print("Rotation activated")
    
    #activate the arrow keys to pan the current shapes
    s.onkeypress(rotCCW, "Left")
    s.onkeypress(rotCW, "Right")

#rotate shapes counter-clockwise
def rotCCW():

    for i in range(len(displayShapes)):

        #if certain shapes are selected
        if selectedShapes:

            #if current shape is one of the selected
            if displayShapes[i]['shape'] in selectedShapes:
                for j in range(len(displayShapes[i]['points'])):
                    displayShapes[i]['points'][j][1] = (displayShapes[i]['points'][j][1]-centre[0])*cos(-theta)+(displayShapes[i]['points'][j][2]-centre[1])*sin(-theta)+centre[0]
                    displayShapes[i]['points'][j][2] = (displayShapes[i]['points'][j][1]-centre[0])*-sin(-theta)+(displayShapes[i]['points'][j][2]-centre[1])*cos(-theta)+centre[1]

        #else rotate all the shapes
        else:
            for j in range(len(displayShapes[i]['points'])):
                displayShapes[i]['points'][j][1] = (displayShapes[i]['points'][j][1]-centre[0])*cos(-theta)+(displayShapes[i]['points'][j][2]-centre[1])*sin(-theta)+centre[0]
                displayShapes[i]['points'][j][2] = (displayShapes[i]['points'][j][1]-centre[0])*-sin(-theta)+(displayShapes[i]['points'][j][2]-centre[1])*cos(-theta)+centre[1]
    draw()

#rotate shapes clockwise
def rotCW(cusAngle=0):

    for i in range(len(displayShapes)):

        #if current shape is one of the selected
        if selectedShapes:

            #if current shape is one of the selected
            if displayShapes[i]['shape'] in selectedShapes:
                for j in range(len(displayShapes[i]['points'])):
                    displayShapes[i]['points'][j][1] = (displayShapes[i]['points'][j][1]-centre[0])*cos(theta)+(displayShapes[i]['points'][j][2]-centre[1])*sin(theta)+centre[0]
                    displayShapes[i]['points'][j][2] = (displayShapes[i]['points'][j][1]-centre[0])*-sin(theta)+(displayShapes[i]['points'][j][2]-centre[1])*cos(theta)+centre[1]

        #else rotate all the shapes
        else:
            for j in range(len(displayShapes[i]['points'])):
                displayShapes[i]['points'][j][1] = (displayShapes[i]['points'][j][1]-centre[0])*cos(theta)+(displayShapes[i]['points'][j][2]-centre[1])*sin(theta)+centre[0]
                displayShapes[i]['points'][j][2] = (displayShapes[i]['points'][j][1]-centre[0])*-sin(theta)+(displayShapes[i]['points'][j][2]-centre[1])*cos(theta)+centre[1]
    draw()


#zoom out function
def zoom(scale):

    #multiply in scaling factor
    for sp in displayShapes:

        #if certain shapes are selected
        if selectedShapes:

            #if current shape is one of the selected shapes
            if sp['shape'] in selectedShapes:
                
                for i in range(len(sp['points'])):
                    sp['points'][i][1] *= scale
                    sp['points'][i][2] *= scale

        #else apply zoom to all shapes 
        else:
            for i in range(len(sp['points'])):
                sp['points'][i][1] *= scale
                sp['points'][i][2] *= scale

    #display shape
    draw()

#get the perimeter of the shape
def getPerimeter():
    global showPeri

    if not showPeri:

        showPeri = not showPeri
        
        #write labels
        tPeri.goto(s.window_width()*40/100, s.window_height()*43/100)
        tPeri.write("Perimeter values:", align='center', font=('Arial', 16, 'underline'))
        
        #holds the total perimeter value
        perimeter = 0
        
        for shape in displayShapes:
            shapeNum = int(shape['shape'])

            for i in range(len(shape['points'])):

                #get the length of each line
                if i == len(shape['points'])-1:     #for last point
                    length = sqrt( (shape['points'][0][1]-shape['points'][i][1])**2 + (shape['points'][0][2]-shape['points'][i][2])**2 )
                else:
                    length = sqrt( (shape['points'][i+1][1]-shape['points'][i][1])**2 + (shape['points'][i+1][2]-shape['points'][i][2])**2 )

                perimeter += length

            tPeri.sety(tPeri.pos()[1]-s.window_height()*3/100)
            tPeri.write(f"Shape {shapeNum}: {abs(perimeter):.2f}", align='center', font=('Arial', 16, 'normal'))
            perimeter = 0

    else:
        tPeri.clear()
        showPeri = not showPeri

#get the area of the shape
def getArea():
    global showArea

    if not showArea:

        showArea = not showArea

        #write labels
        tArea.goto(s.window_width()*40/100, s.window_height()*20/100)
        tArea.write("Area values:", align='center', font=('Arial', 16, 'underline'))
        
        #holds the total area of the shape
        area = 0
        
        for shape in displayShapes:
            shapeNum = int(shape['shape'])

            for i in range(1, len(shape['points'])-1):

                #vertex A
                x1 = shape['points'][i][1] - shape['points'][0][1]
                y1 = shape['points'][i][2] - shape['points'][0][2]

                #vertex B
                x2 = shape['points'][i+1][1] - shape['points'][0][1]
                y2 = shape['points'][i+1][2] - shape['points'][0][2]

                #area of triangle segment (AxBy - AyBx)/2
                area += (x1*y2 - y1*x2)/2

            tArea.sety(tArea.pos()[1]-s.window_height()*3/100)
            tArea.write(f"Shape {shapeNum}: {abs(area):.2f}", align='center', font=('Arial', 16, 'normal'))
            area = 0

    else:
        tArea.clear()
        showArea = not showArea

#check whether point lies within polygon
def checkLiesWithin():

    #write labels
    writeLabel("Checking if point lies within the polygon\nSelect input method of point\nEnter '1' to Type or '2' to Click")

    #prompt for method of input
    ans = s.numinput("Choose input", "Choose method of input\nEnter '1' to Type or '2' to Click", minval=1, maxval=2)

    #choose to type in point
    if ans == 1:

        #write labels
        writeLabel("Type in X and Y coordinates")

        #prompt for x and y coordinates of point
        x = s.numinput("X-coordinate", "X-coordinate of point")
        y = s.numinput("Y-coordinate", "Y-coordinate of point")

        countIntersects(x,y)
        
    #choose to click in point
    elif ans == 2:

        #write labels
        writeLabel("Click on the point you wish to check")
        
        s.onclick(countIntersects)

    else:
        writeLabel()
    
    return

#count intersects of the lines casted from the checking point and determine location
def countIntersects(x,y):
    global selectedShapes
    global isSelecting

    #reset click key binding
    s.onclick(click)

    #mark the click with a cross if checking whether point lies within
    if not isSelecting:
        tcross.goto(x+0.5,y-9)
        tcross.write('x', align='center', font=('Arial', 14, 'normal'))

    #parameter for the circle of lines used to check intersection
    radius = s.window_height()
    
    p1 = (x,y)

    #create counters for each shape
    for shape in displayShapes:
        shape['even'] = 0
        shape['odd'] = 0
        shape['edge'] = False

    #loop through each line used to check for intersection (360 lines)
    for angle in range(360):
        q1 = (radius*cos(radians(angle))+x, radius*sin(radians(angle))+y)

        #loop through the currently displayed shapes to check
        for shape in displayShapes:

            #skip shape if already determined point lies on the edge
            if shape['edge'] == True:
                continue
            
            #create an intersect counter for each shape
            shape['intersectCount'] = 0
        
            for i in range(len(shape['points'])):

                #if at the last index
                if i == len(shape['points'])-1:
                    p2 = (shape['points'][i][1], shape['points'][i][2])
                    q2 = (shape['points'][0][1], shape['points'][0][2])

                else:
                    p2 = (shape['points'][i][1], shape['points'][i][2])
                    q2 = (shape['points'][i+1][1], shape['points'][i+1][2])

                #checking if point on another existing point
                if checkOrientation(p1,p2,q2) == 3:
                    shape['edge'] = True
                    break

                #if the point is collinear to an edge
                elif checkOrientation(p1,p2,q2) == 0:

                    #if point lies on the edge
                    if collinearIntersect(p2,p1,q2):
                        shape['edge'] = True
                        break

                #checking if line intersects the edge
                elif checks(p1,q1,p2,q2) == True:
                    shape['intersectCount'] += 1

            #check if there are even or odd number of intersections
            if shape['intersectCount'] % 2 == 0:
                shape['even'] += 1
            else:
                shape['odd'] += 1

    t.clear()
    t.sety(t.pos()[1]+s.window_height()*5/100)
    #display the results
    for shape in displayShapes:

        #lies on the edge
        if shape['edge'] == True:

            if not isSelecting:
                t.write(f"Point lies on the edge of polygon {shape['shape']}", align='center', font=('Arial', 16, 'normal'))
            selectedShapes.append(shape['shape'])

        #lies outside
        elif shape['even'] > shape['odd']:

            if not isSelecting:
                t.write(f"Point lies outside polygon {shape['shape']}", align='center', font=('Arial', 16, 'normal'))

        #lies inside
        else:

            if not isSelecting:
                t.write(f"Point lies inside polygon {shape['shape']}", align='center', font=('Arial', 16, 'normal'))
            selectedShapes.append(shape['shape'])
            
        t.sety(t.pos()[1]-s.window_height()*3/100)

    #write out the selected shapes
    if isSelecting:
        tSelect.clear()
        tSelect.goto(-s.window_width()*40/100, s.window_height()*43/100)
        tSelect.write(f"Selected Shapes:", align='center', font=('Arial', 16, 'underline'))
                      
        for i in selectedShapes:
            tSelect.sety(tSelect.pos()[1]-s.window_height()*3/100)
            tSelect.write(f"Shape {i}", align='center', font=('Arial', 16, 'normal'))

        isSelecting = False
            

#clear screen and current shapes (except for main buttons)
def clearAll():
    global multiplyShape
    global isSelecting
    
    t.clear()
    sheldon.clear()
    sheldon.pu()
    displayShapes.clear()
    arrow.clear()
    tSelect.clear()
    selectedShapes.clear()
    isSelecting = False
    multiplyShape = False

#draw the button and get the coordinates of the button
def kurtButton(buttonName):

    #button width and height
    width = s.window_width()*7/100
    height = s.window_height()*6/100

    #drawing the perimeter of the button and saving corner coordinates
    a = kurt.pos()
    kurt.pd()
    kurt.seth(0)
    kurt.fd(width)
    b = kurt.pos()
    kurt.seth(90)
    kurt.fd(height)
    c = kurt.pos()
    kurt.seth(180)
    kurt.fd(width)
    d = kurt.pos()
    kurt.seth(270)
    kurt.fd(height)
    kurt.pu()

    #position for writing label
    kurt.goto(kurt.pos()[0]+s.window_width()*35/1000, kurt.pos()[1]+s.window_height()*17/1000)
    kurt.write(buttonName, align='center', font=('Arial', 10, 'bold'))

    kurt.goto(a)
    kurt.bk(s.window_height()*8/100)

    return a,b,c,d


#set up the turtle screen
s = turtle.Screen()
rootwindow = s.getcanvas().winfo_toplevel()
rootwindow.call('wm', 'attributes', '.', '-topmost', '1')
rootwindow.call('wm', 'attributes', '.', '-topmost', '0')
s.setup(0.8, 0.8)
s.title("Polygon creator")

#turtle to draw polygons (sheldon)
sheldon = turtle.Turtle()
sheldon.hideturtle()
sheldon.speed(0)
sheldon.pu()

#turtle to write labels (t)
t = turtle.Turtle()
t.hideturtle()
t.speed(0)
t.pu()
t.goto(0, -s.window_height()*40/100)
writeLabel("Loading please wait...")

#turtle to draw arrows (arrow)
arrow = turtle.Turtle()
arrow.speed(0)
arrow.pu()
arrow.pensize(2)
arrow.hideturtle()

#turtle to draw for modifications (tmod)
tmod = turtle.Turtle()
tmod.speed(0)
tmod.pu()
tmod.hideturtle()

#turtle to draw the point being checked for checkLiesWithin (tcross)
tcross = turtle.Turtle()
tcross.speed(0)
tcross.pu()
tcross.pencolor("#535353")
tcross.hideturtle()

#turtle to write out the perimeter (tPeri)
tPeri = turtle.Turtle()
tPeri.speed(0)
tPeri.pu()
tPeri.hideturtle()

#turtle to write out the area (tArea)
tArea = turtle.Turtle()
tArea.speed(0)
tArea.pu()
tArea.hideturtle()

#turtle to indicate which shapes are selected (tSelect)
tSelect = turtle.Turtle()
tSelect.speed(0)
tSelect.pu()
tSelect.hideturtle()

#turtle to draw buttons (kurt)
kurt = turtle.Turtle()
kurt.speed(0)
kurt.hideturtle()
kurt.pu()
#starting position
kurt.goto(-s.window_width()*45/100, -s.window_height()*45/100)

#new file button
newFile = kurtButton("New File")

#finishDraw button
finishDraw = kurtButton("Finish Draw")

#nextShape button
nextSp = kurtButton("Next Shape")

#display button
display = kurtButton("Display")

#panning button
pan = kurtButton("Pan")

#rotate button
rotate = kurtButton("Rotate")

#scale down button
scaleDown = kurtButton("Zoom-")

#scale up button
scaleUp = kurtButton("Zoom+")

#custom scale button
customScale = kurtButton("Custom Zoom")

#------------starting a new line of buttons----------------------
kurt.goto(-s.window_width()*35/100, -s.window_height()*45/100)

#modify button
mod = kurtButton("Modify")

#multiply button
multiply = kurtButton("Multiply")

#perimeter button
perimeter = kurtButton("Perimeter")

#area button
area = kurtButton("Area")

#check point button
checkPt = kurtButton("Check point")

#Select shape button
selectButton = kurtButton("Select")

#Unselect button
unselectButton = kurtButton("Unselect")

#clear button
clearButton = kurtButton("Clear")

writeLabel()

s.listen()
s.onclick(click)




