from user_features import get_feature_dictionary
import json

def getFeatures(witReply, intent):
	witReply = format_wit_reply(witReply)
	features = []
	features.append(getSecurityFeatures(witReply))
	print features
	for entity in witReply:
		for feature in witReply[entity]:
			dothis(entity,feature)


def format_wit_reply(witReply):
	reply = {}
	for i in witReply:
		x = '_'.join(i.split())
		reply[x] = {}
		for j in witReply[i]:
			reply[x]['_'.join(j.split())] = witReply[i][j]
	return reply




def getSecurityFeatures(witReply):
	security = {}
	place = {}
	if 'security' in witReply:
		security =witReply['security']
		if 'security_place' in witReply:
			place =  witReply['security_place']
	features = []
	features += security
	for i in place:
		for feature in security:
			features.append(feature+'_'+i)
	return list(set(features))



def dothis(entity, feature, intent):
	feature_dict = get_feature_dictionary()[intent]
	if entity == 'project_type':
		if feature in feature_dict[entity]:
			return feature

	elif entity == 'configuration' or entity == 'specification':
		if feature in feature_dict[entity]:


getFeatures({u'security': {u'golf cars road': True}, u'security_place': {u'cricket': True, u'football': True}, u'project_type': {u'row house': True}, u'sentiment': {u'positive': True}}, 'buy')



# print json.dumps(get_feature_dictionary()['buy'], indent = 4)