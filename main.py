#Yuxi QIn
#10 FAST HONKS
#this is a typing test program (although it doesn't save progress)
#that has two full mini-games so far
#and some aesthetic options/instruction pages
#there is one (1) easter egg

from pygame import *
from random import *
import glob
#=====COLOURS
black = (0,0,0)                     #BASICS
white = (255, 255, 255)
grey = (211,211,211)
reasonableGrey = (88,88,88)
somewhatLegitGrey = (112,112,112)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
purple = (255, 0, 255)
cyan = (0, 255, 255)

cardinalR = (196, 30, 58)           #REDS
turkeyR = (169, 17, 1)

piggyP =(253, 221, 230)             #PINKS
chinaP = (222, 111, 161)
cottonCandyP = (255, 188, 217)

lightOR = (254, 216, 177)           #ORANGES
atomicTanOR =(255, 153, 102)
butterscotchOR = (224, 149, 64)
peachOR = (255, 229, 180)
apricotOR = (251, 206, 177)
papayaOR =(255, 239, 213)
teaRose =(248, 131, 121)

lemonY =(255, 250, 205)
munsellY = (239, 204, 0)
maximumY =(250, 250, 55)

medSeaG = (60,179,113)              #GREENS
lightSeaG = (32,178,170)
seaG = (46,139,87)
oliveG = (128,128,0)
darkOliveG = (85,107,47)
oliveDrabG = (107,142,35)
emeraldG = (80, 200, 120)
mintG = (62, 180, 137)
myrtleG = (49, 120, 115)
teaG = (208, 240, 192)
hookerG = (73, 121, 107)

pastelB = (204,229,255)             #BLUES
lightGreyB = (0,153,153)
skyB = (0,204,204)
colombianB = (153,221,255)
discoB = (51, 187, 255)
capriB = (0, 170, 255)

palePUR =(250, 230, 250)            #PURPLES
thistlePUR = (216, 191, 216)
pearlyPUR = (183, 104, 162)
purpureusPUR =(154, 78, 174)
mauvePUR = (224, 176, 255)
mardigrasPUR = (136, 0, 137)
#====

#====
font.init()
ubuntuFont24 = font.Font("fonts/Ubuntu.ttf", 24) #mainly used for drawing text in typing tests
ubuntuFont36 = font.Font("fonts/Ubuntu.ttf", 36)
ubuntuFont30 = font.Font("fonts/Ubuntu.ttf", 30)

bebasFont128 = font.Font("fonts/Bebas.ttf", 128)
bebasFont90 = font.Font("fonts/Bebas.ttf", 90)
bebasFont80 = font.Font("fonts/Bebas.ttf", 80)
bebasFont64 = font.Font("fonts/Bebas.ttf", 64)
bebasFont48 = font.Font("fonts/Bebas.ttf", 48) #used for drawing text in general
bebasFont36 = font.Font("fonts/Bebas.ttf", 36)
bebasFont30 = font.Font("fonts/Bebas.ttf", 30)
bebasFont24 = font.Font("fonts/Bebas.ttf", 24)
bebasFont18 = font.Font("fonts/Bebas.ttf", 18)
bebasFont15 = font.Font("fonts/Bebas.ttf", 15)

screenWid, screenHei = 1000,600
screen = display.set_mode((screenWid,screenHei))
screen.fill(white)
display.set_caption("10 Fast Honks")

accessibleGames = {"gooseArt": True, "gooseFlap":False, "gooseMaze":True, "gooseSnake":False, "gooseTile":False, "gooseCatch": False, "gooseGooseDuck": False}

#====
page = "menu" #credit: menu.py from the McK's FSE prep
day = 0
roundNum = 0
wpmScores = [[0 for a in range(3)]for b in range(7)]

goldenEggMode = False


#======================HELPER FUNCTIONS FOR THE TYPING TEST // BEGINNING
def typingTestWords(day): #getting the raw list of words in random order, pulled from textfiles
    COMunder6 = list(open("textFiles/common words - under 6.txt", "r").read().strip().split())
    COMover6 = list(open("textFiles/common words - over 6.txt", "r").read().strip().split())
    mediumWords = list(open("textFiles/medium words - 150.txt", "r").read().strip().split())
    countries = list(open("textFiles/single word countries - 155.txt", "r").read().strip().split())
    for i in (COMunder6, COMover6, mediumWords,countries):
        shuffle(i)    
    #under6, over6, medium, country - the order of the number of words from each difficulty
    wordRatios = [[500, 50, 20, 10], [475, 60, 20, 10], [450, 70, 25, 10],[425, 80, 25, 10],[400, 90, 30, 10],[375, 100, 30, 10],[350, 110, 35, 10]]
    dayIndex = day-1
    baseVal = [wordRatios[dayIndex][0], wordRatios[dayIndex][1], wordRatios[dayIndex][2], wordRatios[dayIndex][3]] #baseUnder6, baseOver6, baseMed, baseCou
    typingWords = COMunder6[:baseVal[0]] + COMover6[:baseVal[1]] + mediumWords[:baseVal[2]] + countries[:baseVal[3]]
    shuffle(typingWords)
    return(typingWords)

def rowFitInfo(wordList, originX, originY, rowWid, rowHei, font): #spits out a 2d list of information for each word, as well as a list of index information for the indices for each 'row'
    totalRowPx = 0 #the 10 is the starting space
    allWords = [] #all the words, sorted into different rows once everything is added
    rowIndexes = []
    oneRow = []
    rowCount = 0
    for word in range(len(wordList)): #this is inputting lists of information
        txtPic = font.render((wordList[word]), True, (0,0,0))
        picWid, picHei = txtPic.get_width(), txtPic.get_height()
        if totalRowPx + picWid + 10 < rowWid: #the 10 is the spacing in between this one and the next word
            rowCount += 1
            ogx = originX + totalRowPx + 10
            ogy = originY + (rowHei - picHei)//2 #is updated in a later function when it's actually being drawn to the screen
            oneRow.append([wordList[word], picWid, picHei, ogx, ogy, white, black])
            totalRowPx += picWid + 10
        else: #changes the row and adds to the row indeces
            if rowIndexes == []:
                rowIndexes.append([0, len(oneRow)])
            else:
                rowIndexes.append([rowIndexes[-1][1], rowIndexes[-1][1]+len(oneRow)])
            for i in oneRow:
                allWords.append(i)
            oneRow = []
            totalRowPx = 0
    return(allWords,rowIndexes) #returns the list of words, including its dimensions for the picture

