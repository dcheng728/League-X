import numpy as np
import cv2
import os

class leagueMap:
    def __init__(self):
        """
        Constructor, it will create a list of champions and a list of champion names,
        the elements in each should correspond to each other
        """
        self.champions = []
        self.championNames = []
        
    def addChampion(self,givenChampion):
        """
        Takes a leagueChampion object and add it and its name to the lists
        """
        self.champions.append(givenChampion)
        self.championNames.append(givenChampion.name)
        
    def setChampionCoord(self,championName,newCoord):
        """
        Setter for champion coord, the variable newCoord should be a tuple of (x,y)
        """
        self.champions[self.championNames.index(championName)].coord = newCoord
    
    def getChampionCoord(self,championName):
        """
        Returns the coordinate of the input champion name
        """
        return self.champions[self.championNames.index(championName)].coord
    
    def setChampionImage(self,championName,givenImage):
        """
        Sets the image of the given champion
        """
        self.champions[self.championNames.index(championName)].image = givenImage
    def setChampionRecordTime(self,championName,time):
        """
        Sets the last recorded time of the champion
        """
        self.champions[self.championNames.index(championName)].time_recorded = time
        
        

class leagueChampion:
    def __init__(self,champName):
        """
        Set up the name, and coordinate of the champion 
        """
        self.name = champName
        self.coord = None
        self.jungler = False
        self.time_recorded = None
        self.image = np.zeros([24,24,3],dtype=np.uint8)
        self.minimap_image = cv2.imread("minimap_head/"+champName+".png")
        
            
    
    def addImage(self,croppedImage):
        self.image = croppedImage
        


