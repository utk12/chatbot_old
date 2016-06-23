from elasticsearch import Elasticsearch
from random import choice, randint
from string import ascii_lowercase
import json
import numpy as np


es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

def genRandString(n):
	return (''.join(choice(ascii_lowercase) for i in range(n)))


def getUserId():
	return genRandString(8)


def createJSON(user):
	with open('Data/user_features.json', 'r') as f:
		data = f.read()
	es.index(index='chatbot', doc_type='users', id=user, body=data)

def getUserDoc(user):
	body = {
		"query" : {
			"match": {
				"_id" : user
			}
		}
	}
	return es.search(index='chatbot', doc_type='users', body = body)['hits']['hits'][0]['_source']


def get_feature_dictionary():
	with open('features.json', 'r') as f:
		data = json.loads(f.read())
	feature_dict = {}
	for intent in data:
		feature_dict[intent] = {}
		for category in data[intent]:
			feature_dict[intent][category] = []
			for subcategory in data[intent][category]['children']:
				feature_dict[intent][category].append(subcategory)
	return feature_dict



def updateJson(user, userDict):
	print "yo"
	body = {
		"doc" : userDict
	}
	es.update(index='chatbot',doc_type='users',id=user,body=body)
	


def updateUser(user, intent, features):
	userDict = getUserDoc(user)
	for i in features:
		if i in userDict[intent]:
			userDict[intent][i]['found_value'] = 1
			nfeatures = len(userDict[intent][i]['children'])
			userDict[intent][i]['prefer_count'] = nfeatures/2 + (nfeatures == 1)
			userDict[intent][i]['factor_value'] += 0.5
		else :
			for child in userDict[intent]:
				if i in userDict[intent][child]["children"]:
					temp = userDict[intent][child]["children"][i] 
					userDict[intent][child]["children"][i] = 1
					userDict[intent][child]['found_value'] = 1
					userDict[intent][child]['prefer_count'] += abs(temp-1)
					break
	updateJson(user,userDict)




def getUserVector(user, intent):
	userDict = getUserDoc(user)[intent]
	vec = []
	for category in userDict:
		a = float(userDict[category]['found_value'])
		b = float(userDict[category]['prefer_count'])
		c = float(userDict[category]['factor_value'])
		vec.append(a*b*c)
	vec = np.array(vec)
	print vec
	mag = np.linalg.norm(vec)
	if mag > 0:	
		unit_vec = vec/mag
	else:
		unit_vec = vec
	return unit_vec




# print getUserVector('uyzpanbd', 'buy')
# updateUser('uyzpanbd', 'buy', ['security', 'amenities', '2BHK'])
# print getUserDoc('hndwkoiq')
# createJSON(getUserId())


# feature_dict = get_feature_dictionary()
# features = get_features(user_query)





# user = getUserId()
# createJSON(user)