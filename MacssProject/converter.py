import numpy as np
import xml.etree.ElementTree as ET
import collections
from music21 import note, stream, chord

class Converter:
    def __init__(self, notes_array):
        self.notes_array = notes_array
        self.converted_song = stream.Stream()
        self.converter()
    
    def converter(self):
        length_dic = {'whole': 4.0, 'half':2.0, 'quarter': 1.0, 'eighth': 0.5, '16th': 0.25}
        for sound_object in self.notes_array:
            raw_note = sound_object[0]
            octave = sound_object[1]
            quarter_length = length_dic[(sound_object[2])]
            accidental = sound_object[3]

            if raw_note is None:
                self.converted_song.append(note.Rest(quarterLength = quarter_length))
            else:
                if accidental is not None:
                    new_note = str(raw_note) + str(accidental) + str(octave)
                else:
                    new_note = str(raw_note) + str(octave)
                self.converted_song.append(note.Note(new_note, quarterLength = quarter_length))
        
        # self.converted_song.show()
        self.converted_song.write('musicxml', fp='test2.xml')