def referenceList(wordList, rowIndexes, currentRow):
    justWords = []
    beginning = rowIndexes[currentRow][0]
    end = rowIndexes[currentRow][1]
    for a in range(end-beginning):
        justWords.append(wordList[beginning+a][0])
    return(justWords)

def updateInfo(allWords, originX, originY, currentRowINT, currentWordINT, currentRowInput, currentWordInput, rowIndexes): #when used to draw to screen - updates which word it's on as well as which words were already typed
    inputRect = Rect(topx, topy + rowHei*3.25, rowWid, rowHei) #clears the screen
    for i in range(3):
        draw.rect(screen, white, (originX, originY + rowHei*i, rowWid, rowHei), 0)
    draw.rect(screen, atomicTanOR, inputRect, 1) #clearing the previous rows
    
    referenceRow = referenceList(allWords, rowIndexes, currentRowINT)
    beginning = rowIndexes[currentRowINT][0]
    for a in range(len(referenceRow)):
        if a == currentWordINT:
            if currentWordInput == referenceRow[a][:len(currentWordInput)]:
                allWords[beginning+a][5] = grey
            else:
                allWords[beginning+a][5] = cardinalR
        elif a < currentWordINT:
            allWords[beginning+a][6] = emeraldG if currentRowInput[a] == referenceRow[a] else cardinalR
            allWords[beginning+a][5] = white
        draw.rect(screen, allWords[beginning+a+1][5], (allWords[beginning+a+1][3],allWords[beginning+a+1][4],allWords[beginning+a+1][1],allWords[beginning+a+1][2]), 0)
    for row in range(3):
        theoreticalReferenceRow = referenceList(allWords, rowIndexes, (currentRowINT+row))
        for element in range(len(theoreticalReferenceRow)):
            theActualWord = rowIndexes[currentRowINT+row][0]+element
            ogy = originY + (rowHei - allWords[theActualWord][2])//2 + rowHei*row
            allWords[theActualWord][4] = ogy #updated the y value for blitting the picture in the correct place
            txtPic = typingFont.render((allWords[theActualWord][0]), True, allWords[theActualWord][6], allWords[theActualWord][5])
            screen.blit(txtPic, (allWords[theActualWord][3], allWords[theActualWord][4])) #actually everything to the screen
    return(allWords)
    #this function mainly consists of using 2d lists, grabbing information from one index and then changing other aspect accordinly

def checkingStats(wordList, inputRows): #spits out information (integers) for the STAT page, pulls information from the Typing Test, so is techincally stil a part of it
    keyStrokes = 0
    correctKeyStrokes = 0
    incorrectKeyStrokes = 0
    correctWords = 0
    incorrectWords = 0
    for a,b in zip(wordList, inputRows): #just the actual words, and if they match the ones in the list
        if a == b:
            correctWords += 1
        else:
            incorrectWords += 1
        for c in range(min(len(a),len(b))): #checking the individual word characters
            if b[c].isupper():
                keyStrokes += 2
            elif b[c].islower():
                keyStrokes += 1
            if a[c] == b[c]:
                correctKeyStrokes += 1
            else:
                incorrectKeyStrokes += 1
    return keyStrokes, correctKeyStrokes, incorrectKeyStrokes, correctWords, incorrectWords
#====================HELPER FUNCTIOSN FOR THE TYPING TEST // END

