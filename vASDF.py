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
        self.SPACE = False

        
        #debugging variables
        self.missedHits = 0

    def update(self, delta_time):
        self.DetectCollision(delta_time)
        #print(self.listOfNotes)
        if not self.death:
            for notes in self.listOfNotes:
                if notes:
                    for note in notes:
                        note.Move(delta_time)
                        if isinstance(note, ShortNote):
                            if note.y + note.r < 0 and notes.index(note) == 0:
                                self.listOfNotes.remove(notes)
                                self.RemoveLife()
                        else:
                            if note.col:
                                note.ContinuedCol(delta_time)
                            if note.y + note.r + note.length < 0:
                                self.listOfNotes.remove(notes)
                                self.RemoveLife()
            if self.temp >= self.tempo:
                self.listOfNotes.append(self.song.GetNextNote())
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
            for notes in self.listOfNotes:
                if notes:
                    for note in notes:
                        note.Draw()
            for key in self.listOfKeys:
                colBool = False
                for notes in self.listOfNotes:
                    if notes:
                        if isinstance(notes[0], LongNote) and notes[0].col and notes[0].type == key.type and key.pressed:
                            colBool = True
                key.Draw(colBool)
            self.DrawLives()

        if self.death:
            arcade.draw_text("GAME OVER", windowWidth - 600, windowHeight / 2, arcade.color.RED, 50)
            arcade.draw_text("Final score: " + str(self.score), windowWidth / 3, windowHeight / 3, arcade.color.YELLOW, 56)

    def Restart(self):
        self.death = False
        self.respawn = False

    def on_key_press(self, key, modifiers):
        if key == arcade.key.A:
            self.listOfKeys[0].Press()
        if key == arcade.key.S:
            self.listOfKeys[1].Press()
        if key == arcade.key.D:
            self.listOfKeys[2].Press()
        if key == arcade.key.F:
            self.listOfKeys[3].Press()

        if key == arcade.key.SPACE:
            self.SPACE = True

        if key == arcade.key.R and self.death:
            self.respawn = True

        if key == arcade.key.ESCAPE:
            sys.exit()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.A:
            self.listOfKeys[0].UnPress()
        if key == arcade.key.S:
            self.listOfKeys[1].UnPress()
        if key == arcade.key.D:
            self.listOfKeys[2].UnPress()
        if key == arcade.key.F:
            self.listOfKeys[3].UnPress()
        if key == arcade.key.SPACE:
            self.SPACE = False

    def DrawLives(self):
        if self.playerLives <= 0:
            self.playerLives = 0
            if not self.death:
                self.death = True
                self.finalScore = self.score
            self.score = self.finalScore
            for notes in self.listOfNotes:
                self.notes.remove(notes)
            arcade.draw_text("Game Over", windowWidth / 4, windowHeight / 2.1, arcade.color.YELLOW, 96)
            arcade.draw_text("Final score: " +
                             str(self.score), windowWidth / 3, windowHeight / 3, arcade.color.YELLOW, 56)
        arcade.draw_text("Health: " + str(self.playerLives), 0 + 50, windowHeight - 60, arcade.color.YELLOW, 50)
        arcade.draw_text("Score: " + str(self.score), windowWidth - 400, windowHeight - 60, arcade.color.YELLOW, 50)
        #arcade.draw_text("missed hits: " + str(self.missedHits), windowWidth - 600, windowHeight - 120, arcade.color.YELLOW, 50)

    def DetectCollision(self, delta_time):
        touching = 0
        nKeysPressed = 0
        for key in self.listOfKeys:
            if key.pressed:
                nKeysPressed += 1
        for key in self.listOfKeys:
            for notes in self.listOfNotes:
                if notes:
                    hits = 0
                    for note in notes:
                        distance = math.sqrt(((key.xPos + key.radius) - (note.x + note.r)) ** 2
                                             + ((key.yPos + key.radius) - (note.y + note.r)) ** 2)
                        if key.pressed:
                            if self.SPACE and distance < note.r + key.radius and nKeysPressed == notes.__len__():
                                if isinstance(note, ShortNote):
                                    note.Hit()
                                    touching += 1
                                    self.score += int(1000 / distance)
                                if isinstance(note, LongNote):
                                    if not note.col:
                                        self.score += int(1000 / distance)
                                        note.FirstCol()
                                        touching += 1

                        if isinstance(note, LongNote) and note.col and key.type == note.type:
                            if key.pressed:
                                self.score += 20
                            if note.length < key.radius:
                                self.listOfNotes.remove(notes)
                        if note.hit:
                            hits += 1
                    if hits == notes.__len__():
                        self.listOfNotes.remove(notes)
            if touching == 0:
                self.missedHits += 1

    def RemoveLife(self):
        theObjectToRuleThemAll.playerLives -= 1
        if theObjectToRuleThemAll.playerLives == 0:
            theObjectToRuleThemAll.death = True


