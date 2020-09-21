#adding library and importing functions
import os
import math
import random
add_library("minim")
audioPlayer = Minim(this)
score=20
path =os.getcwd()
#creating the class creature
class Creature:
    def __init__(self, x, y, r, img, fwidth, fheight, numf, picHeight):
        self.x = x
        self.y = y
        self.r = r
        self.img = loadImage(path +"/img/"+img)#loading image
        self.fwidth = fwidth #frame width
        self.fheight = fheight #frame height
        self.picHeight = picHeight
        self.numf = numf #number of frames
        self.direction = 1 #the game direction will always be to the right
        self.ground=0
        self.verticalv=0
        self.horizentalv=0
    def det_ground(self):#this function is to determine the ground
        self.ground = g.ground
        self.ground = 800
    
    #gravity function
    def gravity(self):
        self.det_ground()
        if self.y+self.r<self.ground:
            self.verticalv = self.verticalv + 0.3
        elif self.verticalv>0:
            self.verticalv=0
        if self.y + self.r + self.verticalv > self.ground:
            self.y = self.ground - self.r
        else: 
            self.y=self.y+self.verticalv
    def update(self):
        self.gravity()
    #displaying the creature box inhere, and will be used for detection    
    def display(self):
        self.update()
        image(self.img, self.x-g.screen, self.y - self.picHeight//2,
            self.fwidth, self.picHeight)
