import arcade
import note

class Song:

    def __init__(self):
        self.listOfNotes = []
        self.listOfNotes.append(note.Note())

    def DrawNotes(self):
        for i in self.listOfNotes:
            i.Draw()

    def CreateNotes

