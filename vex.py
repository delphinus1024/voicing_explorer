# -*- coding: utf-8 -*-
# Make all voicing possibilities

import itertools
import sys
import argparse
from music21 import *
from enum import Enum
import scale

# choose your favorite
inst = instrument.StringInstrument()
#inst = instrument.Vocalist()
#inst = instrument.Piano()

# default number of voices
voices = 5

# pitch limit
highend = 88

# default sort method
sort_item = "INTERVAL"
sort_reverse = 0

# duration of each chord
note_len    = 4

# interval sizes
INTERVAL_SMALL  = 0
INTERVAL_MEDIUM = 1
INTERVAL_BIG    = 2
INTERVAL_ALL    = 3
INTERVAL_NAME = ["S","M","B","ALL"]

# element filters
filter_top  = -1
filter_bottom  = -1
filter_maj7 = 0
filter_pd = 0
filter_cons = 0
filter_interval = INTERVAL_SMALL

class Voicing:
    def __init__(self, valid, element):
    
        self.min2 = self.count_interval(ret,1)
        self.maj2 = self.count_interval(ret,2)
        self.min3 = self.count_interval(ret,3)
        self.maj3 = self.count_interval(ret,4)
        self.p4 = self.count_interval(ret,5)
        self.aug4 = self.count_interval(ret,6)
        self.p5 = self.count_interval(ret,7)
        self.min6 = self.count_interval(ret,8)
        self.maj6 = self.count_interval(ret,9)
        self.min7 = self.count_interval(ret,10)
        self.maj7 = self.count_interval(ret,11)
        self.min9 = self.count_interval(ret,13)
        
        # calc consonance,dissonance
        self.pd = self.min2 + self.maj7
        self.sd = self.maj2 + self.min7 + self.p4 + self.p5 + self.aug4
        self.cons = self.min3 + self.maj3 + self.min6 + self.maj6
        
        self.valid = valid
        self.element = element
        
        # interval size
        interval = self.total_interval()
        
        if(interval <= 14):
            self.interval_size = INTERVAL_SMALL
            self.interval_name = INTERVAL_NAME[INTERVAL_SMALL]
        elif(interval <= 24):
            self.interval_size = INTERVAL_MEDIUM
            self.interval_name = INTERVAL_NAME[INTERVAL_MEDIUM]
        else:
            self.interval_size = INTERVAL_BIG
            self.interval_name = INTERVAL_NAME[INTERVAL_BIG]
        
    def __lt__(self, other):

        if sort_item == "INTERVAL":
            return self.total_interval() < other.total_interval()
        elif sort_item == "PD":
            return self.pd < other.pd  
        elif sort_item == "TOP_NOTE":
            return (self.element[-1] % 12) < (other.element[-1] % 12)
        elif sort_item == "BOTTOM_NOTE":
            return (self.element[0] % 12) < (other.element[0] % 12)
        elif sort_item == "MAJ7":
            return self.maj7 < other.maj7 
        elif sort_item == "SECOND":
            return (self.min2 + self.maj2) < (other.min2 + other.maj2)
        elif sort_item == "CONSONANCE":
            return self.cons < other.cons  
        elif sort_item == "P5":
            return self.p5 < other.p5  
                
        printf("Error: illegal sort type.");
        exit(-1)
        
    def count_interval(self,element,interval):
        count = 0
        
        for el in itertools.combinations(element, 2):
            if abs(el[0] - el[1]) == interval:
                count = count + 1
        return count
        
    def top_interval(self):
        interval = self.element[-1] - self.element[-2]
        return interval
        
    def bottom_interval(self):
        interval = self.element[1] - self.element[0]
        return interval
        
    def total_interval(self):
        interval = self.element[-1] - self.element[0]
        return interval
        
    def max_adj_interval(self):
        max_interval = 0
        bottom = 1
        prev = self.element[0]
        for e in self.element:
            if not bottom:
                if (e - prev) > max_interval:
                    max_interval = e - prev
            bottom = 0
            prev = e
        
        return max_interval
        
    def set_sort_priority(self,pri_list):
        sort_priority = pri_list
    
# check low interval limit, octave shifts if needed.
def check_lil(n_list):
    ngflag = 0
    modified = 0

    while (ngflag == 0) :
        #check low interval limits of below 3 notes
        if scale.lil_dict[n_list[1] - n_list[0]] > n_list[0]:
            n_list = [x + 12 for x in n_list]
            modified = 1

        if scale.lil_dict[n_list[2] - n_list[1]] > n_list[1]:
            n_list = [x + 12 for x in n_list]
            modified = 1
            
        if n_list[-1] >= highend:
            ngflag = 1

        if modified == 0:
            break
            
        modified = 0
        
    if(ngflag):
        return []
        
    #check double semitone and double 2 degree in lower register
    n_list_oct = [x+12 for x in n_list]
    n_list_ext = n_list + n_list_oct
    
    i = 0
    for x in n_list:
        if ((n_list_ext[i+1] - n_list_ext[i]) == 1) and ((n_list_ext[i+2] - n_list_ext[i + 1]) == 1):
            return []

        if ((n_list_ext[i+1] - n_list_ext[i]) <= 2) and ((n_list_ext[i+2] - n_list_ext[i + 1]) <= 2) and (n_list_ext[i+2] < 60):
            return []
            
        i = i + 1
    
    return n_list

