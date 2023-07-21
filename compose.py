import random
from midiutil import MIDIFile
import json

#读取配置文件
config_file = 'config.json'
with open(config_file) as f:
  config = json.load(f)
chords = config['chords']
chord_probs = config['chord_probs']
chord_start_probs = config['chord_start_probs']

# 选择和弦
def choose_chord(last_chord):
  if last_chord in chord_probs:
     probs = chord_probs[last_chord]
     next_chords = list(probs.keys())
     next_chord = random.choices(next_chords, weights=probs.values())[0]
     return next_chord
  else:
     return random.choices(list(chord_start_probs.keys()), weights=chord_start_probs.values())[0]

# 生成旋律
def generate_melody(chord):
  notes = []
  root = chords[chord][0]
  last_note = root
  for i in range(64):
    step = random.choice([1, 3, 5])
    next_note = last_note + step
    notes.append(next_note)
    last_note = next_note
  return notes
  
# 生成歌曲
midi = MIDIFile(1)
last_chord = 'I'
i=0
while i<512:
  i+=1
  chord = choose_chord(last_chord)
  last_chord = chord
  melody = generate_melody(chord)
  for note in melody:
    midi.addNote(0, 0, note, i, 1, 100)

with open('song.mid', 'wb') as outfile:
  midi.writeFile(outfile)
