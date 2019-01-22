note_name = {
    "C":0,
    "C#":1,
    "Db":1,
    "D":2,
    "D#":3,
    "Eb":3,
    "E":4,
    "F":5,
    "F#":6,
    "Gb":6,
    "G":7,
    "G#":8,
    "Ab":8,
    "A":9,
    "A#":10,
    "Bb":10,
    "B":11
    }

scales = {
    "IONIAN":  [0,2,4,7,9,11],
    "DORIAN": [0,2,3,5,7,10],
    "PHRYGIAN": [0,1,3,5,7,8,10],
    "LYDIAN": [0,4,6,7,9,11],
    "MIXOLYDIAN": [0,2,4,7,9,10],
    "AEORIAN": [0,2,3,5,7,10],
    "LOCRIAN": [0,3,5,6,8,10],
    "MELODIC-MINOR": [0,2,3,5,7,9,11],
    "DORIAN-b2": [0,1,3,5,7,9,10],
    "LYDIAN-AUGUMENTED": [0,2,4,6,8,9,11],
    "LYDIAN-b7": [0,2,4,6,7,9,10],
    "MIXOLYDIAN b6": [0,2,4,5,7,8,10],
    "AEORIAN-b5": [0,2,3,5,6,8,10],
    "SUPER-LOCRIAN": [0,1,3,4,6,8,10],
    "ALTERED": [0,1,3,4,6,8,10],
    "HARMONIC-MINOR": [0,2,3,5,7,8,11],
    "LOCRIAN-N6": [0,1,3,5,6,9,10],
    "IONIAN-5": [0,2,4,5,8,9,11],
    "DORIAN-4": [0,2,3,6,7,9,10],
    "PHRYGIAN-DOMINANT": [0,1,4,5,7,8,10],
    "LYDIAN-2": [0,3,4,6,7,9,11],
    "SUPER-LOCRIAN bb7": [0,1,3,4,6,8,9],
    "HARMONIC-MAJOR": [0,2,4,5,7,8,11],
    "DORIAN-b5": [0,2,3,5,6,9,10],
    "PHRYGIAN-b4": [0,1,3,4,7,8,10],
    "LYDIAN-b3": [0,2,3,6,7,9,11],
    "MIXOLYDIAN-b2": [0,1,4,5,7,9,10],
    "LYDIAN-AUGUMENTED 2": [0,3,4,6,8,9,11],
    "LOCRIAN-bb7": [0,1,3,5,6,8,9],
    "BLUES": [0,3,5,6,7,10],
    "PENTATONIC-MAJOR": [0,2,4,7,9],
    "PENTATONIC-MINOR": [0,3,5,7,10],
    "MAJOR-b2-PENTATONIC": [0,1,4,7,9],
    "MAJOR-b6-PENTATONIC": [0,2,4,7,8],
    "MINOR-6-PENTATONIC": [0,3,5,7,9],
    "MINOR-7b5 PENTATONIC": [0,3,5,6,10],
    "WHOLE-TONE PENTATONIC": [0,4,6,8,10],
    "BANSHIKI-CHO": [0,3,5,8,10],
    "HIRA-JOSHI": [0,2,3,7,8],
    "IWATO": [0,1,5,6,10],
    "KOKIN-JOSHI": [0,1,5,7,10],
    "KUMOI": [0,2,3,7,9],
    "NAKAZORA": [0,1,5,7,8],
    "PEROG": [0,1,3,7,8],
    "RITSU": [0,2,5,7,9],
    "RYUKYU": [0,4,5,7,11],
    "SHIMOCHIDORI": [0,4,6,7,11],
    "AUGUMENTED": [0,3,4,7,8,11],
    "HALF/WHOLE-DIMINISHED": [0,1,3,4,6,7,9,10],
    "WHOLE/HALF-DIMINISHED": [0,2,3,5,6,8,9,11],
    "WHOLE-TONE": [0,2,4,6,8,10],
    "BEBOP-DOMINANT": [0,2,4,5,7,9,10,11],
    "BEBOP-MAJOR": [0,2,4,5,7,8,9,11],
    "BEBOP-TONIC MINOR": [0,2,3,5,7,8,9,11],
    "BEBOP-MINOR": [0,2,3,5,7,8,9,10],
    "SPANISH-8-NOTE": [0,1,3,4,5,6,8,10],
    "ENIGMATIC": [0,1,4,6,8,10,11],
    "GYPSY": [0,2,3,6,7,8,10],
    "HUNGARIAN": [0,3,4,6,7,9,10],
    "HUNGARIAN-MINOR": [0,2,3,6,7,8,11],
    "LEADING-WHOLE-TONE": [0,2,4,6,8,10,11],
    "LYDIAN-MINOR": [0,2,4,6,7,8,10]
    }
    
lil = [
    [[52, 53],1],
    [[53, 51],2],
    [[51, 48],3],
    [[46, 50],4],
    [[51, 46],5],
    [[52, 46],6],
    [[34, 41],7],
    [[43, 51],8],
    [[41, 50],9],
    [[42, 51],10],
    [[41, 51],11],
    [[41, 52],12],
    [[40, 53],13],
    [[39, 53],14],
    [[36, 51],15],
    [[34, 50],16]
    ]

lil_dict = {1:52 ,2:51 ,3:48, 4:46, 5:46, 6:34, 7:43, 8:41, 9:42, 10:41, 11:41}

pitch_sharp = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
pitch_flat  = ["C","Db","D","Eb","E","F","Gb","G","Ab","A","Bb","B"]

def midi2notename(midi,acc = "#"):
    midi = int(midi)
    
    if acc == "#":
        ret = pitch_sharp[midi % 12] + str(int(midi/12))
    else:
        ret = pitch_flat [midi % 12] + str(int(midi/12))
    return ret
