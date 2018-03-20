#!/usr/bin/env python3

import os
import sys
from copy import deepcopy
import lxml.etree as ET

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
	def __init__(self, pbcoreInstantiationPath,pbcoreDescriptionDocumentPath=None):
		try:
			self.pbcoreInstantiation = ET.parse(pbcoreInstantiationPath)
			# pbcoreInstantiationRoot = 
		except:
			print('not a valid xml input ... probably?')
			sys.exit()

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
		self.XPATH_NS_MAP = {
			'p':self.PBCORE_NAMESPACE
			}

		# instantiationContents = [element.tag for ]

		if not pbcoreDescriptionDocumentPath:
			self.descriptionRoot = ET.Element(
				'pbcoreDescriptionDocument',
				{self.attr_qname:"http://www.pbcore.org/PBCore/PBCoreNamespace.html https://raw.githubusercontent.com/WGBH/PBCore_2.1/master/pbcore-2.1.xsd"},
				nsmap=self.NS_MAP
				)

			self.instantiation = ET.SubElement(self.descriptionRoot,'pbcoreInstantiation')

			for element in (element for element in self.pbcoreInstantiation.xpath('/p:pbcoreInstantiationDocument/*',namespaces=self.XPATH_NS_MAP) if not element.tag == '{http://www.pbcore.org/PBCore/PBCoreNamespace.html}pbcoreInstantiationDocument'):
				print(element.tag)
				# if element.tag != '{http://www.pbcore.org/PBCore/PBCoreNamespace.html}pbcoreInstantiationDocument':
					# print(element.tag)
				self.instantiation.append(deepcopy(element))

		# print((ET.tostring(descriptionRoot,pretty_print=True)).decode())
		# print(ET.tostring(instantiationRoot))
		# print(ET.tostring(pbcoreInstantiation, pretty_print=True))
		self._string = ET.tostring(self.pbcoreInstantiation, pretty_print=True)
