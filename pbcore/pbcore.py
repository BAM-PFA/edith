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
		self.XSI_NS = "http://www.w3.org/2001/XMLSchema-instance" 
		self.SCHEMA_LOCATION = "http://www.pbcore.org/PBCore/PBCoreNamespace.html https://raw.githubusercontent.com/WGBH/PBCore_2.1/master/pbcore-2.1.xsd"
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
				'pbcoreDescriptionDocument',
				{self.attr_qname:"http://www.pbcore.org/PBCore/PBCoreNamespace.html https://raw.githubusercontent.com/WGBH/PBCore_2.1/master/pbcore-2.1.xsd"},
				nsmap=self.NS_MAP
				)
			self.descriptionDoc = ET.ElementTree(self.descriptionRoot)

	def tidy(self):
		pass

	def add_instantiation(self, pbcoreInstantiationPath):
		self.pbcoreInstantiationPath = pbcoreInstantiationPath
		try:
			self.pbcoreInstantiation = ET.parse(self.pbcoreInstantiationPath)
			print(self.pbcoreInstantiation)

		except:
			print('not a valid xml input ... probably?')
			sys.exit()
		self.instantiation = ET.SubElement(self.descriptionRoot,'pbcoreInstantiation')

		for element in self.pbcoreInstantiation.xpath('/p:pbcoreInstantiationDocument/*',namespaces=self.XPATH_NS_MAP):
			# print(element.tag)
			self.instantiation.append(deepcopy(element))

	def add_SubElement(self,_parent,_tag,attrib={},_text=None,nsmap=None,**_extra):
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
		self.descriptiveJSONpath = descriptiveJSONpath
		self.descriptiveJSON = json.load(open(self.descriptiveJSONpath))
		# there should be only one asset
		self.asset = list(self.descriptiveJSON.keys())[0]
		self.assetBasename = self.descriptiveJSON[self.asset]['basename']
		print(self.assetBasename)
		self.metadata = self.descriptiveJSON[self.asset]['metadata']
		self.descMetadataFields = []
		for key,value in self.metadata.items():
			if value != "":
				self.descMetadataFields.append(key)

		for field in pbcore_map.BAMPFA_FIELDS:
			if field in self.descMetadataFields:
				mapping = pbcore_map.PBCORE_MAP[field]
				# print(mapping)
				mappingTarget = list(mapping.keys())[0]
				# print(mappingTarget)
				level = mapping[mappingTarget]["LEVEL"]
				if "ATTRIBUTES" in mapping[mappingTarget]:
					mappingAttribs = mapping[mappingTarget]["ATTRIBUTES"]
				else:
					mappingAttribs = {}
				
				if mapping[mappingTarget]["TEXT"] == "value":
					value = self.metadata[field]
					if level == "WORK":
						self.add_SubElement(self.descriptionRoot,mappingTarget,attrib=mappingAttribs,_text=value,nsmap=self.NS_MAP)
					else:
						self.targetInstantiation = self.descriptionRoot.xpath("/p:pbcoreDescriptionDocument/p:pbcoreInstantiation[p:instantiationIdentifier[contains(text(),{})]]".format(self.assetBasename),namespaces=self.XPATH_NS_MAP)
						# print(self.targetInstantiation)
						if not self.targetInstantiation == []:
							self.add_SubElement(self.targetInstantiation[0],mappingTarget,attrib=mappingAttribs,_text=value,nsmap=self.NS_MAP)
				else:
					if level == "WORK":
						self.top = self.add_SubElement(self.descriptionRoot,mappingTarget,attrib=mappingAttribs,nsmap=self.NS_MAP)
						print(self.top)
						for key,value in mapping[mappingTarget]["SUBELEMENTS"].items():
							print(key)
							if "ATTRIBUTES" in mapping[mappingTarget]["SUBELEMENTS"][key]:
								attrib = mapping[mappingTarget]["SUBELEMENTS"][key]["ATTRIBUTES"]
							else:
								attrib = {}
							subelement = self.add_SubElement(self.top,key,attrib=attrib,nsmap=self.NS_MAP)
							print(subelement)
							if mapping[mappingTarget]["SUBELEMENTS"][key]["TEXT"] == "value":
								subelement.text = self.metadata[field]
							else:
								subelement.text = mapping[mappingTarget]["SUBELEMENTS"][key]["TEXT"]


	def to_string(self):
		self._string = ET.tostring(self.descriptionRoot, pretty_print=True)
		print(self._string.decode())

	def xml_to_file(self,outputPath):
		with open(outputPath,'wb') as outXML:
			# self.output = ET.ElementTree(self.descriptionRoot)
			self.descriptionDoc.write(outXML, encoding='utf-8', xml_declaration=True,pretty_print=True)