# Make voicings
def make_voicings(element):
    current = -1
    newlist = []
    
    for x in element:
        x = x - 24
        while x <= current:
            x = x + 12
        newlist.append(x)
        current = x
    
    ngflag = 0
    modified = 0
    
    newlist = check_lil(newlist)
    
    return newlist

# you can add or modify voicing rules here
# current rules adopt herb pomeroy "line writing" rules.
def check_interval(element):
    valid = 1
    
    # make voicings
    v = Voicing(valid,element)
    
    # No 2nds, maj or min in top two voices
    # No aug 4th interval between top two voices
    interval = v.top_interval()
    if (interval < 3) or (interval == 6):
        valid = 0
    
    # Outside two voices a maj 7th or less
    interval = v.total_interval()
    if interval < 12:
        valid = 0
    
    # No b9 interval between any two notes, adjacent or non adjacent
    if v.min9:
        valid = 0
    
    # Do not separate adjacent voices by any more than a major 6th, preferabley a p5th, except between bottom two voices.
    interval = v.max_adj_interval()
    if interval > 9:
        valid = 0
    
    # user controled filter
    if filter_top >= 0:
        if (v.element[-1] % 12) != filter_top:
            v.valid = 0
        
    if filter_bottom >= 0:
        if (v.element[0] % 12) != filter_bottom:
            v.valid = 0
    
    if filter_maj7:
        if v.maj7 == 0:
            v.valid = 0
        
    if filter_pd:
        if v.pd == 0:
            v.valid = 0
        
    if filter_cons:
        if (v.pd != 0): # or (v.sd != 0):
            v.valid = 0
    
    if (filter_interval == INTERVAL_SMALL) and (v.interval_size != INTERVAL_SMALL):
        v.valid = 0
    
    if (filter_interval == INTERVAL_MEDIUM) and (v.interval_size != INTERVAL_MEDIUM):
        v.valid = 0
    
    if (filter_interval == INTERVAL_BIG) and (v.interval_size != INTERVAL_BIG):
        v.valid = 0
    
    if not valid:
        v.valid = 0
    
    return v

def sort_list(voicings):
    Voicing.sort_priority = sort_item

    return sorted(voicings,reverse=sort_reverse)

