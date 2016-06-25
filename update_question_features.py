import json
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

if __name__ == '__main__':
	column_names = ['bot_question','user_question','key_1','key_2','key_3']
	for name in column_names:
		lower_columns(name)
	print data