class Key:
    def __init__(self, type):
        self.radius = 21
        self.type = type
        self.lineWidth = 2

        self.xPos = (windowWidth / 5) * self.type
        self.yPos = windowHeight / 7

        self.distance = 0

        self.pressed = False
        self.hit = False

        if self.type == 1:
            self.color = arcade.color.RED
        if self.type == 2:
            self.color = arcade.color.BLUE
        if self.type == 3:
            self.color = arcade.color.GREEN
        if self.type == 4:
            self.color = arcade.color.YELLOW

    def Draw(self, colBool):
        if self.pressed:
            arcade.draw_circle_outline(self.xPos, self.yPos, self.radius, self.color, 4)
        else:
            arcade.draw_circle_outline(self.xPos, self.yPos, self.radius, self.color, 2)
        if colBool:
            arcade.draw_circle_filled(self.xPos, self.yPos, self.radius, self.color)

    def Press(self):
        self.pressed = True

    def UnPress(self):
        self.pressed = False

    def Hit(self):
        self.hit = True

    def UnHit(self):
        self.hit = False


class ShortNote:

    def __init__(self, x, y, type, speed):
        self.x = x
        self.y = y
        self.r = 20
        self.type = type
        self.speed = speed
        self.hit = False

        if self.type == 1:
            self.color = arcade.color.RED
        if self.type == 2:
            self.color = arcade.color.BLUE
        if self.type == 3:
            self.color = arcade.color.GREEN
        if self.type == 4:
            self.color = arcade.color.YELLOW

    def Move(self, delta_time):
        self.y -= self.speed * delta_time * 60

    def Draw(self):
        arcade.draw_circle_filled(self.x, self.y, self.r, self.color)

    def Hit(self):
        self.hit = True


class LongNote:

    def __init__(self, x, y, type, speed, length):
        self.x = x
        self.y = y
        self.r = 20
        self.speed = speed
        self.type = type
        self.length = length
        self.hit = False
        self.col = False
        if self.type == 1:
            self.color = arcade.color.RED
        if self.type == 2:
            self.color = arcade.color.BLUE
        if self.type == 3:
            self.color = arcade.color.GREEN
        if self.type == 4:
            self.color = arcade.color.YELLOW

    def Move(self, delta_time):
        if not self.col:
            self.y -= self.speed * delta_time * 60

    def Draw(self):
        if not self.col:
            arcade.draw_circle_filled(self.x, self.y, self.r, self.color)
        arcade.draw_rectangle_filled(self.x, self.y + self.length / 2, self.r, self.length, self.color)
        #arcade.draw_text(str(self.length), self.x, self.y, (255, 255, 255))

    def FirstCol(self):
        self.col = True
        self.length += self.y - windowHeight / 7
        self.y = windowHeight / 7

    def ContinuedCol(self, delta_time):
        self.length -= self.speed * delta_time * 60

    def StopCol(self):
        self.col = False


