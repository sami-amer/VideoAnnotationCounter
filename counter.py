import sys
import pandas as pd
from collections import Counter
import pickle

def create_template_list(duration):
    return [0] * int(duration * 1000)

def get_end_time(file_input):
    with open(file_input, "r") as f:
        bTime = 0.0
        eTime = 0.0
        aTime = 0.0
        for line in f:
            line = line.split("\t")
            del line[1]
            line[-1] = line[-1].strip("\n")
            line[1] = float(line[1])
            line[2] = float(line[2])
            line[3] = float(line[3])
            if line[0] == "default":
                continue
            if (line[0] == "Behavioral_Engagement") and line[2] > bTime:
                bTime = line[2]
            elif line[0] == "Attention_Engagement" and line[2] > aTime:
                aTime = line[2]
            elif line[0] == "Emotional_Engagement" and line[2] > eTime:
                eTime = line[2]
    return bTime, aTime, eTime

def get_end_time_multiple(file_list):
    b,a,e = 0.0,0.0,0.0
    for f in file_list:
        b += get_end_time(f)[0]
        a += get_end_time(f)[1]
        e += get_end_time(f)[2]
    return b,a,e

def import_data_ms(file_name): # TODO: make this use data frames
    bTime, aTime, eTime = get_end_time(file_name)
    endtime = max([bTime, aTime, eTime])
    Behavioral_Engagement = [0] * int(endtime * 1000)
    Attention_Engagement = [0] * int(endtime * 1000)
    Emotional_Engagement = [0] * int(endtime * 1000)
    annotation_data = import_data_durations(file_name)

    labeled = {'behavior':Behavioral_Engagement,'attention':Attention_Engagement, 'emotion': Emotional_Engagement}
    ms_data = pd.DataFrame.from_dict(labeled)
    if len(annotation_data['on-task']) > 1:
        for elem in (annotation_data['on-task']): # way to loop this better
            start = int(1000 * (elem[0]))
            stop = int(1000 * (start + elem[1]) + 1)
            ms_data.loc[start:stop,'behavior'] = 2
    
    if len(annotation_data['off-tsak']) > 1:
        for elem in (annotation_data['off-tsak']):
            start = int(1000 * (elem[0]))
            stop = int(1000 * (start + elem[1]) + 1)
            ms_data.loc[start:stop,'behavior'] = 1
  
    if len(annotation_data['distarcted']) > 1:
        for elem in (annotation_data['distarcted']):
            start = int(1000 * (elem[0]))
            stop = int(1000 * (start + elem[1]) + 1)
            ms_data.loc[start:stop,'attention'] = 1

    if len(annotation_data['idle']) > 1:
        for elem in (annotation_data['idle']):
            start = int(1000 * (elem[0]))
            stop = int(1000 * (start + elem[1]) + 1)
            ms_data.loc[start:stop,'attention'] = 2

    if len(annotation_data['focused']) > 1:
        for elem in (annotation_data['focused']):
            start = int(1000 * (elem[0]))
            stop = int(1000 * (start + elem[1]) + 1)
            ms_data.loc[start:stop,'attention'] = 3
 
    if len(annotation_data['Bored']) > 1:
        for elem in (annotation_data['Bored']):
            start = int(1000 * (elem[0]))
            stop = int(1000 * (start + elem[1]) + 1)
            ms_data.loc[start:stop,'emotion'] = 1

    if len(annotation_data['Satisfied']) > 1:
        for elem in (annotation_data['Satisfied']):
            start = int(1000 * (elem[0]))
            stop = int(1000 * (start + elem[1]) + 1)
            ms_data.loc[start:stop,'emotion'] = 3

    if len(annotation_data['Confused']) > 1:     
        for elem in (annotation_data['Confused']):
            start = int(1000 * (elem[0]))
            stop = int(1000 * (start + elem[1]) + 1)
            ms_data.loc[start:stop,'emotion'] = 2        

    return ms_data

def import_multiple(files):
    b,a,e = [],[],[]
    for f in files:
        b1,a1,e1 = import_data(f)
        b.extend(b1)
        a.extend(a1)
        e.extend(e1)
    return b,a,e

def import_paths_from_txt(txt):
    out = []
    with open(txt,'r') as file:
        for line in file:
            line = line.strip("\n")
            out.append(line)
    return out

