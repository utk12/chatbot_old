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
	with open('Data/user_features.json', 'r') as f:
		data = json.loads(f.read())
	feature_dict = {}
	for intent in data:
		feature_dict[intent] = {}
		for category in data[intent]:
			category_new = ''.join(map(lambda x: x.lower() if not x.isupper() else "_"+x.lower(), category))
			feature_dict[intent][category_new] = []
			for subcategory in data[intent][category]['children']:
				if 'BHK' in subcategory:
					subcategory = subcategory.lower()
				else:
					subcategory = ''.join(map(lambda x: x.lower() if not x.isupper() else "_"+x.lower(), subcategory))
				feature_dict[intent][category_new].append(subcategory)
	return feature_dict



def updateJson(user, userDict):
	body = {
		"doc" : userDict
	}
	es.update(index='chatbot',doc_type='users',id=user,body=body)
	


def updateUser(user, intent, features):
	userDict = getUserDoc(user)
	for i in features:
		if i in userDict[intent]:
			userDict[intent][i]['foundValue'] = 1
			nfeatures = len(userDict[intent][i]['children'])
			userDict[intent][i]['preferCount'] = nfeatures/2 + (nfeatures == 1)
			userDict[intent][i]['factorValue'] += 0.5
		else :
			for child in userDict[intent]:
				if i in userDict[intent][child]["children"]:
					temp = userDict[intent][child]["children"][i] 
					userDict[intent][child]["children"][i] = 1
					userDict[intent][child]['foundValue'] = 1
					userDict[intent][child]['preferCount'] += abs(temp-1)
					break
	updateJson(user,userDict)




def getUserVector(user, intent):
	userDict = getUserDoc(user)[intent]
	vec = []
	for category in userDict:
		a = float(userDict[category]['foundValue'])
		b = float(userDict[category]['preferCount'])
		c = float(userDict[category]['factorValue'])
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
# print get_feature_dictionary()

# feature_dict = get_feature_dictionary()
# features = get_features(user_query)
