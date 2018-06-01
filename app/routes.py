from app import app
from flask import request
import os

'''
@app.before_request
def log_curl_from_request():
	headers = ''
	for line in str(request.headers).split('\r\n'):
		if len(line) > 2 and 'Host' not in line:
			headers += ' -H "' + line + '"'
	curl = 'curl -s -X ' + request.method + headers + ' --data ' + str(request.get_data())[1:] + ' "'+request.url.replace(request.url_root,'https://api-example.com/')+'"'
	open('curls.txt','a').write(curl)
	return 'Saved'
'''

import random
import string
import time
import json

def remove_duplicates(target_list):
    key_set = set()
    ret_list = []
    for target in target_list:
        unique_key = target['app'] + ':' + target['version']
        if unique_key not in key_set:
            ret_list.append(target)
            key_set.add(unique_key)
    return ret_list


@app.route("/", methods=['POST'])
def receive():
    data = json.loads(request.form['json'])['appsDetected']
    open('out.txt','a').write(', "apps": ')
    insert_data_list = list(map(lambda d: {
        'app': d['app'],
        'version': d['version']
    }, data.values()))
    old_data = {}
    old_data['apps'] = remove_duplicates(insert_data_list)
    open('out.txt','a').write(str(old_data['apps']).replace("'",'"'))
    return 'Saved.'
