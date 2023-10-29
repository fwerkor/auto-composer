import os
from midiutil import MIDIFile
import music21
import json
import collections

# 分析midi文件中的和弦
def analyze_chords(midi_files):
    chords = [] 
    transition_pairs = []
    for i in range(len(chords)-1):
        from_chord = chords[i]  
        to_chord = chords[i+1]
        transition_pairs.append( (from_chord, to_chord) )
    
    transitions = {}
    
    # 分析过程 
    
    for t in transition_pairs:
        from_chord, to_chord = t
        
        if from_chord not in transitions:
            transitions[from_chord] = {}
        
        if to_chord not in transitions[from_chord]:
            transitions[from_chord][to_chord] = 0
            
        transitions[from_chord][to_chord] += 1

    return chords, transitions

# 根据分析结果生成配置    
def generate_config(chords, transitions):

    config = {
        "chord_probs": {},
        "chord_start_probs": {} 
    }

    # 填充chord_probs
    for k, v in transitions.items():
        config["chord_probs"][k] = v
    
    # 填充chord_start_probs 
    counts = collections.Counter(chords)
    for chord, count in counts.items():
        config["chord_start_probs"][chord] = count / len(chords)

    return config

if __name__ == "__main__":
    
    # 待分析的midi文件
    midi_files = [f for f in os.listdir('resources') if f.endswith('.mid')]
    
    # 分析和弦
    chords, transitions = analyze_chords(midi_files)  
    
    # 生成配置
    config = generate_config(chords, transitions)
    
    # 保存配置文件
    with open('config-output.json', 'w') as f:
        json.dump(config, f, indent=4)