from user_features import get_feature_dictionary
import json

def getFeatures(witReply, intent):
	features = []
	features.append(getSecurityFeatures(witReply))
	
	for entity in witReply:
		for feature in wtReply[entity]:
			dothis(entity,feature)


def getSecurityFeatures(witReply):
	security = {}
	place = {}
	if 'security' in witReply:
		security =witReply['security']
		if 'security_place' in witReply:
			place =  witReply['security_place']
	features = []
	for i in security:
		features.append('_'.join(i.split()))
	for i in place:
		for feature in features:
			features.append(feature+'_'+'_'.join(i.split()))
	return list(set(features))



def dothis(entity, feature, intent):
	feature_dict = get_feature_dictionary()[intent]
	if entity == 'project_type':
		if feature in feature_dict[entity]:
			return feature
		else:
			return '_'.join(feature.split())




print json.dumps(get_feature_dictionary()['buy'], indent = 4)