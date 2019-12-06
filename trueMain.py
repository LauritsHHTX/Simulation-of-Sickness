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
        self.score = 0
        self.playerLives = 3
        self.finalScore = 0
        self.notDead = True
        for i in range(1, 5):
            self.listOfKeys.append(Key(i))
        
        self.death = False
        self.respawn = False

    def update(self, delta_time):
        if self.death == True and self.respawn == True:
            self.Restart()
            self.song = Song()
            self.temp = 0
            self.score = 0
            self.playerLives = 3
            self.finalScore = 0
            self.notDead = True

        if self.death == False:
            for i in self.song.listOfNotes:
                i.Move()
            if self.temp == 60:
                self.song.CreateNotes()
                self.temp = 0
            else:
                self.temp += 1

        if self.death == True and self.respawn == True:
            self.Restart()
            self.song = Song()
            self.temp = 0
            self.score = 0
            self.playerLives = 3
            self.finalScore = 0
            self.notDead = True

    def on_draw(self):
        arcade.start_render()
        if self.death == False:
            for i in self.song.listOfNotes:
                i.Draw()
            for i in self.listOfKeys:
                i.Draw()
            self.DrawLives()

        if self.death == True:
            arcade.draw_text("GAME OVER", windowWidth - 600, windowHeight / 2, arcade.color.RED, 50)
            arcade.draw_text("Final score: " + str(self.score), windowWidth / 3, windowHeight / 3, arcade.color.OLD_GOLD, 56)


    def Restart(self):
        self.death = False
        self.respawn = False

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            for i in self.listOfKeys:
                if i.type == 1:
                    i.DetectCollision()
                    i.lineWidth = 4
        elif key == arcade.key.DOWN:
            for i in self.listOfKeys:
                if i.type == 2:
                    i.DetectCollision()
                    i.lineWidth = 4
        elif key == arcade.key.LEFT:
            for i in self.listOfKeys:
                if i.type == 3:
                    i.DetectCollision()
                    i.lineWidth = 4
        elif key == arcade.key.RIGHT:
            for i in self.listOfKeys:
                if i.type == 4:
                    i.DetectCollision()
                    i.lineWidth = 4

        elif key == arcade.key.R and self.death == True:
            self.respawn = True

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP:
            for i in self.listOfKeys:
                if i.type == 1:
                    i.lineWidth = 2
        elif key == arcade.key.DOWN:
            for i in self.listOfKeys:
                if i.type == 2:
                    i.lineWidth = 2
        elif key == arcade.key.LEFT:
            for i in self.listOfKeys:
                if i.type == 3:
                    i.lineWidth = 2
        elif key == arcade.key.RIGHT:
            for i in self.listOfKeys:
                if i.type == 4:
                    i.lineWidth = 2


    def DrawLives(self):
        if self.playerLives <= 0:
            self.playerLives = 0
            if self.notDead:
                self.notDead = False
                self.finalScore = self.score
            self.score = self.finalScore
            for i in self.song.listOfNotes:
                self.i.remove(i)
            arcade.draw_text("Game Over", windowWidth / 4, windowHeight / 2.1, arcade.color.OLD_GOLD, 96)
            arcade.draw_text("Final score: " +
                             str(self.score), windowWidth / 3, windowHeight / 3, arcade.color.OLD_GOLD, 56)
        arcade.draw_text("Health: " + str(self.playerLives), 0 + 50, windowHeight - 60, arcade.color.OLD_GOLD, 50)
        arcade.draw_text("Score: " + str(self.score), windowWidth - 400, windowHeight - 60, arcade.color.OLD_GOLD, 50)


class Key:
    def __init__(self, type):
        self.radius = 21
        self.type = type
        self.lineWidth = 2

        self.xPos = (windowWidth / 5) * self.type
        self.yPos = windowHeight / 7

        if self.type == 1:
            self.color = arcade.color.RED
        if self.type == 2:
            self.color = arcade.color.BLUE
        if self.type == 3:
            self.color = arcade.color.GREEN
        if self.type == 4:
            self.color = arcade.color.OLD_GOLD

    def Draw(self):
        arcade.draw_circle_outline(self.xPos, self.yPos, self.radius, self.color, self.lineWidth)

    def DetectCollision(self):
        for obj in theObjectToRuleThemAll.song.listOfNotes:
            self.afstand = math.sqrt(((self.xPos + self.radius)
                                      - (obj.x + obj.r)) ** 2 + ((self.yPos + self.radius) - (obj.y + obj.r)) ** 2)
            if self.afstand < obj.r + self.radius:
                theObjectToRuleThemAll.score += int(1000 / self.afstand)
                obj.Destroy()

class ShortNote:

    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.r = 20
        self.type = type

        if self.type == 1:
            self.color = arcade.color.RED
        if self.type == 2:
            self.color = arcade.color.BLUE
        if self.type == 3:
            self.color = arcade.color.GREEN
        if self.type == 4:
            self.color = arcade.color.OLD_GOLD

    def Move(self):
        self.y = self.y - 3
        if self.y + self.r < 0:
            self.Destroy()
            theObjectToRuleThemAll.playerLives -= 1
            if theObjectToRuleThemAll.playerLives == 0:
                theObjectToRuleThemAll.death = True

    def Draw(self):
        arcade.draw_circle_filled(self.x, self.y, self.r, self.color)

    def Destroy(self):
        theObjectToRuleThemAll.song.listOfNotes.remove(self)

class LongNote:

    def __init__(self, x, y, type, length):
        self.x = x
        self.y = y
        self.r = 20
        self.length = length
        self.type = type

        if self.type == 1:
            self.color = arcade.color.RED
        if self.type == 2:
            self.color = arcade.color.BLUE
        if self.type == 3:
            self.color = arcade.color.GREEN
        if self.type == 4:
            self.color = arcade.color.OLD_GOLD

    def Move(self): # NOT DONE
        self.y = self.y - 3
        if self.length + self.r < 0:
            self.Destroy()
            theObjectToRuleThemAll.playerLives -= 1
            if theObjectToRuleThemAll.playerLives == 0:
                theObjectToRuleThemAll.death = True

    def Draw(self):
        arcade.draw_circle_filled(self.x, self.y, self.r, self.color)
        arcade.draw_rectangle_filled(self.x, self.y, self.r, self.length, self.color)

    def Destroy(self):
        pass

class Song:

    def __init__(self):
        self.listOfNotes = []
        self.CreateNotes()

    def DrawNotes(self):
        for i in self.listOfNotes:
            i.Draw()

    def CreateNotes(self):
        var = random.randint(1, 4)
        self.listOfNotes.append(ShortNote(windowWidth/5*var, windowHeight, var))


theObjectToRuleThemAll = Window(windowWidth, windowHeight, "Mit vindue")

arcade.run()
