import os, numpy, time
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC
from sklearn.cross_validation import cross_val_score
from sklearn.naive_bayes import BernoulliNB
from sklearn.linear_model.logistic import LogisticRegression

X = []
label = []
test_X = []

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
years = ['1987']#, '1988', '1989', '1990', '1991']
print 'reading in'
for year in years:
    if year.startswith('.'):
        continue
    print year
    yearPath = BASEPATH + '/' + year
    (con, lab) = readFile(yearPath + '/body.txt')
    X.extend(con)
    label.extend(lab)

print '%d documents' % len(X)

bin = MultiLabelBinarizer()
y = bin.fit_transform(label)
classifiers = [LinearSVC(), BernoulliNB(), LogisticRegression()]
clfNames = ['svm', 'naive bayes', 'logistic regression']
scorings = ['accuracy', 'precision', 'recall']
for i in range(0, 3):
    classifier = Pipeline([('vectorizer', TfidfVectorizer()),
                            ('clf', OneVsRestClassifier(classifiers[i]))])
    print 'training ' + clfNames[i]
    for scoring in scorings:
        t1 = time.clock()
        scores = cross_val_score(classifier, X, y, cv = 5, scoring=scoring)
        t2 = time.clock()
        #print 'trained for %ds' % (t2 - t1)
        print '%s =' % scoring,
        for cvs in scores:
            print '%.1f%%' % (cvs * 100),
        print ''
"""
    classifier.fit(X, y)
    predicted = classifier.predict(test_X)
    #li = bin.inverse_transform(predicted)
"""
