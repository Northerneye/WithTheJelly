#https://www.youtube.com/watch?v=6gNpSuE01qE
# WARNING: ICON IMAGE MUST BE SMALL(if used) OR THE INSTALL WILL CRASH
import kivy
from kivy.core.audio import SoundLoader
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import RoundedRectangle, Color, Rectangle, Line
from kivy.uix.boxlayout import BoxLayout
from kivy.core.image import Image
from kivy.core.window import Window
import math

from kivy.input.shape import ShapeRect

import random

kivy.require('1.9.0')

GlobalWidth = math.floor(Window.size[0]/6)
GlobalSpacing = math.floor(Window.size[0]/6/6)
global SelectedSquare
SelectedSquare = [None,None]
global Turn
Turn = 0 #orange
global Highlight
Highlight = [None, None]
global wincon
wincon = False
global gameType
gameType = 0
global Music
Music = False
global Undo
Undo = False
global lastStacks

Stacks = [
    [[],[],[],[],[]],
    [[],[],[],[],[]],
    [[],[],[],[],[]],
    [[],[],[],[],[]],
    [[],[],[],[],[]]]
lastStacks = [
    [[],[],[],[],[]],
    [[],[],[],[],[]],
    [[],[],[],[],[]],
    [[],[],[],[],[]],
    [[],[],[],[],[]]]

global GlobalStackIndicator
GlobalStackIndicator = None
global GlobalBackgroundWidget
GlobalBackgroundWidget = None

lastState = [[[0,0], 0, [0,0,0,0]] for i in range(13)]
lastState.append([
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]])
print(lastState[13])

MainMenuSong = SoundLoader.load("NoWorries_NoCopyright.mp3")
MainMenuSong.loop = True
VanillaPancakeSong = SoundLoader.load("ALonelyCherryTree_NoCopyright.mp3")
VanillaPancakeSong.loop = True
RoyalJellySong = SoundLoader.load("NinjaToad_NoCopyright.mp3")
RoyalJellySong.loop = True
RoyalPancakeSong = SoundLoader.load("BeginYourJourney_NoCopyright.mp3")
RoyalPancakeSong.loop = True
WinSong = SoundLoader.load("8BitLove_NoCopyright.mp3")
WinSong.loop = True
WinSong.volume = .2


def checkwin():
    global Stacks
    for stack in [Stacks[i][0] for i in range(5)]:
        for jar in stack:
            if(jar.player == 1):
                return 1
    for stack in [Stacks[i][4] for i in range(5)]:
        for jar in stack:
            if(jar.player == 0):
                return 0
    return -1

