#!/usr/bin/env python
from __future__ import print_function
from azure.cli.core import get_default_cli
import datetime
import subprocess
import sys
import os
import json
import requests
import logging

DIR_NAME = os.path.dirname(os.path.realpath(__file__))

def setup_custom_logger(name):
    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    handler = logging.FileHandler('dolos.txt', mode='w')
    handler.setFormatter(formatter)
    screen_handler = logging.StreamHandler(stream=sys.stdout)
    screen_handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    logger.addHandler(screen_handler)
    return logger

logger = setup_custom_logger('dolos')

def az(command):
    return get_default_cli().invoke(command)

def log(message):
    logger.info(message)

def status(code):
    if code != 0:
        log("Error")
        sys.exit(1)
    return True

def cleanup():
    log("Attempting to delete cluster")
    destroy_start_time = datetime.datetime.now()
    az(['group', 'delete', '--name', 'dolos', '--yes'])
    destroy_end_time = datetime.datetime.now()
    log("Cluster delete finished")
    destroy_total_time = destroy_end_time - destroy_start_time
    log("Total destroy time taken: %s" % str(destroy_total_time))
    try:
        subprocess.check_output(['kubectl', 'config', 'unset', 'current-context'])
        subprocess.check_output(['kubectl', 'config', 'unset', 'users.clusterUser_dolos_dolos'])
        subprocess.check_output(['kubectl', 'config', 'delete-cluster', 'dolos'])
        subprocess.check_output(['kubectl', 'config', 'delete-context', 'dolos'])
    except:
        pass

if __name__ == '__main__':

    cleanup()

    create_start_time = datetime.datetime.now()
    log("Starting test")

    log("Creating Resource Group")
    group_create = az(['group', 'create', '--name', 'dolos', '--location', 'eastus'])
    status(group_create)

    log("Creating the AKS cluster")
    aks_create = az(['aks', 'create', '--resource-group', 'dolos', '--name', 'dolos', '--node-count', '1', '--generate-ssh-keys'])
    status(aks_create)

    log("Getting cluster credentials")
    get_creds = az(['aks', 'get-credentials', '--resource-group', 'dolos', '--name', 'dolos'])

    log("Get Nodes")
    nodes = subprocess.check_output(['kubectl', 'get', 'nodes'])
    print(nodes)

    log("Applying Deployment")
    deploy_file = os.path.join(DIR_NAME, 'fixtures', 'azure-vote.yaml')
    deployment = subprocess.check_output(['kubectl', 'apply', '-f', deploy_file])
    print(deployment)

    log("Getting external IP")
    while True:
        try:
            service = subprocess.check_output(['kubectl', 'get', 'service', 'azure-vote-front', '--output', 'json'])
            external_ip = json.loads(service)['status']['loadBalancer']['ingress'][0]['ip']
            if external_ip:
                if any(char.isdigit() for char in external_ip):
                    break
        except:
            pass

    log("Getting web contents from %s" % external_ip)
    content = requests.get("http://" + external_ip).text

    with open(os.path.join(DIR_NAME, 'fixtures', 'azure-vote.html'), 'r') as testfile:
        test_data = testfile.read()

    if test_data == content:
        log("Test passed. Cluster complete.")
        create_end_time = datetime.datetime.now()
        create_total_time = create_end_time - create_start_time
        log("Total create time taken: %s" % str(create_total_time))
    else:
        log("Test failed. Exiting.")
        sys.exit(1)

    cleanup()
