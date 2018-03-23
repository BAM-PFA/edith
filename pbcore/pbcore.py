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

	def add_instantiation(self, pbcoreInstantiationPath):
		pbcoreInstantiationPath = pbcoreInstantiationPath
		try:
			pbcoreInstantiation = ET.parse(pbcoreInstantiationPath)
			print(pbcoreInstantiation)

		except:
			print('not a valid xml input ... probably?')
			sys.exit()
		# self.instantiation = ET.SubElement(self.descriptionRoot,'pbcoreInstantiation')
		instantiation = self.add_SubElement(
			self.descriptionRoot,
			'pbcoreInstantiation',
			nsmap=self.NS_MAP
			)
		# print(self.pbcoreInstantiation.xpath('/p:pbcoreInstantiationDocument/*',namespaces=self.XPATH_NS_MAP))
		for element in pbcoreInstantiation.xpath(
			'/p:pbcoreInstantiationDocument/*',
			namespaces=self.XPATH_NS_MAP
			):
			# print(element.tag)
			instantiation.insert(0,deepcopy(element))

	def add_SubElement(
		self,
		_parent,
		_tag,attrib={},
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

	def add_description_elements(self,descriptiveJSONpath):
		'''
		load metata json file in specific format:
		{asset:{metadata:{field:value,field1:value1}}}
		only add stuff that is applicable to all instantiations
		'''
		descriptiveJSONpath = descriptiveJSONpath
		descriptiveJSON = json.load(open(descriptiveJSONpath))
		# there should be only one asset
		asset = list(descriptiveJSON.keys())[0]
		assetBasename = descriptiveJSON[asset]['basename']
		# if a field applies to an instantiation, 
		# search for the right pbcoreInstantiation
		# by basename and insert the element.
		# currently something is up with my namespace
		# assignment. so no 'p:' for my elements, 
		# but need to use 'p:' for mediainfo elements.
		instantiationXpathExpression = (
			"/pbcoreDescriptionDocument/pbcoreInstantiation["
				"contains(./p:instantiationIdentifier,'{}')"
					"]".format(
						assetBasename)
			)
		targetInstantiation = self.descriptionRoot.xpath(
			instantiationXpathExpression,
			namespaces=self.XPATH_NS_MAP
			)
		# print(assetBasename)
		# grab the metadata dict from the JSON file
		metadata = descriptiveJSON[asset]['metadata']
		descMetadataFields = []
		for key,value in metadata.items():
			if value != "":
				# we only want the fieds with values
				descMetadataFields.append(key)

		for field in pbcore_map.BAMPFA_FIELDS:
			'''
			Im so sorry for writing such ugly code. :(
			I promise I will refactor and clean up the logic...
			'''
			
			# loop through the nonempty fields and 
			# match them to the PBCore mapping
			if field in descMetadataFields:
				print(field)
				# grab the md value and set it for this loop
				mdValue = metadata[field]
				mapping = pbcore_map.PBCORE_MAP[field]
				# print(mapping)
				mappingTarget = list(mapping.keys())[0]
				mappedPbcore = mapping[mappingTarget]
				# print(mappingTarget)
				# check if the field applies to the 
				# WORK or INSTANTIATION level
				level = mappedPbcore["LEVEL"]
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
						if not targetInstantiation == []:
							self.add_SubElement(
								targetInstantiation[0],
								mappingTarget,
								attrib=mappingAttribs,
								_text=mdValue,
								nsmap=self.NS_MAP
								)
					if "SIBLING_FIELDS" in mappedPbcore:
						# this might not really be needed...
						for key, value in mappedPbcore["SIBLING_FIELDS"].items():
							subSib = mappedPbcore["SIBLING_FIELDS"][key]
							if "ATTRIBUTES" in subSib:
								attrib = subSib["ATTRIBUTES"]
							else:
								attrib = {}
							text = subSib["TEXT"]
							self.add_SubElement(
								self.descriptionRoot,
								key,
								attrib=attrib,
								_text=text,
								nsmap=self.NS_MAP
								)
				else:
					'''
					If the meat is in a SubElement
					add the relevant subelement(s)
					'''
					if level == "WORK":
						top = self.add_SubElement(
							self.descriptionRoot,
							mappingTarget,
							attrib=mappingAttribs,
							nsmap=self.NS_MAP
							)
						# print(top)
						for key,value in mappedPbcore["SUBELEMENTS"].items():
							# print(key)
							if "ATTRIBUTES" in mappedPbcore["SUBELEMENTS"][key]:
								attrib = mappedPbcore["SUBELEMENTS"][key]["ATTRIBUTES"]
							else:
								attrib = {}
							subelement = self.add_SubElement(
								top,
								key,
								attrib=attrib,
								nsmap=self.NS_MAP
								)
							# print(subelement)
							if mappedPbcore["SUBELEMENTS"][key]["TEXT"] == "value":
								subelement.text = mdValue
							else:
								subelement.text = mappedPbcore["SUBELEMENTS"][key]["TEXT"]
					else:
						if not targetInstantiation == []:
							top = self.add_SubElement(
								targetInstantiation[0],
								mappingTarget,
								attrib=mappingAttribs,
								nsmap=self.NS_MAP
								)
							for key,value in mappedPbcore["SUBELEMENTS"].items():
								# print(key)
								if "ATTRIBUTES" in mappedPbcore["SUBELEMENTS"][key]:
									attrib = mappedPbcore["SUBELEMENTS"][key]["ATTRIBUTES"]
								else:
									attrib = {}
								subelement = self.add_SubElement(
									top,
									key,
									attrib=attrib,
									nsmap=self.NS_MAP
									)
								# print(subelement)
								if mappedPbcore["SUBELEMENTS"][key]["TEXT"] == "value":
									subelement.text = mdValue
								else:
									subelement.text = mappedPbcore["SUBELEMENTS"][key]["TEXT"]


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

