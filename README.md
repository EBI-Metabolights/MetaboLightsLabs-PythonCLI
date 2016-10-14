
### Python script to upload project folders/files to MetaboLights Labs Projects ###

----------

*Please note this wrapper is still in development. Create an issue if you find a bug.

Dependencies:
os, sys, argparse, json, requests, subprocess

Usage:

    python uploadToMetaboLightsLabs.py -t MetaboLights Labs API_KEY -i [ filesToUpload ] -p MetaboLights Labs Project_ID -n -s ENV

or

    uploadToMetaboLightsLabs.py -t MetaboLights Labs API_KEY -i [ filesToUpload ] -p MetaboLights Labs Project_ID -n -s ENV

Arguments:
	

	    -t MetaboLights Labs API_KEY
    	-i pathToFile1, pathToFile2, . . ., pathToFileN
    	-p MetaboLights Labs Project ID
    	-n Create new project if project doesnt exist
    	-s server [ "prod", "dev", "test" ] 