import sys
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

def import_data(file_name):
    bTime, aTime, eTime = get_end_time(file_name)
    endtime = max([bTime, aTime, eTime])
    Behavioral_Engagement = create_template_list(endtime)
    Attention_Engagement = create_template_list(endtime)
    Emotional_Engagement = create_template_list(endtime)
    with open(file_name, "r") as f:
        for line in f:
            line = line.split("\t")
            del line[1]
            line[-1] = line[-1].strip("\n")
            if line[1] == 'default':
                continue
            if line[4] == "off-tsak" or line[4] == "distarcted" or line[4] == "Bored":
                tag = 1
            if line[4] == "on-task" or line[4] == "idle" or line[4] == "Confused":
                tag = 2
            if line[4] == "Satisfied" or line[4] == "focused":
                tag = 3
            if line[4] == 'None':
                continue
            start = int(float(line[1]) * 1000) - 1
            stop = int(float(line[2]) * 1000)
            if line[0] == "Behavioral_Engagement":
                for i in range(start, stop):
                    Behavioral_Engagement[i] = tag
            elif line[0] == "Attention_Engagement":
                for i in range(start, stop):
                    Attention_Engagement[i] = tag
            elif line[0] == "Emotional_Engagement":
                for i in range(start, stop):
                    Emotional_Engagement[i] = tag
    return Behavioral_Engagement, Attention_Engagement, Emotional_Engagement

    
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
if __name__ == "__main__":

    paths = import_paths_from_txt(r'F:\Work\DataCounter\paths.txt')
    print(len(paths))
    b,a,e = import_multiple(paths)
    print(len(b),len(a),len(e))
    print(association_counter(e,a))
    