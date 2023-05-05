#midi로 화음 만들기 
import mido

# 미디 노트 이벤트 생성
c_note = mido.Message('note_on', note=60, velocity=64, time=0)
c_note_off = mido.Message('note_off', note=60, velocity=64, time=1000)
d_note = mido.Message('note_on', note=62, velocity=64, time=0)
d_note_off = mido.Message('note_off', note=62, velocity=64, time=1000)
e_note = mido.Message('note_on', note=64, velocity=64, time=0)
e_note_off = mido.Message('note_off', note=64, velocity=64, time=1000)
f_note = mido.Message('note_on', note=65, velocity=64, time=0)
f_note_off = mido.Message('note_off', note=65, velocity=64, time=1000)
g_note = mido.Message('note_on', note=67, velocity=64, time=0)
g_note_off = mido.Message('note_off', note=67, velocity=64, time=1000)
a_note = mido.Message('note_on', note=69, velocity=64, time=0)
a_note_off = mido.Message('note_off', note=69, velocity=64, time=1000)
b_note = mido.Message('note_on', note=71, velocity=64, time=0)
b_note_off = mido.Message('note_off', note=71, velocity=64, time=1000)

# 트랙 생성 및 미디 노트 이벤트 추가
track1 = mido.MidiTrack()
track1.append(mido.MetaMessage('track_name', name='Do'))
track1.extend([c_note, c_note_off])

track2 = mido.MidiTrack()
track2.append(mido.MetaMessage('track_name', name='Re'))
track2.extend([d_note, d_note_off])

track3 = mido.MidiTrack()
track3.append(mido.MetaMessage('track_name', name='Mi'))
track3.extend([e_note, e_note_off])

track4 = mido.MidiTrack()
track4.append(mido.MetaMessage('track_name', name='Fa'))
track4.extend([f_note, f_note_off])

track5 = mido.MidiTrack()
track5.append(mido.MetaMessage('track_name', name='Sol'))
track5.extend([g_note, g_note_off])

track6 = mido.MidiTrack()
track6.append(mido.MetaMessage('track_name', name='La'))
track6.extend([a_note, a_note_off])

track7 = mido.MidiTrack()
track7.append(mido.MetaMessage('track_name', name='Si'))
track7.extend([b_note, b_note_off])

# MIDI 파일 생성
midi_file = mido.MidiFile()
midi_file.tracks.extend([track1, track3, track5])
midi_file.save('sample135.mid')
