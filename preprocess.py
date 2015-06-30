__author__ = 'gy'
import os, numpy

BASEPATH = '../data'
cnt = 0
years = ['1987']#, '1988', '1989', '1990', '1991']
for year in years:
    if year.startswith('.'):
        continue
    print year
    dic = {}
    yearPath = BASEPATH + '/' + year
    fin = open(yearPath + '/body.txt', 'r')
    lines = fin.readlines()
    fin.close()
    # first loop to count times
    print 'first loop'
    i = 0
    while i != len(lines):
        i += 2
        while (lines[i].strip() != '-----'):
            words = lines[i].split(' ')
            for w in words:
                if len(w) > 3:
                    t = dic.get(w, 0) + 1
                    dic[w] = t
            i += 1
        i += 1
    print len(dic)
    val = numpy.array(dic.values())
    mean = numpy.mean(val)
    print numpy.mean(val)
    print numpy.percentile(val, 25)
    print numpy.percentile(val, 50)
    print numpy.percentile(val, 75)

    # second loop to filter words
    print 'second loop'
    fout = open(yearPath + '/preprocess.txt', 'w')
    i = 0
    while i != len(lines):
        name = lines[i]
        category = lines[i + 1]
        text = ''
        i += 2
        while (lines[i].strip() != '-----'):
            words = lines[i].split(' ')
            for w in words:
                if (len(w) > 3) and (dic.get(w, 0) > mean):
                    text += (w + ' ')
            i += 1
        if len(text) > 0:
            fout.write(name + category + text + '\n-----\n')
        i += 1
    fout.close()
    break
