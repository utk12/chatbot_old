import pandas as pd
import nltk
import re
import random
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from collections import Counter
import operator

train_data = pd.read_csv("train_data.csv")
predict_data =pd.read_csv("predict_data.csv")


def commonWords(feature,label):                   #Making Set of top 1000 occurring words in particular label
	listWords = []
	for i ,j in feature:
		if j ==label:
			listWords.extend(list(i['words']))
	countWord = Counter(listWords)
	output = sorted(countWord.items(),key = operator.itemgetter(1), reverse=True)
	output = output[:1000]
	temp = [i for i,j in output]
	return set(temp)

def filterFeature(Calvin,dictWord,Labels):        #Dictionary of Labels having count of words in input text
	feature = {}
	for i in Labels:
		feature[i]= 0

	Calvin = re.sub(r'\d+', '', Calvin)                          #Remove Digit
	Calvin = re.sub(r'\b\w{1,3}\b', '', Calvin)                  #Remove string of length less than 3
	Calvin = tokenizer.tokenize(Calvin.lower())                  #Tokenize 
	Calvin_modified = [t for t in Calvin if t not in stopwords]
	for word in Calvin_modified:
		for l in Labels:
			if word in list(dictWord[l]):
				feature[l]+=1

	return feature

def feature_extractor(Calvin):                                   #Preprocessing of text Data
	feature = {}
	Calvin = re.sub(r'\d+', '', Calvin)                          #Remove Digit
	Calvin = re.sub(r'\b\w{1,3}\b', '', Calvin)                  #Remove string of length less than 3
	Calvin = tokenizer.tokenize(Calvin.lower())                  #Tokenize 
	Calvin_modified = [t for t in Calvin if t not in stopwords]
	feature["words"] = tuple(Calvin_modified)
	return feature

tokenizer = RegexpTokenizer(r'\w+')
Calvin = train_data["Calvin"]
Label = train_data["Label"]
stopwords = stopwords.words('english')

feature_set =[]
for i in range(0,len(train_data)):
	t=train_data.ix[i,1]+train_data.ix[i,2]
	f=feature_extractor(t)
	feature_set.append((f,Label[i]))


LabelList =list(set(Label))

commonWordDict={}

for i in LabelList:                                #Dictionary of each label containg top 1000 most occurring words
	commonWordDict[i] = commonWords(feature_set,i)

for i in LabelList:                                #Dictionary having only unique words
	for j in LabelList:
		if (j !=i):
			commonWordDict[i]=commonWordDict[i]-commonWordDict[j]


#Training Model
feature_set =[]
for i in range(0,len(train_data)):
	t=train_data.ix[i,1]+train_data.ix[i,2]
	f=filterFeature(t,commonWordDict,LabelList)
	feature_set.append((f,Label[i]))

random.shuffle(feature_set)
classifier = nltk.NaiveBayesClassifier.train(feature_set)


# train_set, test_set = feature_set[1000:], feature_set[:1000] #To check accuracy on Training Data Itself
# classifier = nltk.NaiveBayesClassifier.train(train_set)	   #Model has 77.4% accuracy
# print(nltk.classify.accuracy(classifier, test_set))

#Predicting Labels
OutputCsV=[]
Final_result=[]
for i in range(0,len(predict_data)):
	dataDict = {}
	u=predict_data.ix[i,1] + predict_data.ix[i,2]
	dataDict["Calvin"] =predict_data.ix[i,1]
	dataDict["Hobbes"] =predict_data.ix[i,2]
	f=filterFeature(u,commonWordDict,LabelList)
	result = classifier.classify(f)
	dataDict["Output_Label"] = result
	Final_result.append(result)
	OutputCsV.append(dataDict)

temp = pd.DataFrame(OutputCsV)
temp.to_csv("Predicted_Labels.csv",index=False)





