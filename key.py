import arcade
import math
import main

class Key:
    def __init__(self, type):
        self.radius = 5.5
        self.type = type
        
        self.xPos = (main.windowWidth / 4) * self.type
        self.yPos = main.windowHeight / 7
        
        if self.type == 1:
            self.color = arcade.color.RED
        if self.type == 2:
            self.color = arcade.color.PURPLE
        if self.type == 3:
            self.color = arcade.color.YANKEES_BLUE
        if self.type == 4:
            self.color = arcade.color.OLD_GOLD

    def Draw(self):
        arcade.draw_circle_outline(self.xPos, self.yPos, self.radius, self.color, 0.5)

    def DetectCollision(self):
        for obj in main.theObjectToRuleThemAll.song.listOfNotes:
            self.afstand = math.sqrt(((self.xPos + self.radius)
                                      - (obj.x + obj.r))**2 + ((self.yPos + self.radius) - (obj.y + obj.r))**2)
            if self.afstand < obj.r:
                obj.Destroy()
