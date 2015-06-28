import os
import xml.dom.minidom as mini


BASEPATH = '../data'
years = os.listdir(BASEPATH)
for year in years:
    if year.startswith('.'):
        continue
    print year
    yearPath = BASEPATH + '/' + year
    months = os.listdir(yearPath)
    for month in months:
        if month.startswith('.'):
            continue
        print month
        monthPath = yearPath + '/' + month
        days = os.listdir(monthPath)
        for day in days:
            if day.startswith('.'):
                continue
            dayPath = monthPath + '/' + day
            fout = open(dayPath + '/body.txt', 'w')
            files = os.listdir(dayPath)
            for file in files:
                if file.startswith('.') or file.endswith('.txt'):
                    continue
                fout.write(file + '\n')
                dom = mini.parse(dayPath + '/' + file)
                classifiers = dom.getElementsByTagName('classifier')
                classes = set()
                for c in classifiers:
                    if c.getAttribute('type') == 'taxonomic_classifier':
                        cla = c.firstChild.data
                        arr = cla.split('/')
                        if len(arr) >= 3:
                            classes.add(arr[2])
                        else:
                            classes.add(arr[-1])
                #print classes
                for c in classes:
                    fout.write(c + '\t')
                fout.write('\n')
                block = dom.getElementsByTagName('block')
                for b in block:
                    if b.getAttribute('class') == 'full_text':
                        paragraphs = b.getElementsByTagName('p')
                        text = ''
                        for p in paragraphs:
                            data = p.firstChild.data.lower()
                            for char in data:
                                if (char >= 'a' and char <= 'z') \
                                        or (char == ' ') or (char == '\n' or char == '\r'):
                                    text += char
                            text += ' '
                        #print text
                        fout.write(text + '\n-----\n')
            fout.close()

