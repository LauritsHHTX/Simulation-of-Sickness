import note
import random
import main

class Song:

    def __init__(self):
        self.listOfNotes = []
        self.listOfNotes.append(note.Note())

    def DrawNotes(self):
        for i in self.listOfNotes:
            i.Draw()

    def CreateNotes(self):
        var = random.randint(1, 4)
        self.listOfNotes.append(note.Note(main.windowWidth/4*var, main.windowHeight))

