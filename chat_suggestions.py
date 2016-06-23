# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 11:15:47 2016

@author: utkarsh
"""
#assume a json object being given
input = ''
from chatbot import get_reply
from wit_get_reply_api import get_say_action

output = {}
output['sug1'] = get_reply(input)
output['sug2'] = get_say_action(input)
