import arcade
import note

class Song:

    def __init__(self):
        self.listOfNotes = []

    def DrawNotes(self):
        for i in self.listOfNotes:
            i.Draw()
