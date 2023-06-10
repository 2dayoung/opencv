import pyaudio
import mido
import struct

# MIDI 파일 로드
midi_file = "sample135.mid"

# PyAudio 초기화
p = pyaudio.PyAudio()

# Stream 열기
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=44100,
                output=True)

# MIDI 파일 재생
with mido.midifiles.MidiFile(midi_file) as midi:
    for msg in midi.play():
        if msg.type == 'note_on' or msg.type == 'note_off':
            # 메시지를 MIDI 신호로 변환
            note = msg.note
            velocity = msg.velocity
            duration = msg.time

            # MIDI 신호를 오디오 신호로 변환
            frequency = 440 * (2 ** ((note - 69) / 12))
            samples_per_cycle = int(stream.get_sample_rate() / frequency)
            samples = [velocity / 127.0 * 0.3 * (1 - i / samples_per_cycle % 1)
                       for i in range(samples_per_cycle * duration)]
            signal = b''.join([struct.pack('f', sample) for sample in samples])

            # 오디오 재생
            stream.write(signal)

# Stream 닫기
stream.stop_stream()
stream.close()

# PyAudio 종료
p.terminate()
