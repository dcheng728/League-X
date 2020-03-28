import numpy as np
import tkinter as tk
from tkinter import messagebox
import os
from PIL import Image,ImageTk
import launch_scanner
import time

class Champion:
    def __init__(self,championName):
        self.name = championName
        self.image = ImageTk.PhotoImage(file = "champion_head/" + championName + ".png")
        self.selectedImage = ImageTk.PhotoImage(file = "selected_head/" + championName + ".png")
        self.smallImage = tk.PhotoImage(file = "champion_head/" + championName + ".png").subsample(2,2)    

class SelectFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.topChampions = ["Aatrox","Akali","Camille","Chogath","Darius","DrMundo","Ekko","Fiora","Gangplank","Garen",
                        "Gnar","Illaoi","Irelia","Jax","Jayce","Kayle","Kennen","Kled","Malphite","Maokai","Mordekaiser",
                        "Nasus","Ornn","Pantheon","Poppy","Quinn","Renekton","Riven","Rumble","Ryze","Sett","Shen","Singed","Sion","Skarner","Teemo",
                        "Tryndamere","Urgot","Vayne","Volibear","Vladimir","Yasuo","Yorick"]

        self.jungleChampions = ["Amumu","Ekko","Elise","Evelynn","Gragas","Graves","Hecarim","Ivern","JarvanIV","Jax",
                        "Karthus","Kayn","Khazix","Kindred","LeeSin","MasterYi","MonkeyKing","Nocturne","Nunu","Olaf","Qiyana",
                        "Rammus","RekSai","Rengar","Riven","Sejuani","Shaco","Shyvana","Skarner","Taliyah","Trundle","Udyr",
                        "Vi","Warwick","Nidalee","XinZhao","Zac"]

        self.midChampions = ["Ahri","Akali","Anivia","Annie","AurelionSol","Azir","Cassiopeia","Corki","Diana","Ekko","Fizz",
                        "Galio","Heimerdinger","Irelia","Kassadin","Katarina","Leblanc","Lissandra","Lux","Malzahar","MonkeyKing","Neeko",
                        "Orianna","Qiyana","Rakan","Riven","Ryze","Sylas","Syndra","Taliyah","Talon","TwistedFate","Veigar","Velkoz","Viktor",
                        "Vladimir","Xerath","Yasuo","Zed","Ziggs","Zilean","Zoe"]

        self.botChampions = ["Aphelios","Ashe","Caitlyn","Draven","Ezreal","Jinx","Jhin","Kaisa","Kalista","KogMaw","Lucian","Senna",
                        "Sivir","Tristana","Twitch","Varus","Vayne","Yasuo","Xayah"]

        self.suppChampions = ["Alistar","Blitzcrank","Brand","Fiddlesticks","Janna","Leona","Lulu","Lux","Morgana","Nami","Nautilus",
                        "Pyke","Rakan","Senna","Sona","Soraka","Swain","TahmKench","Taric","Thresh","Yuumi","Xerath","Zilean","Zyra"]

        self.allChampNames = [champion[0:len(champion)-4] for champion in os.listdir("champion_head/")]
        
        self.posChampions = [self.topChampions,self.jungleChampions,self.midChampions,self.botChampions,self.suppChampions,self.allChampNames]
        
        self.allChampions = []
        for champion in os.listdir("champion_head/"):
            self.allChampions.append(Champion(champion[0:len(champion)-4]))

        self.leftFrame = tk.Frame(self,width = 400, height = 600, bg = 'black',highlightthickness=0)
        self.leftFrame.pack(side = tk.LEFT)
        self.selectedFrame = tk.Frame(self.leftFrame,width = 400, height = 600, bg = 'black',highlightthickness=0)
        self.selectedFrame.place(x = 0, y = 0)
        self.gapCanvas = tk.Canvas(self,width = 30, height = 600, bg = 'black',highlightthickness=0)
        self.gapCanvas.pack(side = tk.LEFT)
        
        self.initScroll()
        self.championButtons = {}
        self.initButtons()
        
        self.displayingPos = self.displayButtons(5)
        self.selectedChampions = []
        self.selectedChampionButtons = []
        self.launchImage = ImageTk.PhotoImage(file = "GUI_Images/launch_scanner4.jpg")
        self.launchButton = tk.Button(self.leftFrame,image = self.launchImage,bg = '#555555',bd = 30,command = self.launchScanner)
        self.launchButton.place(x = 30, y = 400,anchor = tk.NW)
           
    def scrollFunction(self,event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"),width=1080,height=600)
    
    def initScroll(self):
        self.canvas=tk.Canvas(self,width = 1080, height = 600,bg = 'black',highlightthickness=0)
        self.buttonsFrame=tk.Frame(self.canvas, width = 1080,height = 4000,bg = 'black')
        self.myscrollbar=tk.Scrollbar(self,orient="vertical",command=self.canvas.yview,bg = 'black')
        self.canvas.configure(yscrollcommand=self.myscrollbar.set)

        self.myscrollbar.pack(side="right",fill="y")
        self.canvas.pack(side = tk.LEFT)
        self.canvas.create_window((0,0),window=self.buttonsFrame,anchor='nw')
        self.bind("<Configure>",self.scrollFunction)
    
    def selectIcon(self,index):
        champName = self.allChampions[index].name
        currentColor = self.championButtons[champName].cget("bg")
        if (currentColor == '#000000' and len(self.selectedChampions) < 5): #if the button is not selected
            self.championButtons[champName].config(bg = '#000001')
            self.championButtons[champName].config(image = self.allChampions[index].selectedImage)
            self.selectedChampions.append(self.allChampions[index])
        elif (currentColor != '#000000' ):
            self.championButtons[champName].config(bg = '#000000')
            self.championButtons[champName].config(image = self.allChampions[index].image)
            self.selectedChampions.remove(self.allChampions[index])
        
        #Update the left frame with all selected champions
        for button in self.selectedChampionButtons:
            button.place_forget()
        for n in range(len(self.selectedChampions)):
            newButton = tk.Button(self.leftFrame,text = self.selectedChampions[n].name,image = self.selectedChampions[n].smallImage,bd = 0, bg = '#000000')
            self.selectedChampionButtons.append(newButton)
            newButton.place(x = 175, y = 10+ 75*n)
        
    def launchScanner(self):
        if (len(self.selectedChampions) < 2):
            messagebox.showinfo("Message from League-X", "Please select at least two champions, you" + 
                                " can make your selection simply by clicking the champion's icon on the right panel." + 
                                " You can filter position of the champion by clicking the corresponding position above," + 
                                " or type in the name of the champion in the search bad on the upper right corner.")
        else:
            file = open('selectedChampions.txt','w')
            toWrite = ''
            for n in range(len(self.selectedChampions)):
                toWrite = toWrite + self.selectedChampions[n].name.lower() + ','
            toWrite = toWrite[0:len(toWrite)-1]
            file.write(toWrite)
            file.close()
            champions_found = launch_scanner.launchScanner()
            if 0 in champions_found:
                not_found_champions_string = "        "
                for n in range(len(champions_found)):
                    if champions_found[n] == 0:
                        not_found_champions_string = not_found_champions_string + self.selectedChampions[n].name + '\n        '
                response = messagebox.askyesno("Message from League-X","The Following champions are not supported by League-X at this moment: \n\n" + 
                                                 not_found_champions_string + "\nWould you like to continue?")
                if response:
                    import CNN
                    messagebox.showinfo("Message from League-X","Training complete! Now run liveDisplayImage.py in this directory to use the scanner! You can now termiante this GUI")
            else:
                messagebox.showinfo("Message from League-X","Training Data preparation complete, training have started" + 
                                   ", please allow 30 seconds to 5 minutes (depending on machine), you can also check " + 
                                   "the console output for status updates.")
                import CNN
                messagebox.showinfo("Message from League-X","Training complete! Now run liveDisplayImage.py in this directory to use the scanner! You can now terminate this GUI")
                
        
        
    def initButtons(self):
        for n in range(len(self.allChampions)):
            self.championButtons[self.allChampions[n].name] = tk.Button(self.buttonsFrame,image = self.allChampions[n].image, text = self.allChampions[n].name,bg = '#000000',bd = 10, command = lambda c = n: self.selectIcon(c))
        
    
    def displayButtons(self,position):
        for button in self.championButtons.values():
            button.place_forget()
        for n in range(len(self.posChampions[position])):
            row,column = divmod(n,7)
            champName = self.posChampions[position][n]
            self.championButtons[champName].place(x = 25 + 150*column, y = 10 + 150*row)
        return position
    
    def displaySearchedButtons(self,nameList):
        for button in self.championButtons.values():
            button.place_forget()
        for n in range(len(nameList)):
            row,column = divmod(n,7)
            champName = nameList[n]
            self.championButtons[champName].place(x = 25 + 150*column, y = 10 + 150*row)        
        

root = tk.Tk()
root.title("Champion Select")
root.geometry("1600x900")

backgroundImage = ImageTk.PhotoImage(file = "GUI_Images/bg.jpg")
searchImage = ImageTk.PhotoImage(file = "GUI_Images/search.png")

background_label = tk.Label(root, image=backgroundImage)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

searchLabel = tk.Label(root,image = searchImage, bg = '#434b4d')
searchLabel.place(x = 1240,y = 235,anchor = tk.SW)
s = SelectFrame(root,width = 1480, height = 600,bg = 'black')
s.place(x = 20, y = 250, anchor = tk.NW)

def selectPos(posIndex):
    buttonColor = posButtons[posIndex].cget('bg')
    if buttonColor == '#000000': #put a button to clicked state
        for n in range(len(posButtons)):
            if n == posIndex:
                posButtons[n].config(bg = '#000001')
                posButtons[n].config(image = posImagesClicked[n])
            else:
                posButtons[n].config(bg = '#000000')
                posButtons[n].config(image = posImages[n])
        
    else: #put a button to not clicked state
        posButtons[posIndex].config(bg = '#000000')
        posButtons[posIndex].config(image = posImages[posIndex])
        
    if (s.displayingPos == 5):
        s.displayingPos = s.displayButtons(posIndex)
        buttonColor = posButtons[s.displayingPos].cget('bg')
            
    elif s.displayingPos == posIndex:
        s.displayingPos = s.displayButtons(5)
        
    else:
        s.displayingPos = s.displayButtons(posIndex)

def searchBar(sv):
    rawText = sv.get()
    filteredText = ""
    for character in rawText:
        if character.isalpha():
            filteredText = filteredText + character
    #print(filteredText)
    toDisplay = []
    for champion in s.posChampions[s.displayingPos]:
        if filteredText.lower() in champion.lower():
            toDisplay.append(champion)
    s.displaySearchedButtons(toDisplay)

posImages = [tk.PhotoImage(file = 'GUI_Images/top_position.png').subsample(2,2),
             tk.PhotoImage(file = 'GUI_Images/jungle_position.png').subsample(2,2),
             tk.PhotoImage(file = 'GUI_Images/mid_position.png').subsample(2,2),
             tk.PhotoImage(file = 'GUI_Images/bot_position.png').subsample(2,2),
             tk.PhotoImage(file = 'GUI_Images/supp_position.png').subsample(2,2)]

posImagesClicked = [tk.PhotoImage(file = 'GUI_Images/top_position_clicked.png').subsample(2,2),
             tk.PhotoImage(file = 'GUI_Images/jungle_position_clicked.png').subsample(2,2),
             tk.PhotoImage(file = 'GUI_Images/mid_position_clicked.png').subsample(2,2),
             tk.PhotoImage(file = 'GUI_Images/bot_position_clicked.png').subsample(2,2),
             tk.PhotoImage(file = 'GUI_Images/supp_position_clicked.png').subsample(2,2)]

posButtons = [tk.Button(root,text = "top", image = posImages[0], bd = 0,bg = '#000000', command = lambda : selectPos(0)), #000000 signifies not selected
              tk.Button(root,text = "jungle", image = posImages[1], bd = 0,bg = '#000000', command = lambda : selectPos(1)),
              tk.Button(root,text = "mid",image = posImages[2], bd = 0,bg = '#000000', command = lambda : selectPos(2)),
              tk.Button(root,text = "bot",image = posImages[3], bd = 0,bg = '#000000', command = lambda : selectPos(3)),
              tk.Button(root,text = "support",image = posImages[4], bd = 0,bg = '#000000', command = lambda : selectPos(4))]

posButtons[0].place(x = 450,y = 180)
posButtons[1].place(x = 550,y = 180)
posButtons[2].place(x = 650,y = 180)
posButtons[3].place(x = 750,y = 180)
posButtons[4].place(x = 850,y = 180)

sv = tk.StringVar()
sv.trace("w", lambda name, index, mode, sv=sv: searchBar(sv))
e = tk.Entry(root,bg = '#252525', fg = '#efefef', font = ("Calibri 17"), width = 20,textvariable = sv)
e.place(x = 1530, y = 230,anchor = tk.SE)



root.mainloop()