def association_counter(a,b):
    counterDic ={
        'zero' : 0,
        'one' : 0,
        'two' : 0,
        'three' : 0,
        'zeroone' : 0,
        'zerotwo' : 0,
        'zerothree' : 0,
        'onezero': 0,
        'oneone' : 0,
        'onetwo' : 0,
        'onethree' : 0,
        'twozero' : 0,
        'twoone' : 0,
        'twotwo' : 0,
        'twothree': 0,
        'threezero':0,
        'threeone': 0,
        'threetwo' : 0,
        'threethree': 0
    }
    for elemA, elemB in zip(a,b):
            if elemA == 0:
                counterDic['zero'] += 1
                if elemB == 1:
                    counterDic['zeroone'] += 1 
                elif elemB == 2:
                    counterDic['zerotwo'] += 1
                elif elemB == 3:
                    counterDic['zerothree'] += 1
                elif elemB == 0:
                    # print('empty segment, skipping...')
                    continue
            elif elemA == 1:
                counterDic['one'] += 1
                if elemB == 1:
                    counterDic['oneone'] += 1 
                elif elemB == 2:
                    counterDic['onetwo'] += 1
                elif elemB == 3:
                    counterDic['onethree'] += 1
                elif elemB == 0:
                    counterDic['onezero'] += 1
            elif elemA == 2:
                counterDic['two'] += 1
                if elemB == 1:
                    counterDic['twoone'] += 1 
                elif elemB == 2:
                    counterDic['twotwo'] += 1
                elif elemB == 3:
                    counterDic['twothree'] += 1
                elif elemB == 0:
                    counterDic['twozero'] += 1
            elif elemA == 3:
                counterDic['three'] += 1
                if elemB == 1:
                    counterDic['threeone'] += 1 
                elif elemB == 2:
                    counterDic['threetwo'] += 1
                elif elemB == 3:
                    counterDic['threethree'] += 1
                elif elemB == 0:
                    counterDic['threezero'] +=1
    return counterDic


def get_percentages(df, window,previndex,i):
    
    behaviorCounts = df[previndex:i]['behavior'].value_counts()
    attentionCounts = df[previndex:i]['attention'].value_counts()
    emotionCounts = df[previndex:i]['emotion'].value_counts()
    try:
        percentOnTask = behaviorCounts[2] / window
    except:
        percentOnTask = 0
    try:
        percentOffTask = behaviorCounts[1] / window
    except:
        percentOffTask = 0
    try:
        percentSatisfied = emotionCounts[3]/ window
    except:
        percentSatisfied = 0
    try:
        percentConfused = emotionCounts[2]/ window
    except:
        percentConfused = 0
    try:
        percentBored = emotionCounts[1]/ window
    except:
        percentBored = 0
    try:
        percentFocused = attentionCounts[3]/ window
    except:
        percentFocused = 0
    try:
        percentIdle = attentionCounts[2]/ window
    except:
        percentIdle = 0
    try:
        percentDistracted = attentionCounts[1]/ window
    except:
        percentDistracted = 0
    percentDict = {'on-task':percentOnTask,'off-task':percentOffTask,'satisfied':percentSatisfied,'confused': percentConfused,
    'bored':percentBored,'focused':percentFocused,'idle':percentIdle,'distracted': percentDistracted}
    return percentDict


def clean_cuts(df, window):
    previndex = 0
    data = {"sequence":[],"on-task": [],"off-task":[],"satisfied":[],"confused":[],"bored": [], "focused": [],"idle":[],"distracted":[]}
    seq = 0
    for i in range(len(df) + 1):
        if i == 0:
            continue
        if i % window == 0:
            seq += 1
            percentages = get_percentages(df, window, previndex, i) ## percentages shoudl be a dict
            previndex = i
            data["sequence"].append(seq)
            data['on-task'].append(percentages['on-task'])
            data['off-task'].append(percentages['off-task'])
            data['satisfied'].append(percentages['satisfied'])
            data['confused'].append(percentages['confused'])
            data['bored'].append(percentages['bored'])
            data['focused'].append(percentages['focused'])
            data['distracted'].append(percentages['distracted'])
            data['idle'].append(percentages['idle'])
    df = pd.DataFrame(data)
    return df

if __name__ == "__main__":

    # paths = import_paths_from_txt('F:\\Work\\DataCounter\\paths.txt')
    # print(len(paths))
    
    # b,a,e = import_multiple(paths)
    # with open('timeSaver\\b.txt','wb') as f: 
    #     pickle.dump(b,f)
    # with open('timeSaver\\a.txt','wb') as f: 
    #     pickle.dump(a,f)
    # with open('timeSaver\\e.txt','wb') as f: 
    #     pickle.dump(e,f)
    with open('timeSaver\\b.txt','rb') as f: 
        b = pickle.load(f)
    with open('timeSaver\\a.txt','rb') as f: 
        a = pickle.load(f)
    with open('timeSaver\\e.txt','rb') as f: 
        e = pickle.load(f)

    # print(len(b))
    # print(len(b),len(a),len(e))
    # counter = 0
    # for elemB, elemA, elemE in zip(b,a,e):
    #     if elemB == 1 and elemE == 1 and elemA == 1:
    #         counter +=1
    # print(counter/1000)
    df = (clean_cuts(b,a,e,1000))
    (df.to_csv('sequences.csv',index=False))