class MyRoot(Widget):
    def __init__(self):
        super(MyRoot, self).__init__()
        #MainMenuSong.play()
    
    def on_touch_move(self, touch):
            True
    
    def on_touch_down(self, touch):
        global gameType
        global SelectedSquare
        global Highlight
        global Turn
        global Music
        global wincon
        if(gameType == 1):
            self.VanillaPancakeEdition(touch)
        elif(gameType == 2):
            self.RoyalJellyVariation(touch)
        elif(gameType == 3):
            self.RoyalPancakeVariation(touch)
        elif(touch.pos[0] > Window.size[0]*12/20 and touch.pos[0] < Window.size[0]*5/6 and touch.pos[1] > Window.size[1]*5/9 and touch.pos[1] < Window.size[1]*13/18):#on first touch (touch to play!)
            GlobalBackgroundWidget.Tutorial1()
            gameType = -1
        elif(gameType == -1):
            GlobalBackgroundWidget.Tutorial2()
            gameType = -2
        elif(gameType == -2):
            GlobalBackgroundWidget.MainMenu()
            gameType = 0
        elif(touch.pos[0] > 0 and touch.pos[0] < Window.size[0]*1/5 and touch.pos[1] > Window.size[1]*5/6 and touch.pos[1] < Window.size[1]):#on first touch (touch to play!)
            if(Music):
                Music = False
                MainMenuSong.stop()
            else:
                Music = True
                MainMenuSong.play()
        elif(touch.pos[0] > Window.size[0]*1/7 and touch.pos[0] < Window.size[0]*4/9 and touch.pos[1] > Window.size[1]*2/3 and touch.pos[1] < Window.size[1]*4/5):#on first touch (touch to play!)
            GlobalBackgroundWidget.VanillaPancakeBackground()
            for child in self.children[:]:
                child.refresh()
            if(Music):
                MainMenuSong.stop()
                VanillaPancakeSong.play()
            gameType = 1
        elif(touch.pos[0] > Window.size[0]*12/20 and touch.pos[0] < Window.size[0]*5/6 and touch.pos[1] > Window.size[1]*5/6 and touch.pos[1] < Window.size[1]*9/10):#on first touch (touch to play!)
            GlobalBackgroundWidget.RoyalJellyBackground()
            for child in self.children[:]:
                if(child.position == [2,0] or child.position == [2,4]):
                    child.royal = True
                    child.texture = Image("RoyalR.jpg").texture
                child.refresh()
            if(Music):
                MainMenuSong.stop()
                RoyalJellySong.play()
            gameType = 2
        elif(touch.pos[0] > Window.size[0]*2/5 and touch.pos[0] < Window.size[0]*3/5 and touch.pos[1] > Window.size[1]*8/9 and touch.pos[1] < Window.size[1]*26/27):#on first touch (touch to play!)
            GlobalBackgroundWidget.RoyalPancakeBackground()
            for child in self.children[:]:
                if(child.position == [1,2] or child.position == [2,2] or child.position == [3,2]):
                    child.royal = True
                    child.texture = Image("RoyalR.jpg").texture
                child.refresh()
            if(Music):
                MainMenuSong.stop()
                RoyalPancakeSong.play()
            gameType = 3
        elif(gameType == 0):
            if(MainMenuSong.state == 'stop' and Music):
                MainMenuSong.play()
    def on_touch_up(self, touch):
        if touch.grab_current is self:
            touch.ungrab(self)
            return True

    def VanillaPancakeEdition(self, touch):
        global gameType
        global SelectedSquare
        global Highlight
        global Turn
        global wincon
        global Music
        global Stacks
        global Undo
        global lastStacks
        myflag = True
        if(math.floor(touch.pos[0]/(GlobalWidth+GlobalSpacing)) == 0 and touch.pos[1] > Window.size[1]-GlobalWidth-GlobalSpacing):#Exit
            gameType = 0
            Stacks = [
                [[],[],[],[],[]],
                [[],[],[],[],[]],
                [[],[],[],[],[]],
                [[],[],[],[],[]],
                [[],[],[],[],[]]]
            wincon = False
            Undo = False
            SelectedSquare = [None,None]
            Highlight = [None, None]
            Turn = 0
            for child in self.children[:]:
                child.reset()
            if(Music):
                VanillaPancakeSong.stop()
                WinSong.stop()
                MainMenuSong.play()

        if(math.floor(touch.pos[0]/(GlobalWidth+GlobalSpacing)) == 4 and touch.pos[1] > Window.size[1]-GlobalWidth-GlobalSpacing and Undo):#Undo
            SelectedSquare = [None,None]
            Highlight = [None, None]
            Turn = (Turn+1)%2
            for i in range(5):
                for j in range(5):
                    Stacks[i][j] = lastStacks[i][j][:]
            for child in self.children[:]:
                if(child.id>=0):
                    child.selected = 0
                    child.position = lastState[child.id][0][:]
                    child.state = lastState[child.id][1]
                    child.color = lastState[child.id][2][:]
                    if(Stacks[child.position[0]][child.position[1]][len(Stacks[child.position[0]][child.position[1]])-1] == child):
                        child.refresh()
                    else:
                        child.clear()
            Undo = False
            GlobalBackgroundWidget.VanillaPancakeBackground()
            for i in range(5):
                for j in range(5):
                    GlobalStackIndicator.board[i][j] = lastState[13][i][j]
            GlobalStackIndicator.refresh()
            
        
        if(math.floor(touch.pos[0]/(GlobalWidth+GlobalSpacing)) == 2 and touch.pos[1] < GlobalWidth+GlobalSpacing):#Stop Music
            if(Music):
                Music = False
                VanillaPancakeSong.stop()
                WinSong.stop()
            else:
                Music = True
                if(wincon):
                    WinSong.play()
                else:
                    VanillaPancakeSong.play()
            GlobalBackgroundWidget.VanillaPancakeBackground()
        if(wincon == False):
            SelectedSquare[0] = math.floor(touch.pos[0]/(GlobalWidth+GlobalSpacing))
            SelectedSquare[1] = math.floor((touch.pos[1]-Window.size[1]/5)/(GlobalWidth+GlobalSpacing))
            if(SelectedSquare[0] < 0 or SelectedSquare[0] > 4):
                SelectedSquare = [None, None]
            if(SelectedSquare[0] != None):
                if(SelectedSquare[1] < 0 or SelectedSquare[1] > 4):
                    SelectedSquare = [None, None]
            Highlight = SelectedSquare[:]
            if(SelectedSquare[0] != None):
                if(Stacks[SelectedSquare[0]][SelectedSquare[1]] == []):
                    Highlight = [None, None]
            GlobalStackIndicator.refresh()
            for child in self.children[:]: #Select Child
                if(SelectedSquare[0] != None):
                    if(SelectedSquare[0] == child.position[0] and SelectedSquare[1] == child.position[1] and Stacks[child.position[0]][child.position[1]][len(Stacks[child.position[0]][child.position[1]])-1] == child):
                        child.selected = 1
                
            for child in self.children[:]:
                if(child.selected==2): #place child
                    if(SelectedSquare[0] != None):
                        if((((((SelectedSquare[0] >= child.position[0]-1 and SelectedSquare[0] <= child.position[0]+1 and SelectedSquare[1] == child.position[1]) or (SelectedSquare[1] >= child.position[1]-1 and SelectedSquare[1] <= child.position[1]+1 and SelectedSquare[0] == child.position[0])) and child.royal == False) or (((SelectedSquare[0] == child.position[0]-1 and SelectedSquare[1] == child.position[1]-1) or (SelectedSquare[0] == child.position[0]-1 and SelectedSquare[1] == child.position[1]+1) or (SelectedSquare[0] == child.position[0]+1 and SelectedSquare[1] == child.position[1]-1) or (SelectedSquare[0] == child.position[0]+1 and SelectedSquare[1] == child.position[1]+1)) and child.royal == True)) and (SelectedSquare[0] >= 0 and SelectedSquare[0] <=4 and SelectedSquare[1] >= 0 and SelectedSquare[1] <= 4))):
                            if(Stacks[child.position[0]][child.position[1]][len(Stacks[child.position[0]][child.position[1]])-1].state == 0):
                                myflag = False
                                Undo = True
                                for i in range(5):
                                    for j in range(5):
                                        lastState[13][i][j] = GlobalStackIndicator.board[i][j]
                                GlobalBackgroundWidget.VanillaPancakeBackground()
                                for i in range(5):
                                    for j in range(5):
                                        lastStacks[i][j] = Stacks[i][j][:]
                                for child2 in self.children[:]:
                                    if(child2.id >=0):
                                        lastState[child2.id][0] = child2.position[:]
                                        lastState[child2.id][1] = child2.state
                                        lastState[child2.id][2] = child2.color[:]
                                for child2 in self.children[:]:
                                    if(child2.player==2 and child2.state>0):#update pancakes
                                        child2.state = child2.state - 1
                                        if(child2.state == 1):
                                            child2.color = [.85,.45,.4,1]
                                        if(child2.state == 0):
                                            child2.color = [.7,.55,0,1]
                                        if(Stacks[child2.position[0]][child2.position[1]][len(Stacks[child2.position[0]][child2.position[1]])-1] == child2):
                                            child2.refresh()
                                if(child.player == 2):
                                    child.state = 2
                                    child.color = [.9,.3,0,1]
                                if(len(Stacks[child.position[0]][child.position[1]])<=2):#Take away brown highlight
                                    GlobalStackIndicator.remove(xpos=child.position[0],ypos=child.position[1])
                                Stacks[child.position[0]][child.position[1]].pop()#Remove from stack
                                if(Stacks[child.position[0]][child.position[1]] != []):#Display top jelly of old stack
                                    Stacks[child.position[0]][child.position[1]][len(Stacks[child.position[0]][child.position[1]])-1].refresh()
                                for child2 in self.children[:]:#removes all children underneath
                                    if(SelectedSquare[0] == child2.position[0] and SelectedSquare[1] == child2.position[1]):
                                        child2.x = -GlobalWidth
                                        child2.clear()
                                        GlobalStackIndicator.add(xpos=SelectedSquare[0],ypos=SelectedSquare[1])
                                    child2.selected = 0
                                child.position[0] = SelectedSquare[0]
                                child.position[1] = SelectedSquare[1]
                                SelectedSquare = [None, None]
                                Stacks[child.position[0]][child.position[1]].append(child)
                                GlobalStackIndicator.refresh()
                                child.refresh()
                                Turn = (Turn + 1)%2
                    child.selected = 0
            for child in self.children[:]:
                if(child.selected == 1):
                    if(SelectedSquare[0] != None):
                        if(myflag and Stacks[SelectedSquare[0]][SelectedSquare[1]] != []):
                            if((Stacks[SelectedSquare[0]][SelectedSquare[1]][len(Stacks[SelectedSquare[0]][SelectedSquare[1]])-1].player == Turn or Stacks[SelectedSquare[0]][SelectedSquare[1]][len(Stacks[SelectedSquare[0]][SelectedSquare[1]])-1].player == 2)):
                                child.selected = 2
                            else:
                                child.selected = 0
                                GlobalStackIndicator.refresh()
                        else:
                            Highlight = [None, None]
                            SelectedSquare = [None, None]
                            GlobalStackIndicator.refresh()
                            child.selected = 0
                    else:
                        child.selected = 0
            if(SelectedSquare[0] != None):
                if(Stacks[SelectedSquare[0]][SelectedSquare[1]] != []):
                    if((Stacks[SelectedSquare[0]][SelectedSquare[1]][len(Stacks[SelectedSquare[0]][SelectedSquare[1]])-1].player != Turn and Stacks[SelectedSquare[0]][SelectedSquare[1]][len(Stacks[SelectedSquare[0]][SelectedSquare[1]])-1].player != 2)):
                        SelectedSquare = [None, None]
                        GlobalStackIndicator.refresh()
            if(checkwin() != -1):
                if(checkwin() == 0):
                    wincon = True
                    Undo = False
                    GlobalStackIndicator.win(0)
                else:
                    wincon = True
                    GlobalStackIndicator.win(1)
                                
                        
            if touch.is_double_tap:
                True
            if touch.is_triple_tap:
                True
            if self.collide_point(*touch.pos):
                touch.grab(self)
    
    def RoyalJellyVariation(self, touch):
        global gameType
        global SelectedSquare
        global Highlight
        global Turn
        global wincon
        global Music
        global Stacks
        global Undo
        global lastStacks
        myflag = True
        if(math.floor(touch.pos[0]/(GlobalWidth+GlobalSpacing)) == 0 and touch.pos[1] > Window.size[1]-GlobalWidth-GlobalSpacing):#Exit
            gameType = 0
            Stacks = [
                [[],[],[],[],[]],
                [[],[],[],[],[]],
                [[],[],[],[],[]],
                [[],[],[],[],[]],
                [[],[],[],[],[]]]
            wincon = False
            Undo = False
            SelectedSquare = [None,None]
            Highlight = [None, None]
            Turn = 0
            for child in self.children[:]:
                child.reset()
            if(Music):
                RoyalJellySong.stop()
                WinSong.stop()
                MainMenuSong.play()
            
        if(math.floor(touch.pos[0]/(GlobalWidth+GlobalSpacing)) == 4 and touch.pos[1] > Window.size[1]-GlobalWidth-GlobalSpacing and Undo):#Undo
            SelectedSquare = [None,None]
            Highlight = [None, None]
            Turn = (Turn+1)%2
            for i in range(5):
                for j in range(5):
                    Stacks[i][j] = lastStacks[i][j][:]
            for child in self.children[:]:
                if(child.id>=0):
                    child.selected = 0
                    child.position = lastState[child.id][0][:]
                    child.state = lastState[child.id][1]
                    child.color = lastState[child.id][2][:]
                    if(Stacks[child.position[0]][child.position[1]][len(Stacks[child.position[0]][child.position[1]])-1] == child):
                        child.refresh()
                    else:
                        child.clear()
            Undo = False
            GlobalBackgroundWidget.RoyalJellyBackground()
            for i in range(5):
                for j in range(5):
                    GlobalStackIndicator.board[i][j] = lastState[13][i][j]
            GlobalStackIndicator.refresh()
        
        if(math.floor(touch.pos[0]/(GlobalWidth+GlobalSpacing)) == 2 and touch.pos[1] < GlobalWidth+GlobalSpacing):
            if(Music):
                Music = False
                RoyalJellySong.stop()
                WinSong.stop()
            else:
                Music = True
                if(wincon):
                    WinSong.play()
                else:
                    RoyalJellySong.play()

            GlobalBackgroundWidget.RoyalJellyBackground()
        if(wincon == False):
            SelectedSquare[0] = math.floor(touch.pos[0]/(GlobalWidth+GlobalSpacing))
            SelectedSquare[1] = math.floor((touch.pos[1]-Window.size[1]/5)/(GlobalWidth+GlobalSpacing))
            if(SelectedSquare[0] < 0 or SelectedSquare[0] > 4):
                SelectedSquare = [None, None]
            if(SelectedSquare[0] != None):
                if(SelectedSquare[1] < 0 or SelectedSquare[1] > 4):
                    SelectedSquare = [None, None]
            Highlight = SelectedSquare[:]
            if(SelectedSquare[0] != None):
                if(Stacks[SelectedSquare[0]][SelectedSquare[1]] == []):
                    Highlight = [None, None]
            GlobalStackIndicator.refresh()
            for child in self.children[:]: #Select Child
                if(SelectedSquare[0] != None):
                    if(SelectedSquare[0] == child.position[0] and SelectedSquare[1] == child.position[1] and Stacks[child.position[0]][child.position[1]][len(Stacks[child.position[0]][child.position[1]])-1] == child):
                        child.selected = 1
                
            for child in self.children[:]:
                if(child.selected==2): #place child
                    if(SelectedSquare[0] != None):
                        if((((((SelectedSquare[0] >= child.position[0]-1 and SelectedSquare[0] <= child.position[0]+1 and SelectedSquare[1] == child.position[1]) or (SelectedSquare[1] >= child.position[1]-1 and SelectedSquare[1] <= child.position[1]+1 and SelectedSquare[0] == child.position[0])) and child.royal == False) or (((SelectedSquare[0] == child.position[0]-1 and SelectedSquare[1] == child.position[1]-1) or (SelectedSquare[0] == child.position[0]-1 and SelectedSquare[1] == child.position[1]+1) or (SelectedSquare[0] == child.position[0]+1 and SelectedSquare[1] == child.position[1]-1) or (SelectedSquare[0] == child.position[0]+1 and SelectedSquare[1] == child.position[1]+1)) and child.royal == True)) and (SelectedSquare[0] >= 0 and SelectedSquare[0] <=4 and SelectedSquare[1] >= 0 and SelectedSquare[1] <= 4))):
                            if(Stacks[child.position[0]][child.position[1]][len(Stacks[child.position[0]][child.position[1]])-1].state == 0):
                                myflag = False
                                Undo = True
                                for i in range(5):
                                    for j in range(5):
                                        lastState[13][i][j] = GlobalStackIndicator.board[i][j]
                                GlobalBackgroundWidget.RoyalJellyBackground()
                                for i in range(5):
                                    for j in range(5):
                                        lastStacks[i][j] = Stacks[i][j][:]
                                for child2 in self.children[:]:
                                    if(child2.id >=0):
                                        lastState[child2.id][0] = child2.position[:]
                                        lastState[child2.id][1] = child2.state
                                        lastState[child2.id][2] = child2.color[:]
                                for child2 in self.children[:]:
                                    if(child2.player==2 and child2.state>0):#update pancakes
                                        child2.state = child2.state - 1
                                        if(child2.state == 1):
                                            child2.color = [.85,.45,.4,1]
                                        if(child2.state == 0):
                                            child2.color = [.7,.55,0,1]
                                        if(Stacks[child2.position[0]][child2.position[1]][len(Stacks[child2.position[0]][child2.position[1]])-1] == child2):
                                            child2.refresh()
                                if(child.player == 2):
                                    child.state = 2
                                    child.color = [.9,.3,0,1]
                                if(len(Stacks[child.position[0]][child.position[1]])<=2):#Take away brown highlight
                                    GlobalStackIndicator.remove(xpos=child.position[0],ypos=child.position[1])
                                Stacks[child.position[0]][child.position[1]].pop()#Remove from stack
                                if(Stacks[child.position[0]][child.position[1]] != []):#Display top jelly of old stack
                                    Stacks[child.position[0]][child.position[1]][len(Stacks[child.position[0]][child.position[1]])-1].refresh()
                                for child2 in self.children[:]:#removes all children underneath
                                    if(SelectedSquare[0] == child2.position[0] and SelectedSquare[1] == child2.position[1]):
                                        child2.x = -GlobalWidth
                                        child2.clear()
                                        GlobalStackIndicator.add(xpos=SelectedSquare[0],ypos=SelectedSquare[1])
                                    child2.selected = 0
                                child.position[0] = SelectedSquare[0]
                                child.position[1] = SelectedSquare[1]
                                SelectedSquare = [None, None]
                                Stacks[child.position[0]][child.position[1]].append(child)
                                GlobalStackIndicator.refresh()
                                child.refresh()
                                Turn = (Turn + 1)%2
                    child.selected = 0
            for child in self.children[:]:
                if(child.selected == 1):
                    if(SelectedSquare[0] != None):
                        if(myflag and Stacks[SelectedSquare[0]][SelectedSquare[1]] != []):
                            if((Stacks[SelectedSquare[0]][SelectedSquare[1]][len(Stacks[SelectedSquare[0]][SelectedSquare[1]])-1].player == Turn or Stacks[SelectedSquare[0]][SelectedSquare[1]][len(Stacks[SelectedSquare[0]][SelectedSquare[1]])-1].player == 2)):
                                child.selected = 2
                            else:
                                child.selected = 0
                                GlobalStackIndicator.refresh()
                        else:
                            Highlight = [None, None]
                            SelectedSquare = [None, None]
                            GlobalStackIndicator.refresh()
                            child.selected = 0
                    else:
                        child.selected = 0
            if(SelectedSquare[0] != None):
                if(Stacks[SelectedSquare[0]][SelectedSquare[1]] != []):
                    if((Stacks[SelectedSquare[0]][SelectedSquare[1]][len(Stacks[SelectedSquare[0]][SelectedSquare[1]])-1].player != Turn and Stacks[SelectedSquare[0]][SelectedSquare[1]][len(Stacks[SelectedSquare[0]][SelectedSquare[1]])-1].player != 2)):
                        SelectedSquare = [None, None]
                        GlobalStackIndicator.refresh()
            if(checkwin() != -1):
                if(checkwin() == 0):
                    wincon = True
                    Undo = False
                    GlobalStackIndicator.win(0)
                else:
                    wincon = True
                    GlobalStackIndicator.win(1)

    def RoyalPancakeVariation(self, touch):
        global gameType
        global SelectedSquare
        global Highlight
        global Turn
        global wincon
        global Music
        global Stacks
        global Undo
        global lastStacks
        myflag = True
        if(math.floor(touch.pos[0]/(GlobalWidth+GlobalSpacing)) == 0 and touch.pos[1] > Window.size[1]-GlobalWidth-GlobalSpacing):#Exit
            gameType = 0
            Stacks = [
                [[],[],[],[],[]],
                [[],[],[],[],[]],
                [[],[],[],[],[]],
                [[],[],[],[],[]],
                [[],[],[],[],[]]]
            wincon = False
            Undo = False
            SelectedSquare = [None,None]
            Highlight = [None, None]
            Turn = 0
            for child in self.children[:]:
                child.reset()
            if(Music):
                RoyalPancakeSong.stop()
                WinSong.stop()
                MainMenuSong.play()

        if(math.floor(touch.pos[0]/(GlobalWidth+GlobalSpacing)) == 4 and touch.pos[1] > Window.size[1]-GlobalWidth-GlobalSpacing and Undo):#Undo
            SelectedSquare = [None,None]
            Highlight = [None, None]
            Turn = (Turn+1)%2
            for i in range(5):
                for j in range(5):
                    Stacks[i][j] = lastStacks[i][j][:]
            for child in self.children[:]:
                if(child.id>=0):
                    child.selected = 0
                    child.position = lastState[child.id][0][:]
                    child.state = lastState[child.id][1]
                    child.color = lastState[child.id][2][:]
                    if(Stacks[child.position[0]][child.position[1]][len(Stacks[child.position[0]][child.position[1]])-1] == child):
                        child.refresh()
                    else:
                        child.clear()
            Undo = False
            GlobalBackgroundWidget.RoyalPancakeBackground()
            for i in range(5):
                for j in range(5):
                    GlobalStackIndicator.board[i][j] = lastState[13][i][j]
            GlobalStackIndicator.refresh()
        
        if(math.floor(touch.pos[0]/(GlobalWidth+GlobalSpacing)) == 2 and touch.pos[1] < GlobalWidth+GlobalSpacing):
            if(Music):
                Music = False
                RoyalPancakeSong.stop()
                WinSong.stop()
            else:
                Music = True
                if(wincon):
                    WinSong.play()
                else:
                    RoyalPancakeSong.play()

            GlobalBackgroundWidget.RoyalPancakeBackground()
        if(wincon == False):
            SelectedSquare[0] = math.floor(touch.pos[0]/(GlobalWidth+GlobalSpacing))
            SelectedSquare[1] = math.floor((touch.pos[1]-Window.size[1]/5)/(GlobalWidth+GlobalSpacing))
            if(SelectedSquare[0] < 0 or SelectedSquare[0] > 4):
                SelectedSquare = [None, None]
            if(SelectedSquare[0] != None):
                if(SelectedSquare[1] < 0 or SelectedSquare[1] > 4):
                    SelectedSquare = [None, None]
            Highlight = SelectedSquare[:]
            if(SelectedSquare[0] != None):
                if(Stacks[SelectedSquare[0]][SelectedSquare[1]] == []):
                    Highlight = [None, None]
            GlobalStackIndicator.refresh()
            for child in self.children[:]: #Select Child
                if(SelectedSquare[0] != None):
                    if(SelectedSquare[0] == child.position[0] and SelectedSquare[1] == child.position[1] and Stacks[child.position[0]][child.position[1]][len(Stacks[child.position[0]][child.position[1]])-1] == child):
                        child.selected = 1
                
            for child in self.children[:]:
                if(child.selected==2): #place child
                    if(SelectedSquare[0] != None):
                        if((((((SelectedSquare[0] >= child.position[0]-1 and SelectedSquare[0] <= child.position[0]+1 and SelectedSquare[1] == child.position[1]) or (SelectedSquare[1] >= child.position[1]-1 and SelectedSquare[1] <= child.position[1]+1 and SelectedSquare[0] == child.position[0])) and child.royal == False) or (((SelectedSquare[0] == child.position[0]-1 and SelectedSquare[1] == child.position[1]-1) or (SelectedSquare[0] == child.position[0]-1 and SelectedSquare[1] == child.position[1]+1) or (SelectedSquare[0] == child.position[0]+1 and SelectedSquare[1] == child.position[1]-1) or (SelectedSquare[0] == child.position[0]+1 and SelectedSquare[1] == child.position[1]+1)) and child.royal == True)) and (SelectedSquare[0] >= 0 and SelectedSquare[0] <=4 and SelectedSquare[1] >= 0 and SelectedSquare[1] <= 4))):
                            if(Stacks[child.position[0]][child.position[1]][len(Stacks[child.position[0]][child.position[1]])-1].state == 0):
                                myflag = False
                                Undo = True
                                for i in range(5):
                                    for j in range(5):
                                        lastState[13][i][j] = GlobalStackIndicator.board[i][j]
                                GlobalBackgroundWidget.RoyalPancakeBackground()
                                for i in range(5):
                                    for j in range(5):
                                        lastStacks[i][j] = Stacks[i][j][:]
                                for child2 in self.children[:]:
                                    if(child2.id >=0):
                                        lastState[child2.id][0] = child2.position[:]
                                        lastState[child2.id][1] = child2.state
                                        lastState[child2.id][2] = child2.color[:]
                                for child2 in self.children[:]:
                                    if(child2.player==2 and child2.state>0):#update pancakes
                                        child2.state = child2.state - 1
                                        if(child2.state == 1):
                                            child2.color = [.85,.45,.4,1]
                                        if(child2.state == 0):
                                            child2.color = [.7,.55,0,1]
                                        if(Stacks[child2.position[0]][child2.position[1]][len(Stacks[child2.position[0]][child2.position[1]])-1] == child2):
                                            child2.refresh()
                                if(child.player == 2):
                                    child.state = 2
                                    child.color = [.9,.3,0,1]
                                if(len(Stacks[child.position[0]][child.position[1]])<=2):#Take away brown highlight
                                    GlobalStackIndicator.remove(xpos=child.position[0],ypos=child.position[1])
                                Stacks[child.position[0]][child.position[1]].pop()#Remove from stack
                                if(Stacks[child.position[0]][child.position[1]] != []):#Display top jelly of old stack
                                    Stacks[child.position[0]][child.position[1]][len(Stacks[child.position[0]][child.position[1]])-1].refresh()
                                for child2 in self.children[:]:#removes all children underneath
                                    if(SelectedSquare[0] == child2.position[0] and SelectedSquare[1] == child2.position[1]):
                                        child2.x = -GlobalWidth
                                        child2.clear()
                                        GlobalStackIndicator.add(xpos=SelectedSquare[0],ypos=SelectedSquare[1])
                                    child2.selected = 0
                                child.position[0] = SelectedSquare[0]
                                child.position[1] = SelectedSquare[1]
                                SelectedSquare = [None, None]
                                Stacks[child.position[0]][child.position[1]].append(child)
                                GlobalStackIndicator.refresh()
                                child.refresh()
                                Turn = (Turn + 1)%2
                    child.selected = 0
            for child in self.children[:]:
                if(child.selected == 1):
                    if(SelectedSquare[0] != None):
                        if(myflag and Stacks[SelectedSquare[0]][SelectedSquare[1]] != []):
                            if((Stacks[SelectedSquare[0]][SelectedSquare[1]][len(Stacks[SelectedSquare[0]][SelectedSquare[1]])-1].player == Turn or Stacks[SelectedSquare[0]][SelectedSquare[1]][len(Stacks[SelectedSquare[0]][SelectedSquare[1]])-1].player == 2)):
                                child.selected = 2
                            else:
                                child.selected = 0
                                GlobalStackIndicator.refresh()
                        else:
                            Highlight = [None, None]
                            SelectedSquare = [None, None]
                            GlobalStackIndicator.refresh()
                            child.selected = 0
                    else:
                        child.selected = 0
            if(SelectedSquare[0] != None):
                if(Stacks[SelectedSquare[0]][SelectedSquare[1]] != []):
                    if((Stacks[SelectedSquare[0]][SelectedSquare[1]][len(Stacks[SelectedSquare[0]][SelectedSquare[1]])-1].player != Turn and Stacks[SelectedSquare[0]][SelectedSquare[1]][len(Stacks[SelectedSquare[0]][SelectedSquare[1]])-1].player != 2)):
                        SelectedSquare = [None, None]
                        GlobalStackIndicator.refresh()
            if(checkwin() != -1):
                if(checkwin() == 0):
                    wincon = True
                    Undo = False
                    GlobalStackIndicator.win(0)
                else:
                    wincon = True
                    GlobalStackIndicator.win(1)
                                                    
            if touch.is_double_tap:
                True
            if touch.is_triple_tap:
                True
            if self.collide_point(*touch.pos):
                touch.grab(self)
    
  
