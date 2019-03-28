#!/usr/bin/env python3
# standard library imports
import json
import os
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
		self.basename = os.path.basename(self.objectPath)
		self.idNumber = self.get_primary_identifier(self.basename)
		self.barcode = self.get_barcode_from_filename(self.basename)

		# init a base dict
		self.metadataDict = {"hasBAMPFAmetadata":False}
		# get all the defined fields from the db
		self.availableMetadataFields = db.session.query(Metadata_Field).all()
		for field in self.availableMetadataFields:
			# build out the metadata dict
			self.metadataDict[field.fieldUniqueName] = None

	def get_primary_identifier(self,basename):
		'''
		Parse a 5-digit ID number from self.basename
		'''
		idRegex = re.compile(r'(.+\_)(\d{5})((\_.*)|($))')
		idMatch = re.match(idRegex, basename)
		if not idMatch == None: 
			idNumber = idMatch.group(2)
			if not idNumber == "00000":
				idNumber = idNumber.lstrip("0")
		else:
			idNumber = "--"	

		print("THIS IS THE ID NUMBER: "+idNumber)

		return idNumber

	def get_barcode_from_filename(self,basename):
		'''
		Try to get a "PM1234567" barcode from self.basename
		'''
		barcodeRegex = re.compile(r"(.+\_\d{5}\_)(pm\d{7})(.+)",re.IGNORECASE)
		barcodeMatch = re.match(barcodeRegex,basename)
		if not barcodeMatch == None:
			barcode = barcodeMatch.group(2)
		else:
			barcode = "000000000"
		return barcode

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



