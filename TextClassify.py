import os
import numpy
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC
from sklearn.datasets import make_multilabel_classification

content = []
label = []
test_content = []

BASEPATH = '../data'
years = os.listdir(BASEPATH)
cnt = 0
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
            fin = open(dayPath + '/body.txt', 'r')
            lines = fin.readlines()
            i = 0
            while i != len(lines) :
                i += 1
                labels = set(lines[i].strip().split('\t'))
                label.append(labels)
                i += 1
                text = lines[i]
                i += 1
                while lines[i] != '-----\n':
                    text += lines[i]
                    i += 1
                content.append(text)
                i += 1
            fin.close()
            break
        break
    break
    cnt += 1
    if cnt == 2:
        break

l = len(content)
vec = TfidfVectorizer()
bin = MultiLabelBinarizer()
a = vec.fit_transform(content)
b = bin.fit_transform(label)
numpy.set_printoptions(threshold='nan')
print b[100:120]

classifier = OneVsRestClassifier(LinearSVC())
classifier.fit(a[0:-5], b[0:-5])
pre = classifier.predict(a[102])
print bin.inverse_transform(pre)