class Jelly(Widget):
    def __init__(self, position = [0,0], color = [1,0,0,1], texture = None, player = 2, id = -1):
        self.startingPosition = position[:]
        self.position = position
        Stacks[self.position[0]][self.position[1]].append(self)
        self.x = self.position[0]*(GlobalWidth+GlobalSpacing)+GlobalSpacing
        self.y = self.position[1]*(GlobalWidth+GlobalSpacing)+GlobalSpacing+Window.size[1]/5
        self.Width = GlobalWidth
        self.Height = GlobalWidth
        self.startingColor = color
        self.color = color
        self.player = player
        self.state = 0
        self.royal = False
        self.id = id
        if(texture != None):
            self.texture = Image(texture).texture
        else:
            self.texture = None
        self.selected = 0
        super(Jelly, self).__init__()
        
    def refresh(self):
        self.canvas.clear()
        self.x = self.position[0]*(GlobalWidth+GlobalSpacing)+GlobalSpacing
        self.y = self.position[1]*(GlobalWidth+GlobalSpacing)+GlobalSpacing+Window.size[1]/5
        with self.canvas:
            if(self.state == 0):
                Color(self.color[0],self.color[1],self.color[2],self.color[3])
                RoundedRectangle(texture = self.texture, pos=(self.x,self.y), size=(self.Width, self.Height), radius=[(30,30),(30,30),(30,30),(30,30)])
            elif(self.state == 1):#for pancake state == 1
                Color(.85,.45,.4,1)
                RoundedRectangle(texture = self.texture, pos=(self.x,self.y), size=(self.Width, self.Height), radius=[(30,30),(30,30),(30,30),(30,30)])
            elif(self.state == 2):#for pancake state == 2
                Color(.9,.3,0,1)
                RoundedRectangle(texture = self.texture, pos=(self.x,self.y), size=(self.Width, self.Height), radius=[(30,30),(30,30),(30,30),(30,30)])
            
    def reset(self):
        self.position = self.startingPosition[:]
        Stacks[self.position[0]][self.position[1]].append(self)
        self.x = self.position[0]*(GlobalWidth+GlobalSpacing)+GlobalSpacing
        self.y = self.position[1]*(GlobalWidth+GlobalSpacing)+GlobalSpacing+Window.size[1]/5
        self.color = self.startingColor
        self.state = 0
        self.royal = False
        self.texture = None
        self.selected = 0
        self.refresh()
        self.canvas.clear()
        
    def clear(self):
        self.canvas.clear()