#====================================================================================                   TYPING TEST PAGE
def typingTest(day, roundNum):
    import time as t
    running = True
    myClock = time.Clock()
    screen.fill(white)
    buttons = [Rect(50, 525, 300, 50), Rect(650, 525, 300, 50)]
    vals = ["menu", "typingTest"]
    labels = ["back to menu", "restart"]

    #grabbing information    
    global typingFont
    global topx,topy,rowWid,rowHei
    topx = 50
    topy = 250
    rowWid = 900
    rowHei = 60
    typingFont = ubuntuFont30

    wordDisplayRect = Rect(topx, topy, rowWid, rowHei*3)
    inputRect = Rect(topx, topy + rowHei*3.25, rowWid, rowHei)
    inputWords = [] #holds everything in the row nums, referencing to the actual list
    inputRow = [] #will be cleared every time a row is completed, and is adding to the overall InputWords
    currentWord = "" #holds the current word
    currentWordStats = [0,0] #row, element #
    instructionsRect = Rect(325,120, 340, 115)

    typingTestBack = transform.scale(image.load("gamePics/typingTest/background.jpg"), (screen.get_width(), screen.get_height()-110))
    instructions = transform.scale(image.load("gamePics/typingTest/instructions.png"), (instructionsRect[2], instructionsRect[3]))
    dayPic = bebasFont48.render("Day " + str(day+1), True, black)
    roundPic = bebasFont48.render("Round " + str(roundNum+1), True, black) #loading pictures

    draw.rect(screen, white, (0, 0, screen.get_width(), 110),0)
    typingtestTitle = bebasFont90.render("typing test", True, black)
    screen.blit(typingtestTitle, ( (screen.get_width()-typingtestTitle.get_width())//2, 10)) #drawing the title

    screen.blit(typingTestBack, (0, 110))   #pasting the instructions excerpt
    screen.blit(dayPic, (50, instructionsRect[1]))
    screen.blit(roundPic, (50, instructionsRect[1]+dayPic.get_height()))
    screen.blit(instructions, (instructionsRect[0],instructionsRect[1]))
    draw.rect(screen, lightOR, instructionsRect, 2)
                
    keysPressed = 0 #used to help get the time remaining
    typingTestWordList = typingTestWords(day)
    allWords = updateInfo(rowFitInfo(typingTestWordList, topx, topy, rowWid, rowHei, typingFont)[0], topx, topy, currentWordStats[0], currentWordStats[1], inputRow, currentWord, rowFitInfo(typingTestWordList, topx, topy, rowWid, rowHei, typingFont)[1])
    typedWords = []
    referencedWords = []
    wordToYeet = 0
    start = t.time()
    while running:
        for evt in event.get():
            if evt.type == QUIT:
                return "exit"
            if evt.type == KEYDOWN: #if a key on the keyboard is pressed down
                keyVal = evt.unicode
                if keysPressed == 0:
                    start = t.time() #TIME STARTED
                draw.rect(screen, white, inputRect, 0)
                referenceRow = referenceList(allWords, rowFitInfo(typingTestWordList, topx, topy, rowWid, rowHei, typingFont)[1],  currentWordStats[0])
                if keyVal != "\r" and keyVal != "\t":
                    currentWord += keyVal
                    keysPressed += 1
                    if keyVal == "\b":
                        currentWord = currentWord[0:-2]
                        draw.rect(screen, white, inputRect, 0)
                        draw.rect(screen, blue, inputRect, 1)
                    if keyVal == " ":
                        if currentWord == " ":
                            currentWord = ""
                        else: #address the length of the input list, and checks when it's time to blit the next 'row'
                            if len(inputRow)+1 == len(referenceRow):
                                currentWordStats[0] += 1
                                currentWordStats[1] = 0
                                inputWords.append(inputRow)                                
                                inputRow = []
                                currentWord = ""
                                wordToYeet = 0
                            else:
                                inputRow.append(currentWord.strip(" "))
                                typedWords.append(currentWord.strip(" "))
                                referencedWords.append(referenceRow[wordToYeet])
                                wordToYeet += 1
                                currentWord = ""
                                draw.rect(screen, white, inputRect, 0)
                                currentWordStats[1] += 1 #changes the word within the list
        if keysPressed == 0:
            start = t.time() #to ensure that the timer doesn't start counting down without any input
        if keysPressed > 0 and 60 - (t.time()-start) < 0: #when time runs out, take the information and throws it to the STATS page
            statInfo = checkingStats(referencedWords, typedWords)
            global kS,cKS,iKS,cW,iW
            kS = statInfo[0]
            cKS = statInfo[1]
            iKS = statInfo[2]
            cW = statInfo[3]
            iW = statInfo[4]
            screen.fill(white)
            return "stats"

        if start>0 and 60- (t.time()-start) > 0: #during the actual typing test
            allWords = updateInfo(rowFitInfo(typingTestWordList, topx, topy, rowWid, rowHei, typingFont)[0], topx, topy, currentWordStats[0], currentWordStats[1], inputRow, currentWord, rowFitInfo(typingTestWordList, topx, topy, rowWid, rowHei, typingFont)[1])
            txtPic = typingFont.render((currentWord), True, black)
            screen.set_clip(inputRect)
            draw.rect(screen, white, inputRect, 0)
            centered = (rowHei - txtPic.get_height())//2
            screen.blit(txtPic, (inputRect[0] + 10, inputRect[1] + centered))
            screen.set_clip(None)
            draw.rect(screen, atomicTanOR,inputRect, 2)

            timeElapsed = "%i:%i%i" %( int(t.time()-start)//60, (60 - int(t.time()-start)%60)//10, (60 - int(t.time()-start)%60)%10)
            timeLeftPic = bebasFont80.render((timeElapsed), True, black, white)
            timeRect = Rect(680, 120, 270, 115)        
            draw.rect(screen, white, timeRect, 0)
            screen.blit(timeLeftPic, ((timeRect[0]+(timeRect[2]-timeLeftPic.get_width())//2), (timeRect[1]+(timeRect[3]-timeLeftPic.get_height())//2)))
            draw.rect(screen, lightOR, timeRect, 2)

        mx,my = mouse.get_pos()
        mb = mouse.get_pressed()
        for b,v,lab in zip(buttons, vals, labels): #going to other pages
            draw.rect(screen, papayaOR, b, 0)
            txtPic = bebasFont30.render(lab, True, black)
            screen.blit(txtPic, (b[0]+(b[2]-txtPic.get_width())//2, b[1]+(b[3]-txtPic.get_height())//2))
            if b.collidepoint(mx,my):
                draw.rect(screen,teaRose , b, 2)
                if mb[0] == 1:
                    return v
            else:
                draw.rect(screen, lightOR, b, 3)
                
        draw.rect(screen, atomicTanOR, (topx, topy, rowWid, rowHei*3), 2) #outlining the display (for words)
        display.flip()

#====================================================================================                   STATS PAGE
def stats(keyStrokes, correctKeyStrokes, incorrectKeyStrokes, correctWords, incorrectWords):
    wpm = round(correctKeyStrokes/5, 2) #calculating the overall wpm
    if wpm > correctKeyStrokes/5 + 0.5:
        wpm = int(wpm + 1)
    else:
        wpm = int(wpm)
        
    running = True
    myClock = time.Clock()
    buttons = [Rect(510,510,225,70),Rect(755,510,225,70)]
    vals = ["minigames","typingTest"]
    labels = ["Go to Mini-Games", "Next"]

    statBox = Rect(20, 20, 470, 560)
    gameBox = Rect(510, 20, 470, 470)
    background = transform.scale(image.load("background/stats.jpg"), (screen.get_width(), screen.get_height()))
    screen.blit(background, (0,0))
    
    draw.rect(screen, white, statBox, 0)
    draw.rect(screen, purpureusPUR, statBox, 2)
    draw.rect(screen, purpureusPUR, gameBox, 2)
    
    wpmPic = bebasFont128.render(str(wpm), True, black) #everything within the stats box
    wpmWordPic = bebasFont80.render("wpm", True, black)
    wpmStats = [("Correct Words:", True, black),(str(correctWords), True, emeraldG), ("Wrong Words:", True, black),(str(incorrectWords), True, cardinalR)]
    cpmStats = [("Keystrokes:", True, black),("(", True, black) ,(str(correctKeyStrokes), True, emeraldG), (" -", True, black), (str(incorrectKeyStrokes), True, cardinalR),(")", True, black), (str(correctKeyStrokes + incorrectKeyStrokes), True, black)]
    screen.blit(wpmPic, (20 + (480-(wpmPic.get_width()+wpmWordPic.get_width()))//2, 30))
    screen.blit(wpmWordPic, (20 + wpmPic.get_width() + 10 +( 480-(wpmPic.get_width()+wpmWordPic.get_width()))//2, wpmPic.get_height()//2-5))        
 
    cpmXval = 135
    for c in range(len(cpmStats)):      #drawing the status text to the box (to the left with CPM, WPM, and all that jazz with the correct/incorrect words)
        font = bebasFont48
        y = 70 + wpmWordPic.get_height()
        if c == 0:
            txtPic = bebasFont30.render(cpmStats[c][0], cpmStats[c][1], cpmStats[c][2])
            screen.blit(txtPic, (40,y+10))
        elif c in (1,3,5):
            cpmXval += 60
            txtPic = bebasFont48.render(cpmStats[c][0], cpmStats[c][1], cpmStats[c][2])
            screen.blit(txtPic, (cpmXval,y))
        elif c == 6:
            cpmXval = 410
            txtPic = bebasFont48.render(cpmStats[c][0], cpmStats[c][1], cpmStats[c][2])
            screen.blit(txtPic, (cpmXval,y))
        else:
            cpmXval += 30
            txtPic = bebasFont48.render(cpmStats[c][0], cpmStats[c][1], cpmStats[c][2])
            screen.blit(txtPic, (cpmXval,y))
            
    for a in range(len(wpmStats)):
        if (a+1)%2 == 0:
            y = 140+wpmWordPic.get_height() if a == 1 else 205+wpmWordPic.get_height()
            txtPic = bebasFont48.render(wpmStats[a][0], wpmStats[a][1], wpmStats[a][2])
            screen.blit(txtPic, (410,y))
        else:
            y = 140+wpmWordPic.get_height() if a == 0 else 205+wpmWordPic.get_height()
            txtPic = bebasFont36.render(wpmStats[a][0], wpmStats[a][1], wpmStats[a][2])
            screen.blit(txtPic, (40,y))

    locked = bebasFont128.render("LOCKED", True, black)
    screen.blit(locked, (gameBox[0] + (gameBox[2]-locked.get_width())//2, gameBox[1] + (gameBox[3]-locked.get_height())//2))
    draw.line(screen, black, (40, 370), (470, 370), 3)
    
    for a in range(3):  #drawing the WPM from previous rounds - undeveloped so far
        txtPic = bebasFont36.render("Round "+str(a+1)+":", True, black)
        screen.blit(txtPic, (40, 400+60*a))
        roundwpmPic = bebasFont36.render("x wpm", True, black)
        screen.blit(roundwpmPic, (statBox[0]+(statBox[2]-roundwpmPic.get_width())//2, 400+60*a))

    while running:
        for evt in event.get():
            if evt.type == QUIT:
                return "exit"
        mx,my = mouse.get_pos()
        mb = mouse.get_pressed()
        
        for b,v in zip(buttons, vals): #going to other pages
                draw.rect(screen, palePUR, b, 0)
                txtPic = bebasFont36.render(labels[vals.index(v)], True, black)
                screen.blit(txtPic, (b[0] + (b[2]-txtPic.get_width())//2, b[1] + (b[3]-txtPic.get_height())//2))
                if b.collidepoint(mx,my):
                    draw.rect(screen, mardigrasPUR, b, 2)
                    if mb[0] == 1:
                        return v
                else:
                    draw.rect(screen, pearlyPUR, b, 2)
        display.flip()
        
#====================================================================================                   INSTRUCTIONS PAGE
def INSTRUCTIONS():
    running = True
    myClock = time.Clock()
    draw.rect(screen, white, (0, 0, screen.get_width(), 110),0)
    minigameTitle = bebasFont90.render("Instructions", True, black)
    screen.blit(minigameTitle, ( (screen.get_width()-minigameTitle.get_width())//2, 10))

    background = transform.scale(image.load("background/instructions.jpg"), (screen.get_width(), screen.get_height()-110))
    actualInstructions = image.load("background/instructions.png")
    screen.blit(background, (0, 110))
    screen.blit(actualInstructions, (100, 150))
    
    buttons = [Rect(40,20,150,60)]
    vals = ["menu"]
    labels = ["back to menu"]
    
    while running:
        for evt in event.get():
            if evt.type == QUIT:
                return "exit"
        mx,my = mouse.get_pos()
        mb = mouse.get_pressed()
        for b,v, lab in zip(buttons, vals, labels):
            draw.rect(screen, piggyP, b, 0)
            txtPic = bebasFont24.render(lab, True, black)
            screen.blit(txtPic, (b[0] + (b[2]-txtPic.get_width())//2, b[1] + (b[3]-txtPic.get_height())//2))
            if b.collidepoint(mx,my):
                draw.rect(screen, chinaP, b, 2)
                if mb[0] == 1:
                    return v
            else:
                draw.rect(screen, cottonCandyP, b, 2)
        display.flip()
#====================================================================================                   OPTIONS PAGE
def OPTIONS():
    running = True
    myClock = time.Clock()
    screen.fill(yellow)
    buttons = [Rect(40,20,150,60)]
    vals = ["menu"]
    labels = ["back to menu"]

    draw.rect(screen, white, (0, 0, screen.get_width(), 110),0)
    optionsTitle = bebasFont90.render("options", True, black)
    screen.blit(optionsTitle, ( (screen.get_width()-optionsTitle.get_width())//2, 10))

    background = transform.scale(image.load("background/options.jpg"), (screen.get_width(), screen.get_height()-110))
    screen.blit(background, (0, 110))

    goldenEgg = transform.scale(image.load("background/goldenEgg.png"), (100, 140)) #'easter egg'
    goldenEggRect = Rect((screen.get_width()-goldenEgg.get_width())//2, (screen.get_height()-goldenEgg.get_height())//2,100,140)
    screen.blit(goldenEgg, (goldenEggRect[0], goldenEggRect[1]))    
  
    while running:
        for evt in event.get():
            if evt.type == QUIT:
                return "exit"
        mx,my = mouse.get_pos()
        mb = mouse.get_pressed()
        for b,v,lab in zip(buttons, vals, labels):
            draw.rect(screen, lemonY, b, 0)
            txtPic = bebasFont24.render(lab, True, black)
            screen.blit(txtPic, (b[0] + (b[2]-txtPic.get_width())//2, b[1] + (b[3]-txtPic.get_height())//2))
            if b.collidepoint(mx,my):
                draw.rect(screen, munsellY, b, 2)
                if mb[0] == 1:
                    return v
            else:
                draw.rect(screen, maximumY, b, 2)

        yeet = randint(50, 750), randint(120, 550)
        if goldenEggRect.collidepoint(mx,my) and mb[0] == 1:
            global goldenEggMode
            goldenEggMode = True

        if goldenEggMode == True:
            txtPic = bebasFont48.render("hmm... what did you unlock?", True, black) #just to mess with the player
            screen.blit(background, (0, 110))
            screen.blit(goldenEgg, (goldenEggRect[0], goldenEggRect[1]))
            screen.blit(txtPic, (497, 392))         
        
        display.flip()
#====================================================================================                   MINI-GAME PAGE
def MINIGAMES(): #mini-game page
    running = True
    myClock = time.Clock()
    screen.fill(lightSeaG)
    
    buttons = [Rect(40,20,150,70)]
    buttonVals = ["menu"]
    buttonWords = ["Back to Menu"]
    
    games = [] #actual boxes
    gamesPlay = [] #rectangular 'play' buttons
    gameVals = ["gooseArt", "gooseFlap", "gooseMaze", "gooseSnake", "gooseTile", "gooseCatch", "gooseGooseDuck"]
    gameWords = ["Pixel Goose", "Flappy Goose", "Maze", "Goose", "Goose Tile", "The Sky Is Falling", "Duck Duck Goose"]

    pixelGooseBack = transform.scale(image.load("background/minigamesPIXEL.png"), (200, 200))
    mgGooseMazeBack = transform.scale(image.load("background/minigamesMAZE.png"), (200, 200))
    
    while len(games) <= 7:
        for a in range(4):
            for b in range(2):
                games.append(Rect(40*(a+1) + 200*a, 110+ 30*(b+1) + 200*b, 200, 200))
                gamesPlay.append(Rect(40*(a+1) + 200*a + 50, 110+ 30*(b+1) + 200*b + 120, 100, 50))

    draw.rect(screen, white, (0, 0, screen.get_width(), 110),0)
    minigameTitle = bebasFont90.render("Mini-Games", True, black)
    screen.blit(minigameTitle, ( (screen.get_width()-minigameTitle.get_width())//2, 10))
    background = transform.scale(image.load("background/minigames.jpg"), (screen.get_width(), screen.get_height()-110))
    screen.blit(background, (0, 110))
    
    while running:
        for evt in event.get():
            if evt.type == QUIT:
                return "exit"
        mx,my = mouse.get_pos()
        mb = mouse.get_pressed()

        for g,p,v,w in zip(games, gamesPlay, gameVals, gameWords):
            draw.rect(screen, white, g, 0)
            if v == "gooseArt": #if I actually finished the game :))
                screen.blit(pixelGooseBack, (g[0], g[1]))
            if v == "gooseMaze":
                screen.blit(mgGooseMazeBack, (g[0], g[1]))
            draw.rect(screen, colombianB, g, 2)
            playWord = bebasFont24.render("PLAY", True, black)
            if accessibleGames[v] == True: #if the player is allowed to play this game (have they unlocked it) - in which case there would only be 2 available
                draw.rect(screen, white, p, 0)
                draw.rect(screen, colombianB, p, 2)
                word = bebasFont30.render(w, True, black,white)
                draw.rect(screen, (255,255,255,120), (g[0] + (g[2]-word.get_width())//2 - 20, g[1] + 25 - 10, word.get_width()+40, word.get_height()+20), 0)
                screen.blit(word, ( g[0] + (g[2]-word.get_width())//2, g[1] + 25))
                screen.blit(playWord, ( p[0] + (p[2]-playWord.get_width())//2, p[1]+(p[3]-playWord.get_height())//2))
                if g.collidepoint(mx,my):
                    draw.rect(screen, discoB, g, 2)
                if p.collidepoint(mx,my):
                    draw.rect(screen, capriB, p, 2)
                    if mb[0] == 1:
                        return v                  
            elif accessibleGames[v] == False:
                word = bebasFont64.render("LOCKED", True, black)
                screen.blit(word, ( g[0] + (g[2]-word.get_width())//2, g[1] + (g[3]-word.get_height())//2))
                if g.collidepoint(mx,my):
                    draw.rect(screen, discoB, g, 2)
            else:
                draw.rect(screen, colombianB, b, 2)

        for b,v,w in zip(buttons, buttonVals, buttonWords):
            draw.rect(screen, white, b, 0)
            word = bebasFont24.render(w, True, black)
            screen.blit(word, ( b[0] + (b[2]-word.get_width())//2, b[1] + (b[3]-word.get_height())//2))
            if b.collidepoint(mx,my):
                draw.rect(screen, discoB, b, 2)
                if mb[0] == 1:
                    return v
            else:
                draw.rect(screen, colombianB, b, 2)
        display.flip()

#====================================================================================                   MENU
def menu():
    running = True
    myClock = time.Clock()
    menuBack = transform.scale(image.load("background/menu.jpg"), screen.get_size())
    screen.blit(menuBack, (0,0))
    buttons = [Rect(700, 60+y*125, 250, 100) for y in range(4)]
    vals = ["typingTest", "instructions", "options", "minigames"]
    labels = ["Typing Test", "Instructions", "Options", "Mini-Games"]

    fastHonk = bebasFont128.render("10 Fast Honks", True, black)
    cred = bebasFont48.render("Inspired by 10FastFingers", True, reasonableGrey)
    yuxi = bebasFont36.render("Created by yuxi qin", True, somewhatLegitGrey)
    addition = transform.scale(image.load("background/menuAddition2.png"), (224,396))
    screen.blit(addition, (175, 250))

    screen.blit(fastHonk, (25,40))
    screen.blit(cred, (45, fastHonk.get_height()+7))
    screen.blit(yuxi, (45, fastHonk.get_height()+cred.get_height()))
    
    while running:
        for evt in event.get():
            if evt.type == QUIT:
                return "exit"
        mx,my = mouse.get_pos()
        mb = mouse.get_pressed()
        for b,v,lab in zip(buttons, vals, labels):
            draw.rect(screen, white, b, 0)
            txtPic = bebasFont48.render(lab, True, black)
            screen.blit(txtPic, (b[0]+(b[2]-txtPic.get_width())//2, b[1]+(b[3]-txtPic.get_height())//2))
            if b.collidepoint(mx,my):
                draw.rect(screen, reasonableGrey, b, 2)
                if mb[0] == 1:
                    return v
            else:
                draw.rect(screen, grey, b, 2)
        display.flip()

#====================================================================================                   PIXEL (GOOSE) ART
def gooseArt():
    import time as t
    running = True
    myClock = time.Clock()
    buttons = [Rect(720,445,120,65), Rect(720, 520, 245, 65)]
    vals = ["gooseArt", "minigames"]
    otherButtons = [Rect(845,445,120,65),Rect(720,445,120,65),Rect(720, 520, 245, 65)]
    otherWords = ["RESET", "NEW", "BACK TO MINI-GAMES"]
    
    #drawing the necessary basics - reference picture and 'fill in' (user canvas)
    background = transform.scale(image.load("gamePics/pixelArt/back.png"), (screen.get_width(), screen.get_height()))
    screen.blit(background, (0,0))

    instructions = transform.scale(image.load("gamePics/pixelArt/instructions.png"), (322,140))
    screen.blit(instructions, (23, 435))
    congratulations = image.load("gamePics/pixelArt/congratulations.png")

    refx = 25 #top left corner (where the reference picture will be blitted - where (0,0) is, essentially
    refy = 25
    pixelSize = 16 #how large each 'pixel' will be on both the reference picture as well as user-recreation

    refPic = Rect(refx, refy, (20*pixelSize), (25*pixelSize))
    fillPic = Rect(refPic[0]+refPic[2]+30, refy, (20*pixelSize), (25*pixelSize))
    refPicOUTLINE = Rect(refx-2, refy-2, (20*pixelSize)+3, (25*pixelSize)+3)
    fillPicOUTLINE = Rect(refx-2+(20*pixelSize)+30, refy-2, (20*pixelSize)+3, (25*pixelSize)+3)
    draw.rect(screen, white, refPic, 0)
    #so that the colours from the background don't mess up the RGB values that is derived from the reference picture
    #(and so that it doesn't give anyone panic attacks with basically the same colour showing up multiple times lol)
    
    pictures = []    
    for picture in glob.glob("gamePics/pixelArt/ART*.png"):
        picture = transform.scale(image.load(picture), (20*pixelSize, 25*pixelSize))
        pictures.append(picture)
    screen.blit(choice(pictures), (refx, refy))
        
    draw.rect(screen, black, refPicOUTLINE, 2)
    draw.rect(screen, black, fillPicOUTLINE, 2)

    timeElapsed = bebasFont36.render(("Time Elapsed:"), True, black)
    screen.blit(timeElapsed, (fillPic[0]+(fillPic[2]-timeElapsed.get_width())//2,440))
    
    #getting the rgb values in the reference picture
    refRGB = [[0 for a in range(25)] for b in range(20)]
    fillRGB = [[(255,255,255) for a in range(25)] for b in range(20)]
    colourBlocks = []
    for a in range(20):
        for b in range(25):
            x,y = refx+a*pixelSize, refy+b*pixelSize
            refRGB[a][b] = screen.get_at((x+1, y+1))    #each 16 x 16 pixel will be the same colour - i drew it all yay
            if refRGB[a][b] not in colourBlocks:
                colourBlocks.append(refRGB[a][b])
                
    #drawing the selection of colours from the reference picture
    colourRects = [] #what we'll be adding the rects to, is the equivalent of buttons but for colours
    rowCol = 0
    for col in range(len(colourBlocks)): #draws the colour selections
        if col%3 == 0 and col != 0:
            rowCol += 1
        colourRects += [Rect(720+(col%3*75)+(col%3*10), 23+(rowCol*75)+(rowCol*10), 75,75)] #diff colours
    for a in range(len(colourRects)): #drawing it to the screen
        draw.rect(screen, colourBlocks[a], colourRects[a], 0)
        draw.rect(screen, black, colourRects[a], 1)

    endClick = False
    clicked = False
    fillColour = white
    while running:
        click = False
        for evt in event.get():
            if evt.type == QUIT:
                return "exit"
        mx,my = mouse.get_pos()
        mb = mouse.get_pressed()

        if clicked == False:
            firstClick = t.time()

        #buttons that just check and returns colours within the same function (ex. clearing the entire page or something)
        for c,v in zip(colourRects, colourBlocks):
            draw.rect(screen, black, c, 1)
            if c.collidepoint(mx,my):
                draw.rect(screen, seaG, c, 1)
                if mb[0] == 1:
                    fillColour = v
                else:
                    draw.rect(screen, white, c, 1)       

        #buttons that actually go to places/does stuff (like to menu and all that)
        for b, v in zip(buttons, vals):
            draw.rect(screen, pastelB, b, 0)
            if b.collidepoint(mx,my):
                draw.rect(screen, lightGreyB, b, 2)
                if mb[0] == 1:
                    return v
                    draw.rect(screen, skyB, b, 2)
            else:
                draw.rect(screen, black, b, 2)

        #buttons that do other things within the game (doesn't lead anywhere outside)
        for r,text in zip(otherButtons, otherWords):
            draw.rect(screen, pastelB, r, 0)
            txtPic = bebasFont24.render(text,True, black, pastelB)
            blitX = (r[2]-txtPic.get_width())//2
            blitY = (r[3]-txtPic.get_height())//2
            screen.blit(txtPic, (r[0]+blitX, r[1]+blitY))
            if r.collidepoint(mx,my):
                draw.rect(screen, lightGreyB, r, 2)
                if mb[0] == 1:
                    fillRGB = [[(255,255,255) for a in range(25)] for b in range(20)]
                    clicked = False
                    draw.rect(screen, skyB, r, 2)
            else:
                draw.rect(screen, black, r, 2)
                
        #when the user is actually drawing to the 'input canvas'
        if fillPic.collidepoint(mx,my):
            screen.set_clip(fillPic)
            by,bx = (mx-fillPic[0])//pixelSize, (my-fillPic[1])//pixelSize
            if mb[0] == 1:
                fillRGB[by][bx] = fillColour
                if clicked == False:
                    clicked = True
                    firstClick = t.time() #first click - countdown
            if mb[2] == 1:
                fillRGB[by][bx] = white
            screen.set_clip(None)
                
        for a in range(len(fillRGB)): #y 
            for b in range(len(fillRGB[a])): #x
                draw.rect(screen, fillRGB[a][b], ((fillPic[0]+pixelSize*a), (fillPic[1]+pixelSize*b), pixelSize, pixelSize), 0)
                #drawing everything to the screen

        font = bebasFont48
        
        #elapsed time
        timeElapsed = "%i:%i%i" %(
            int(t.time()-firstClick)//60,
            (int(t.time()-firstClick)%60)//10,
            (int(t.time()-firstClick)%60)%10)
        timeElapsedPic = font.render((timeElapsed), True, black)
        draw.rect(screen, white, (500,475, timeElapsedPic.get_width()+30, timeElapsedPic.get_height()), 0)
        screen.blit(timeElapsedPic, (500,475))
      
        fillCorrect = 0 #the amount of colours that are in the right position
        for a in range(len(refRGB)):
            for b in range(len(refRGB[a])):
                if refRGB[a][b] == fillRGB[a][b]:
                    fillCorrect += 1
        percentageComplete = round(fillCorrect/(25*20)*100, 2)
           
        showPercentage = (str(percentageComplete) + "% complete")
        showPercentagePic = bebasFont18.render((showPercentage), True, black)
        draw.rect(screen, white, (455, 530, 175, 30), 0)
        screen.blit(showPercentagePic, (490, 530))

        if percentageComplete == 100 and endClick == False: #if the player has fully completed the drawing
            endClick = True
            endTime = t.time()
        if endClick == True:
            endTimeElapsed = "%i:%i%i" %(
            int(endTime-firstClick)//60,
            (int(endTime-firstClick)%60)//10,
            (int(endTime-firstClick)%60)%10)
            draw.rect(screen, white, (373, 445, 322, 138), 0)
            screen.blit(congratulations, (373, 445)) #320, 125
            congratTime = bebasFont24.render(endTimeElapsed, True, black)
            screen.blit(congratTime, (620, 500))  

        display.flip()
#=======================================================================================================                GOOSE MAZE
def gooseMaze():
    import time as t
    running = True
    screen.fill(white)
    myClock = time.Clock()
    
    #going to other pages
    buttons = [Rect(600, 500,375, 70), Rect(600,417, 375, 70)]
    vals = ["minigames", "gooseMaze"]
    labels = ["back to mini-games", "new"]

    BOUNDARY = black
    CENTER = red

    x = 280
    y = 50
    offsetX = 25
    offsetY = 25

    #SPRITES
    frameDelay = 10
    frame = 0
    stand = []
    up = []
    down = []
    left = []
    right = []
    direction = down
    for i in range(3):
            up.append(image.load("gamePics/gooseMaze/gooseUp/gooseUp" + str(i) + ".png"))
    for i in range(3):
            down.append(image.load("gamePics/gooseMaze/gooseDown/gooseDown" + str(i) + ".png"))
    for i in range(3):
            left.append(image.load("gamePics/gooseMaze/gooseLeft/gooseLeft" + str(i) + ".png"))
    for i in range(3):
            right.append(image.load("gamePics/gooseMaze/gooseRight/gooseRight" + str(i) + ".png"))
            
    #getting the different levels of things
    difficulty = [Rect(600, 280, 355//3, 125), Rect(728, 280, 355//3, 125), Rect(857, 280, 355//3, 125)]
    diffLabels = ["easy", "medium", "hard"]
    difficultyLevel = 0
    differentMazes = [[],[],[]]
    differentMasks = [[],[],[]]

    #loading the masks and their corresponding maze pictures
    for e,j in zip(sorted(glob.glob("gamePics/gooseMaze/EASYmaze*.*")),sorted(glob.glob("gamePics/gooseMaze/EASYmask*.*"))):
        e = transform.scale(image.load(e), (550, 550))
        j = transform.scale(image.load(j), (550, 550))
        differentMazes[0].append(e)
        differentMasks[0].append(j)

    for m,j in zip(sorted(glob.glob("gamePics/gooseMaze/MEDmaze*.*")),sorted(glob.glob("gamePics/gooseMaze/MEDmask*.*"))):
        m = transform.scale(image.load(m), (550, 550))
        j = transform.scale(image.load(j), (550, 550))
        differentMazes[1].append(m)
        differentMasks[1].append(j)

    for h,j in zip(sorted(glob.glob("gamePics/gooseMaze/HARDmaze*.*")), sorted(glob.glob("gamePics/gooseMaze/HARDmask*.*"))):
        h = transform.scale(image.load(h), (550, 550))
        j = transform.scale(image.load(j), (550, 550))
        differentMazes[2].append(h)
        differentMasks[2].append(j)

    congratulations = transform.scale(image.load("gamePics/gooseMaze/congratulations.png"), (375,150))    
    background = transform.scale(image.load("gamePics/gooseMaze/gooseMazeBack.jpg"), (screen.get_width(), screen.get_height()))
    screen.blit(background, (0,0))

    mazePic = choice(differentMazes[difficultyLevel])
    maskPic = differentMasks[difficultyLevel][(differentMazes[difficultyLevel]).index(mazePic)]
    
    timeElapsed = bebasFont48.render(("Time Elapsed:"), True, black)
    screen.blit(timeElapsed, (mazePic.get_width() + (screen.get_width()-mazePic.get_width()+50 - timeElapsed.get_width())//2, offsetY)) #centered

    instructions = transform.scale(image.load("gamePics/gooseMaze/instructions.png"), (375, 115))
    screen.blit(instructions, (600, 150))
    
    for a in buttons:
        draw.rect(screen, white, a, 2)
    for a in difficulty:
        draw.rect(screen, white, a, 2)

    start = t.time()
    endTimeV = False
    clicked = False
    keysPressed = 0
    while running:
        for evt in event.get():
            if evt.type == QUIT:
                return "exit"
            if evt.type == KEYDOWN:
                keysPressed += 1
                if keysPressed == 1:
                    start = t.time()
            if clicked == True:
                clicked = False
        mx,my = mouse.get_pos()
        mb = mouse.get_pressed()                
        keys = key.get_pressed()

        if keysPressed == 0: #as long as the player hasn't pressed any keys, the timer will be dead
            start = t.time()
        if endTimeV == False:
            timeElapsedNum = "%i:%i%i" %(
                int(t.time()-start)//60,
                (int(t.time()-start)%60)//10,
                (int(t.time()-start)%60)%10)
            timeElapsedPic = bebasFont64.render((timeElapsedNum), True, black)
            draw.rect(screen, white, (mazePic.get_width() + (screen.get_width()-mazePic.get_width()+50 - timeElapsedPic.get_width())//2 -20, offsetY + 50, timeElapsedPic.get_width()+40, timeElapsedPic.get_height()), 0)
            screen.blit(timeElapsedPic, (mazePic.get_width() + (screen.get_width()-mazePic.get_width()+50 - timeElapsedPic.get_width())//2, offsetY+50))

        if endTimeV == True:
            screen.blit(congratulations, ((mazePic.get_width()+50), offsetY))
            endtimeNum = "%i:%i%i" %(
            int(endtime-start)//60,
            (int(endtime-start)%60)//10,
            (int(endtime-start)%60)%10)
            endtimePic = bebasFont24.render((endtimeNum), True, black)
            screen.blit(endtimePic, (775, 120))
            
        #integrated 3 functions into one giant loop
        if offsetX<x<(offsetX+maskPic.get_width()) and offsetY<y<(offsetY+maskPic.get_height()):
            if keys[K_UP] and maskPic.get_at((x-offsetX,y-offsetY-direction[frame].get_height()//2-2)) != BOUNDARY:
                y -= 2
                direction = up
                frameDelay -= 1                         # count down to zero
                if frameDelay == 0:                     # then advance frame like normal
                    frameDelay = 10                     #CREDS TO MCKENZIE'S FSE PREP - SPRITE EXAMPLES
                    frame += 1
                    if frame == 3: frame = 0

            elif keys[K_DOWN] and maskPic.get_at((x-offsetX,y-offsetY+direction[frame].get_height()//2+2)) != BOUNDARY:
                y += 2
                direction = down
                frameDelay -= 1
                if frameDelay == 0:
                    frameDelay = 10
                    frame += 1
                    if frame == 3: frame = 0

            elif keys[K_LEFT] and maskPic.get_at((x-offsetX-direction[frame].get_width()//2-2,y-offsetY)) != BOUNDARY:
                x -= 2
                direction = left
                frameDelay -= 1
                if frameDelay == 0:
                    frameDelay = 10
                    frame += 1
                    if frame == 3: frame = 0
                    
            elif keys[K_RIGHT] and maskPic.get_at((x-offsetX+direction[frame].get_width()//2+2,y-offsetY)) != BOUNDARY:
                x += 2
                direction = right
                frameDelay -= 1
                if frameDelay == 0:
                    frameDelay = 10
                    frame += 1
                    if frame == 3: frame = 0
                    
        draw.rect(screen, white, (offsetX,offsetY, mazePic.get_width(), mazePic.get_height()), 0)
        screen.blit(mazePic, (offsetX,offsetY))
        draw.rect(screen, black, (offsetX,offsetY, mazePic.get_width(), mazePic.get_height()), 3)
        screen.blit(direction[frame], (x-(direction[frame].get_width()//2),y-(direction[frame].get_height())//2)) #simulating centering the goose picture, and blitting it so instead of from the corner

        for b,v,a in zip(buttons,vals,labels):
            draw.rect(screen, teaG, b,0)
            txtPic = bebasFont36.render(a, True,black)
            screen.blit(txtPic, (b[0]+(b[2]-txtPic.get_width())//2, b[1]+(b[3]-txtPic.get_height())//2)) #centered
            if b.collidepoint(mx,my):
                draw.rect(screen, myrtleG, b, 2)
                if mb[0] == 1:
                    return v
            else:
                draw.rect(screen,mintG,b,2)
                
        for b,v in zip(difficulty,diffLabels):
            draw.rect(screen, teaG, b,0)
            txtPic = bebasFont36.render(v, True,black)
            screen.blit(txtPic, (b[0]+(b[2]-txtPic.get_width())//2, b[1]+(b[3]-txtPic.get_height())//2)) #centered
            if b.collidepoint(mx,my):
                draw.rect(screen, myrtleG, b, 2)
                if mb[0] == 1:
                    draw.rect(screen, black, b, 2)
                    difficultyLevel = diffLabels.index(v)
                    keysPressed = 0
                    if clicked == False:
                        mazePic = choice(differentMazes[difficultyLevel])
                        maskPic = differentMasks[difficultyLevel][(differentMazes[difficultyLevel]).index(mazePic)]
                        x = 280
                        y = 50
                        start = t.time()
                        #so that it would only 'reload' once, and not just continuously blit
                    clicked = True
            else:
                draw.rect(screen,myrtleG,b,2)
                
        if maskPic.get_at((x-offsetX,y-offsetY)) == CENTER:
            endTimeV = True
            endtime = t.time()

            
        display.flip()

#=============================================================================================================================

def gooseFlap():
    return

def gooseSnake():
    return

def gooseTile():
    return

def gooseCatch():
    return

def gooseGooseDuck():
    return

#==========================THIS IS A PROTECTED ZONE THAT NO FUCKUPERY CAN OCCUR HERE OR U JUST STOOPID
running = True
while page != "exit":
    if page == "menu":
        page = menu()
    if page == "designGoose":
        page = PLAYdesignGoose()
    if page == "instructions":
        page = INSTRUCTIONS() #done
    if page == "options":
        page = OPTIONS()
    if page == "minigames":
        page = MINIGAMES() #done

    if page == "typingTest":
        page = typingTest(day,roundNum) #sorta done
    if page == "stats":
        print(kS,cKS, iKS, cW, iW)
        page = stats(kS, cKS, iKS,cW,iW)

    if page == "gooseArt":  #MINI GAME PAGES
        page = gooseArt() #done
    if page == "gooseFlap":
        page = gooseFlap()
    if page == "gooseMaze": #done
        page = gooseMaze()
    if page == "gooseSnake":
        page = gooseSnake()
    if page == "gooseTile":
        page = gooseTile()
    if page == "gooseCatch":
        page = gooseCatch()
    if page == "gooseGooseDuck":
        page = gooseGooseDuck()

    display.flip()
quit()
