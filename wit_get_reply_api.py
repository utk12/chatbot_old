import requests,json
#get_message
#Use different session ids for different users

def get_message_format_wit(str):
	str.replace(' ','%20')
	return str

def get_say_action_wit(message):
	message = get_message_format_wit(message)
	r = requests.post('https://api.wit.ai/converse?v=20160610&session_id=8&q='+str(message),
		headers = {'Authorization': 'Bearer QZBAVFA3VWR3UBH4PDUCGWELMGIE2T4O'})
	obj = json.loads(r.text)
	while(obj['type'] != 'msg'):
		r = requests.post('https://api.wit.ai/converse?v=20160610&session_id=8',data={},
			headers = {'Authorization': 'Bearer QZBAVFA3VWR3UBH4PDUCGWELMGIE2T4O'})
		obj = json.loads(r.text)
	return obj['msg']

def get_output_wit(message):
	message = get_message_format_wit(message)
	r = requests.post('https://api.wit.ai/message?v=20160610&session_id=8&q='+str(message),
		headers = {'Authorization': 'Bearer QZBAVFA3VWR3UBH4PDUCGWELMGIE2T4O'})
	obj = json.loads(r.text)
	return obj

def get_entities_json_wit(json_object):
	for key,value in json_object.iteritems():
		if key == 'entities':
			entities = json_object[key]
	return entities

if __name__ == '__main__':
	message = raw_input('Enter a message\n')
	print json.dumps(get_entities_wit(message),indent = 4)