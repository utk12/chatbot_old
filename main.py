import json
from sentence_corrector import main
from wit_get_reply_api import *

if __name__ == '__main__':
	message = 'I want a row-house in golf corse road,ggn by seesipal vihar.'
	message =  main(message)
	output_wit=get_output_wit(message)	#this is whole output from wit
	entities = get_entities_json_wit(output_wit) #this is json object of entities from wit.
	print json.dumps(output_wit,indent = 4)
