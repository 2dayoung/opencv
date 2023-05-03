import pygame.midi
import time

# Initialize Pygame and the MIDI module
pygame.init()
pygame.midi.init()

# Get the ID of the first output device
device_id = pygame.midi.get_default_output_id()

# Open the MIDI output port
output = pygame.midi.Output(device_id)

# Define a dictionary that maps note names to MIDI note numbers
notes = {'C': 60, 'D': 62, 'E': 64, 'F': 65, 'G': 67, 'A': 69, 'B': 71}

# Define a function to play a note
def play_note(note_name):
    # Convert the note name to a MIDI note number
    note_number = notes[note_name]
    # Create a note on message and send it to the output port
    note_on = [0x90, note_number, 127]
    output.write_short(*note_on)
    # Wait for a short time to simulate the duration of the note
    time.sleep(0.5)
    # Create a note off message and send it to the output port
    note_off = [0x80, note_number, 0]
    output.write_short(*note_off)

# Sample event data for testing
event_data = [1, 2, 3, 4]

# Play the notes corresponding to the event data
for event in event_data:
    if event == 1:
        play_note('C')
    elif event == 2:
        play_note('D')
    elif event == 3:
        play_note('E')
    elif event == 4:
        play_note('F')

# Close the MIDI output port and the Pygame module
output.close()
pygame.midi.quit()
