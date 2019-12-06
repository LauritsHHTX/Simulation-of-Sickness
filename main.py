import arcade

windowWidth = 900
windowHeight = 600



class MitSpilKlasse(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title) # Call the parent class's init function


    def update(self, delta_time):
        pass

    def on_draw(self):
        pass


mitVindue = MitSpilKlasse(windowWidth, windowHeight, "Mit vindue")

arcade.run()
