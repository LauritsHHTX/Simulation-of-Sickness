import arcade
import note

class Key:
    def __init__(self, type):
        self.radius = 5.5
        self.type = type
        
        if self.type == 1:
            self.color = arcade.color.RED
        if self.type == 2:
            self.color = arcade.color.PURPLE
        if self.type == 3:
            self.color = arcade.color.YANKEES_BLUE
        if self.type == 4:
            self.color = arcade.color.OLD_GOLD


    def Draw(self):
        pass

    def DetectCollision(self):
        pass