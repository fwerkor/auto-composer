import random
from midiutil.MidiFile import MIDIFile, MIDITrack
import json
import midiutil


#读取配置文件
config_file = 'config.json'
with open(config_file) as f:
  config = json.load(f)
chords = config['chords']
chord_probs = config['chord_probs']
chord_start_probs = config['chord_start_probs']
styles = config['styles']
paras = config['paras']
melody_length = config['melody_length']
instruments = config['instruments']
num_melodies = config['num_melodies']
parts = config['parts']
harmony_duration = config['harmony_duration']
harmonic_progressions = config['harmonic_progressions']



song = MIDIFile(len(instruments))
time=0.0
melodies=[]
txt_output=''

track=0
for instrument in instruments.keys():#instrument中：种类(1或2或3),MIDI音色编号,channel,basic_volume,动态值
    song.addProgramChange(track,instruments[instrument][2],0,instruments[instrument][1])#track,channel,time,program
    #此处有待添加对每个track的备注
    track+=1










# 选择和弦
def choose_chord(last_chord):
  if last_chord in chord_probs:
     probs = chord_probs[last_chord]
     next_chords = list(probs.keys())
     next_chord = random.choices(next_chords, weights=probs.values())[0]
     chord_probs[last_chord][next_chord]*=2
     return next_chord
  else:
     return random.choices(list(chord_start_probs.keys()), weights=chord_start_probs.values())[0]

# 生成旋律
def generate_melody():
    melody=[]
    last_chord = 'None'
    durations = random.choice(list(styles.values()))
    for i in range(melody_length):
        chord = choose_chord(last_chord)
        last_chord = chord
        duration =durations[i%len(durations)]
        if (i%len(durations))%2==0:
            volume=random.choice(range(-2,3))+15-(i%len(durations)-1)
        else:
            volume=random.choice(range(-1,2))
        melody.append([chord,duration,volume])
    return melody
    
#根据乐器种类写入音符
def write_notes(instrument_type,track,channel,chord,time_temp,duration,volume):
    global txt_output
    global song
    txt_output+=str([list(instruments.keys())[track],channel,chord,time_temp,duration,volume])+'\n'
    if instrument_type==1:
        for note in chords[chord]:
            song.addNote(track,channel, note, time_temp, duration, volume)
    if instrument_type==2:
        note=chords[chord][0]
        song.addNote(track,channel, note, time_temp, duration, volume)
    if instrument_type==3:
        song.addNote(track,channel, 60, time_temp, duration, volume)
        
    
def generate_para(endtime,channels):
    global time
    correct_endtime=endtime
    for channel in channels:
        time_temp=time
        if channel in parts["main_melody"]:
            the_channel_instruments=[]
            for instrument in instruments.keys():
                if instruments[instrument][2]==channel:
                    the_channel_instruments.append(instrument)
            while time_temp<=endtime:
                weights=[]
                for i in range(1,num_melodies+1):
                    weights.append(1/i)
                melody_id=random.choices(range(num_melodies),weights=weights)[0]
                melody=melodies[melody_id]
                for element in melody:
                    for instrument in the_channel_instruments:
                        write_notes(instruments[instrument][0],list(instruments.keys()).index(instrument),channel,element[0],time_temp,element[1],instruments[instrument][3]+element[2])
                    time_temp+=element[1]
            correct_endtime=max(correct_endtime,time_temp)
        if channel in parts["harmony"]:
            harmonic_progression=random.choice(list(harmonic_progressions.keys()))
            i=0
            while time_temp<=endtime:
                for instrument in instruments.keys():
                    if instruments[instrument][2]==channel:
                        chord=harmonic_progressions[harmonic_progression][i%len(harmonic_progressions[harmonic_progression])]
                        write_notes(instruments[instrument][0],list(instruments.keys()).index(instrument),channel,chord,time_temp,harmony_duration,instruments[instrument][3])
                time_temp+=harmony_duration
                i+=1
            correct_endtime=max(correct_endtime,time_temp)
        #此处有待添加其它声部=
    time=correct_endtime


# 生成歌曲
this_para=0
for i in range(num_melodies):
    melodies.append(generate_melody())
for para_name, para_info in paras.items():#para_info中：endtime,channels
    generate_para(para_info[0], para_info[1]) 


with open('notes.txt', 'w') as outfile:
    outfile.write(txt_output) 
with open('song.mid', 'wb') as outfile:
    song.writeFile(outfile)
from midi2audio import FluidSynth
fs = FluidSynth('')
fs.midi_to_audio('song.mid', 'song.wav')