class StackIndicator(Widget):
    def __init__(self, texture=None):
        self.x = 0
        self.y = 0
        self.Width = 0
        self.Height = 0
        self.player = 3
        self.id = -3
        self.position = [-1,-1]
        global GlobalStackIndicator
        GlobalStackIndicator = self
        self.board = [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]]
        self.color = [0,0,0,0]
        if(texture != None):
            self.texture = Image(texture).texture
        else:
            self.texture = None
        self.selected = 0
        super(StackIndicator, self).__init__()

    def add(self, xpos=0, ypos=0):
        self.board[xpos][ypos]=1
        
    def remove(self, xpos=0, ypos=0):
        self.board[xpos][ypos]=0

    def refresh(self):
        self.canvas.clear()
        with self.canvas:
            for i in range(len(self.board)):
                for j in range(len(self.board[0])):
                    if(self.board[i][j]==1):
                        Color(.6,.45,0,1)
                        Rectangle(texture=self.texture, pos=((GlobalWidth+GlobalSpacing)*i+GlobalSpacing/2,(GlobalWidth+GlobalSpacing)*j+GlobalSpacing/2+Window.size[1]/5), size=(GlobalWidth+GlobalSpacing, GlobalWidth+GlobalSpacing))
            if(Highlight[0] != None):
                Color(.8,.8,.8,1)
                Rectangle(texture=self.texture, pos=((GlobalWidth+GlobalSpacing)*Highlight[0]+GlobalSpacing/2,(GlobalWidth+GlobalSpacing)*Highlight[1]+GlobalSpacing/2+Window.size[1]/5), size=(GlobalWidth+GlobalSpacing, GlobalWidth+GlobalSpacing))
            if(SelectedSquare[0] != None):
                if(Stacks[SelectedSquare[0]][SelectedSquare[1]] != []):
                    if(Stacks[SelectedSquare[0]][SelectedSquare[1]][len(Stacks[SelectedSquare[0]][SelectedSquare[1]])-1].state == 0):
                        Color(.5,.5,1,1)
                        Rectangle(texture=self.texture, pos=((GlobalWidth+GlobalSpacing)*SelectedSquare[0]+GlobalSpacing/2,(GlobalWidth+GlobalSpacing)*SelectedSquare[1]+GlobalSpacing/2+Window.size[1]/5), size=(GlobalWidth+GlobalSpacing, GlobalWidth+GlobalSpacing))
                        Color(.5,.8,.5,1)
                        if(Stacks[SelectedSquare[0]][SelectedSquare[1]][len(Stacks[SelectedSquare[0]][SelectedSquare[1]])-1].royal):
                            if(SelectedSquare[0] > 0):
                                if(SelectedSquare[1] > 0):
                                    Rectangle(texture=self.texture, pos=((GlobalWidth+GlobalSpacing)*(SelectedSquare[0]-1)+GlobalSpacing/2,(GlobalWidth+GlobalSpacing)*(SelectedSquare[1]-1)+GlobalSpacing/2+Window.size[1]/5), size=(GlobalWidth+GlobalSpacing, GlobalWidth+GlobalSpacing))
                                if(SelectedSquare[1] < 4):
                                    Rectangle(texture=self.texture, pos=((GlobalWidth+GlobalSpacing)*(SelectedSquare[0]-1)+GlobalSpacing/2,(GlobalWidth+GlobalSpacing)*(SelectedSquare[1]+1)+GlobalSpacing/2+Window.size[1]/5), size=(GlobalWidth+GlobalSpacing, GlobalWidth+GlobalSpacing))
                            if(SelectedSquare[0] < 4):
                                if(SelectedSquare[1] > 0):
                                    Rectangle(texture=self.texture, pos=((GlobalWidth+GlobalSpacing)*(SelectedSquare[0]+1)+GlobalSpacing/2,(GlobalWidth+GlobalSpacing)*(SelectedSquare[1]-1)+GlobalSpacing/2+Window.size[1]/5), size=(GlobalWidth+GlobalSpacing, GlobalWidth+GlobalSpacing))
                                if(SelectedSquare[1] < 4):
                                    Rectangle(texture=self.texture, pos=((GlobalWidth+GlobalSpacing)*(SelectedSquare[0]+1)+GlobalSpacing/2,(GlobalWidth+GlobalSpacing)*(SelectedSquare[1]+1)+GlobalSpacing/2+Window.size[1]/5), size=(GlobalWidth+GlobalSpacing, GlobalWidth+GlobalSpacing))
                        else:
                            if(SelectedSquare[0] > 0):
                                Rectangle(texture=self.texture, pos=((GlobalWidth+GlobalSpacing)*(SelectedSquare[0]-1)+GlobalSpacing/2,(GlobalWidth+GlobalSpacing)*SelectedSquare[1]+GlobalSpacing/2+Window.size[1]/5), size=(GlobalWidth+GlobalSpacing, GlobalWidth+GlobalSpacing))
                            if(SelectedSquare[0] < 4):
                                Rectangle(texture=self.texture, pos=((GlobalWidth+GlobalSpacing)*(SelectedSquare[0]+1)+GlobalSpacing/2,(GlobalWidth+GlobalSpacing)*SelectedSquare[1]+GlobalSpacing/2+Window.size[1]/5), size=(GlobalWidth+GlobalSpacing, GlobalWidth+GlobalSpacing))
                            if(SelectedSquare[1] > 0):
                                Rectangle(texture=self.texture, pos=((GlobalWidth+GlobalSpacing)*SelectedSquare[0]+GlobalSpacing/2,(GlobalWidth+GlobalSpacing)*(SelectedSquare[1]-1)+GlobalSpacing/2+Window.size[1]/5), size=(GlobalWidth+GlobalSpacing, GlobalWidth+GlobalSpacing))
                            if(SelectedSquare[1] < 4):
                                Rectangle(texture=self.texture, pos=((GlobalWidth+GlobalSpacing)*SelectedSquare[0]+GlobalSpacing/2,(GlobalWidth+GlobalSpacing)*(SelectedSquare[1]+1)+GlobalSpacing/2+Window.size[1]/5), size=(GlobalWidth+GlobalSpacing, GlobalWidth+GlobalSpacing))
            if(Highlight[0] != None):
                localpos = 0
                Color(.7,.7,1,1)#gray background
                Rectangle(texture=None, pos=(GlobalSpacing/2,(GlobalWidth+GlobalSpacing)*5+GlobalSpacing/2+Window.size[1]/5), size=(Window.size[0]-GlobalSpacing, (GlobalWidth+GlobalSpacing*2)))    
                for jar in Stacks[Highlight[0]][Highlight[1]]:
                    Color(jar.color[0], jar.color[1], jar.color[2], jar.color[3])#show stack
                    Rectangle(texture=jar.texture, pos=((GlobalWidth+GlobalSpacing)/2*localpos+GlobalSpacing,(GlobalWidth+GlobalSpacing)*5+GlobalSpacing+Window.size[1]/5), size=((GlobalWidth+GlobalSpacing)/2, (GlobalWidth+GlobalSpacing)))
                    Color(0,0,0,1)
                    Line(points=((GlobalWidth+GlobalSpacing)/2*localpos+GlobalSpacing,(GlobalWidth+GlobalSpacing)*5+GlobalSpacing+Window.size[1]/5, (GlobalWidth+GlobalSpacing)/2*localpos+(GlobalWidth+GlobalSpacing)/2+GlobalSpacing,(GlobalWidth+GlobalSpacing)*5+GlobalSpacing+Window.size[1]/5,  (GlobalWidth+GlobalSpacing)/2*localpos+(GlobalWidth+GlobalSpacing)/2+GlobalSpacing,(GlobalWidth+GlobalSpacing)*6+GlobalSpacing+Window.size[1]/5, (GlobalWidth+GlobalSpacing)/2*localpos+GlobalSpacing,(GlobalWidth+GlobalSpacing)*6+GlobalSpacing+Window.size[1]/5, (GlobalWidth+GlobalSpacing)/2*localpos+GlobalSpacing,(GlobalWidth+GlobalSpacing)*5+GlobalSpacing+Window.size[1]/5))
                    localpos += 1

    def win(self, winner):
        global Music
        if(Music):
            RoyalJellySong.stop()
            VanillaPancakeSong.stop()
            RoyalPancakeSong.stop()
            WinSong.play()
        with self.canvas:
            if(winner == 0):
                self.canvas.clear()
                Color(0,.8,0,1)
                Rectangle(texture=self.texture, pos=(0,Window.size[1]/5), size=((GlobalWidth+GlobalSpacing)*5+GlobalSpacing/2, (GlobalWidth+GlobalSpacing)*2+GlobalSpacing/2))
                Color(.8,0,0,1)
                Rectangle(texture=self.texture, pos=(0,(GlobalWidth+GlobalSpacing)*3+GlobalSpacing/2+Window.size[1]/5), size=((GlobalWidth+GlobalSpacing)*5+GlobalSpacing/2, (GlobalWidth+GlobalSpacing)*2+GlobalSpacing/2))
            if(winner == 1):
                self.canvas.clear()
                Color(.8,0,0,1)
                Rectangle(texture=self.texture, pos=(0,Window.size[1]/5), size=((GlobalWidth+GlobalSpacing)*5+GlobalSpacing/2, (GlobalWidth+GlobalSpacing)*2+GlobalSpacing/2))
                Color(0,.8,0,1)
                Rectangle(texture=self.texture, pos=(0,(GlobalWidth+GlobalSpacing)*3+GlobalSpacing/2+Window.size[1]/5), size=((GlobalWidth+GlobalSpacing)*5+GlobalSpacing/2, (GlobalWidth+GlobalSpacing)*2+GlobalSpacing/2))
            Color(0, 0, 0,1)
            Line(points=(GlobalSpacing/2, GlobalSpacing/2+Window.size[1]/5, GlobalSpacing/2, (GlobalWidth+GlobalSpacing)*5+GlobalSpacing/2+Window.size[1]/5))
            Line(points=((GlobalWidth+GlobalSpacing)+GlobalSpacing/2, GlobalSpacing/2+Window.size[1]/5, (GlobalWidth+GlobalSpacing)+GlobalSpacing/2, (GlobalWidth+GlobalSpacing)*5+GlobalSpacing/2+Window.size[1]/5))
            Line(points=((GlobalWidth+GlobalSpacing)*2+GlobalSpacing/2, GlobalSpacing/2+Window.size[1]/5, (GlobalWidth+GlobalSpacing)*2+GlobalSpacing/2, (GlobalWidth+GlobalSpacing)*5+GlobalSpacing/2+Window.size[1]/5))
            Line(points=((GlobalWidth+GlobalSpacing)*3+GlobalSpacing/2, GlobalSpacing/2+Window.size[1]/5, (GlobalWidth+GlobalSpacing)*3+GlobalSpacing/2, (GlobalWidth+GlobalSpacing)*5+GlobalSpacing/2+Window.size[1]/5))
            Line(points=((GlobalWidth+GlobalSpacing)*4+GlobalSpacing/2, GlobalSpacing/2+Window.size[1]/5, (GlobalWidth+GlobalSpacing)*4+GlobalSpacing/2, (GlobalWidth+GlobalSpacing)*5+GlobalSpacing/2+Window.size[1]/5))
            Line(points=((GlobalWidth+GlobalSpacing)*5+GlobalSpacing/2, GlobalSpacing/2+Window.size[1]/5, (GlobalWidth+GlobalSpacing)*5+GlobalSpacing/2, (GlobalWidth+GlobalSpacing)*5+GlobalSpacing/2+Window.size[1]/5))
            
            Line(points=(GlobalSpacing/2, GlobalSpacing/2+Window.size[1]/5, (GlobalWidth+GlobalSpacing)*5+GlobalSpacing/2, GlobalSpacing/2+Window.size[1]/5))
            Line(points=(GlobalSpacing/2, (GlobalWidth+GlobalSpacing)+GlobalSpacing/2+Window.size[1]/5, (GlobalWidth+GlobalSpacing)*5+GlobalSpacing/2, (GlobalWidth+GlobalSpacing)+GlobalSpacing/2+Window.size[1]/5))
            Line(points=(GlobalSpacing/2, (GlobalWidth+GlobalSpacing)*2+GlobalSpacing/2+Window.size[1]/5, (GlobalWidth+GlobalSpacing)*5+GlobalSpacing/2, (GlobalWidth+GlobalSpacing)*2+GlobalSpacing/2+Window.size[1]/5))
            Line(points=(GlobalSpacing/2, (GlobalWidth+GlobalSpacing)*3+GlobalSpacing/2+Window.size[1]/5, (GlobalWidth+GlobalSpacing)*5+GlobalSpacing/2, (GlobalWidth+GlobalSpacing)*3+GlobalSpacing/2+Window.size[1]/5))
            Line(points=(GlobalSpacing/2, (GlobalWidth+GlobalSpacing)*4+GlobalSpacing/2+Window.size[1]/5, (GlobalWidth+GlobalSpacing)*5+GlobalSpacing/2, (GlobalWidth+GlobalSpacing)*4+GlobalSpacing/2+Window.size[1]/5))
            Line(points=(GlobalSpacing/2, (GlobalWidth+GlobalSpacing)*5+GlobalSpacing/2+Window.size[1]/5, (GlobalWidth+GlobalSpacing)*5+GlobalSpacing, (GlobalWidth+GlobalSpacing)*5+GlobalSpacing/2+Window.size[1]/5))
                
    def reset(self):
        self.canvas.clear()
        self.board = [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]]
        self.color = [0,0,0,0]
        self.selected = 0

