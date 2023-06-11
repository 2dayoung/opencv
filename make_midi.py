import mido

# Instantiate a MIDI file object
mid = mido.MidiFile() # 이거 반복문 안에 넣으면 한음만 출력, 밖에 내놓으면 화음 출력 됨 

for note in [60, 62, 64, 65, 67, 69, 71,72,74,76]:
    
    # Add a track to the MIDI file
    track = mido.MidiTrack()
    mid.tracks.append(track)

    note_on = mido.Message('note_on', note=note, velocity=64, time=0)
    note_off = mido.Message('note_off', note=note, velocity=64, time=1000)
    track.append(note_on)
    track.append(note_off)

    filename = str(note) + '.mid'

    # Save the MIDI file
    mid.save(filename)


'''
여기서 note_on 이벤트는 노트를 켜는 이벤트이며, 노트 번호(note)와 
소리 크기(velocity)를 지정해줍니다. note_off 이벤트는 노트를 끄는 이벤트이며,
 note_on 이벤트와 동일한 노트 번호와 소리 크기를 가지며, time 값을 통해 
 이벤트 간의 시간 간격을 설정합니다.'''
