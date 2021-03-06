import arcade
import math
import random
import sys


windowWidth = 900
windowHeight = 600


class Window(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)  # Call the parent class's init function
        self.listOfKeys = []
        self.song = Song('Megalovania_Medium')
        self.audio = arcade.sound.load_sound('Megalovania.mp3')
        self.tempo = self.song.tempo
        #self.tempo = 7.03555
        self.tempIncrement = self.song.tI
        self.temp = self.tempo
        self.framesModulo = self.song.fM
        self.noteSpeed = self.song.nS
        self.score = 0
        self.maxLives = 1000
        self.playerLives = self.maxLives
        self.finalScore = 0
        self.death = False
        self.respawn = False
        for i in range(1, 5):
            self.listOfKeys.append(Key(i))
        self.compensation = (height - self.listOfKeys[0].yPos)/self.noteSpeed
        self.frames = 0
        self.songStarted = False
        self.listOfNotes = []
        self.A = False
        self.S = False
        self.D = False
        self.F = False
        self.ENTER = False

        
        #debugging variables
        self.missedHits = 0

    def update(self, delta_time):
        self.CheckInput()
        if not self.death:
            for i in self.listOfNotes:
                if i:
                    i.Move(delta_time)
            if self.temp >= self.tempo:
                nextNote, nextNote1, nextNote2 = self.song.GetNextNote()
                if nextNote == 2:
                    self.listOfNotes.append(nextNote1)
                    self.listOfNotes.append(nextNote2)
                else:
                    self.listOfNotes.append(nextNote)
                self.temp -= self.tempo
            else:
                if self.frames % self.framesModulo == 0:
                    self.temp += self.tempIncrement

        if self.death and self.respawn:
            self.Restart()
            self.song = Song('Megalovania_Medium')
            self.temp = 0
            self.score = 0
            self.playerLives = self.maxLives
            self.finalScore = 0
            self.death = False
        self.frames += 1

        if self.frames > self.compensation and not self.songStarted:
            arcade.sound.play_sound(self.audio)
            self.songStarted = True

    def on_draw(self):
        arcade.start_render()
        if not self.death:
            for i in self.listOfNotes:
                if i:
                    i.Draw()
            for i in self.listOfKeys:
                i.Draw()
            self.DrawLives()

        if self.death:
            arcade.draw_text("GAME OVER", windowWidth - 600, windowHeight / 2, arcade.color.RED, 50)
            arcade.draw_text("Final score: " + str(self.score), windowWidth / 3, windowHeight / 3, arcade.color.YELLOW, 56)

    def Restart(self):
        self.death = False
        self.respawn = False

    def on_key_press(self, key, modifiers):
        if key == arcade.key.A:
            self.A = True
        if key == arcade.key.S:
            self.S = True
        if key == arcade.key.D:
            self.D = True
        if key == arcade.key.F:
            self.F = True

        if key == arcade.key.ENTER:
            self.ENTER = True

        if key == arcade.key.R and self.death:
            self.respawn = True

        if key == arcade.key.ESCAPE:
            sys.exit()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.A:
            self.A = False
            for i in self.listOfKeys:
                if i.type == 1:
                    i.lineWidth = 2
        if key == arcade.key.S:
            self.S = False
            for i in self.listOfKeys:
                if i.type == 2:
                    i.lineWidth = 2
        if key == arcade.key.D:
            self.D = False
            for i in self.listOfKeys:
                if i.type == 3:
                    i.lineWidth = 2
        if key == arcade.key.F:
            self.F = False
            for i in self.listOfKeys:
                if i.type == 4:
                    i.lineWidth = 2
        if key == arcade.key.ENTER:
            self.ENTER = False

    def CheckInput(self):
        if self.A:
            for i in self.listOfKeys:
                if i.type == 1:
                    if self.ENTER:
                        i.DetectCollision()
                    i.lineWidth = 4
        if self.S:
            for i in self.listOfKeys:
                if i.type == 2:
                    if self.ENTER:
                        i.DetectCollision()
                    i.lineWidth = 4
        if self.D:
            for i in self.listOfKeys:
                if i.type == 3:
                    if self.ENTER:
                        i.DetectCollision()
                    i.lineWidth = 4
        if self.F:
            for i in self.listOfKeys:
                if i.type == 4:
                    if self.ENTER:
                        i.DetectCollision()
                    i.lineWidth = 4

    def DrawLives(self):
        if self.playerLives <= 0:
            self.playerLives = 0
            if not self.death:
                self.death = True
                self.finalScore = self.score
            self.score = self.finalScore
            for i in self.listOfNotes:
                self.i.remove(i)
            arcade.draw_text("Game Over", windowWidth / 4, windowHeight / 2.1, arcade.color.YELLOW, 96)
            arcade.draw_text("Final score: " +
                             str(self.score), windowWidth / 3, windowHeight / 3, arcade.color.YELLOW, 56)
        arcade.draw_text("Health: " + str(self.playerLives), 0 + 50, windowHeight - 60, arcade.color.YELLOW, 50)
        arcade.draw_text("Score: " + str(self.score), windowWidth - 400, windowHeight - 60, arcade.color.YELLOW, 50)
        #arcade.draw_text("missed hits: " + str(self.missedHits), windowWidth - 600, windowHeight - 120, arcade.color.YELLOW, 50)


