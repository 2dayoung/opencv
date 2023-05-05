
import threading
import time
import pygame

def play_music(filename):
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
      continue  

def do_something_else():
    
  print("Doing something else...")
  play_music('64.mid')
  time.sleep(1)

# Initialize pygame mixer
pygame.mixer.init()

midi_filename = []
notes = [60, 62, 64, 65, 67, 69, 71]
for i, note in enumerate(notes):    
    midi_filename.append(str(note) +'.mid')
    

  # Start playing music in a new thread
music_thread = threading.Thread(target=play_music, args=(midi_filename[0],))
music_thread.start()
music_thread.join()
music_thread1 = threading.Thread(target=play_music, args=(midi_filename[1],))
do_something_else()
music_thread1.start()

# Do something else in the main thread

do_something_else()
# Wait for the music to finish playing

music_thread1.join()
