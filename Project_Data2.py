from elasticsearch import Elasticsearch
import json
import numpy as np
import demjson

def getAllKeys(projectFeature):
    keys = []
    checkKeys = projectFeature.keys()[0]         # considering only buy for now
    #keys = keys + [checkKeys] 
    topFeatures  = projectFeature[checkKeys]
    topLayer = topFeatures.keys()
    topLayer.remove('rating')
    topLayer.remove('price')
    topLayer.remove('size')
    topLayer.remove('accommodation')
    topLayer.remove('nearby')
    #keys = keys + topLayer
    for f in topLayer:
        tempKeys = topFeatures[f]['children'].keys()
        keys = keys + tempKeys
    return keys

def featureDict(keyValues,dictionary,keys):
    #keyValues = dict()
    dKeys = dictionary.keys()
    for key in dKeys:
        if isinstance(dictionary[key],dict):
            if key in keys:
                keyValues[key] = 1
            featureDict(keyValues,dictionary[key],keys)
        elif key in keys:
            if dictionary[key] != 0 and dictionary[key] != '':
                keyValues[key] = 1
            else:
                keyValues[key] = 0 
    return keyValues

def mapValues(values,projectFeature):
    checkKeys = projectFeature.keys()[0]         # considering only buy for now
    #keys = keys + [checkKeys] 
    #topFeatures  = projectFeature[checkKeys]
    #topLayer =projectFeature[checkKeys].keys()
    projectFeature[checkKeys].keys().remove('rating')
    projectFeature[checkKeys].keys().remove('price')
    projectFeature[checkKeys].keys().remove('size')
    projectFeature[checkKeys].keys().remove('accommodation')
    for f in projectFeature[checkKeys].keys():
        #features = projectFeature[checkKeys][f]['children'].keys()
        for fs in projectFeature[checkKeys][f]['children'].keys():
            if fs in values:
                projectFeature[checkKeys][f]['children'][fs]['foundValue'] = values[fs]
    return projectFeature
    #keys = keys + topLayer

def calculateMean(projectData):
    price =[]
    size = []
    rating = []
    
    for key in projectData.keys():
        #For project IDs loop has to iterate through all IDs to get all prices of all projects
        #for project_id in project_ids:
        price.append(projectData[key]['units']['id1']['configurations']['price'])
        size.append(projectData[key]['units']['id1']['configurations']['superArea'])  #super area (or) carpet area
        #rating.append(projectData[key]['units']['id1']['configurations']['rating'])
    price.sort()
    size.sort()
    #rating.sort()
    
    highPrice = np.mean(price)+(max(price) - np.mean(price))*.5
    lowPrice = min(price) + (np.mean(price)-min(price))*.5
    
    highSize = np.mean(size) + (max(size)-np.mean(size))*.5
    lowSize = min(size) + np.mean(size)*.5
    
    #highRating = np.mean(rating) + (max(rating) - np.mean(rating))*.5
    #lowRating = min(rating) - np.mean(rating)
    
    #meanDict = {'price':(highPrice,lowPrice),'size':(highSize,lowSize),'rating':(highRating,lowRating)}
    
    meanDict = {'price':(highPrice,lowPrice),'size':(highSize,lowSize)}
    
    return meanDict

def hmlMapping(projectData,projectFeature,projectStatus):
    meanDict = calculateMean(projectData)
    if projectData[projectStatus]['units']['id1']['configurations']['price'] < meanDict['price'][1]:
        projectFeature['buy']['price']['children']['low'] = 1
    elif projectData[projectStatus]['units']['id1']['configurations']['price'] > meanDict['price'][0]:
        projectFeature['buy']['price']['children']['high'] = 1
    else:
        projectFeature['buy']['price']['children']['medium'] = 1
        
    if projectData[projectStatus]['units']['id1']['configurations']['superArea'] < meanDict['size'][1]:
        projectFeature['buy']['size']['children']['low'] = 1
    elif projectData[projectStatus]['units']['id1']['configurations']['superArea'] > meanDict['size'][0]:
        projectFeature['buy']['size']['children']['high'] = 1
    else:
        projectFeature['buy']['size']['children']['medium'] = 1
        
    return projectFeature
    # Rating data has yet to added 
def accoMapping(projectData,projectFeature):
    data = projectData['underConstruction']['units']['id1']['configurations']['propertyType']

    if data in projectFeature['buy']['accommodation']['children'].keys():
        projectFeature['buy']['accommodation']['children'][data]['foundValue'] = 1
    return projectFeature

def allProjectsFeatureMapping():
    return None

if __name__ == '__main__':
    
    es = Elasticsearch([{'host':'localhost','port':9200}])

##    with open('ready_to_move.json') as open_file:
##        es.index(index='ready_to_move',doc_type='project_data',id= 1,body=json.load(open_file))

    with open('project_data.json') as open_file:
        es.index(index='project_data',doc_type='projectData',id=1,body=json.load(open_file))

    with open('project_features.json') as open_file:
        es.index(index='project_features_index',doc_type='project_features_doc',id=1,body=json.load(open_file))

##    with open('project.json') as open_file:
##        es.index(index='project_features',doc_type='project_feature',id= 1,body=json.load(open_file))

    project_data_json = es.get(index='project_data',doc_type='projectData',id=1)
    project_data_json = project_data_json['_source']

    project_features_json = es.get(index='project_features_index',doc_type='project_features_doc',id=1)
    project_features_json = project_features_json['_source']

##    project_data = es.get(index='ready_to_move',doc_type='project_data',id=1)
##    project_data = project_data['_source']

##    project_features = es.get(index='project_features',doc_type='project_feature',id=1)
##    project_features = project_features['_source']

    allKeys =  getAllKeys(project_features_json)

    
    dictionary = project_data_json['underConstruction']     #has to change for every type of field 
    
    keys = getAllKeys(project_features_json)                #returns all keys present in features which are to be updated with values
    keyValues = {}

    dictValues = featureDict(keyValues,dictionary,keys)     # returns a dictionary having keys and values of above keys 
    dictValues['underConstruction'] = 1
    pfs = mapValues(dictValues,project_features_json)       # maps all values to the feature JSON

    jpfs = json.dumps(pfs)

    calculateMean(project_data_json)                        # calculates the mean pf price and size of all projects

    projectF = hmlMapping(project_data_json,project_features_json,'underConstruction')#maps price and size values to high,medium or low

    projectF = accoMapping(project_data_json,project_features_json)
    pj = json.dumps(projectF)

    print pj