class Key:
    def __init__(self, type):
        self.radius = 21
        self.type = type
        self.lineWidth = 2

        self.xPos = (windowWidth / 5) * self.type
        self.yPos = windowHeight / 7

        self.distance = 0

        if self.type == 1:
            self.color = arcade.color.RED
        if self.type == 2:
            self.color = arcade.color.BLUE
        if self.type == 3:
            self.color = arcade.color.GREEN
        if self.type == 4:
            self.color = arcade.color.YELLOW

    def Draw(self):
        arcade.draw_circle_outline(self.xPos, self.yPos, self.radius, self.color, self.lineWidth)

    def DetectCollision(self):
        touching = 0
        for note in theObjectToRuleThemAll.listOfNotes:
            if note:
                self.distance = math.sqrt(((self.xPos + self.radius)
                                          - (note.x + note.r)) ** 2 + ((self.yPos + self.radius) - (note.y + note.r)) ** 2)
                if isinstance(note, ShortNote):
                    if self.distance < note.r + self.radius:
                        theObjectToRuleThemAll.score += int(1000 / self.distance)
                        note.Destroy()
                        touching += 1
                if isinstance(note, LongNote):
                    if self.distance < note.r + self.radius:
                        theObjectToRuleThemAll.score += int(1000 / self.distance)
                        note.IsHit()
        if touching == 0:
            theObjectToRuleThemAll.missedHits += 1


class ShortNote:

    def __init__(self, x, y, type, speed):
        self.x = x
        self.y = y
        self.r = 20
        self.type = type
        self.speed = speed

        if self.type == 1:
            self.color = arcade.color.RED
        if self.type == 2:
            self.color = arcade.color.BLUE
        if self.type == 3:
            self.color = arcade.color.GREEN
        if self.type == 4:
            self.color = arcade.color.YELLOW

    def Move(self, delta_time):
        self.y = self.y - self.speed * delta_time * 60
        if self.y + self.r < 0:
            self.Destroy()
            theObjectToRuleThemAll.playerLives -= 1
            if theObjectToRuleThemAll.playerLives == 0:
                theObjectToRuleThemAll.death = True

    def Draw(self):
        arcade.draw_circle_filled(self.x, self.y, self.r, self.color)

    def Destroy(self):
        theObjectToRuleThemAll.listOfNotes.remove(self)


class LongNote:

    def __init__(self, x, y, type, speed, length):
        self.x = x
        self.y = y
        self.r = 20
        self.speed = speed
        self.type = type
        self.length = length
        self.hit = False

        if self.type == 1:
            self.color = arcade.color.RED
        if self.type == 2:
            self.color = arcade.color.BLUE
        if self.type == 3:
            self.color = arcade.color.GREEN
        if self.type == 4:
            self.color = arcade.color.YELLOW

    def Move(self, delta_time): # NOT DONE
        self.y = self.y - self.speed * delta_time * 60
        '''if self.length + self.r < 0:
            self.Destroy()
            theObjectToRuleThemAll.playerLives -= 1
            if theObjectToRuleThemAll.playerLives == 0:
                theObjectToRuleThemAll.death = True'''

    def Draw(self):
        if not self.hit:
            arcade.draw_circle_filled(self.x, self.y, self.r, self.color)
        arcade.draw_rectangle_filled(self.x, self.y + self.length / 2, self.r, self.length, self.color)

    def IsHit(self):
        self.hit = True
        if self.y < windowHeight / 7:
            self.length -= self.speed
            if self.length < self.speed:
                theObjectToRuleThemAll.listOfNotes.remove(self)


