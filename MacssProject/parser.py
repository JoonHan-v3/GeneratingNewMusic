import numpy as np
import xml.etree.ElementTree as ET
import collections

class Parser:
    def __init__(self, filename):
        self.filename = filename
        self.root = ET.parse(filename).getroot()

        self.states_dict = collections.OrderedDict()
        self.states_list = []
        self.sounds_list = []

        self.initial_vector = []
        self.transition_matrix = []
        self.tempo = None

        self.parse()
        self.build_transition_matrix()
        self.build_initial_vector()

    def parse(self):
        direction_blocks = self.root.find('part').find('measure').findall('direction')
        for direction_block in direction_blocks:
            if self.tempo is None and direction_block.find('sound') is not None and 'tempo' in direction_block.find('sound').attrib:
                self.tempo = int(direction_block.find('sound').attrib['tempo'])

        self.build_sound_dict_and_list()

    def build_sound_dict_and_list(self):
        note = None
        octave = None
        duration = None
        accidental = None
        sound_object = []

        for i, part in enumerate(self.root.findall('part')):
            for j, measure in enumerate(part.findall('measure')):
                for k, note_info in enumerate(measure.findall('note')):
                    # sets note and octave
                    if note_info.find('pitch') is not None:
                        note = note_info.find('pitch').find('step').text
                        octave = (note_info.find('pitch').find('octave')).text
                    else:
                        note = None 
                        octave = None
                    
                    # sets duration
                    duration = note_info.find('type').text

                    # sets accidental
                    if note_info.find('accidental') is None:
                        accidental = None
                    else:
                        if note_info.find('accidental').text == 'flat':
                            accidental = 'b'
                        elif note_info.find('accidental').text == 'sharp':
                            accidental = '#'

                    # creates sound object
                    sound_object = (note, octave, duration, accidental)
                   
                    # adds sound_object to state_list
                    if sound_object not in self.states_list:
                        self.states_list.append(sound_object)

                    #adds sound_object to sounds_dict
                    if sound_object not in self.states_dict:
                        self.states_dict[sound_object] = 1
                    else:
                        self.states_dict[sound_object] += 1

                    # adds sound_object to sounds_list
                    self.sounds_list.append(sound_object)

    def build_transition_matrix(self):
        for i in range(len(self.states_list)):
            state_transition_matrix = []
            for j in range(len(self.states_list)):
                frequency = 0
                for k in range(len(self.sounds_list) - 1):
                    if self.sounds_list[k] == self.states_list[i] and self.sounds_list[k + 1] == self.states_list[j]:
                        frequency += 1
                state_transition_matrix.append(frequency)
            state_transition_matrix /= np.sum(state_transition_matrix)
            state_transition_matrix = np.cumsum(state_transition_matrix)
            self.transition_matrix.append(state_transition_matrix)

    def build_initial_vector(self):
        for value in self.states_dict.values():
            self.initial_vector.append(value)

        sum= np.sum(self.initial_vector)
        self.initial_vector /= sum
        self.initial_vector = np.cumsum(self.initial_vector)

# parser = Parser('My_heart_will_go_on_flute.musicxml')
# # print(len(parser.states_dict))
# # print(len(parser.states_list))
# print(parser.initial_vector)
