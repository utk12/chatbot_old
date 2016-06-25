from interpret_wit_reply import format_wit_reply
import json


filters_data = getFiltersJson()

def getFiltersJson():
	with open('Data/filters.json', 'r') as f:
		data = json.loads(f.read())
	result = {}
	for cat in data:
		cat1 = 	''.join(map(lambda x: x.lower() if not x.isupper() else "_"+x.lower(), cat))
		result[cat1] = {}
		for i in data[cat]:
			subcat = ''.join(map(lambda x: x.lower() if not x.isupper() else "_"+x.lower(), i))
			if isinstance(data[cat][i], dict):
				result[cat1][subcat] = {}
				for j in data[cat][i]:
					key = ''.join(map(lambda x: x.lower() if not x.isupper() else "_"+x.lower(), j))
					result[cat1][subcat][key] = ''
			else:
				result[cat1][subcat] = ''
	return result



def wit_extract_filters(witReply):
	witReply = format_wit_reply(witReply)
	filters = {}
	filters['sports_activities'], filters['club_house'] = getAmenitiesFilters(witReply)
	filters['specifications'] = getSpecifications(witReply)
	filters['other'], filters['configurations'] = getConfigurations(witReply)
	filters['security'] = getSecurityFilters(witReply)



def getSecurityFilters(witReply):
	filters = {}
	if ['security'] in witReply:
		if ['security_place'] in witReply:
			filters['place_flag'] = True
			for i in witReply['security_place']:
				for j in witReply['security']:
					if j in filters_data['security'][i]:
						filters[i][j] = True
		else:
			filters['place_flag'] = False
			for i in witReply['security']:
				if i in filters_data['security']['tower']:
					filters['tower'][i] = True
				elif i in filters_data['security']['main_gate']:
					filters['main_gate'][i] = True
	return filters




def getConfigurations(witReply):
	others = {}
	configurations = {}
	if 'configurations' in witReply:
		for i in witReply['configurations']:
			if i in filters_data['other']:
				others['i'] = True
			elif i in filters_data['configurations']:
				configurations[i] = True
	if 'project_type' in witReply:
		for i in witReply['project_type']:
			configurations['property_type'] = witReply['project_type'][i]
	if 'accommodation' in witReply:
		for i in witReply['accommodation']:
			configurations['type'] = witReply['accommodation'][i]
	if 'area' in witReply:
		area = []
		for i in witReply['area']:
			area.append(i.split()[0])
		if 'area_type' in witReply:
			area_type = []
			for i in witReply['area_type']:
				area_type.append(i)
			x = len(area)
			y = len(area_type)
			area = [:min(x,y)]
			area_type = [:min(x,y)]
			if len(area) == 2:
				configurations['super_area'] = max(area[0], area[1])
				configurations['carpet_area'] = min(area[0], area[1])
			else:
				configurations[area_type[0]+'_area'] = area[0] 
		else:
			configurations['super_area'] = area[0]
				break
		if 'level' in witReply:
			for i in witReply['level']:
				level.append(i)
			level = [:len(area)]
			for i in level:
				if i in ['high', 'greater']:
					i = 'high'
				elif i in['low', 'lower']:
					i = 'low'
				else:
					i = 'medium'
				configurations['area_level'][i] = True
		else:
				configurations['area_level']['medium'] = True





def getSpecifications(witReply):
	filters = {}
	if 'specifications' in witReply:
		for i in witReply['specifications']:
			if i == 'modular_kitchen':
				i = 'kitchen_modular'
			if i in filters_data['specifications']:
				filters[i] = True

	return filters



def getAmenitiesFilters(witReply):
	sports = {}
	club = {}
	if 'amenities' in witReply:
		for i in witReply['amenities']:
			if i in filters_data['sports_activities']:
				sports[i] = True
			elif i in filters_data['club_house']:
				club[i] = True
	return sports, club


print json.dumps(getFiltersJson(), indent=4)
