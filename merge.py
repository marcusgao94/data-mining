__author__ = 'gy'
import os

BASEPATH = '../data'
years = os.listdir(BASEPATH)
cnt = 0
for year in years:
    if year.startswith('.'):
        continue
    print year
    yearPath = BASEPATH + '/' + year
    #fout = open(yearPath + '/body.txt', 'w')
    months = os.listdir(yearPath)
    for month in months:
        if month.startswith('.') or month.endswith('.txt'):
            continue
        print month
        monthPath = yearPath + '/' + month
        days = os.listdir(monthPath)
        for day in days:
            if day.startswith('.'):
                continue
            dayPath = monthPath + '/' + day
            files = os.listdir(dayPath)
            for file in files:
                if file.endswith('.xml'):
                    cnt += 1
            #fin = open(dayPath + '/body.txt', 'r')
            #fout.write(fin.read())
    #fout.close()
    break
print cnt