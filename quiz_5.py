"""Solution for quiz_5"""
# Written by Shupeng Xue for COMP9021

import csv
from collections import defaultdict
from re import match


def analyse(gender, age):
    #pylint: disable=possibly-unused-variable
    """main function"""
    if gender == 'M':
        print('The following might particularly '
              f'contribute to cardio problems for males aged {age}:')
    else:
        print('The following might particularly '
              f'contribute to cardio problems for females aged {age}:')
    genders = ('', 'F', 'M')
    dic = (defaultdict(list), defaultdict(list))
    mnm = (defaultdict(lambda: [999, 0]), defaultdict(lambda: [999, 0]))
    count = [0, 0]
    with open('cardio_train.csv', encoding='utf-8', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            if reader.line_num == 1:
                continue
            for i, number in enumerate(row):
                if i in range(3, 7):
                    row[i] = float(number)
                else:
                    row[i] = int(number)
            _, age_day, gen, hei, wei, ap_hi, ap_lo, chole, gluc, smoke,\
                alco, active, cardio = row
            ages = (int(age_day) - 1)//365
            if ages != age or gender != genders[gen] or hei < 150\
                    or hei > 200 or wei < 50 or wei > 150 or ap_hi < 80 or\
                    ap_hi > 200 or ap_lo < 70 or ap_lo > 140:
                continue
            count[cardio] += 1
            for i in ('hei', 'wei', 'ap_hi', 'ap_lo', 'chole', 'gluc',
                      'smoke', 'alco', 'active'):
                dic[cardio][i].append(locals()[i])
                if i in ('hei', 'wei', 'ap_hi', 'ap_lo'):
                    mnm[cardio][i][0] = min(mnm[cardio][i][0], locals()[i])
                    mnm[cardio][i][1] = max(mnm[cardio][i][1], locals()[i])
    for i in ('hei', 'wei', 'ap_hi', 'ap_lo'):
        mnm[0][i][1] += 0.1
        mnm[1][i][1] += 0.1
    bounday = (defaultdict(list), defaultdict(list))
    for i in (0, 1):
        for j in ('hei', 'wei', 'ap_hi', 'ap_lo'):
            span = (mnm[i][j][1]-mnm[i][j][0])/5
            bounday[i][j].append(mnm[i][j][0])
            for k in range(1, 5):
                bounday[i][j].append(mnm[i][j][0]+k*span)
            bounday[i][j].append(mnm[i][j][1])
    freq = (defaultdict(float), defaultdict(float))
    order = {}
    for j in ('hei', 'wei', 'ap_hi', 'ap_lo'):
        for k in range(1, 6):
            order[f'{j}{k}'] = len(order)
            for i in (0, 1):
                freq[i][f'{j}{k}'] = len([0 for x in dic[i][j]
                                         if bounday[i][j][k-1] <= x < bounday[i][j][k]])/count[i]
    for j in ('chole', 'gluc'):
        for k in (1, 2, 3):
            order[f'{j}{k}'] = len(order)
            for i in (0, 1):
                freq[i][f'{j}{k}'] = len([0 for x in dic[i][j]
                                         if x == k])/count[i]
    for k in (0, 1):
        for j in ('smoke', 'alco', 'active'):
            order[f'{j}{k}'] = len(order)
            for i in (0, 1):
                freq[i][f'{j}{k}'] = len([0 for x in dic[i][j]
                                         if x == k])/count[i]
    ratio = defaultdict(float)
    for i in freq[0]:
        if freq[0][i] == 0:
            ratio[i] = float('inf')
            continue
        ratio[i] = freq[1][i]/freq[0][i]
    for i in sorted(ratio, key=lambda x: (-ratio[x], order[x])):
        if ratio[i] <= 1:
            continue
        print(f'   {ratio[i]:.2f}: ', end='')
        if match(r'hei', i):
            print(f'Height in category {i[-1]} (1 lowest, 5 highest)')
        elif match(r'wei', i):
            print(f'Weight in category {i[-1]} (1 lowest, 5 highest)')
        elif match(r'ap_hi', i):
            print(
                f'Systolic blood pressure in category {i[-1]} (1 lowest, 5 highest)')
        elif match(r'ap_lo', i):
            print(
                f'Diastolic blood pressure in category {i[-1]} (1 lowest, 5 highest)')
        elif match(r'chole', i):
            print(f'Cholesterol in category {i[-1]} (1 lowest, 3 highest)')
        elif match(r'gluc', i):
            print(f'Glucose in category {i[-1]} (1 lowest, 3 highest)')
        elif match(r'smoke', i):
            print(int(i[-1])*'Not smoking' + (not int(i[-1]))*'Smoking')
        elif match(r'alco', i):
            print(int(i[-1])*'Not drinking' + (not int(i[-1]))*'Drinking')
        elif match(r'active', i):
            print(int(i[-1])*'Being active' +
                  (not int(i[-1]))*'Not being active')
