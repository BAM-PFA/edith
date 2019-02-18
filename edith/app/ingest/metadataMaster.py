#!/usr/bin/env python3
# standard library imports
import json
# local imports
from config import app_config
from .. import db
from ..models import Metadata_Field



metadataMasterDict = {}

metadataMasterDict['tags'] = ''
metadataMasterDict['country'] = ''
metadataMasterDict['title'] = ''
metadataMasterDict['nameSubjects'] = ''
metadataMasterDict['frameRateProxy'] = ''
metadataMasterDict['altTitle'] = ''
metadataMasterDict['releaseYear'] = ''
metadataMasterDict['accPref'] = ''
metadataMasterDict['accDepos'] = ''
metadataMasterDict['accItem'] = ''
metadataMasterDict['accFull'] = ''
metadataMasterDict['projGrp'] = ''
metadataMasterDict['directorsNames'] = ''
metadataMasterDict['credits'] = ''
metadataMasterDict['generalNotes'] = ''
metadataMasterDict['conditionNote'] = ''
metadataMasterDict['Barcode'] = ''
metadataMasterDict['language'] = ''
metadataMasterDict['soundCharacteristics'] = ''
metadataMasterDict['color'] = ''
metadataMasterDict['runningTime'] = ''
metadataMasterDict['medium'] = ''
metadataMasterDict['dimensions'] = ''
metadataMasterDict['videoFormat'] = ''
metadataMasterDict['videoStandard'] = ''
metadataMasterDict['ingestUUID'] = ''
metadataMasterDict['eventTitle'] = ''
metadataMasterDict['eventYear'] = ''
metadataMasterDict['eventFullDate'] = ''
metadataMasterDict['eventSeries'] = ''
metadataMasterDict['eventRelatedExhibition'] = ''
metadataMasterDict['eventLocation'] = ''
metadataMasterDict['description'] = ''
metadataMasterDict['creator'] = ''
metadataMasterDict['creatorRole'] = ''
metadataMasterDict['eventOrganizer'] = ''
metadataMasterDict['assetExternalSource'] = ''
metadataMasterDict['copyrightStatement'] = ''
metadataMasterDict['restrictionsOnUse'] = ''
metadataMasterDict['generation'] = ''
metadataMasterDict['frameRateTRTdetails'] = ''
metadataMasterDict['platformOutlet'] = ''
metadataMasterDict['editSequenceSettings'] = ''
metadataMasterDict['additionalCredits'] = ''
metadataMasterDict['postProcessing'] = ''
metadataMasterDict['exportPublishDate'] = ''
metadataMasterDict['PFAfilmSeries'] = ''
metadataMasterDict['recordingDate'] = ''
metadataMasterDict['digitizedBornDigital'] = ''
metadataMasterDict['digitizer'] = ''
metadataMasterDict['locationOfRecording'] = ''
metadataMasterDict['speakerInterviewee'] = ''
metadataMasterDict['filmTitleSubjects'] = ''
metadataMasterDict['topicalSubjects'] = ''
metadataMasterDict['recordingAnalogTechnicalNotes'] = ''
metadataMasterDict['audioRecordingID'] = ''
metadataMasterDict['recordingPermissionsNotes'] = ''
metadataMasterDict['analogTapeNumber'] = ''
metadataMasterDict['analogTapeSide'] = ''
metadataMasterDict['digitizationQCNotes'] = ''

# metadataMasterDict[''] = ''

metadataMasterDict['hasBAMPFAmetadata'] = ""

class Metadata:
	'''
	Metadata instance for an asset being ingested
	use object input path as ID ... ?
	'''
	def __init__(self,objectPath):
		self.objectPath = objectPath
		# init a base dict
		self.metadataDict = {"hasBAMPFAmetadata":False}
		# get all the defined fields from the db
		self.availableMetadataFields = db.session.query(Metadata_Field).all()
		for field in self.availableMetadataFields:
			# build out the metadata dict
			self.metadataDict[field.fieldUniqueName] = None

	def get_external_identifier(self):
		'''
		Parse the ID/accession number from self.objectPath
		'''
		# self.idNumber = parse self.objectPath
		# return self.idNumber
		pass

	def get_json(self):
		metadata = self.metadataDict
		_json = json.dumps(metadata)

		return(_json)

	def write_json_file(self,jsonPath):
		'''
		Provided an output path for a JSON file,
		write self.metadataDict to it
		'''
		self.metadataFilepath = jsonPath
		with open(jsonPath,'w+') as jsonTemp:
			json.dump(self.metadataDict,jsonTemp)

		return self

	def fetch_metadata(self,dataSourceAccessDetails):
		'''
		Given a set of target credentials for an external data source,
		go get some metadata based on self.idNumber
		take logic from ingestProcesses.get_metadata()
		'''
		# return self.metadataDict ... i guess?
		pass



