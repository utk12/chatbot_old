# -*- coding: utf-8 -*-
"""
Created on Tue Jun 21 15:18:31 2016

@author: utkarsh
"""

import json
with open('/home/utkarsh/roofpik/features_roofpik/json_features/project.json') as project:
    pfs = json.loads(project.read())
#pfs = project feature set
#print(pfs)
with open('/home/utkarsh/roofpik/features_roofpik/json_features/project_data.json') as project_data:
    pd = json.loads(project_data.read())
#pd = project dataset
#print(pd)
def update_ratio_score():
    for key in pfs: #buy level
        for k in pfs[key]:  #project_type level
            for k1 in pfs[key][k]:  #ratio_score level
                if k1 == 'children':
                    sum1 = 0.0
                    count = 0.0
                    for k2 in pfs[key][k][k1]:    #values of children level                        
                        count += 1
                        sum1 += pfs[key][k][k1][k2]
                    pfs[key][k]['ratio_score'] = sum1/count
