import sys
import os
# insert at 1, 0 is the script path (or '' in REPL)
currDir = os.getcwd()
pythonAPI = currDir + '/libsvm-3.24/python'
sys.path.insert(1, pythonAPI)

from svmutil import *
from commonutil import *
from sklearn.metrics import confusion_matrix

trainFile = input('Enter Training File: ')
testFile = input('Enter Testing File: ')


trainLabels, trainData = svm_read_problem(trainFile, return_scipy=True)
testLabels, testData = svm_read_problem(testFile, return_scipy=True)

# print("Train Labels: " + str(trainLabels))
# print("Train Data: " + str(trainData))


scale_paramTrain = csr_find_scale_param(trainData, lower=0)
scale_paramTest = csr_find_scale_param(testData, lower=0)

scaled_trainData = csr_scale(trainData, scale_paramTrain)
scaled_testData = csr_scale(testData, scale_paramTest)

model = svm_train(trainLabels, scaled_trainData, '-c 2.0 -g 0.03125')

pLabels, accuracy, pVals = svm_predict(testLabels, scaled_testData, model)

# print('Accuracy: ' + str(accuracy))

# print(len(pLabels))
# print(len(testLabels))

confMatrix = confusion_matrix(testLabels,pLabels)

print(confMatrix)    
