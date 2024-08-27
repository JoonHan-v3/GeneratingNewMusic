import random
import numpy as np

class Generator:
    def __init__(self, sounds_list, states_list, distribution_matrix, initial_vector):
        self.sounds_list = sounds_list
        self.states_list = states_list
        self.distribution_matrix = distribution_matrix
        self.initial_vector = initial_vector
        self.new_song = []

        self.generate_new_music()
        
    def generate_new_music(self):
        random_prob = random.uniform(0,1)
        sound = self.get_new_sound_object(random_prob, self.initial_vector)
        self.new_song.append(sound)

        for i in range(1, len(self.sounds_list)):
            row_index = self.get_index(sound, self.states_list)
            row = self.distribution_matrix[row_index]
            random_prob = random.uniform(0,1)
            sound = self.get_new_sound_object(random_prob, row)
            self.new_song.append(sound)
    
    def get_index(self, element, array):
        index = None
        for i in range(len(array)):
            if element == array[i]:
                index = i
        return index
    
    def get_new_sound_object(self, target, probs_array):
        index = None
        for i in range(len(probs_array)):
            if target <= probs_array[i]:
                print(target, probs_array[i-1])
                index = i  
                return self.states_list[index]
        