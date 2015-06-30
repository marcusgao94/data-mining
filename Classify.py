import os, numpy, time
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import BernoulliNB
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model.logistic import LogisticRegression
from sklearn.cross_validation import cross_val_score
from sklearn.cross_validation import train_test_split

X = []
label = []
test_X = []

def autoCrossValidation():
    classifiers = [LinearSVC(), BernoulliNB(), LogisticRegression()]
    clfNames = ['svm', 'naive bayes', 'logistic regression']
    scorers = ['accuracy', 'precision_weighted', 'recall_weighted']
    for i in range(0, 3):
        classifier = OneVsRestClassifier(classifiers[i])
        print clfNames[i]
        for scorer in scorers:
            t1 = time.clock()
            scores = cross_val_score(classifier, x, y, cv = 5, scoring=scorer)
            t2 = time.clock()
            #print 'trained for %ds' % (t2 - t1)
            print '%s =' % scorer,
            for cvs in scores:
                print '%.1f%%' % (cvs * 100),
            print ''

def selfCrossValidation(x, y):
    classifiers = [LinearSVC(), BernoulliNB(), LogisticRegression()]
    clfNames = ['svm', 'naive bayes', 'logistic regression']
    for i in range(0, 3):
        classifier = OneVsRestClassifier(classifiers[i])
        print clfNames[i]
        xTrain, xTest, yTrain, yTest = train_test_split(x, y)
        classifier.fit(xTrain, yTrain)
        yPred = classifier.predict(xTest)
        yTest = yTest
        right = 0
        total = len(yPred)
        for i in range(0, yPred.shape[0]):
            for j in range(0, yPred.shape[1]):
                if yPred[i][j] == 1 and yTest[i][j] == 1:
                    right += 1
                    break
        print 'accuracy = %.1f' % (float(right) / total * 100)


# read file from a given path
def readFile(filePath):
    con = []
    lab = []
    fin = open(filePath)
    lines = fin.readlines()
    i = 0
    while i != len(lines):
        labels = set(lines[i + 1].strip().split('\t'))
        lab.append(labels)
        text = ''
        i += 2
        while lines[i] != '-----\n':
            text += lines[i]
            i += 1
        con.append(text)
        """
        if len(con) > 10000:
            break
            """
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
    (con, lab) = readFile(yearPath + '/preprocess.txt')
    X.extend(con)
    label.extend(lab)

x = TfidfVectorizer().fit_transform(X)
y = MultiLabelBinarizer().fit_transform(label)
print '%d documents, %d words, %d categories' % (x.shape[0], x.shape[1], y.shape[1])
# autoCrossValidation()
# selfCrossValidation(x, y)

