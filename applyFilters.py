# from getFilters import wit_extract_filters
from elasticsearch import Elasticsearch
import json
from update_question_features import convert_underscore_to_camelcase as toCamel

def toCamel(text):
	components = text.split('_')
	return components[0] + "".join(x.title() for x in components[1:])

es = Elasticsearch([{'host':'localhost','port':9200}])

def getProjects(filters_dict):
	body = prepareBody(filters_dict)
	project_list = search(body)
	project_list = applyUnitsFilter(project_list)



def search(body):
	return es.search(index = 'chatbot', doc_type = 'projects', body = body)['hits']['hits']



def prepareBody(filters_dict):
	fliterMust = []
	club = {"bool" : {"should" : []	}}
	for i in filters_dict['club_house']:
		i = toCamel(i)
		club['bool']['should'].append({"term":{'clubHouse.'+i : True}})

	sports = {"bool" : {"should" : [] }}
	for i in filters_dict['sports_activities']:
		i = toCamel(i)
		sports['bool']['should'].append({"term":{'sportsActivities.'+i : True}})

	other = {"bool" : {"must" : [] }}
	for i in filters_dict['other']:
		i = toCamel(i)
		other['bool']['must'].append({"term":{'other.'+i : True}})

	sec = {
		"bool" : {
			"should" : [],
			"must" : []	
		}
	}
	security = filters_dict['security']
	if len(security) > 0:
		if security['place_flag']:
			for i in security:
					if i != 'place_flag':
						for j in security[i]:
							i = toCamel(i)
							j = toCamel(j)
							sec['bool']['must'].append({"term":{"security."+i+"."+j : True}})
		else:
			for i in security:
				if i != 'place_flag':
					for j in security[i]:
						i = toCamel(i)
						j = toCamel(j)
						sec['bool']['should'].append({"term":{"security."+i+"."+j : True}})

	details = {"bool" : {"must" : [] }}
	
	for i in filters_dict['project_details']:
		if i == 'project_name' or i == 'builder':
			x = []
			for j in filters_dict['project_details'][i]:
				i = toCamel(i)
				j = toCamel(j)
				x.append({"match_phrase":{'projectDetails.'+i : j}})
			details['bool']['must'].append({'bool' : {'should':x}})

		elif i == 'project_type':
			x = []
			for j in filters_dict['project_details'][i]:
				i = toCamel(i)
				j = toCamel(j)
				x.append({"term":{'projectDetails.'+i+'.'+j : True}})
			details['bool']['must'].append({'bool' : {'should':x}})

		elif i == 'car_parking' or i == 'vastu_compliant':
			i = toCamel(i)
			details['bool']['must'].append({"term":{'projectDetails.'+i : True}})

		elif i == 'address':
			x = []
			for j in filters_dict['project_details'][i]:
				if j == 'city':
					x.append({"match_phrase":{"projectDetails."+toCamel(i)+"."+toCamel(j) : filters_dict['project_details'][i][j]}})
				elif j == 'zone':
					y = {'bool':{'should' : []}}
					for k in filters_dict['project_details'][i][j]:
						y['bool']['should'].append({"match_phrase":{"projectDetails."+toCamel(i)+"."+toCamel(j) : k}})
					x.append(y)
				elif j == 'location':
					y = {'bool':{'should' : []}}
					for k in filters_dict['project_details'][i][j]:
						
						y['bool']['should'].append({"query_string":{"fields" : ["projectDetails."+toCamel(i)+"."+toCamel(j)+".*.name"], "query" : "\""+k+"\""}})
					x.append(y)
			details['bool']['must'].append({'bool' : {'must':x}})


	# specs = {"bool" : {"must" : [] }}
	# for i in filters_dict['specifications']:
	fliterMust.append(club)
	fliterMust.append(sports)
	fliterMust.append(sec)
	fliterMust.append(details)
	fliterMust.append(other)


	body = {
	  "query": {
		"filtered" : {
			"query" : {
				"match_all" : {}
			},
			"filter" : [
				{
					"bool" : {
						"must" : fliterMust
					}
				}
			]
		}
	  }
	}

	return body



filters_dict = {
	"club_house": {}, 
	"specifications": {}, 
	"sports_activities": {
		"cricket": True
	}, 
	"project_details": {
		"address": {
			"city": "gurgaon", 
			"zone": {
				"sohna road": True,
				"sector 48" : True
			},
			"location" : {
				"vipul trade centre" : True
			}
		},
		"project_name" : {
			"Vipul Greens" : True
		},
		"project_type": {
			"row_house" : True
		}
	}, 
	"security": {
		"place_flag": True, 
		"tower": {
			"guards": True
		}
	}, 
	"other": {}, 
	"configurations": {
		"property_type": {
			"row_house": True
		}
	}
}

print json.dumps(prepareBody(filters_dict), indent=2)