class Song:

    def __init__(self, song):

        if song == 'Megalovania_Hard':
            self.songFormula = [['s', 1], ['s', 1], ['s', 4], ['p'], ['s', 4],
                                ['p'], ['p'], ['p'], ['s', 2], ['p'], ['s', 2], ['p'], ['s', 1],
                                ['p'], ['s', 2], ['s', 3], ['s', 2], ]

        if song == 'Megalovania_Medium':
            self.nS = 10
            self.tempo = 7.44
            self.tI = 1.5
            self.fM = 3
            h = self.nS * self.tempo * self.fM / 2 + 30
            self.songFormula = [['s', 1],
                                ['s', 4], ['s', 4], ['p'], ['s', 2], ['s', 2], ['l', 1, h], ['s', 3], ['s', 1],
                                ['s', 4], ['s', 4], ['p'], ['s', 2], ['s', 2], ['l', 1, h], ['s', 3], ['s', 1],
                                ['s', 4], ['s', 4], ['p'], ['s', 2], ['s', 2], ['l', 1, h], ['s', 3], ['s', 1],
                                ['s', 4], ['s', 4], ['p'], ['s', 2], ['s', 2], ['l', 1, h], ['s', 3], ['s', 1],
                                ['s', 4], ['s', 4], ['p'], ['s', 2], ['s', 2], ['l', 1, h], ['s', 3], ['s', 1],
                                ['s', 4], ['s', 4], ['p'], ['s', 2], ['s', 2], ['l', 1, h], ['s', 3], ['s', 1],
                                ['s', 4], ['s', 4], ['p'], ['s', 2], ['s', 2], ['l', 1, h], ['s', 3], ['s', 1],
                                ['s', 4], ['s', 4], ['p'], ['s', 2], ['s', 2], ['l', 1, h], ['s', 3], ['s', 1],

                                [2,['s',3],['s',4]],[2,['s',3],['s',4]],['p'],[2,['s',1],['s',3]],[2,['s',1],['s',3]],['l', 1, h],[2,['s',2],['s',3]],[2, ['s', 1], ['s', 2]],
                                [2,['s',3],['s',4]],[2,['s',3],['s',4]],['p'],[2,['s',1],['s',3]],[2,['s',1],['s',3]],['l', 1, h],[2,['s',2],['s',3]],[2, ['s', 1], ['s', 2]],
                                [2,['s',3],['s',4]],[2,['s',3],['s',4]],['p'],[2,['s',1],['s',3]],[2,['s',1],['s',3]],['l', 1, h],[2,['s',2],['s',3]],[2, ['s', 1], ['s', 2]],
                                [2,['s',3],['s',4]],[2,['s',3],['s',4]],['p'],[2,['s',1],['s',3]],[2,['s',1],['s',3]],['l', 1, h],[2,['s',2],['s',3]],[2, ['s', 1], ['s', 2]],
                                [2,['s',3],['s',4]],[2,['s',3],['s',4]],['p'],[2,['s',1],['s',3]],[2,['s',1],['s',3]],['l', 1, h],[2,['s',2],['s',3]],[2, ['s', 1], ['s', 2]],
                                [2,['s',3],['s',4]],[2,['s',3],['s',4]],['p'],[2,['s',1],['s',3]],[2,['s',1],['s',3]],['l', 1, h],[2,['s',2],['s',3]],[2, ['s', 1], ['s', 2]],
                                [2,['s',3],['s',4]],[2,['s',3],['s',4]],['p'],[2,['s',1],['s',3]],[2,['s',1],['s',3]],['l', 1, h],[2,['s',2],['s',3]],[2, ['s', 1], ['s', 2]],

                                [2,['s',3],['s',4]],[2,['s',3],['s',4]],['p'],[2,['s',1],['s',3]],[2,['s',1],['s',3]],['l', 1, h],[2,['s',2],['s',3]],

                                ['l', 3, h * 2], ['p'], ['s', 3], ['l', 2, h], ['s', 2], ['l', 1, h], ['s', 1], ['p'],
                                ['l', 3, h * 2], ['p'], ['s', 3], ['l', 4, h * 2], ['p'], ['s', 3], ['s', 1], ['p'],
                                ['l', 3, h * 2], ['p'], ['s', 3], ['s', 3], [2, ['s', 3], ['s', 4]], [2, ['s', 3], ['s', 4]], ['l', 4, h * 2], ['p'], ['s', 3], ['s', 3], ['s', 2], ['s', 3], ['l', 4, h * 2], ['p'], ['p'], ['p'],
                                ['l', 2, h], ['s', 2], ['l', 1, h], ['s', 1], ['l', 3, h], ['s', 3], ['l', 1, h * 2], ['p'],
                                ['l', 3, h], ['s', 3], ['l', 2, h], ['s', 2], ['l', 3, h * 2], ['p'], ['s', 3], ['s', 3],
                                ['l', 4, h], ['l', 3, h], ['l', 2, h], ['l', 1, h], ['l', 4, h], ['l', 3, h], ['l', 2, h], ['l', 1, h],
                                ['l', 3, h * 2], ['p'], ['s', 3], ['s', 3],  ['l', 4, h * 4], ['p'], ['p'], ['p'], ['p'], ['p'], ['p'], ['p'],
                                ['s', 1], ['s', 4], ['s', 2], ['s', 4], ['l', 3, h], ['s', 2,], ['l', 3, h * 2], ['p'], ['p'],



                                ['p'], ['p'], ['p'], ['p'], ['p'], ['p'], ['p'], ['p'], ['p'], ['p'], ['p'], ['p'], ['p'], ['p'], ['p'], ['p'], ['p'], ['p'], ['p'], ['p'], ['p'], ['p'], ['p'], ['p'], ['p'],['p'], ['p'], ['p'], ['p'], ['p'], ['p'], ['p'], ['p'], ['p'], ['p'], ['p'], ['p'], ['p'],]

    def GetNextNote(self):
        var = 4
        if self.songFormula.__len__() > 0:
            var = self.songFormula.pop(0)
            if var[0] == 's':
                return [ShortNote(windowWidth / 5 * var[1], windowHeight, var[1], theObjectToRuleThemAll.noteSpeed)]
            if var[0] == 'l':
                return [LongNote(windowWidth / 5 * var[1], windowHeight, var[1], theObjectToRuleThemAll.noteSpeed, var[2])]
            if var[0] == 'p':
                return False
            if var[0] == 2:
                return [ShortNote(windowWidth / 5 * var[1][1], windowHeight, var[1][1], theObjectToRuleThemAll.noteSpeed),
                        ShortNote(windowWidth / 5 * var[2][1], windowHeight, var[2][1], theObjectToRuleThemAll.noteSpeed)]
        else:
            var = random.randint(1, 5)
            if var == 1 or var == 2 or var == 3 or var == 4:
                return [ShortNote(windowWidth/5*var, windowHeight, var, theObjectToRuleThemAll.noteSpeed)]
            else:
                return False


theObjectToRuleThemAll = Window(windowWidth, windowHeight, "Game Window")

arcade.run()
