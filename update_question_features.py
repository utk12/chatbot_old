import json
import numpy as np
import pandas as pd
pd.set_option('expand_frame_repr', False)
data = pd.read_csv('Data/buy_questions.csv')
data.index = data['sn']

def lower_columns(name):
	for item in data[str(name)]:
		item = str(item)
		item1 = item.lower()
		for index in data[data[str(name)] == item].index.tolist():
			data[str(name)][index] = item1

def get_list_distinct_fields(data,key_field):
	l1 = list(set(data[key_field]))
	l1 = [l for l in l1 if str(l) != 'nan']
	l1 = [l for l in l1 if l not in [str(m) for m in range(100)]]
	return l1

def convert_underscore_to_camelcase(text):
	components = text.split('_')
	return components[0] + "".join(x.title() for x in components[1:])

def convert_camelcase_to_underscore(str):
	return ''.join(map(lambda x: x.lower() if not x.isupper() else "_"+x.lower(),str))

def convert_space_to_underscore(str):
	return ''.join(map(lambda x:x.lower() if x != ' ' else "_",str))

def get_dict_parent_numchild():
	dict1 = {}
	for item in get_list_distinct_fields(data,'key_2'):
		# item = convert_space_to_underscore(item)
		dict1[item] = data['key_3'][data.index[data['key_2'] == item]].item()
	return dict1

def get_children_values(k,num):
	i1 = int(data.index[data['key_2'] == k])
	i2 = int(data.index[data['key_2'] == k]) + int(num)
	list1 = []
	for item in data['key_3'][i1:i2]:
		list1.append(item)
	return list1

def update_question_features_key_level(feature):
	for key in get_list_distinct_fields(data,'key_2'):
		#converting into underscore format
		key_new = ''.join(map(lambda x:x.lower() if x != ' ' else "_",key))
		for k in feature:
			#k is projectType,.....
			k_new = ''.join(map(lambda x: x.lower() if not x.isupper() else "_"+x.lower(),k))
			if key_new == k_new:
				for k1 in feature[k]:
					data['bot_question'][data.index[data['key_2'] == key]].item()
					if k1 == 'bot_question':
						feature[k][k1] = data['bot_question'][data.index[data['key_2'] == key]].item()
					elif k1 == 'user_question':
						feature[k][k1] = data['user_question'][data.index[data['key_2'] == key]].item()
			# json_data.seek(0)
			# json_data.write(json.dumps(feature,indent = 4,sort_keys = True))

def update_question_features_value_level(feature):
	for key,num in get_dict_parent_numchild().iteritems():
		key_new = convert_space_to_underscore(key)
		for children in get_children_values(key,num):
			# print children
			index1 = int(data.index[data['key_2'] == key])
			index2 = index1 + int(num)
			data_subset = data.loc[index1:index2]
			# print data_subset
			# print '-------------------------------------------------'
			children_new = convert_space_to_underscore(children)	
			for k in feature:
				k_new = convert_camelcase_to_underscore(k)
				if((k_new == key_new) and feature[k].has_key('children')):
					for k1 in feature[k]['children']:
						k1_new = convert_camelcase_to_underscore(k1)
						if(k1_new == children_new):						
							for k2 in feature[k]['children'][k1]:
								if k2 == 'bot_question':
									feature[k]['children'][k1][k2] = data_subset[k2][data_subset.index[data_subset['key_3'] == children]].item()
								elif k2 == 'user_question':
									feature[k]['children'][k1][k2] = data_subset[k2][data_subset.index[data_subset['key_3'] == children]].item()

def write_output(operation):
	# operation is buy/rent
	with open('Data/question_features_'+str(operation)+'.json') as json_data:
		feature = json.loads(json_data.read())
	update_question_features_key_level(feature)
	update_question_features_value_level(feature)
	# print json.dumps(feature,indent = 4)
	with open('Data/question_features_'+str(operation)+'_output.json','w') as outfile:
		json.dump(feature,outfile)

def get_output(operation):
	# operation is buy/rent
	operation = operation.lower()
	with open('Data/question_features_'+str(operation)+'.json') as json_data:
		feature = json.loads(json_data.read())
	update_question_features_key_level(feature)
	update_question_features_value_level(feature)
	return json.dumps(feature,indent = 4)

if __name__ == '__main__':
	#below 3 lines hsould not be commented out.
	column_names = ['bot_question','user_question','key_1','key_2','key_3']
	for name in column_names:
		lower_columns(name)
	# print get_list_distinct_fields(data,'key_3')
	# update_question_features_key_level()

	# print get_dict_parent_numchild()
	# print iterate('amenities',34)
	print get_output('buy')
