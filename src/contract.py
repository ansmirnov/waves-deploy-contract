import json
import os
import requests
import sys


def find_param_value(params, name):
    for param in params:
        if param['key'] == name: return param['value']
    return None


def print_success(results):
    print(json.dumps(results, separators=(',', ':')))


def print_error(message):
    print(message)
    sys.exit(3)


def get_value(contract_id):
    node = os.environ['NODE_API']
    if not node:
        print_error("Node REST API address is not defined")
    token = os.environ["API_TOKEN"]
    if not token:
        print_error("Node API token is not defined")
    headers = {'X-Contract-Api-Token': token}
    url = '{0}/internal/contracts/{1}/sum'.format(node, contract_id)
    r = requests.get(url, verify=False, timeout=2, headers=headers)
    data = r.json()
    return data['value']


if __name__ == '__main__':
    command = os.environ['COMMAND']
    if command == 'CALL':
        contract_id = json.loads(os.environ['TX'])['contractId']
        value = get_value(contract_id)
        print_success([{
            "key": "sum",
            "type": "integer",
            "value": value + 1}])
    elif command == 'CREATE':
        print_success([{
            "key": "sum",
            "type": "integer",
            "value": 0}])
    else:
        print_error("Unknown command {0}".format(command))
