import requests
import json
import datetime
import os

# Required Endpoints
#
# | Method  | Endpoint             |
# |---------|----------------------|
# | POST    | /backup              | --> Portainer Config Backup | optional Parm "password"
# | GET     | /stacks              | --> List Stacks. Param filters: EndpointID, SwarmID
# | GET     | /stacks/{id}/file    | --> Returns Docker Compose of Stack as JSON (slightly cursed)
# | POST    | /stacks/{id}/stop    | --> Stop Stack | Needs Parm id (of Stack) and endpointId
# | POST    | /stacks/{id}/start   | --> Start Stack | Needs Parm id (of Stack) and endpointId
#
# To Do
# * Define Execution Order
#   --> Portainer Backup, Get Stack Ids and Stop them, copy Container Data to back up server, start Stacks
# * How to access remote Server (with tools like rsync, etc.)
# * Copy Data from Homelab to back up Server
# * Restore Script


def get_endpoints():
    # ==================================================================================
    # Example that gets Endpoints and saves them in a json file

    with open('pi.key', 'r') as file:
        api_key = file.read()
    api_url = 'http://192.168.1.90:9000/api'
    api_endpoint = '/endpoints'

    headers = {'X-API-Key': api_key}
    request = requests.get(api_url + api_endpoint, headers=headers)

    if request.status_code == 200:
        data_list = request.json()
        sorted_request = sorted(data_list, key=lambda x: x.get('Name', ''))
        response = json.dumps(sorted_request, indent=2)

        with open('output/settings.json', 'w') as file:
            file.write(response)
    else:
        date = datetime.datetime.now()
        print(f'Error {request.status_code} - {request.text}')

        with open('output/error.log', 'a') as log:
            log.write(f'{date} \n{request.status_code} -=- {request.text} \n')
    # ==================================================================================


get_endpoints()
print('Done')
