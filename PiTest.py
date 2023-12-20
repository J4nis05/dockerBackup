import requests
import json
import os

with open('pi.key', 'r') as file:
    api_key = file.read()
api_url = 'http://192.168.1.90:9000/api'
api_endpoint = '/endpoints'

headers = {'X-API-Key': api_key}
request = requests.get(api_url + api_enpoint, headers=headers)

if request.status_code == 200:
    data_list = request.json()
    sorted_request = sorted(data_list, key=lambda x: x.get('Name', ''))
    response = json.dumps(sorted_request, indent=2)

    if os.path.exists('output/endpoints.json'):
        os.remove('output/endpoints.json')

    with open('output/endpoints.json', 'w') as file:
        file.write(response)

    print('done!')
else:
    print(f'Error {request.status_code} - {request.text}')
