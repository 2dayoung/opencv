import mido



# open MIDI file
mid = mido.MidiFile('60.mid')

# open MIDI output port
outport = mido.open_output()

# play MIDI messages
for message in mid.play():
    outport.send(message)
