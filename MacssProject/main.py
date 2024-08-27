import parser
import generator
import converter

data_parser = parser.Parser("My_heart_will_go_on_flute.musicxml")
sounds_list = data_parser.sounds_list
states_list = data_parser.states_list
transition_matrix = data_parser.transition_matrix
initial_vector = data_parser.initial_vector

music_generator = generator.Generator(sounds_list, states_list, transition_matrix, initial_vector)
music_converter = converter.Converter(music_generator.new_song)