class Song:

    def __init__(self, song):

        if song == 'Megalovania_Hard':
            self.songFormula = [['s', 1], ['s', 1], ['s', 4], ['p'], ['s', 4],
                                ['p'], ['p'], ['p'], ['s', 2], ['p'], ['s', 2], ['p'], ['s', 1],
                                ['p'], ['s', 2], ['s', 3], ['s', 2], ]

        if song == 'Megalovania_Medium':
            self.nS = 10
            self.tempo = 7.45
            self.tI = 1.5
            self.fM = 3
            h = self.nS * self.tempo * self.fM
            self.songFormula = [['s', 1],
                                ['s', 4], ['s', 4], ['p'], ['s', 2], ['s', 2], ['s', 1], ['s', 3], ['s', 1],
                                ['s', 4], ['s', 4], ['p'], ['s', 2], ['s', 2], ['s', 1], ['s', 3], ['s', 1],
                                ['s', 4], ['s', 4], ['p'], ['s', 2], ['s', 2], ['s', 1], ['s', 3], ['s', 1],
                                ['s', 4], ['s', 4], ['p'], ['s', 2], ['s', 2], ['s', 1], ['s', 3], ['s', 1],
                                ['s', 4], ['s', 4], ['p'], ['s', 2], ['s', 2], ['s', 1], ['s', 3], ['s', 1],
                                ['s', 4], ['s', 4], ['p'], ['s', 2], ['s', 2], ['s', 1], ['s', 3], ['s', 1],
                                ['s', 4], ['s', 4], ['p'], ['s', 2], ['s', 2], ['s', 1], ['s', 3], ['s', 1],
                                ['s', 4], ['s', 4], ['p'], ['s', 2], ['s', 2], ['s', 1], ['s', 3], ['s', 1],

                                [2,['s',3],['s',4]],[2,['s',3],['s',4]],['p'],[2,['s',1],['s',3]],[2,['s',1],['s',3]],[2,['s',1],['s',2]],[2,['s',2],['s',3]],['s', 1],
                                [2,['s',3],['s',4]],[2,['s',3],['s',4]],['p'],[2,['s',1],['s',3]],[2,['s',1],['s',3]],[2,['s',1],['s',2]],[2,['s',2],['s',3]],['s', 1],
                                [2,['s',3],['s',4]],[2,['s',3],['s',4]],['p'],[2,['s',1],['s',3]],[2,['s',1],['s',3]],[2,['s',1],['s',2]],[2,['s',2],['s',3]],['s', 1],
                                [2,['s',3],['s',4]],[2,['s',3],['s',4]],['p'],[2,['s',1],['s',3]],[2,['s',1],['s',3]],[2,['s',1],['s',2]],[2,['s',2],['s',3]],['s', 1],
                                [2,['s',3],['s',4]],[2,['s',3],['s',4]],['p'],[2,['s',1],['s',3]],[2,['s',1],['s',3]],[2,['s',1],['s',2]],[2,['s',2],['s',3]],['s', 1],
                                [2,['s',3],['s',4]],[2,['s',3],['s',4]],['p'],[2,['s',1],['s',3]],[2,['s',1],['s',3]],[2,['s',1],['s',2]],[2,['s',2],['s',3]],['s', 1],
                                [2,['s',3],['s',4]],[2,['s',3],['s',4]],['p'],[2,['s',1],['s',3]],[2,['s',1],['s',3]],[2,['s',1],['s',2]],[2,['s',2],['s',3]],['s', 1],
                                [2,['s',3],['s',4]],[2,['s',3],['s',4]],['p'],[2,['s',1],['s',3]],[2,['s',1],['s',3]],[2,['s',1],['s',2]],[2,['s',2],['s',3]],['s', 1],
                                ['p'], ['p'], ['p'], ['p'], ['p'],
                                ['l', 3, h], ['p'], ['p'], ['p'], ['p'], ['p']]

    def GetNextNote(self):
        var = 4
        if self.songFormula.__len__() > 0:
            var = self.songFormula.pop(0)
            if var[0] == 's':
                return ShortNote(windowWidth / 5 * var[1], windowHeight, var[1], theObjectToRuleThemAll.noteSpeed), None, None
            if var[0] == 'l':
                return LongNote(windowWidth / 5 * var[1], windowHeight, var[1], theObjectToRuleThemAll.noteSpeed, var[2]), None, None
            if var[0] == 'p':
                return False, None, None
            if var[0] == 2:
                return 2, ShortNote(windowWidth / 5 * var[1][1], windowHeight, var[1][1], theObjectToRuleThemAll.noteSpeed),\
                            ShortNote(windowWidth / 5 * var[2][1], windowHeight, var[2][1], theObjectToRuleThemAll.noteSpeed)
        else:
            var = random.randint(1, 5)
            if var == 1 or var == 2 or var == 3 or var == 4:
                return ShortNote(windowWidth/5*var, windowHeight, var, theObjectToRuleThemAll.noteSpeed), None, None
            else:
                return False, None, None


theObjectToRuleThemAll = Window(windowWidth, windowHeight, "Game Window")

arcade.run()
