'''
This dict serves as a map to metadata sources and the xpath expressions
needed to access the fields in a FileMaker XML resultSet document.

It assumes of course that the metadata source is FileMaker, which is 
true at the moment but not necessarily forever. I think the dict
structure should either make it possible to add other qualifiers (mysql-related perhaps?)
or make it easier to transition to defining all the fields in a table in the database
and having any required qualifiers/xpath/details stored as attributes of each field, 
or maybe relate them to existing data_source entities. ~(2019/02/11)
'''

metadataMappings = {
 	"PFA_COLLECTION" : {
		"NAMESPACE": {"filemaker":"http://www.filemaker.com/xml/fmresultset"},
		"FIELD_NAME" : "FILEMAKER_XML_XPATH_EXPRESSION",
		"title" : "./filemaker:field[@name='m_245a_CompleteTitle']",
		"altTitle" : "./filemaker:field[@name='AlternativeTitle']"
		},
	"AUDIO_COLLECTION" : {
		"NAMESPACE" : {"filemaker":"http://www.filemaker.com/xml/fmresultset"},
		"FIELD_NAME" : "FILEMAKER_XML_XPATH_EXPRESSION"
		}
}