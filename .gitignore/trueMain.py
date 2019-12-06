import arcade
import math
import random

windowWidth = 900
windowHeight = 600



class Window(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title) # Call the parent class's init function
        self.song = Song()
        self.listOfKeys = []
        self.temp = 0
        for i in range(1, 5):
            self.listOfKeys.append(Key(i))

    def update(self, delta_time):
        for i in self.song.listOfNotes:
            i.Move()
        if self.temp == 5:
            self.song.CreateNotes()
            self.temp = 0
        else:
            self.temp += 1

    def on_draw(self):
        arcade.start_render()
        for i in self.song.listOfNotes:
            i.Draw()
        for i in self.listOfKeys:
            i.Draw()


    def OnKeyPress(self, key, modifiers):
        if key == arcade.key.UP:
            for i in self.listOfKeys:
                if i.type == 1:
                    i.DetectCollision()
        elif key == arcade.key.DOWN:
            for i in self.listOfKeys:
                if i.type == 2:
                    i.DetectCollision()
        elif key == arcade.key.LEFT:
            for i in self.listOfKeys:
                if i.type == 3:
                    i.DetectCollision()
        elif key == arcade.key.RIGHT:
            for i in self.listOfKeys:
                if i.type == 4:
                    i.DetectCollision()

class Key:
    def __init__(self, type):
        self.radius = 16
        self.type = type

        self.xPos = (windowWidth / 5) * self.type
        self.yPos = windowHeight / 7

        if self.type == 1:
            self.color = arcade.color.RED
        if self.type == 2:
            self.color = arcade.color.PURPLE
        if self.type == 3:
            self.color = arcade.color.GREEN
        if self.type == 4:
            self.color = arcade.color.OLD_GOLD

    def Draw(self):
        arcade.draw_circle_outline(self.xPos, self.yPos, self.radius, self.color, 2)

    def DetectCollision(self):
        for obj in theObjectToRuleThemAll.song.listOfNotes:
            self.afstand = math.sqrt(((self.xPos + self.radius)
                                      - (obj.x + obj.r)) ** 2 + ((self.yPos + self.radius) - (obj.y + obj.r)) ** 2)
            if self.afstand < obj.r:
                obj.Destroy()

class Note:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.r = 15

    def Move(self):
        self.y = self.y - 5
        if self.y + self.r < 0:
            self.Destroy()

    def Draw(self):
        arcade.draw_circle_filled(self.x, self.y, self.r, arcade.color.ROYAL_PURPLE)

    def Destroy(self):
        theObjectToRuleThemAll.song.listOfNotes.remove(self)

class Song:

    def __init__(self):
        self.listOfNotes = []
        self.CreateNotes()

    def DrawNotes(self):
        for i in self.listOfNotes:
            i.Draw()

    def CreateNotes(self):
        var = random.randint(1, 4)
        self.listOfNotes.append(Note(windowWidth/5*var, windowHeight))


theObjectToRuleThemAll = Window(windowWidth, windowHeight, "Mit vindue")

arcade.run()