if __name__ == "__main__":
    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("root_name", help="Root note (C,C#,Db,D...)",type=str)    
    parser.add_argument("scale_name", help="Scale name (IONIAN,DORIAN...)",type=str)
    parser.add_argument("-t","--filter_top", help="Show only specified top note. (C,C#,Db,D...)",type=str,default="")
    parser.add_argument("-b","--filter_bottom", help="Show only specified bottom note. (C,C#,Db,D...)",type=str,default="")
    parser.add_argument("-m","--filter_maj7", help="Show only chord with maj7 inside.",type=int,default=0)
    parser.add_argument("-p","--filter_pd", help="Show only chord with pd.",type=int,default=0)
    parser.add_argument("-c","--filter_cons", help="Show only chord only consonance.",type=int,default=0)
    parser.add_argument("-i","--filter_interval", help="Show only specified interval size. (0:SMALL, 1:MEDIUM, 2:LARGE)",type=int,default=INTERVAL_ALL)
    parser.add_argument("-s","--sorting", help="Sort method. (INTERVAL,PD,TOP_NOTE,BOTTOM_NOTE,MAJ7,SECOND,CONSONANCE,P5)",type=str,default="INTERVAL")
    parser.add_argument("-r","--sort_reverse", help="Sorting reverse when set to 1.",type=int,default=0)
    parser.add_argument("-l","--length", help="Length of each chord.",type=float,default=4.0)
    parser.add_argument("-v","--voices", help="Number of voices.",type=int,default=5)
    
    args = parser.parse_args()
    
    # Calc note group
    if args.scale_name in scale.scales:
        scale_list = scale.scales[args.scale_name]
    else:
        print("Error: illegal scale name");
        exit(-1)

    if args.root_name in scale.note_name:
        root = scale.note_name[args.root_name]
    else:
        print("Error: illegal root note");
        exit(-1)
    
    if len(args.filter_top) != 0:
        if args.filter_top in scale.note_name:
            filter_top = scale.note_name[args.filter_top]
        else:
            print("Error: illegal top note");
            exit(-1)
        
    if len(args.filter_bottom) != 0:
        if args.filter_bottom in scale.note_name:
            filter_bottom = scale.note_name[args.filter_bottom]
        else:
            print("Error: illegal bottom note");
            exit(-1)
        
    filter_maj7 = args.filter_maj7
    filter_pd = args.filter_pd
    filter_cons = args.filter_cons
    filter_interval = args.filter_interval
    sort_item = args.sorting
    sort_reverse = args.sort_reverse
    note_len = args.length
    voices = args.voices
    
    if(note_len <= 0.) :
        print("Error: Note length must be > 0.");
        exit(-1)
        
    print("==== Info ====")
    print("Scale:",args.scale_name,",",scale_list)
    print("Root :",args.root_name,",",root)
    
    if filter_top >= 0:
        print("Filter Top:",filter_top)
        
    if filter_bottom >= 0:
        print("Filter Bottom:",filter_bottom)
        
    if filter_maj7 >= 0:
        print("Filter Maj7:",filter_maj7)
        
    if filter_pd >= 0:
        print("Filter PD:",filter_pd)
        
    if filter_cons >= 0:
        print("Filter Consonance:",filter_cons)
        
    if filter_interval >= 0:
        print("Filter Interval:",filter_interval)
        
    print("Sort:",sort_item)
    print("Sort reverse:",sort_reverse)
    print("Voices:",voices)
    print("==============")
    
    # Score caption
    caption = "Scale:" + args.scale_name + " Root:" + args.root_name + "\n"
    
    need_cr = False
    
    if filter_top >= 0:
        caption = caption + "Top: " + args.filter_top + " "
        need_cr = True
        
    if filter_bottom >= 0:
        caption = caption + " Btm: " + args.filter_bottom + " "
        need_cr = True
    
    if filter_maj7:
        caption = caption + " Maj7 only. "
        need_cr = True
    
    if filter_pd:
        caption = caption + "PD only. "
        need_cr = True
    
    if filter_cons:
        caption = caption + "CONS only. "
        need_cr = True
    
    if filter_interval:
        caption = caption + "ITVL:" + INTERVAL_NAME[filter_interval]
        need_cr = True
    
    if need_cr:
        caption = caption + "\n"
        
    caption = caption + "Sort:" + sort_item + " Rev:" + str(sort_reverse)
    
    midi_offset = 60 - (2*12) 
    
    scale_list = list(map(lambda x: x + root + midi_offset, scale_list)) 
    
    initial_sharp_scale = [scale.pitch_sharp[i % 12] for i in scale_list]
    initial_flat_scale = [scale.pitch_flat[i % 12] for i in scale_list]
    print("Initial Scale:",initial_sharp_scale, " or ",initial_flat_scale)
    
    if len(scale_list) < 3:
        print ("Number of notes > 2")
        exit(-1)
    
    ele_list = []
    
    # make all possibilities of voicings
    limit = 0
    for element in itertools.permutations(scale_list,voices): # len(scale_list)):
        ret=make_voicings(element)
        if len(ret) > 0:
            v= check_interval(ret)
            
            if v.valid:
                ele_list.append(v)
            
    # sort list in certain rules
    ele_list = sort_list(ele_list)
    
    if len(ele_list) == 0:
        print("No voicing available.")
        quit()
    
    # Create Score
    dur = duration.Duration(note_len) #4)
    
    stream1 = stream.Part()
    stream2 = stream.Part()
    
    stream1.append(inst)
    stream2.append(inst)
    
    tc = clef.TrebleClef()
    bc = clef.BassClef()
    
    stream1.append(tc)
    stream2.append(bc)
    
    # To piano staves
    for x in ele_list:
        # note information
        note_info1 = "m2:{} M2:{} p4:{} p5:{}".format(x.min2,x.maj2,x.p4,x.p5)
        note_info2 = "m7:{} +4:{} CO:{}".format(x.min7,x.aug4,x.cons)
        note_info3 = "iv:{} PD:{} SD:{} M7:{}".format(x.interval_name,x.pd,x.sd,x.maj7)
        note_info = note_info3 + "\n" + note_info1 + "\n" + note_info2
        
        x2 = [y for y in x.element if y >= 60]
        
        if len(x2):
            c=chord.Chord(x2)
            
        else:
            c=note.Rest()
            
        c.duration = dur
        stream1.append(c)

        x2 = [y for y in x.element if y < 60]
        if len(x2):
            c=chord.Chord(x2)
            c.addLyric(note_info)
        else:
            c=note.Rest()
            c.addLyric(note_info)

        c.duration = dur            
        stream2.append(c)
        
    mm1 = tempo.MetronomeMark(number=60)
    
    inst = instrument.StringInstrument()
    stream1.insert(inst)
    stream2.insert(inst)
    
    score = stream.Score()
    score.insert(0, metadata.Metadata())
    score.metadata.title = caption
    
    score.insert(0, stream1)
    score.insert(0, stream2)

    score.show('musicxml')

