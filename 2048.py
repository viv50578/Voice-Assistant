from tkinter import *
import random
import pygame
from tkinter import messagebox
pygame.mixer.init()
class Board:
    #A dictionary that stores background color for every cell
    bg_color={
        '2': 'seagreen1',
        '4': 'maroon1',
        '8': 'turquoise2',
        '16': 'indianred1',
        '32': 'sky blue',
        '64': 'mediumpurple1',
        '128': 'lawn green',
        '256': 'tomato',
        '512': 'darkorchid3',
        '1024': 'hotpink',
        '2048': 'gold',
    }
    # A dictionary that stores foreground color for every cell
    color={
         '2': 'grey1',
        '4': 'grey2',
        '8': 'grey3',
        '16': 'grey4',
        '32': 'grey5',
        '64': 'grey6',
        '128': 'grey7',
        '256': 'grey8',
        '512': 'grey9',
        '1024': 'grey10',
        '2048': 'grey11',
    }
     # constructor: It opens ths game window and initializes the flag variables
    def __init__(self):
        self.n=4
        self.window=Tk()
        self.window.title('2048 GAME by Parth Chaudhary, Dhairya Thakkar, Vivek Iyer')
        self.gameArea=Frame(self.window, bg = 'grey1')
        self.board=[]
        self.matrix_cell=[[0]*4 for i in range(4)]
        self.compress=False
        self.merge=False
        self.moved=False
    
        for i in range(4):
            rows=[]
            for j in range(4):
                l=Label(self.gameArea, text='', bg='azure4', font=('cambria',32,'bold'), width=4, height=2)
                l.grid(row=i,column=j,padx=4,pady=4)

                rows.append(l)
            self.board.append(rows)
        self.gameArea.grid()
    
    # Reverses the whole matrix,turns the matrix around the vertical axis
    def reverse(self):
        for ind in range(4):
            i=0
            j=3
            while(i<j):
                self.matrix_cell[ind][i],self.matrix_cell[ind][j]=self.matrix_cell[ind][j],self.matrix_cell[ind][i]
                i+=1
                j-=1

    # Takes transpose of the matrix
    def transpose(self):
        self.matrix_cell=[list(t)for t in zip(*self.matrix_cell)]

    # moving the tiles in the left direction
    def shift_left(self):
        self.compress=False
        temp=[[0] *4 for i in range(4)]
        for i in range(4):
            cnt=0
            for j in range(4):
                if self.matrix_cell[i][j]!=0:
                    temp[i][cnt]=self.matrix_cell[i][j]
                    if cnt!=j:
                        self.compress=True
                    cnt+=1
        self.matrix_cell=temp

    #merges two adjacent tiles, if their values are equal
    #makes the value of the cell to the left most side into 2 times and makes the value of the adjacent tile 0(vacant)
    def merge_same(self):
        self.merge=False
        for i in range(4):
            for j in range(3):
                if self.matrix_cell[i][j] == self.matrix_cell[i][j + 1] and self.matrix_cell[i][j] != 0:
                    self.matrix_cell[i][j] *= 2
                    self.matrix_cell[i][j + 1] = 0
                    self.merge = True
    #First goes through the whole matrix_cell list and collects the indices of the empty cells
    #stores each pair of indices into a tuple and adds it to cells list.
    # Then chooses a random tuple from the cells list and assigns that cell the value 2
    def random_cell(self):
        cells=[]
        for i in range(4):
            for j in range(4):
                if self.matrix_cell[i][j] == 0:
                    cells.append((i, j))
        appendable=random.choice(cells)
        self.matrix_cell[appendable[0]][appendable[1]] = 2
    # Compares the adjacent cells in the grid first horizontally and then vertically. 
    # Returns true if it finds two adjacent cells of the same value, otherwise returns false. 
    # The return statement is the last statement that is executed in a function.
    # After the return statement, the control comes out of the function.
    def can_merge(self):
        for i in range(4):
            for j in range(3):
                if self.matrix_cell[i][j] == self.matrix_cell[i][j+1]:
                    return True
        
        for i in range(3):
            for j in range(4):
                if self.matrix_cell[i+1][j] == self.matrix_cell[i][j]:
                    return True
        return False
    #Does the work of giving colours and displaying the value of each cell. 
    #If the value is zero, it displays no text and gives the colour azure4 to the cell, otherwise it gets the corresponding text and colour from the bg_colour and colour dictionaries.
    def paint_grid(self):
        for i in range(4):
            for j in range(4):
                if self.matrix_cell[i][j]==0:
                    self.board[i][j].config(text='',bg='papaya whip')
                else:
                    self.board[i][j].config(text=str(self.matrix_cell[i][j]),
                    bg=self.bg_color.get(str(self.matrix_cell[i][j])),
                    fg=self.color.get(str(self.matrix_cell[i][j]))) 
