from interpret_wit_reply import format_wit_reply
import json


def wit_extract_filters(witReply):
	witReply = format_wit_reply(witReply)
	filters = {}
	filters['aports_activities'], filters['club_house'] = getAmenitiesFilters(witReply)


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


def getAmenitiesFilters(witReply):
	filters_data = getFiltersJson()
	sports = {}
	club = {}
	if 'amenities' in witReply:
		for i in witReply['amenities']:
			if i in filtersData['sports_activities']:
				sports[i] = True
			elif i in filtersData['club_house']:
				club[i] = True
	return sports, club

