import mido

# Instantiate a MIDI file object
mid = mido.MidiFile()

# Add a track to the MIDI file
track = mido.MidiTrack()
mid.tracks.append(track)

# Add a note on and note off message to the track
note_on = mido.Message('note_on', note=60, velocity=64, time=0)
note_off = mido.Message('note_off', note=60, velocity=64, time=500)
track.append(note_on)
track.append(note_off)

# Save the MIDI file
mid.save('example1.mid')

'''
여기서 note_on 이벤트는 노트를 켜는 이벤트이며, 노트 번호(note)와 
소리 크기(velocity)를 지정해줍니다. note_off 이벤트는 노트를 끄는 이벤트이며,
 note_on 이벤트와 동일한 노트 번호와 소리 크기를 가지며, time 값을 통해 
 이벤트 간의 시간 간격을 설정합니다.'''