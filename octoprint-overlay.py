#!/usr/bin/python
import sys
import requests
import json
import config
import argparse

headers = {
   "Accept": "application/json",
   "Content-Type": "application/json",
   "Authorization": "Bearer " + config.apikey
}

def httpgetrequest(url):
  response = requests.request(
    "GET",
    url,
    headers=headers
  )
  return response

def getPrinterState():
  response = httpgetrequest(config.octoprinturl + "/api/job")
  jobState = 'Offline'
  jobInfo = json.loads(response.text)
  if 'Offline' in jobInfo['state']:
    print "Printer is offline"
    sys.exit()       

def getStats():
  response = httpgetrequest(config.octoprinturl + "/api/job")
  jobData = json.loads(response.text)
  if jobData['job']['file']['name']: 
    print jobData['job']['file']['name']
  if jobData['progress']['printTime']:
    print "Print time: %s" % ("{}:{:02d}".format(*divmod(jobData['progress']['printTime']/60, 60)))
  if jobData['progress']['printTimeLeft']:
    print "%s remaining" % ("{}:{:02d}".format(*divmod(jobData['progress']['printTimeLeft']/60, 60)))

  response = httpgetrequest(config.octoprinturl + "/api/printer")
  printerData = json.loads(response.text)
  print "Bed temp: %sC" % (printerData['temperature']['bed']['actual']) 
  print "Extruder temp: %sC" % (printerData['temperature']['tool0']['actual'])

getPrinterState()
getStats()