#Start of class Game
#Defines instance variables.
class Game:
    def __init__(self,gamepanel):
        self.gamepanel=gamepanel
        self.end=False
        self.won=False

    #imported audio and used module pygame for playing it    
    def play(self):
            pygame.mixer.music.load("audio.mp3")
            pygame.mixer.music.play(loops=10)
      
     #It calls random_cell twice to assign ‘2’ to matrix_cell value of two random cells and then it paints the grid
    def start(self):
        #creates a button for selecting music option on the game panel
        play_button1 = Button(self.gamepanel.window, text="Rock n Roll!", font=("cambria", 25), command=self.play)
        play_button1.grid(pady=5)
        self.gamepanel.random_cell()
        self.gamepanel.random_cell()
        self.gamepanel.paint_grid()
        #it calls link_keys to link up, down, left, and right keys
        self.gamepanel.window.bind('<Key>', self.link_keys)
        self.gamepanel.window.mainloop()

    
    #First checks if the game is won or lost, in that case it executes the return statement and stops. Otherwise, it keeps running.
    def link_keys(self,event):
        if self.end or self.won:
            return

        self.gamepanel.compress = False
        self.gamepanel.merge = False
        self.gamepanel.moved = False

        presed_key=event.keysym

        if presed_key=='Up':
            self.gamepanel.transpose()
            self.gamepanel.shift_left()
            self.gamepanel.merge_same()
            self.gamepanel.moved = self.gamepanel.compress or self.gamepanel.merge
            self.gamepanel.shift_left() 
            self.gamepanel.transpose()

        elif presed_key=='Down':
            self.gamepanel.transpose()
            self.gamepanel.reverse()
            self.gamepanel.shift_left()
            self.gamepanel.merge_same()
            self.gamepanel.moved = self.gamepanel.compress or self.gamepanel.merge
            self.gamepanel.shift_left()
            self.gamepanel.reverse()
            self.gamepanel.transpose()

        elif presed_key=='Left':
            self.gamepanel.shift_left()
            self.gamepanel.merge_same()
            self.gamepanel.moved = self.gamepanel.compress or self.gamepanel.merge
            self.gamepanel.shift_left()

        elif presed_key=='Right':
            self.gamepanel.reverse()
            self.gamepanel.shift_left()
            self.gamepanel.merge_same()
            self.gamepanel.moved = self.gamepanel.compress or self.gamepanel.merge
            self.gamepanel.shift_left()
            self.gamepanel.reverse()
        else:
            pass

        self.gamepanel.paint_grid()
       
        # winning condition 
        flag=0
        for i in range(4):
            for j in range(4):
                if(self.gamepanel.matrix_cell[i][j] == 2048):
                    self.won=True
                    messagebox.showinfo('2048', message="Y0U WONNNN!!!")
                    print("won")
                    break
        
       #for checking if there is any vacant tile left or any tile can merge, game will continue,flag set to 1
        for i in range(4):
            for j in range(4):
                if self.gamepanel.matrix_cell[i][j]==0:
                    flag=1
                    break
        #if there is no vacant tile left or no tile can merge, message print(game over),flag set to 0
        if not (flag or self.gamepanel.can_merge()):
            self.end=True
            messagebox.showinfo('2048','Game Over!!!')
            print("Game Over")

        if self.gamepanel.moved:
            self.gamepanel.random_cell()
            self.gamepanel.paint_grid()
    
gamepanel = Board()
game2048 = Game(gamepanel)
game2048.start()