class BackgroundWidget(Widget):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.Width = 0
        self.Height = 0
        self.player = 3
        self.color = [0,0,0,0]
        self.texture = None
        self.position = [-1, -1]
        self.selected = 0
        self.id = -2
        global GlobalBackgroundWidget
        GlobalBackgroundWidget = self
        super(BackgroundWidget, self).__init__()
        self.MainMenu()
        
    def MainMenu(self):
        self.canvas.clear()
        with self.canvas:
            Color(1,1,1,1)
            Rectangle(texture=Image("TitleScreen.png").texture, pos=(0,0), size=(Window.size[0], Window.size[1]))

    def Tutorial1(self):
        self.canvas.clear()
        with self.canvas:
            Color(1,1,1,1)
            Rectangle(texture=Image("Tutorial1.png").texture, pos=(0,0), size=(Window.size[0], Window.size[1]))
    
    def Tutorial2(self):
        self.canvas.clear()
        with self.canvas:
            Color(1,1,1,1)
            Rectangle(texture=Image("Tutorial2.png").texture, pos=(0,0), size=(Window.size[0], Window.size[1]))

    def VanillaPancakeBackground(self):
        global Music
        global Undo
        self.canvas.clear()
        with self.canvas:
            Color(0, .6, 0, 1)
            Rectangle(pos=(0,0), size=(Window.size[0],Window.size[1]))
            Color(1, 1, .8, 1)
            Rectangle(pos=(GlobalSpacing/2,GlobalSpacing/2+Window.size[1]/5), size=(Window.size[0]-GlobalSpacing,(GlobalWidth+GlobalSpacing)*5))
            Color(0, 0, 0, 1) 
            Line(points=(GlobalSpacing/2, GlobalSpacing/2+Window.size[1]/5, GlobalSpacing/2, (GlobalWidth+GlobalSpacing)*5+GlobalSpacing/2+Window.size[1]/5))
            Line(points=((GlobalWidth+GlobalSpacing)+GlobalSpacing/2, GlobalSpacing/2+Window.size[1]/5, (GlobalWidth+GlobalSpacing)+GlobalSpacing/2, (GlobalWidth+GlobalSpacing)*5+GlobalSpacing/2+Window.size[1]/5))
            Line(points=((GlobalWidth+GlobalSpacing)*2+GlobalSpacing/2, GlobalSpacing/2+Window.size[1]/5, (GlobalWidth+GlobalSpacing)*2+GlobalSpacing/2, (GlobalWidth+GlobalSpacing)*5+GlobalSpacing/2+Window.size[1]/5))
            Line(points=((GlobalWidth+GlobalSpacing)*3+GlobalSpacing/2, GlobalSpacing/2+Window.size[1]/5, (GlobalWidth+GlobalSpacing)*3+GlobalSpacing/2, (GlobalWidth+GlobalSpacing)*5+GlobalSpacing/2+Window.size[1]/5))
            Line(points=((GlobalWidth+GlobalSpacing)*4+GlobalSpacing/2, GlobalSpacing/2+Window.size[1]/5, (GlobalWidth+GlobalSpacing)*4+GlobalSpacing/2, (GlobalWidth+GlobalSpacing)*5+GlobalSpacing/2+Window.size[1]/5))
            Line(points=((GlobalWidth+GlobalSpacing)*5+GlobalSpacing/2, GlobalSpacing/2+Window.size[1]/5, (GlobalWidth+GlobalSpacing)*5+GlobalSpacing/2, (GlobalWidth+GlobalSpacing)*5+GlobalSpacing/2+Window.size[1]/5))
            
            Line(points=(GlobalSpacing/2, GlobalSpacing/2+Window.size[1]/5, (GlobalWidth+GlobalSpacing)*5+GlobalSpacing/2, GlobalSpacing/2+Window.size[1]/5))
            Line(points=(GlobalSpacing/2, (GlobalWidth+GlobalSpacing)+GlobalSpacing/2+Window.size[1]/5, (GlobalWidth+GlobalSpacing)*5+GlobalSpacing/2, (GlobalWidth+GlobalSpacing)+GlobalSpacing/2+Window.size[1]/5))
            Line(points=(GlobalSpacing/2, (GlobalWidth+GlobalSpacing)*2+GlobalSpacing/2+Window.size[1]/5, (GlobalWidth+GlobalSpacing)*5+GlobalSpacing/2, (GlobalWidth+GlobalSpacing)*2+GlobalSpacing/2+Window.size[1]/5))
            Line(points=(GlobalSpacing/2, (GlobalWidth+GlobalSpacing)*3+GlobalSpacing/2+Window.size[1]/5, (GlobalWidth+GlobalSpacing)*5+GlobalSpacing/2, (GlobalWidth+GlobalSpacing)*3+GlobalSpacing/2+Window.size[1]/5))
            Line(points=(GlobalSpacing/2, (GlobalWidth+GlobalSpacing)*4+GlobalSpacing/2+Window.size[1]/5, (GlobalWidth+GlobalSpacing)*5+GlobalSpacing/2, (GlobalWidth+GlobalSpacing)*4+GlobalSpacing/2+Window.size[1]/5))
            Line(points=(GlobalSpacing/2, (GlobalWidth+GlobalSpacing)*5+GlobalSpacing/2+Window.size[1]/5, (GlobalWidth+GlobalSpacing)*5+GlobalSpacing, (GlobalWidth+GlobalSpacing)*5+GlobalSpacing/2+Window.size[1]/5))
                
            Color(1, .3, .3, 1)
            RoundedRectangle(texture=Image("ExitButton.png").texture,pos=(GlobalSpacing,Window.size[1]-GlobalWidth-GlobalSpacing), size=(GlobalWidth,GlobalWidth))
            
            if(Undo):
                Color(.5, 1, .5, 1)
                RoundedRectangle(texture=Image("UndoButton.png").texture,pos=(Window.size[0]-GlobalSpacing-GlobalWidth,Window.size[1]-GlobalSpacing-GlobalWidth), size=(GlobalWidth,GlobalWidth))
            else:
                Color(1, .4, .4, 1)
                RoundedRectangle(texture=Image("UndoButton.png").texture,pos=(Window.size[0]-GlobalSpacing-GlobalWidth,Window.size[1]-GlobalSpacing-GlobalWidth), size=(GlobalWidth,GlobalWidth))
            
            if(Music):
                Color(.5, 1, .5, 1)
                RoundedRectangle(texture=Image("MusicButton.png").texture,pos=((GlobalWidth+GlobalSpacing)*2+GlobalSpacing,GlobalSpacing), size=(GlobalWidth,GlobalWidth))
            else:
                Color(1, .4, .4, 1)
                RoundedRectangle(texture=Image("MusicButton.png").texture,pos=((GlobalWidth+GlobalSpacing)*2+GlobalSpacing,GlobalSpacing), size=(GlobalWidth,GlobalWidth))
            
    def RoyalJellyBackground(self):
        global Music
        self.canvas.clear()
        with self.canvas:
            Color(.6, .4, 0, 1)
            Rectangle(pos=(0,0), size=(Window.size[0],Window.size[1]))
            Color(1, 1, .8, 1)
            Rectangle(pos=(GlobalSpacing/2,GlobalSpacing/2+Window.size[1]/5), size=(Window.size[0]-GlobalSpacing,(GlobalWidth+GlobalSpacing)*5))
            Color(0, 0, 0, 1) 
            Line(points=(GlobalSpacing/2, GlobalSpacing/2+Window.size[1]/5, GlobalSpacing/2, (GlobalWidth+GlobalSpacing)*5+GlobalSpacing/2+Window.size[1]/5))
            Line(points=((GlobalWidth+GlobalSpacing)+GlobalSpacing/2, GlobalSpacing/2+Window.size[1]/5, (GlobalWidth+GlobalSpacing)+GlobalSpacing/2, (GlobalWidth+GlobalSpacing)*5+GlobalSpacing/2+Window.size[1]/5))
            Line(points=((GlobalWidth+GlobalSpacing)*2+GlobalSpacing/2, GlobalSpacing/2+Window.size[1]/5, (GlobalWidth+GlobalSpacing)*2+GlobalSpacing/2, (GlobalWidth+GlobalSpacing)*5+GlobalSpacing/2+Window.size[1]/5))
            Line(points=((GlobalWidth+GlobalSpacing)*3+GlobalSpacing/2, GlobalSpacing/2+Window.size[1]/5, (GlobalWidth+GlobalSpacing)*3+GlobalSpacing/2, (GlobalWidth+GlobalSpacing)*5+GlobalSpacing/2+Window.size[1]/5))
            Line(points=((GlobalWidth+GlobalSpacing)*4+GlobalSpacing/2, GlobalSpacing/2+Window.size[1]/5, (GlobalWidth+GlobalSpacing)*4+GlobalSpacing/2, (GlobalWidth+GlobalSpacing)*5+GlobalSpacing/2+Window.size[1]/5))
            Line(points=((GlobalWidth+GlobalSpacing)*5+GlobalSpacing/2, GlobalSpacing/2+Window.size[1]/5, (GlobalWidth+GlobalSpacing)*5+GlobalSpacing/2, (GlobalWidth+GlobalSpacing)*5+GlobalSpacing/2+Window.size[1]/5))
            
            Line(points=(GlobalSpacing/2, GlobalSpacing/2+Window.size[1]/5, (GlobalWidth+GlobalSpacing)*5+GlobalSpacing/2, GlobalSpacing/2+Window.size[1]/5))
            Line(points=(GlobalSpacing/2, (GlobalWidth+GlobalSpacing)+GlobalSpacing/2+Window.size[1]/5, (GlobalWidth+GlobalSpacing)*5+GlobalSpacing/2, (GlobalWidth+GlobalSpacing)+GlobalSpacing/2+Window.size[1]/5))
            Line(points=(GlobalSpacing/2, (GlobalWidth+GlobalSpacing)*2+GlobalSpacing/2+Window.size[1]/5, (GlobalWidth+GlobalSpacing)*5+GlobalSpacing/2, (GlobalWidth+GlobalSpacing)*2+GlobalSpacing/2+Window.size[1]/5))
            Line(points=(GlobalSpacing/2, (GlobalWidth+GlobalSpacing)*3+GlobalSpacing/2+Window.size[1]/5, (GlobalWidth+GlobalSpacing)*5+GlobalSpacing/2, (GlobalWidth+GlobalSpacing)*3+GlobalSpacing/2+Window.size[1]/5))
            Line(points=(GlobalSpacing/2, (GlobalWidth+GlobalSpacing)*4+GlobalSpacing/2+Window.size[1]/5, (GlobalWidth+GlobalSpacing)*5+GlobalSpacing/2, (GlobalWidth+GlobalSpacing)*4+GlobalSpacing/2+Window.size[1]/5))
            Line(points=(GlobalSpacing/2, (GlobalWidth+GlobalSpacing)*5+GlobalSpacing/2+Window.size[1]/5, (GlobalWidth+GlobalSpacing)*5+GlobalSpacing, (GlobalWidth+GlobalSpacing)*5+GlobalSpacing/2+Window.size[1]/5))

            Color(1, .3, .3, 1)
            RoundedRectangle(texture=Image("ExitButton.png").texture,pos=(GlobalSpacing,Window.size[1]-GlobalWidth-GlobalSpacing), size=(GlobalWidth,GlobalWidth))
            
            if(Undo):
                Color(.5, 1, .5, 1)
                RoundedRectangle(texture=Image("UndoButton.png").texture,pos=(Window.size[0]-GlobalSpacing-GlobalWidth,Window.size[1]-GlobalSpacing-GlobalWidth), size=(GlobalWidth,GlobalWidth))
            else:
                Color(1, .4, .4, 1)
                RoundedRectangle(texture=Image("UndoButton.png").texture,pos=(Window.size[0]-GlobalSpacing-GlobalWidth,Window.size[1]-GlobalSpacing-GlobalWidth), size=(GlobalWidth,GlobalWidth))

            if(Music):
                Color(.5, 1, .5, 1)
                RoundedRectangle(texture=Image("MusicButton.png").texture,pos=((GlobalWidth+GlobalSpacing)*2+GlobalSpacing,GlobalSpacing), size=(GlobalWidth,GlobalWidth))
            else:
                Color(1, .4, .4, 1)
                RoundedRectangle(texture=Image("MusicButton.png").texture,pos=((GlobalWidth+GlobalSpacing)*2+GlobalSpacing,GlobalSpacing), size=(GlobalWidth,GlobalWidth))
    
    def RoyalPancakeBackground(self):
        global Music
        self.canvas.clear()
        with self.canvas:
            Color(.5, .5, 1, 1)
            Rectangle(pos=(0,0), size=(Window.size[0],Window.size[1]))
            Color(1, 1, .8, 1)
            Rectangle(pos=(GlobalSpacing/2,GlobalSpacing/2+Window.size[1]/5), size=(Window.size[0]-GlobalSpacing,(GlobalWidth+GlobalSpacing)*5))
            Color(0, 0, 0, 1)
            Line(points=(GlobalSpacing/2, GlobalSpacing/2+Window.size[1]/5, GlobalSpacing/2, (GlobalWidth+GlobalSpacing)*5+GlobalSpacing/2+Window.size[1]/5))
            Line(points=((GlobalWidth+GlobalSpacing)+GlobalSpacing/2, GlobalSpacing/2+Window.size[1]/5, (GlobalWidth+GlobalSpacing)+GlobalSpacing/2, (GlobalWidth+GlobalSpacing)*5+GlobalSpacing/2+Window.size[1]/5))
            Line(points=((GlobalWidth+GlobalSpacing)*2+GlobalSpacing/2, GlobalSpacing/2+Window.size[1]/5, (GlobalWidth+GlobalSpacing)*2+GlobalSpacing/2, (GlobalWidth+GlobalSpacing)*5+GlobalSpacing/2+Window.size[1]/5))
            Line(points=((GlobalWidth+GlobalSpacing)*3+GlobalSpacing/2, GlobalSpacing/2+Window.size[1]/5, (GlobalWidth+GlobalSpacing)*3+GlobalSpacing/2, (GlobalWidth+GlobalSpacing)*5+GlobalSpacing/2+Window.size[1]/5))
            Line(points=((GlobalWidth+GlobalSpacing)*4+GlobalSpacing/2, GlobalSpacing/2+Window.size[1]/5, (GlobalWidth+GlobalSpacing)*4+GlobalSpacing/2, (GlobalWidth+GlobalSpacing)*5+GlobalSpacing/2+Window.size[1]/5))
            Line(points=((GlobalWidth+GlobalSpacing)*5+GlobalSpacing/2, GlobalSpacing/2+Window.size[1]/5, (GlobalWidth+GlobalSpacing)*5+GlobalSpacing/2, (GlobalWidth+GlobalSpacing)*5+GlobalSpacing/2+Window.size[1]/5))
            
            Line(points=(GlobalSpacing/2, GlobalSpacing/2+Window.size[1]/5, (GlobalWidth+GlobalSpacing)*5+GlobalSpacing/2, GlobalSpacing/2+Window.size[1]/5))
            Line(points=(GlobalSpacing/2, (GlobalWidth+GlobalSpacing)+GlobalSpacing/2+Window.size[1]/5, (GlobalWidth+GlobalSpacing)*5+GlobalSpacing/2, (GlobalWidth+GlobalSpacing)+GlobalSpacing/2+Window.size[1]/5))
            Line(points=(GlobalSpacing/2, (GlobalWidth+GlobalSpacing)*2+GlobalSpacing/2+Window.size[1]/5, (GlobalWidth+GlobalSpacing)*5+GlobalSpacing/2, (GlobalWidth+GlobalSpacing)*2+GlobalSpacing/2+Window.size[1]/5))
            Line(points=(GlobalSpacing/2, (GlobalWidth+GlobalSpacing)*3+GlobalSpacing/2+Window.size[1]/5, (GlobalWidth+GlobalSpacing)*5+GlobalSpacing/2, (GlobalWidth+GlobalSpacing)*3+GlobalSpacing/2+Window.size[1]/5))
            Line(points=(GlobalSpacing/2, (GlobalWidth+GlobalSpacing)*4+GlobalSpacing/2+Window.size[1]/5, (GlobalWidth+GlobalSpacing)*5+GlobalSpacing/2, (GlobalWidth+GlobalSpacing)*4+GlobalSpacing/2+Window.size[1]/5))
            Line(points=(GlobalSpacing/2, (GlobalWidth+GlobalSpacing)*5+GlobalSpacing/2+Window.size[1]/5, (GlobalWidth+GlobalSpacing)*5+GlobalSpacing, (GlobalWidth+GlobalSpacing)*5+GlobalSpacing/2+Window.size[1]/5))

            Color(1, .3, .3, 1)
            RoundedRectangle(texture=Image("ExitButton.png").texture,pos=(GlobalSpacing,Window.size[1]-GlobalWidth-GlobalSpacing), size=(GlobalWidth,GlobalWidth))
            
            if(Undo):
                Color(.5, 1, .5, 1)
                RoundedRectangle(texture=Image("UndoButton.png").texture,pos=(Window.size[0]-GlobalSpacing-GlobalWidth,Window.size[1]-GlobalSpacing-GlobalWidth), size=(GlobalWidth,GlobalWidth))
            else:
                Color(1, .4, .4, 1)
                RoundedRectangle(texture=Image("UndoButton.png").texture,pos=(Window.size[0]-GlobalSpacing-GlobalWidth,Window.size[1]-GlobalSpacing-GlobalWidth), size=(GlobalWidth,GlobalWidth))
            
            if(Music):
                Color(.5, 1, .5, 1)
                RoundedRectangle(texture=Image("MusicButton.png").texture,pos=((GlobalWidth+GlobalSpacing)*2+GlobalSpacing,GlobalSpacing), size=(GlobalWidth,GlobalWidth))
            else:
                Color(1, .4, .4, 1)
                RoundedRectangle(texture=Image("MusicButton.png").texture,pos=((GlobalWidth+GlobalSpacing)*2+GlobalSpacing,GlobalSpacing), size=(GlobalWidth,GlobalWidth))


    def reset(self):
        self.MainMenu()

    def refresh(self):
        True
        

