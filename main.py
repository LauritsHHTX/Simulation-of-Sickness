import arcade
import song
import key

windowWidth = 900
windowHeight = 600



class Window(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title) # Call the parent class's init function
        self.song = song.Song
        self.listOfKeys = []
        for i in range(1, 4):
            self.listOfKeys.append(key.Key(i))

    def update(self, delta_time):
        for i in self.song.listOfNotes:
            i.Move()
        self.song.CreateNotes()

    def on_draw(self):
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


theObjectToRuleThemAll = Window(windowWidth, windowHeight, "Mit vindue")

arcade.run()
