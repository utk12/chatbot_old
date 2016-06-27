# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 11:08:59 2016

@author: utkarsh
"""

import pandas as pd
pd.set_option('expand_frame_repr', False)
data = pd.read_csv('Data/buy_questions.csv')
data = pd.DataFrame(data)
data.index = data['sn']
data_subset = data.loc[4:7]
print data_subset['bot_question'][data_subset.index == 6]