class Falcon(Creature):
    #creating class falcon for my character, and inherting creature in it
    def __init__(self, x, y, r, img, fwidth, fheight, numf, picHeight,horizentalv):
        self.hv=horizentalv
        Creature.__init__(self, x, y, r, img, fwidth, fheight, numf, picHeight)
        #key pressings
        self.key_pressed = {UP: False, RIGHT: False}
        self.key_pressed = {LEFT: False, RIGHT: False, UP: False}
        #loading sounds
        self.soundfly = audioPlayer.loadFile(path + "/sound/sfx_fly.wav")
        self.soundhit = audioPlayer.loadFile(path + "/sound/sfx_hit.wav")
        self.soundpoint = audioPlayer.loadFile(path + "/sound/sfx_point.wav")
        #return variable point so when the object hit the green collision, it return and gets another chance
        self.left_return=0
        self.up_return=0
    def update(self):
        #score of the game
        global score
        self.gravity()
        self.horizentalv=self.hv
        #movement of the game
        if self.x <= self.left_return:
            self.direction = 1   
        if self.y <= self.up_return:
            self.verticalv = 0
            self.up_return = 0
        if self.key_pressed[UP] and self.verticalv > 0:
            self.verticalv = -5
            self.soundfly.rewind()
            self.soundfly.play()
        if self.x+self.verticalv>0:
            self.x+=self.horizentalv*self.direction
            if self.x > g.width // 2:
                g.screen += self.horizentalv*self.direction
                
        #putting the variable of the four pints of my rectangle in a list to detect them with platforms        
        l=[[self.x,self.y- self.fheight//2], [self.x+self.fwidth, self.y- self.fheight//2], [self.x,self.y+self.fheight- self.fheight//2], [self.x+self.fwidth, self.y+self.fheight- self.fheight//2]]
        # for i in range(len(l)):
        #     stroke(255,0, 0)
        #     point(l[i][0], l[i][1])
        # bottom green pipes collision detection
        for platform in g.platformss1:
            for p in l:
                if p[0]>=platform.x and p[0]<=platform.x+platform.width and p[1]>platform.y and p[1]<platform.y+platform.height:
                    
                    self.left_return = self.x-50
                    self.verticalv = -5
                    self.direction=-1
                    
                    #self.up_return = self.y-100
                    #print(p[0], p[1],platform.x, platform.y +platform.height)
                    score-=1#decreamenting the score if it hits the pipe
                    self.soundhit.rewind()
                    self.soundhit.play()
                    break

                    

                    ##print("test")
                    #print(p[0], platform.x, "kjdfhgkfdh")
        
        # top green pipes platfor detection
        for platform in g.platformss2:
            for p in l:
                if p[0]>=platform.x and p[0]<=platform.x+platform.width and p[1]<=platform.y+platform.height and p[1]>platform.y :
                    self.left_return = self.x-50
                    self.direction=-1 #decreamenting the score if it hits the pipe


                    self.verticalv = 5
                    #self.up_return = self.y100
                    #print(self.x, self.y)
                    #print(p[0], p[1],platform.x, platform.y +platform.height)
                    #print("test")
                    score-=1
                    self.soundhit.rewind()
                    self.soundhit.play()
                    break

        # both top and bottom red pipes detection
        for platform in g.platforms:
            for p in l:
                if p[0]>=platform.x and p[0]<=platform.x+platform.width and p[1]>platform.y and p[1]<platform.y+platform.height:
                    #print("hhhhh")
                    score=0 #losing the game if it hits the red pipe
                    self.soundhit.rewind()
                    self.soundhit.play()
        #marks detection and removing them
        for mark in g.marks:
            for p in l:
                if p[0]>=mark.x and p[0]<=mark.x+mark.width and p[1]>mark.y and p[1]<mark.y+mark.height:
                    score+=1
                    g.marks.remove(mark)
                    self.soundpoint.rewind()
                    self.soundpoint.play()

        # if score==0:
            # self.sounddie.rewind()
            # self.sounddie.play()
        # if self.falcon.x==8000:
        #     self.gamestate="gamecomplete"
      
        #print(score)
# the next 4 classes is to create the platform up and down for red and green pipes and creating display function for them  
class PlatformTop:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.img = loadImage(path + "/img/top.png")
    
    def display(self):
        image(self.img, self.x - g.screen, self.y)
class PlatformBottom:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.img = loadImage(path + "/img/bottom.png")
    
    def display(self):
        image(self.img, self.x - g.screen, self.y)
class PlatformTop2:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.img = loadImage(path + "/img/top2.png")
    
    def display(self):
        image(self.img, self.x - g.screen, self.y)
class PlatformBottom2:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.img = loadImage(path + "/img/bottom2.png")
    
    def display(self):
        image(self.img, self.x - g.screen, self.y)
#creating class for the stat and displaying it
class Marks:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.img = loadImage(path + "/img/mark.png")
    
    def display(self):
        image(self.img, self.x - g.screen, self.y)

class Game:
#creating game class
    def __init__(self, width, height, ground):
        self.pointlist=[0]
        self.init(width, height, ground)
    def init(self, width, height, ground):
        #loading sound
        self.soundintro = audioPlayer.loadFile(path + "/sound/intro.wav")
        self.soundvictory = audioPlayer.loadFile(path + "/sound/victory.wav")
        self.soundgameover = audioPlayer.loadFile(path + "/sound/gameover.mp3")


        self.width= width
        self.height= height
        self.ground=ground
        self.falcon = Falcon(100, 100, 35, "falcon1.png", 50, 70, 11, 100, 2)
        self.platformss1= []
        self.platformss2= []
        self.platforms= []
        self.gamestate= "menu"
        self.marks=[]
        #text for buttons
        self.text1=[]
        self.text2=[]
        self.text3=[]
        self.text4=[]
        self.text5=[]
        # self.sounddie = audioPlayer.loadFile(path + "/sound/sfx_die.wav")

        # if self.falcon.y==765:
        #     self.sounddie.rewind()
        #     self.sounddie.play()           
        # if self.falcon.y<15:
        #     self.sounddie.rewind()
        #     self.sounddie.play()  
        #loading images for backgrounds
        self.screen=0
        self.im1= loadImage(path+"/img/1.jpg")
        self.im2= loadImage(path+"/img/2.jpg")
        self.im3= loadImage(path+"/img/3.jpg") 
        self.im4= loadImage(path+"/img/4.jpg")
        self.im5= loadImage(path+"/img/5.jpg")
        self.im6= loadImage(path+"/img/6.jpg")
        self.im7= loadImage(path+"/img/7.jpg")
        self.im8= loadImage(path+"/img/8.jpg")
        self.im9= loadImage(path+"/img/menu.jpg")
        self.im10= loadImage(path+"/img/instruc.jpg")
        self.im11= loadImage(path+"/img/menu2.jpg")
        self.im12= loadImage(path+"/img/gameover.jpg")
        self.im13= loadImage(path+"/img/gamecomplete.jpg")  
        #appeanding words to list so they could be chosen as buttons      
        self.text1.append(Options("Start Game", self.width//2 - 100, self.height//2 -150, 50, 250))
        self.text1.append(Options("Instructions", self.width//2 - 100, self.height//2 + 200, 50, 250))
        self.text2.append(Options("Menu", self.width//2 + 400, self.height//2 + 300, 50, 250))
        self.text3.append(Options("Menu", self.width//2 + 400, self.height//2 + 300, 50, 250))
        self.text4.append(Options("Menu", self.width//2 + 400, self.height//2 + 300, 50, 250))
        self.text5.append(Options("Slow Purple Falcon", self.width//2-200, self.height//2 + 150, 50, 250))
        self.text5.append(Options("Fast Black Falcon", self.width//2 +200, self.height//2 + 150, 50, 250))

        #placing the platforms completly randomly, 5 red pipes, 15 green, and 5 marks
        numreds=0
        nummark=0
        numgreen=0
        redlist= []
        marklist=[]
        greenlist=[]
        #assigning the positions of each of the platforms from 1-25
        while numreds<4:
            randnumb=random.randint(0,24)
            if randnumb not in redlist:
                redlist.append(randnumb)
                numreds+=1
        #print(redlist)
        while nummark<5:
            randnumb=random.randint(0,24)
            if randnumb not in redlist and randnumb not in marklist :
                marklist.append(randnumb)
                nummark+=1
        while numgreen<16:
            randnumb=random.randint(0,24)
            if randnumb not in redlist and randnumb not in greenlist and randnumb not in marklist :
                greenlist.append(randnumb)
                numgreen+=1
        # print(marklist)
        # print(redlist)
        # print(greenlist)
        #putting them on the screen and randomize their place on the screen
        for i in range (500,9001, 350):
            ind = (i - 500) / 350
            # print(ind)
            #print(i)
            r= random.randint(-90,90)
            
            n=random.randint(100,200)
            #print(r)
            y= random.randint(-50,50)                
            if ind in redlist:
                platformbottom2 = PlatformBottom2(i+r, 400+y, 98, 500)
                self.platforms.append(platformbottom2)
                platformtop2 = PlatformTop2(i+r, -300+y, 100, 500)
                self.platforms.append(platformtop2)
                #print("Added redhi")            
            if ind in greenlist:
                platformbottom = PlatformBottom(i+r, 400+y,98 , 500)
                self.platformss1.append(platformbottom)
                platformtop = PlatformTop(i+r, -300+y, 100, 500)
                self.platformss2.append(platformtop)
            if ind in marklist:
                mark1 = Marks(i+r, 400+y, 50, 50)
                self.marks.append(mark1)
    #display menu function
    def displaymenu(self):
        background(0)
        image(self.im9, 0,0, width, height)
        for t in self.text1:
            t.display() 
        textSize(40)
        global score
        #print(score)
        fill(255)
        #printing high score
        #print(self.pointlist)
        text("HighScore:"+str(max(self.pointlist))+"/20",530,400)
        self.soundintro.play()
    #display second menu to choose the falcon
    def displaymenu2(self):
        background(0)
        image(self.im11, 0,0, width, height)

        self.soundintro.play()
        for t in self.text5:
            t.display()
    #display the instruction menu
    def displayinstructions(self):
        background(0)
        image(self.im10, 0,0, width, height)
        for t in self.text2:
            t.display()  
        # textSize(20);
        # text("word", 10, 30); 
        # fill(0, 255, 0);
    #display gameover screen
    def displaygameover(self):
        background(0)
        image(self.im12, 0,0, width, height)
        self.soundgameover.play()
        for t in self.text3:
            t.display()
        textSize(40)
        global score
        #print(score)
        text("score:"+str(score)+"/20",40,40)
    #display game completed
    def displaygamecomplete(self):
        background(0)
        image(self.im13, 0,0, width, height)
        self.soundvictory.play()
        for t in self.text4:
            t.display()
        textSize(40)
        global score
        #print(score)
        text("score:"+str(score)+"/20",40,40)
    #display the game
    def displaygame(self):
        #print(self.falcon.x, width/2)
        if self.falcon.x >= width/2:#displayed pictures one after another, and start moving them when falcon reached the middle
            image(self.im1, 0-self.falcon.x+width/2,0)
            image(self.im2, width-self.falcon.x+width/2,0)
            image(self.im3, width*2-self.falcon.x+width/2, 0)
            image(self.im4, width*3-self.falcon.x+width/2, 0)
            image(self.im5, width*4-self.falcon.x+width/2, 0)
            image(self.im6, width*5-self.falcon.x+width/2, 0)
            image(self.im7, width*6-self.falcon.x+width/2, 0)
            image(self.im8, width*7-self.falcon.x+width/2, 0)
        else:
            #print("INIT")
            image(self.im1, 0,0, width, height)
        
            
        #print(self.falcon.x)
        #displaying platforms
        self.falcon.display()
        for platform in self.platformss1:
            platform.display()
        for platform in self.platformss2:
            platform.display()
        for platform in self.platforms:
            platform.display()
        for mark in self.marks:
            mark.display()
        textSize(40)
        global score
        #printing score
        text("score:"+str(score)+"/20",40,40) 
            
    #function to display the game and the differnt tyope of screens based on conditions made in mousepressed function
    def display(self):
        #print(score, self.falcon.x, self.falcon.y)
        #print(self.gamestate)
        global score
        #conditions to when the game would complete or it would be gameover
        if self.gamestate != "gameover" and score == 0:
            self.gamestate = "gameover"    
        if self.falcon.x>=9050:
            #appeanding the scores on the list
            self.pointlist.append(score)
            self.gamestate="gamecomplete"
            self.falcon.x = 100
        if self.falcon.y==765:
            #print("OVER 1")
            score=0
            self.gamestate="gameover"            
        if self.falcon.y<=15:
            #print("OVER 2")
            score=0
            self.gamestate="gameover"  
      #conditions to change between screens          
        if self.gamestate=="menu":
            self.displaymenu()
        elif self.gamestate=="instruc":
            self.displayinstructions()
        elif self.gamestate=="menu2":
            self.displaymenu2()
        elif self.gamestate=="game1":
            self.displaygame()
        elif self.gamestate=="game2":
            self.displaygame()
        elif self.gamestate=="gameover":
            self.displaygameover()
        elif self.gamestate=="gamecomplete":
            self.displaygamecomplete()
        
        
      #keypress function  
    def keypress(self):
        if keyCode == RIGHT:
            self.falcon.key_pressed[RIGHT] = True
        elif keyCode == UP:
            self.falcon.key_pressed[UP] = True  
      #key release  
    def keyrelease(self):
        if keyCode == RIGHT:
            self.falcon.key_pressed[RIGHT] = False
        elif keyCode == UP:
            self.falcon.key_pressed[UP] = False
        #this mousepressed functionis to assign the button to the state of the game, so if the user click 
        #on a specifc button, it will take them to another screen and based on this, those states would be used in display function
    def mousepressed(self): 
        global score       
        if self.text1[0].mouse():
            self.gamestate = "menu2"
        if self.text1[1].mouse():
            self.gamestate = "instruc"
        if self.text2[0].mouse():
            self.falcon.y = 1000000
            #print("RESET 1")
            score = 20
            self.gamestate = "menu"
        if self.text3[0].mouse():
            score = 20
            #print("RESET 2")
            self.gamestate = "menu"
        if self.text4[0].mouse():
            # score = 20
            #print("RESET 3")
            self.gamestate = "menu"
        if self.text5[0].mouse():
            self.init(self.width, self.height, self.ground)
            #for purple and slow falcon
            self.gamestate = "game1"
            #score = 20
            #print("GAME 1")
            self.falcon = Falcon(100, 100, 35, "falcon1.png", 50, 70, 11, 100, 2)
            self.displaygame()
        if self.text5[1].mouse():
            #for black and fast falcon
            self.init(self.width, self.height, self.ground)
            self.gamestate = "game2"
            #print("GAME 2")
            #score = 20
            self.falcon = Falcon(100, 100, 35, "falcon2.png", 50, 70, 11, 100, 8)
            self.displaygame()
        #print(score)

            


#this clas is for the mouse and clicking    
class Options:
    def __init__(self,title,x, y,height, width):
        self.title=title
        self.x=x
        self.y=y
        self.height=height
        self.width=width
    def mouse(self):
        return self.x <= mouseX <= self.x + self.width and self.y - self.height <= mouseY <= self.y
    def display(self):
        #if the mouse is hovering over the words, display red, else display white
        if self.mouse():
            fill (255,0,0)
        else:
            fill (255)
        textSize(40)
        text(self.title, self.x, self.y)

        
    
g= Game(1300, 800, 585)
def setup():
    size(g.width, g.height)
def draw():
    g.display()
def keyPressed():
    g.keypress()
def keyReleased():
    g.keyrelease()
def mousePressed():
    g.mousepressed()


        
        
    

        


        
        
    
        
        
