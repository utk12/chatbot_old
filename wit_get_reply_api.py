import requests,json
#get_message
#Use different session ids for different users

def get_message_format_wit(str):
	str.replace(' ','%20')
	return str

def get_say_action_wit(message):
	message = get_message_format_wit(message)
	r = requests.post('https://api.wit.ai/converse?v=20160624&session_id=8&q='+str(message),
		headers = {'Authorization': 'Bearer QZBAVFA3VWR3UBH4PDUCGWELMGIE2T4O'})
	obj = json.loads(r.text)
	while(obj['type'] != 'msg'):
		r = requests.post('https://api.wit.ai/converse?v=20160624&session_id=8',data={},
			headers = {'Authorization': 'Bearer QZBAVFA3VWR3UBH4PDUCGWELMGIE2T4O'})
		obj = json.loads(r.text)
	return obj['msg']

def get_output_wit(message):
	message = get_message_format_wit(message)
	r = requests.post('https://api.wit.ai/message?v=20160624&session_id=8&q='+str(message),
		headers = {'Authorization': 'Bearer QZBAVFA3VWR3UBH4PDUCGWELMGIE2T4O'})
	obj = json.loads(r.text)
	return obj

def get_entities_list_wit():
	r = requests.get('https://api.wit.ai/entities',
		headers = {'Authorization': 'Bearer QZBAVFA3VWR3UBH4PDUCGWELMGIE2T4O'})
	obj = r.text
	return obj

def get_entities_json_wit(json_object):
	for key,value in json_object.iteritems():
		if key == 'entities':
			entities = json_object[key]
	return entities

def create_new_entity_wit(entity,values):
	headers = {'Authorization':'Bearer QZBAVFA3VWR3UBH4PDUCGWELMGIE2T4O'}
	data = {}
	data['id'] = entity
	data['values'] = []
	for item in values:
		dict1 = {}
		dict1['value'] = item
		data['values'].append(dict1)
	data = json.dumps(data)
	r=requests.post('https://api.wit.ai/entities?v=20160624',headers = headers,data = data)
	return r.text

def interpret_wit_output(json_object):
	# list1 = []
	dict1 = {}
	for key in json_object:
		dict1[key] = {}
		for i in range(len(json_object[key])):
			dict1[key][json_object[key][i]['value']] = True

	return dict1

if __name__ == '__main__':
	entity = 'trial'
	values = ['1','2']
	print create_new_entity_wit(entity,values)