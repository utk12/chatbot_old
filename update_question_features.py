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
	return l1
def update_question_features():
	with open('Data/question_features_buy.json') as json_data:
		feature = json.loads(json_data.read())
	for key in get_list_distinct_fields(data,'key_2'):
		#converting into underscore format
		key_new = ''.join(map(lambda x:x.lower() if x != ' ' else "_",key))
		for k in feature:
			#k is projectType,.....
			k_new = ''.join(map(lambda x: x.lower() if not x.isupper() else "_"+x.lower(),k))
			if key_new == k_new:
				print 'yes'
				for k1 in feature[k]:
					print k
					print k1
					data['bot_question'][data.index[data['key_2'] == key]].item()
					if k1 == 'bot_question':
						feature[k][k1] = data['bot_question'][data.index[data['key_2'] == key]].item()
					elif k1 == 'user_question':
						feature[k][k1] = data['user_question'][data.index[data['key_2'] == key]].item()
			# json_data.seek(0)
			# json_data.write(json.dumps(feature,indent = 4,sort_keys = True))
	print json.dumps(feature,indent = 4)

if __name__ == '__main__':
	column_names = ['bot_question','user_question','key_1','key_2','key_3']
	for name in column_names:
		lower_columns(name)

	# print get_list_distinct_fields(data,'key_2')
	update_question_features()

