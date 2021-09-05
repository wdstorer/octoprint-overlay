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
  else:
    print "Printer is online"

def getStats():
  response = httpgetrequest(config.octoprinturl + "/api/job")
  jobData = json.loads(response.text)
  print jobData['job']['file']['name']
  if jobData['progress']['printTimeLeft']:
    print "Print time left: %s minutes" % (jobData['progress']['printTimeLeft']/60)

  response = httpgetrequest(config.octoprinturl + "/api/printer")
  printerData = json.loads(response.text)
  if not printerData['error']:
    print "Temperature (bed): %s" % (printerData['temperature']['bed']['actual'])
    print "Temperature (extruder): %s" % (printerData['temperature']['tool0']['actual'])

getPrinterState()
getStats()

