import arcade
import song

windowWidth = 900
windowHeight = 600



class Window(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title) # Call the parent class's init function
        self.song = song.Song


    def update(self, delta_time):
        pass

    def on_draw(self):
        pass

    def OnKeyPress(self):
        pass


theObjectToRuleThemAll = Window(windowWidth, windowHeight, "Mit vindue")

arcade.run()