class WithTheJelly(App):
    def build(self):
        myOrange = [.96,.64,0,1]
        myPurple = [.6,0,.6,1]
        myLightBrown = [.7,.55,0,1]
        myDarkBrown = [.6,.45,0,1]
        myRoot = MyRoot()
        backgroundWidget = BackgroundWidget()
        myRoot.add_widget(backgroundWidget)#widget, index  --- lower indexes are drawn on front
        stackIndicator = StackIndicator()
        myRoot.add_widget(stackIndicator)#widget, index  --- lower indexes are drawn on front
        orangeJelly1 = Jelly(position=[0,0], color=myOrange, texture=None, player = 0, id = 0)
        myRoot.add_widget(orangeJelly1)#widget, index  --- s are drawn on front
        orangeJelly2 = Jelly(position=[1,0], color=myOrange, texture=None, player = 0, id = 1)
        myRoot.add_widget(orangeJelly2)#widget, index  --- s are drawn on front
        orangeJelly3 = Jelly(position=[2,0], color=myOrange, texture=None, player = 0, id = 2)
        myRoot.add_widget(orangeJelly3)#widget, index  --- s are drawn on front
        orangeJelly4 = Jelly(position=[3,0], color=myOrange, texture=None, player = 0, id = 3)
        myRoot.add_widget(orangeJelly4)#widget, index  --- s are drawn on front
        orangeJelly5 = Jelly(position=[4,0], color=myOrange, texture=None, player = 0, id = 4)
        myRoot.add_widget(orangeJelly5)#widget, index  --- s are drawn on front
        grapeJelly1 = Jelly(position=[0,4], color=myPurple, texture=None, player = 1, id = 5)
        myRoot.add_widget(grapeJelly1)#widget, index  --- l are drawn on front
        grapeJelly2 = Jelly(position=[1,4], color=myPurple, texture=None, player = 1, id = 6)
        myRoot.add_widget(grapeJelly2)#widget, index  --- l are drawn on front
        grapeJelly3 = Jelly(position=[2,4], color=myPurple, texture=None, player = 1, id = 7)
        myRoot.add_widget(grapeJelly3)#widget, index  --- l are drawn on front
        grapeJelly4 = Jelly(position=[3,4], color=myPurple, texture=None, player = 1, id = 8)
        myRoot.add_widget(grapeJelly4)#widget, index  --- l are drawn on front
        grapeJelly5 = Jelly(position=[4,4], color=myPurple, texture=None, player = 1, id = 9)
        myRoot.add_widget(grapeJelly5)#widget, index  --- lower indexes are drawn on front
        pancake1 = Jelly(position=[1,2], color=myLightBrown, texture=None, player = 2, id = 10)
        myRoot.add_widget(pancake1)#widget, index  ---es are drawn on front
        pancake2 = Jelly(position=[2,2], color=myLightBrown, texture=None, player = 2, id = 11)
        myRoot.add_widget(pancake2)#widget, index  ---es are drawn on front
        pancake3 = Jelly(position=[3,2], color=myLightBrown, texture=None, player = 2, id = 12)
        myRoot.add_widget(pancake3)#widget, index  --- lower indexes are drawn on front

        #neuralRandom.remove_widget()
        #neuralRandom.clear_widgets()
        #for child in myRoot.children[:]:
        return myRoot

withTheJelly = WithTheJelly()
withTheJelly.run()