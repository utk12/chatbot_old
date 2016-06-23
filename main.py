import json
from english_corrector import EnglishCorrector
from wit_get_reply_api import *
from chatbot import *

def main(str1):
	str1 = str1.lower()
	ec = EnglishCorrector()
	if(len(str1)>0):
		res = ec.correct(str1)
	return res

def getInput():
	print("Enter sentence to correct (Give blank input to exit):")
	sentence = raw_input()
	return sentence.lower()

def show(text):
	print(json.dumps(text,indent=2))

if __name__ == '__main__':
	message = 'I want a row-house in golf corse road,ggn by seesipal vihar.'
	message =  main(message)
	print message
	output_wit=get_output_wit(message)	#this is whole output from wit
	entities = get_entities_json_wit(output_wit) #this is json object of entities from wit.
	print json.dumps(output_wit,indent = 4)