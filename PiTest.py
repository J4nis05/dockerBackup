import requests
import json
from datetime import datetime

# Required Endpoints
#
# | Method  | Endpoint             |
# |---------|----------------------|
# | POST    | /backup              | --> Portainer Config Backup | optional Parm "password"
# | GET     | /stacks              | --> List Stacks. Param filters: EndpointID, SwarmID
# | POST    | /stacks/{id}/stop    | --> Stop Stack | Needs Parm id (of Stack) and endpointId
# | POST    | /stacks/{id}/start   | --> Start Stack | Needs Parm id (of Stack) and endpointId
#
# To Do
# * Define Execution Order
#   --> Portainer Backup, Get Stack Ids and Stop them, copy Container Data to back up server, start Stacks
# * How to access remote Server (with tools like rsync, etc.)
# * Copy Data from Homelab to back up Server
# * Restore Script

api_url = 'http://192.168.1.90:9000/api'
with open('pi.key', 'r') as file:
    api_key = file.read()


def get_endpoints():
    # ==================================================================================
    # Example that gets Endpoints and saves them in a json file
    api_endpoint = '/endpoints'
    headers = {'X-API-Key': api_key}
    request = requests.get(api_url + api_endpoint, headers=headers)

    if request.status_code == 200:
        data_list = request.json()
        sorted_request = sorted(data_list, key=lambda x: x.get('Name', ''))
        response = json.dumps(sorted_request, indent=2)

        with open('output/endpoints.json', 'w') as endpoints:
            endpoints.write(response)
    else:
        date = datetime.now()
        print(f'Error {request.status_code} - {request.text}')

        with open('output/error.log', 'a') as log:
            log.write(f'{date} \n{request.status_code} -=- {request.text} \n')
    # ==================================================================================


def get_backup():
    api_endpoint = '/backup'
    headers = {'X-API-Key': api_key, 'Content-Type': 'application/json'}
    data = {'password': ''}

    request = requests.post(api_url + api_endpoint, headers=headers, data=json.dumps(data))

    if request.status_code == 200:
        response_headers = request.headers
        filename = response_headers.get('Content-Disposition').split('filename=')[1]
        response_content = request.content

        with open(f'output/{filename}', 'wb') as backup:
            backup.write(response_content)

        print(f'Backup file "{filename}" successfully created.')
    else:
        date = datetime.now()
        print(f'Error {request.status_code} - {request.text}')

        with open('output/error.log', 'a') as log:
            log.write(f'{date} \n{request.status_code} -=- {request.text} \n')

        print('Backup file creation failed.')


def get_stacks():
    api_endpoint = '/stacks'
    headers = {'X-API-Key': api_key, 'Content-Type': 'application/json'}
    request = requests.get(api_url + api_endpoint, headers=headers)

    if request.status_code == 200:
        response_json = json.loads(request.text)

        stack_ids = [stack['Id'] for stack in response_json]
        entrypoint_ids = [entrypoint['Id'] for entrypoint in response_json]

        return stack_ids, entrypoint_ids
    else:
        date = datetime.now()
        print(f'Error {request.status_code} - {request.text}')

        with open('output/error.log', 'a') as log:
            log.write(f'{date} \n{request.status_code} -=- {request.text} \n')

        return None


def stop_stacks(stack_ids, entrypoint_ids):
    print(stack_ids + entrypoint_ids)


stacks, entrypoints = get_stacks()
stop_stacks(stacks)
print('Done!')
