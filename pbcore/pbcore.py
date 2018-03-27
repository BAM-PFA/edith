#!/usr/bin/env python3
# standard library modules
import os
import sys
import json
from copy import deepcopy
# nonstandard libraries
import lxml.etree as ET
# local modules
import pbcore_elements
import pbcore_map

class PBCoreDocument:
	'''
	Takes a preexisting well-formed pbcoreInstantiationDocument
	(in this case taken from `mediainfo --Output=PBCore2 inputfile`),
	extracts the elements under `<pbcoreInstantiationDocument>`,
	and inserts them under `<pbcoreDescriptionDocument><pbcoreInstantiation>`,
	returning an pbcoreDescriptionDocument that contains 
	descriptive metadata, info on the physical asset, plus as many
	pbcoreInstantiation tags as are necessary.
	Alternatively, it can also take in both an existing 
	pbcoreDescriptionDocument and insert additional 
	pbcoreInstantiationDocument tags.
	'''
	def __init__(self, pbcoreDescriptionDocumentPath=None):
		self.pbcoreDescriptionDocumentPath = pbcoreDescriptionDocumentPath

		self.PBCORE_NAMESPACE = "http://www.pbcore.org/PBCore/PBCoreNamespace.html"
		self._PBCORE = "{{}}".format(self.PBCORE_NAMESPACE)
		self.XSI_NS = "http://www.w3.org/2001/XMLSchema-instance" 
		self.SCHEMA_LOCATION = ("http://www.pbcore.org/PBCore/PBCoreNamespace.html "
			"https://raw.githubusercontent.com/WGBH/PBCore_2.1/master/pbcore-2.1.xsd")
		# reference for namespace inclusion: 
		# https://stackoverflow.com/questions/46405690/how-to-include-the-namespaces-into-a-xml-file-using-lxml
		self.attr_qname = ET.QName(self.XSI_NS, "schemaLocation")

		self.NS_MAP = {
			None:self.PBCORE_NAMESPACE,
			'xsi':self.XSI_NS
			}
		# can't use an empty namespace alias with xpath
		self.XPATH_NS_MAP = {
			'p':self.PBCORE_NAMESPACE
			}

		if not pbcoreDescriptionDocumentPath:
			self.descriptionRoot = ET.Element(
				self._PBCORE+'pbcoreDescriptionDocument',
				{self.attr_qname:
					("http://www.pbcore.org/PBCore/PBCoreNamespace.html "
					"https://raw.githubusercontent.com/WGBH/PBCore_2.1/master/pbcore-2.1.xsd")
					},
				nsmap=self.NS_MAP
				)
			self.descriptionDoc = ET.ElementTree(self.descriptionRoot)

	def tidy(self):
		'''
		Should fix ordering if needed?
		i.e. put the work-level stuff before the instantiation(s)
		since the descriptive stuff will be added last.. i think.
		'''
		pass

	def add_instantiation(self, pbcoreInstantiationPath, descriptiveJSONpath=None, level=None):
		'''
		Add an instantiation via mediainfo output.
		Add a json file of BAMPFA descriptive metadata
		to relate the instantiation to the instantiation for
		the physical asset.
		`level` should refer to:
		Preservation master, Access copy, Mezzanine
		'''

		try:
			pbcoreInstantiation = ET.parse(pbcoreInstantiationPath)
			# print(pbcoreInstantiation)

		except:
			print('not a valid xml input ... probably?')
			sys.exit()
		
		instantiation = self.add_SubElement(
			self.descriptionRoot,
			'pbcoreInstantiation',
			nsmap=self.NS_MAP
			)

		for element in pbcoreInstantiation.xpath(
			'/p:pbcoreInstantiationDocument/*',
			namespaces=self.XPATH_NS_MAP
			):
			instantiation.insert(0,deepcopy(element))

		if descriptiveJSONpath != None:
			self.add_related_physical(
				instantiation,
				_id=self.get_related_physical_ID(descriptiveJSONpath)
				)

		if level != None:
			comment = ET.Comment(level)
			instantiation.insert(0,comment)

		return instantiation

	def add_related_physical(self,instantiation,_id=None):
		if _id == None:
			return None
		else:
			relation = self.add_SubElement(
					instantiation,
					'instantiationRelation',
					nsmap=self.NS_MAP
					)
			self.add_SubElement(
				relation,
				'instantiationRelationType',
				attrib={
					'source':'PBCore relationType',
					'ref':(
						'http://metadataregistry.org/'
						'concept/list/vocabulary_id/161.html'
						)
				},
				_text='Derived from',
				nsmap=self.NS_MAP
				)
			self.add_SubElement(
				relation,
				'instantiationRelationIdentifier',
				_text=_id,
				nsmap=self.NS_MAP
			)

	def get_related_physical_ID(self, descriptiveJSONpath):
		'''
		Look for a barcode or an accession number for the 
		instantiationRelationIdentifier value. 
		This relies on the FMP barcode output which concatenates
		all reel barcodes into one string. I should redo this to look for a 
		barcode in the filename a la the filename parsing in fmQuery.py
		'''
		descriptiveJSON = json.load(open(descriptiveJSONpath))
		asset = list(descriptiveJSON.keys())[0]
		assetBarcode = descriptiveJSON[asset]['metadata']['Barcode']
		assetAccNo = descriptiveJSON[asset]['metadata']['accFull']

		if assetAccNo != "":
			physicalAccXpath = (
				"/pbcoreDescriptionDocument/pbcoreInstantiation/"
				"instantiationIdentifier[@source='PFA accession number']/text()"
				)
			physicalAccNo = self.descriptionRoot.xpath(
				physicalAccXpath,
				namespaces=self.XPATH_NS_MAP
				)

			_id = physicalAccNo[0]

			return _id

		elif assetAccNo == "" and assetBarcode != "":
			physicalBarcodeXpath = (
				"/pbcoreDescriptionDocument/pbcoreInstantiation/"
				"instantiationIdentifier[@source='PFA barcode']/text()"
				)
			physicalBarcode = self.descriptionRoot.xpath(
				physicalBarcodeXpath,
				namespaces=self.XPATH_NS_MAP
				)
			_id = physicalBarcode[0]

			return _id

		else:
			return None

	def add_SubElement(
		self,
		_parent,
		_tag,
		attrib={},
		_text=None,
		nsmap=None,
		**_extra
		):
		# e.g. >> sample.add_SubElement(
		#							sample.descriptionRoot,
		#							'pbcoreSub',{},'HELLO',
		#							sample.NS_MAP)
		result = ET.SubElement(_parent,_tag,attrib,nsmap)
		result.text = _text
		return result

	def add_pbcore_subelements(self,top,mappedSubelements,mdValue):
		for key,value in mappedSubelements.items():
			# print(key)
			if "ATTRIBUTES" in mappedSubelements[key]:
				attrib = mappedSubelements[key]["ATTRIBUTES"]
			else:
				attrib = {}
			subelement = self.add_SubElement(
				top,
				key,
				attrib=attrib,
				nsmap=self.NS_MAP
				)
			# print(subelement)
			if mappedSubelements[key]["TEXT"] == "value":
				subelement.text = mdValue
			else:
				subelement.text = mappedSubelements[key]["TEXT"]

	def add_physical_elements(self,descriptiveJSONpath):
		'''
		load metadata json file in specific format,
		drawn from BAMPFA CMS:
		{assetpath:{
			metadata:{
				field1:value1,
				field2:value2
			},
			basename:assetBasename
			}
		}
		'''
		# add an empty instantiation for the physical asset
		physicalInstantiation = self.add_SubElement(
			self.descriptionRoot,
			'pbcoreInstantiation',
			nsmap=self.NS_MAP
			)

		comment = ET.Comment("Physical Asset")
		physicalInstantiation.insert(0,comment)
		descriptiveJSON = json.load(open(descriptiveJSONpath))
		# there should be only one asset
		asset = list(descriptiveJSON.keys())[0]
		assetBasename = descriptiveJSON[asset]['basename']

		# grab the metadata dict from the JSON file
		metadata = descriptiveJSON[asset]['metadata']
		descMetadataFields = []
		for key,value in metadata.items():
			if value != "":
				# we only want the fieds with values
				descMetadataFields.append(key)

		for field in pbcore_map.BAMPFA_FIELDS:
			# loop through the nonempty fields and 
			# match them to the PBCore mapping
			if field in descMetadataFields:
				# print(field)
				# grab the md value and set it for this loop
				mdValue = metadata[field]
				mapping = pbcore_map.PBCORE_MAP[field]
				mappingTarget = list(mapping.keys())[0]
				mappedPbcore = mapping[mappingTarget]
				# check if the field applies to the 
				# WORK or INSTANTIATION level
				level = mappedPbcore["LEVEL"]
				
				# set any attributes if applicable
				if "ATTRIBUTES" in mappedPbcore:
					mappingAttribs = mappedPbcore["ATTRIBUTES"]
				else:
					mappingAttribs = {}
				
				if mappedPbcore["TEXT"] == "value":
					'''
					If there are no subfields involved, just write the 
					value to the pbcore element.
					'''
					if level == "WORK":
						self.add_SubElement(
							self.descriptionRoot,
							mappingTarget,
							attrib=mappingAttribs,
							_text=mdValue,
							nsmap=self.NS_MAP
							)
					else:
						self.add_SubElement(
							physicalInstantiation,
							mappingTarget,
							attrib=mappingAttribs,
							_text=mdValue,
							nsmap=self.NS_MAP
							)

				else:
					'''
					If the meat is in a SubElement
					add the relevant subelement(s)
					'''
					mappedSubelements = mappedPbcore["SUBELEMENTS"]

					if level == "WORK":
						top = self.add_SubElement(
							self.descriptionRoot,
							mappingTarget,
							attrib=mappingAttribs,
							nsmap=self.NS_MAP
							)
						self.add_pbcore_subelements(top,mappedSubelements,mdValue)
					else:
						if not targetInstantiation == []:
							top = self.add_SubElement(
								physicalInstantiation,
								mappingTarget,
								attrib=mappingAttribs,
								nsmap=self.NS_MAP
								)
							self.add_pbcore_subelements(top,mappedSubelements,mdValue)

	def to_string(self):
		self._string = ET.tostring(self.descriptionRoot, pretty_print=True)
		print(self._string.decode())

	def xml_to_file(self,outputPath):
		with open(outputPath,'wb') as outXML:
			# self.output = ET.ElementTree(self.descriptionRoot)
			self.descriptionDoc.write(
				outXML, 
				encoding='utf-8', 
				xml_declaration=True,
				pretty_print=True)
