import json
import pandas as pd
pd.set_option('expand_frame_repr', False)
data = pd.read_csv('Data/map_questions_filters.csv')
data.index = data['sn']
def lower_bot_questions():
	for item in data['bot_question']:
		item = str(item)
		item = item.lower()
		data['bot_question'].index = item
lower_bot_questions()
print data['bot_question']