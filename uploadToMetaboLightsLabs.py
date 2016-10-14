#!/usr/bin/env python

"""
Python script to upload project folders/files to MetaboLights Labs Projects

Dependencies:
	os, sys, argparse, json, requests, subprocess

Usage:
	python uploadToMetaboLightsLabs.py -t <MetaboLights Labs API_KEY> -i [ <filesToUpload> ] -p <MetaboLights Labs Project_ID> -n -s <ENV>
	or
	uploadToMetaboLightsLabs.py -t <MetaboLights Labs API_KEY> -i [ <filesToUpload> ] -p <MetaboLights Labs Project_ID> -n -s <ENV>

Arguments:
	-t MetaboLights Labs API_KEY
	-i pathToFile1, pathToFile2, . . ., pathToFileN
	-p MetaboLights Labs Project ID
	-n Create new project if project doesnt exist
	-s server [ "prod", "dev", "test" ] 
"""

import os
import sys
import argparse
import logging
import json
import requests
import subprocess

api_token = None
directories = []
files = []
project_id = None
new_project_flag = False
log_file = "log.txt"
env = "dev"
servers = [ "prod", "dev", "test" ]
serverPortDictionary = {
	"prod" : {
		"server" : "http://www.ebi.ac.uk/metabolights/",
		"port" : ""
	},
	"dev" : {
		"server" : "http://wwwdev.ebi.ac.uk/metabolights/",
		"port" : ""
	},
	"test" : {
		"server" : "http://localhost.ebi.ac.uk:8080/metabolights/",
		"port" : ""
	}
}

def main(arguments):
	logging.basicConfig(filename=log_file, level=logging.INFO)
	parser = argparse.ArgumentParser( description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
	parser.add_argument('-t', required = True, help='MetaboLights API Key')
	parser.add_argument('-i', required = True, nargs='+', help="Input folder(s)/file(s)")
	parser.add_argument('-p', help='MetaboLights Labs Project ID')
	parser.add_argument('-n', help='Create new MetaboLights Labs Project if doesnt exist',  action='store_true')
	parser.add_argument('-s', help='Server details. Allowed values are '.join(servers) ,  choices=servers)
	args = parser.parse_args(arguments)
	#parser.print_help()
	logging.info("Validating Input Parameters")
	# validating input
	if parseInput(args):
		# Input validation success
		logging.info("Input validation Success")
		# Request MetaboLights Labs webservice for aspera upload configuration 
		logging.info("Requesting project aspera upload configuration")
		asperaConfiguration = requestUploadConfiguration()
		logging.info("Required project details obtained")
		# Compile the aspera CLI command from the configuration
		logging.info("Compling aspera command")
		asperaCommand  = compileAsperaCommand(asperaConfiguration)
		logging.info("Checking aspera Environment variables")
		executeAsperaUpload(asperaCommand)
		logging.info("Executing aspera command")
		logging.info("File(s)/Folder(s) upload successful")				
	else:
		logging.info("Input validation Failed: Terminating program")
		print "Invalid Input: Please check the "+log_file+" for more details"

def executeAsperaUpload(cmd):
	#print cmd
	p = subprocess.Popen(['ls', '-a'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out, err = p.communicate()
	logging.info(out)
	logging.error(err)

def compileAsperaCommand(asperaConfiguration):
	asperaConfiguration = json.loads(asperaConfiguration)
	return ["./ascp", "-QT", "-L- -l 1000M", ''.join(str(e) for e in directories), ''.join(str(e) for e in files), asperaConfiguration['asperaUser'] + "@" + asperaConfiguration['asperaServer'] +":/" + env + "/userSpace/" + asperaConfiguration['asperaURL']]

def requestUploadConfiguration():
	# Requesting MetaboLightsLabs Webservice for the project configuration
	url = serverPortDictionary[env]["server"] + "webservice/workspace/asperaConfiguration"
	payload = json.dumps({'api_token': api_token, 'project_id': project_id, 'new_project_flag': new_project_flag });
	headers = { 'content-type': "application/json", 'cache-control': "no-cache" }
	try:
		response = requests.request("POST", url, data=str(payload), headers=headers)
	except requests.exceptions.RequestException as e:  # This is the correct syntax
		logging.error(e)
		print "Request failed! Refer to the log file for more details"
		sys.exit(1)
	return json.loads(response.text)['content']

def parseInput(args):
	# Assigning the user api token to the global variable
	global api_token 
	api_token = args.t
	logging.info('API Key:' + str(api_token))

	# Checking whether the input files and folders are valid and exist 
	# Creating a array of files and folders that needs to be uploaded
	for entity in args.i:
		if os.path.isfile(entity):
			global files
			files.append(entity)
			logging.info("Adding " + entity + " to the files to be uploaded list")
		if os.path.isdir(entity): 
			global directories
			directories.append(entity)
			logging.info("Adding " + entity + " to the folders to be uploaded list")
	
	# Assigning env to the global variable
	global env 
	env = args.s
	logging.info("Setting env flag: " + str(env))

	# Assigning create new flag to the global variable
	global new_project_flag 
	new_project_flag = str(args.n).lower()
	logging.info("Create new project flag provided: " + str(new_project_flag))

	# Assigning ML project id to the global variable
	global project_id 
	# If create new project flag is not set, making sure the project id exist
	if not new_project_flag:
		project_id = args.p
		logging.warning("Project_id assigned: " + str(project_id))
		if not project_id:
			logging.warning("Project_ID not assigned. Please provide -n flag if you would like to create a new project")
			return False
	else:
		project_id = args.p
		logging.info("Project_id assigned: " + str(project_id))

	# Checking if no files or folders exist
	if (len(files) == 0  and len(directories) == 0):
		logging.warning("No valid files or directories provided")
		return False
	return True

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))