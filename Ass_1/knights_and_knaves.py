"""Solution for COMP9021 Assignment 1 by z5407387 Shupeng Xue"""
from itertools import product
import re
import sys


Sirs = set()
Sir_list = []
Recordings = []


def is_name(word):
    """find is a word Sir name or I, if is return name
    without mark, if not return none"""
    if re.match(r'[A-Z][a-z]*', word):
        name = re.sub(r'[^\w\s]', '', word)
        if not re.match('Knight', name)\
                and not re.match('Knave', name) and not re.match('Sir', name):
            return name
    return None


def find_new_sirs(sent):
    """Record new sir names in given sentence"""
    if 'Sir' not in sent and 'Sirs' not in sent:
        return
    try:
        index = sent.index('Sir')
    except ValueError:
        index = sent.index('Sirs')
    for word in sent[index+1:]:
        if is_name(word) and is_name(word) != 'I':
            Sirs.add(is_name(word))


def junction(sub, sent):
    """return a junction set of Sirs"""
    group = set()
    for word in sent:
        if is_name(word):
            name = is_name(word)
            if name == 'I': #consider 'I'
                group.add(sub)
            else:
                group.add(name)
    if not group: #consider 'us'
        group = Sirs
    return group


def encode_junction_type(pattern, sub, state):
    """common function to encode a junction type record
    sub = who said the statement"""
    group = junction(sub, state)
    return Recordings.append((pattern, sub, group, state[-1] in ('Knight', 'Knights')))


def record(sub, state_raw):
    """Record a statement"""
    state = [re.sub(r'[^\w\s]', '', word) for word in state_raw]
    #remove all marks
    string = ' '.join(state) #use string for re.match
    if re.match(r'[Aa]t least', string):
        encode_junction_type(0, sub, state[1:])
    elif re.match(r'[Aa]t most', string):
        encode_junction_type(1, sub, state[1:])
    elif re.match(r'[Ee]xactly', string):
        encode_junction_type(2, sub, state[1:])
    elif re.match(r'[Aa]ll of us', string):
        Recordings.append((3, sub, Sirs, state[-1] == 'Knights'))
    elif re.match(r'I am a', string):
        if state[-1] == 'Knave':
            return 'No_Solution' #'I am a Knave' is a paradox
        Recordings.append((4, sub, {sub}, 1))
    elif re.match(r'Sir \w+ is a', string):
        group = junction(sub, state[1:])
        Recordings.append((5, sub, group, state[-1] == 'Knight'))
    elif re.match(r'[\w ]+ or [\w ]+ is a', string):
        encode_junction_type(6, sub, state[1:])
    elif re.match(r'[ \w]+ and [ \w]+ are', string):
        encode_junction_type(7, sub, state[1:])
    return None


def anaylize(sent):
    """Anaylize a list of words"""
    find_new_sirs(sent)
    said_start = -1
    for j, word in enumerate(sent):
        if '"' in word: #find if sentence contains a statement
            if said_start < 0:
                said_start = j
            else:
                said_end = j
                break
    else:
        return None #no statement
    subject = None #find who said that
    if said_start > 1:
        for word in sent[1:said_start]:
            if is_name(word):
                subject = is_name(word)
    if subject is None:
        if said_end < len(sent)-1:
            for word in sent[said_end+1:len(sent)]:
                if is_name(word):
                    subject = is_name(word)
    statement = sent[said_start:said_end+1]
    return record(subject, statement) #record who said and the statement


def check(dic, rec):
    """check if the statement match current assumation"""
    pattern = rec[0]
    sub_name = rec[1]
    group_of_name = rec[2]
    kork = rec[3] #knave or knight for 0 or 1
    sub = dic[sub_name]
    group = [dic[name] for name in group_of_name]
    if pattern in (0, 6):
        return sub == (group.count(kork) > 0)
    if pattern == 1:
        return sub == (group.count(kork) < 2)
    if pattern in (2, 5):
        return sub == (group.count(kork) == 1)
    if pattern in (3, 7):
        return sub == (group.count(kork) == len(group))
    if pattern == 4:
        return kork
    return None


print('Which text file do you want to use for the puzzle?', end=' ')
file_name = input()
raw = []
with open(file_name, encoding='utf-8') as file:
    for line in file.readlines():
        line = line.rstrip('\n')
        raw.extend(line.split(' ')) #raw is a list of words of original text
try:
    while True:
        raw.remove('') #remove empty
except ValueError:
    pass
sentence = []
NO_SOLUTION = False
while raw:
    splitter = raw.pop(0)
    sentence.append(splitter)
    if re.search(r'[/./?!]', splitter): #split a single sentence
        if anaylize(sentence) == 'No_Solution':
            NO_SOLUTION = True
        sentence.clear()
if len(Sirs) == 1:
    print('The Sir is:', end='')
else:
    print('The Sirs are:', end='')
Sir_list = sorted(Sirs)
for sir in Sir_list:
    print(' '+sir, end='')
print()
if NO_SOLUTION:
    print('There is no solution.')
    sys.exit()
possibilities = list(product({0, 1}, repeat=len(Sir_list)))
#list of 2^n tuples, n = number of sirs, represent all possibilities whether
#a sir is knave or knight
solutions = []
for poss in possibilities:
    dictionary = dict(zip(Sir_list, poss))
    #map sir names to 0 or 1
    for recording in Recordings:
        if not check(dictionary, recording):
            break
    else:
        solutions.append(poss)
if len(solutions) == 0:
    print('There is no solution.')
elif len(solutions) > 1:
    print(f'There are {len(solutions)} solutions.')
elif len(solutions) == 1:
    print('There is a unique solution:')
    for i, sir in enumerate(Sir_list):
        print('Sir', sir, f'is a Kn{["ave","ight"][solutions[0][i]]}.')
