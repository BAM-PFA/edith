#!/usr/bin/env python3
# standard library imports
import json
import os
import re
import urllib.parse
# local imports
from config import app_config
from .. import db
from ..models import Metadata_Field
from .. import utils



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
		self.idNumber = self.parse_primary_identifier()
		self.barcode = self.parse_barcode_from_filename()

		self.metadataSource = 0	

		# init a base dict
		self.innerMetadataDict = {"hasBAMPFAmetadata":False}
		self.metadataDict = {
			self.objectPath:{
				"basename":self.basename,
				"metadata":{
					"":""
					}
				}
			}
		# get all the defined fields from the db
		self.availableMetadataFields = db.session.query(Metadata_Field).all()
		for field in self.availableMetadataFields:
			# build out the metadata dict
			self.innerMetadataDict[field.fieldUniqueName] = None

		self.retrievedExternalMetadata = False

		self.metadataJSON = None
		self.metadataJSONpath = None

		self.resourcespaceQuotedJSON = None

	def parse_primary_identifier(self):
		'''
		Parse a 5-digit ID number from self.basename
		BAMPFA filenames require this be between underscores:
		  something_12345_something-else.ext
		'''
		idRegex = re.compile(r'(.+\_)(\d{5})((\_.*)|($))')
		idMatch = re.match(idRegex, self.basename)
		if not idMatch == None: 
			idNumber = idMatch.group(2)
			if not idNumber == "00000":
				# actually, take off leading zeroes just in case
				# the db record doesn't include it.
				self.idNumber = idNumber.lstrip("0")
			else:
				self.idNumber = idNumber
		else:
			self.idNumber = "--"	

		print("THIS IS THE ID NUMBER: "+self.idNumber)

		return self.idNumber

	def parse_barcode_from_filename(self):
		'''
		Try to get a "PM1234567" barcode from self.basename
		'''
		barcodeRegex = re.compile(r"(.+\_\d{5}\_)(pm\d{7})(.+)",re.IGNORECASE)
		barcodeMatch = re.match(barcodeRegex,self.basename)
		if not barcodeMatch == None:
			self.barcode = barcodeMatch.group(2)
		else:
			self.barcode = "000000000"
		return self.barcode

	def fetch_metadata(self,dataSourceAccessDetails):
		'''
		Given a set of target credentials for an external data source,
		go get some metadata based on self.idNumber or self.barcode.
		'''
		if self.idNumber == "--":
			print("NO BAMPFA ID NUMBER")

		elif self.idNumber == '00000':
			# if the acc item number is zeroed out,
			# try looking for a barcode to search on
			try:
				if self.barcode == "000000000":
					print("ID AND BARCODE BOTH ZEROED OUT")

				else:
					FMmetadata = metadataQuery.xml_query(
						self.barcode,
						dataSourceAccessDetails
						)
					if FMmetadata:
						# add any filemaker metadata to the dict
						self.add_more_metadata(FMmetadata)
						self.retrievedExternalMetadata = True
			except:
				print("Error searching FileMaker on ID and barcode")
		else:
			try:
				print('searching FileMaker on '+self.idNumber)
				FMmetadata = metadataQuery.xml_query(
					self.idNumber,dataSourceAccessDetails)

				if FMmetadata:
					# add any filemaker metadata to the dict
					self.add_more_metadata(FMmetadata)
					self.retrievedExternalMetadata = True
			except:
				# if no results, try padding with zeros
				idNumberPadded = "{0:0>5}".format(self.idNumber)
				print('Now searching FileMaker on '+self.idNumber)
				try:
					FMmetadata = metadataQuery.xml_query(
						idNumberPadded,
						dataSourceAccessDetails
						)
					if FMmetadata:
						# add any filemaker metadata to the dict
						self.add_more_metadata(FMmetadata)
						self.retrievedExternalMetadata = True
				except:
					# give up
					pass

		print('metadataDict')
		print(self.innerMetadataDict)
		return True

	def add_more_metadata(self,moreMetadata):
		'''
		moreMetadata should be a dict with keys aligning with the
		canonical metadata fields in the EDITH instance.
		It could be supplied by the user during the ingest process,
		or could be supplied by an external data source.
		'''
		for key, value in moreMetadata.items():
			if key in self.innerMetadataDict:
				self.innerMetadataDict[key] = value

		return True

	def clear_empty_metadata_fields(self):
		'''
		Remove empty metadata fields
		'''
		self.innerMetadataDict = {
			key:value for key, value in self.innerMetadataDict.items()
			if value not in ('',None,"null","Null")
		}

	def set_hasBAMPFAmetadata(self):
		if all(
			value in ('',None,"null","Null") for value in 
				self.innerMetadataDict.values()
			):
			self.innerMetadataDict['hasBAMPFAmetadata'] = False
		else:
			self.innerMetadataDict['hasBAMPFAmetadata'] = True

	def set_json(self):
		'''
		Make self.metadataDict a JSON object
		'''
		self.metadataDict[self.objectPath]['metadata'] = self.innerMetadataDict
		try:
			self.metadataJSON = json.loads(self.metadataDict)
		except:
			self.metadataJSON = self.metadataDict
		return True

	def write_json_file(self):
		'''
		Write self.metadataDict to a JSON file
		in the EDITH temp directory.
		'''
		self.set_json()
		tempDir = utils.get_temp_dir()
		outpath = os.path.join(tempDir,self.basename+".json")
		with open(outpath,'w+') as jsonTemp:
			json.dump(self.metadataJSON,jsonTemp)
		if os.path.isfile(outpath):
			print("Wrote JSON file to {}".format(outpath))
			self.metadataJSONpath = outpath
		else:
			print("Error writing JSON to file at {}".format(outpath))
			self.metadataJSONpath = None

		return outpath

	def delete_temp_JSON_file(self):
		if os.path.isfile(self.metadataJSONpath):
			try:
				os.remove(self.metadataJSONpath)
			except:
				print("Couldn't delete the temp JSON file at {}".format(
					self.metadataJSONpath
					)
				)
		else:
			print("{} is not an existing file, can't delete".format(
				self.metadataJSONpath
				)
			)
		return self

	def prep_resourcespace_JSON(self):
		'''
		Prepare URL-escaped JSON for posting to ResourceSpace
		'''
		rsMetaDict = {}
		for key, value in self.innerMetadataDict.items():
			try:
				field = Metadata_Field.query.filter_by(
					fieldUniqueName=key
					).first()
				rsFieldID = field.rsFieldID
				rsMetaDict[int(rsFieldID)] = value
			except:
				pass

		# hard coded proxy framerate 
		# -->the field id is a default in resourcespace!
		# if it's empty (e.g. for audio), ignore it
		frameRateProxy = self.innerMetadataDict['frameRateProxy']
		if not frameRateProxy in ('',None,"null","Null"):
			rsMetaDict[76] = self.innerMetadataDict['frameRateProxy']

		rsMetaJSON = json.dumps(rsMetaDict,ensure_ascii=False)
		# print(rsMetaJSON)
		quotedJSON = urllib.parse.quote(rsMetaJSON.encode())
		if "%5Cn" in quotedJSON:
			print("REPLACING NEWLINES")
			quotedJSON = quotedJSON.replace('%5Cn','%3Cbr%2F%3E')

		self.resourcespaceQuotedJSON = quotedJSON

		return quotedJSON

