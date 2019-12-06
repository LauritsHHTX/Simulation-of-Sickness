import arcade

class Note:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.r = 5

    def Move(self):
        self.y = self.y - 5

    def Draw(self):
        arcade.draw_circle_filled(self.x, self.y, self.r, arcade.color.ROYAL_PURPLE)

    def Destroy(self):
        theObjectToRuleThemAll.song.listOfNotes.remove(self)
