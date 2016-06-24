from user_features import get_feature_dictionary

def getFeatures(witReply, intent):
	features = []
	for entity in witReply:
		for feature in wtReply[entity]:
			dothis(entity,feature)

def dothis(entity, feature, intent):
	feature_dict = get_feature_dictionary()[intent]
	if entity == 'project_type':
		if feature in 

get_feature_dictionary()