import os
import numpy
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC
from sklearn.datasets import make_multilabel_classification

content = []
label = []
test_content = []

def readFile(filePath):
    con = []
    lab = []
    fin = open(filePath)
    lines = fin.readlines()
    i = 0
    while i != len(lines):
        labels = set(lines[i+1].strip().split('\t'))
        lab.append(labels)
        text = lines[i+1]
        i += 3
        while lines[i] != '-----\n':
            text += lines[i]
            i += 1
        con.append(text)
        i += 1
    fin.close()
    return (con, lab)

BASEPATH = '../data'
years = ['1987', '1988', '1989', '1990', '1991', '1992', '1993', '1994', '1995', '1996']
cnt = 0
for year in years:
    if year.startswith('.'):
        continue
    print year
    yearPath = BASEPATH + '/' + year
    (con, lab) = readFile(yearPath + '/body.txt')
    content.extend(con)
    label.extend(lab)
    cnt += 1
    if cnt == 1:
        break

(test_content, lab) = readFile(BASEPATH + '/1996/body.txt')

l = len(content)
print l
vec = TfidfVectorizer()
bin = MultiLabelBinarizer()
a = vec.fit_transform(content)
b = bin.fit_transform(label)
analyze = vec.build_analyzer()
classifier = Pipeline([('vectorizer', TfidfVectorizer()),
                       ('clf', OneVsRestClassifier(LinearSVC()))])
classifier.fit(content, b)
predicted = classifier.predict(test_content)
print bin.inverse_transform(predicted)

"""
numpy.set_printoptions(threshold='nan')


classifier = OneVsRestClassifier(LinearSVC())
print 'begin training'
classifier.fit(a[0:-5], b[0:-5])
print 'begin predicting'
pre = classifier.predict(a[-1])
print bin.inverse_transform(pre)
"""
