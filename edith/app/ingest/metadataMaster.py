#!/usr/bin/env python3
# standard library imports
import json
import os
import re ,sys
import urllib.parse
# local imports
from config import app_config
from .. import db
from . import metadataQuery
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
metadataMasterDict['inputType'] = ''
metadataMasterDict['canonicalName'] = ''

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
		
		self.idNumber = None
		self.parse_primary_identifier()
		
		self.barcode = None
		self.parse_barcode_from_filename()

		self.filemakerID = None
		self.parse_fmID_from_filename()

		# `identifier` is "the one" ID to search filemaker on
		self.identifier = None
		self.set_identifier()

		self.metadataSource = 0	

		# init a base dict
		self.innerMetadataDict = {"hasBAMPFAmetadata":False}
		self.metadataDict = {
			self.objectPath:{
				"basename":self.basename,
				"metadata": self.innerMetadataDict
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
				print("THIS IS THE ID NUMBER: "+self.idNumber)
			else:
				self.idNumber = None
		else:
			self.idNumber = None	

		return True

	def parse_barcode_from_filename(self):
		'''
		Try to get a "PM1234567" barcode from self.basename
		'''
		barcodeRegex = re.compile(r"(.+)(pm\d{7})(.*)",re.IGNORECASE)
		barcodeMatch = re.match(barcodeRegex,self.basename)
		if not barcodeMatch == None:
			self.barcode = barcodeMatch.group(2)
		else:
			self.barcode = None
		return True

	def parse_fmID_from_filename(self):
		'''
		Try to get a FileMaker record id "ITM1234567"
		from self.basename
		'''
		fmIDRegex = re.compile(r"(.+\_)(ITM\d{7})(.*)",re.IGNORECASE)
		fmIDRegexMatch = re.match(fmIDRegex,self.basename)
		self.filemakerID = None

		try:
			self.filemakerID = fmIDRegexMatch.group(2)
		except:
			pass

		print("THIS IS THE FILEMAKER RECORD ID: {}".format(str(self.filemakerID)))
		return True

	def set_identifier(self):
		'''
		Look for one of the three possible BAMPFA FileMaker identifiers:
		  the order of precedence is:
		    accession # -> barcode -> filemaker record ID


		'''
		print(self.idNumber,self.barcode,self.filemakerID)
		if self.idNumber != None:
			self.identifier = self.idNumber
		elif self.idNumber == None and self.barcode != None:
			self.identifier = self.barcode
		elif (self.idNumber == None and self.barcode == None) and self.filemakerID != None:
			self.identifier = self.filemakerID
		else:
			self.identifier = None

		print("THIS IS THE IDENTIFIER: {}".format(str(self.identifier)))

		return True

	def fetch_metadata(self,dataSourceAccessDetails):
		'''
		Given a set of target credentials for an external data source,
		go get some metadata based on self.identifier.
		'''
		if self.identifier != None:
			try:
				print('searching FileMaker on '+str(self.identifier))
				FMmetadata = metadataQuery.xml_query(
					self,
					self.identifier,
					dataSourceAccessDetails
					)
				if FMmetadata:
					# add any filemaker metadata to the dict
					self.add_more_metadata(FMmetadata)
					self.retrievedExternalMetadata = True
			except:
				if len(self.identifier) < 5:
					idNumberPadded = "{0:0>5}".format(str(self.idNumber))
					print('searching FileMaker on '+idNumberPadded)
					try:
						FMmetadata = metadataQuery.xml_query(
							self,
							idNumberPadded,
							dataSourceAccessDetails
							)
						if FMmetadata:
							# add any filemaker metadata to the dict
							self.add_more_metadata(FMmetadata)
							self.retrievedExternalMetadata = True
					except:
						print("Error searching FileMaker on "\
							"{}".format(str(self.identifier)
							)
				else:
					print("Didn't find a FileMaker record for "\
							"{}".format(str(self.identifier))
							)
		else:
			print("Didn't find an identifier to search FileMaker with.")
			pass

		print('metadataDict')
		print(self.innerMetadataDict)
		return True

	def add_more_metadata(self,moreMetadata):
		'''
		This actually adds metadata values to the object.
		`moreMetadata` should be a dict with keys aligning with the
		canonical metadata fields in the EDITH instance.
		It could be supplied by the user during the ingest process,
		or could be supplied by an external data source.
		'''
		for key, value in moreMetadata.items():
			if key in self.innerMetadataDict:
				if self.innerMetadataDict[key] in (None,'None',''):
					self.innerMetadataDict[key] = value
				else:
					# IF THERE'S ALREADY A VALUE HERE, DON'T REPLACE IT
					# THIS MAKES IT SO THAT USER-SUPPLIED METADATA ** REPLACES **
					# ANYTHING THAT EXISTS IN A FILEMAKER SOURCE
					pass

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

