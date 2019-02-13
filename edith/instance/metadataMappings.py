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

metadataMaps = {
 	"PFA_Collection" : {
		"NAMESPACE": {"filemaker":"http://www.filemaker.com/xml/fmresultset"},
		"FIELDS": {
			"title" : {
				"XPATH_EXPRESSION" : "./filemaker:field[@name='m_245a_CompleteTitle']"
				},
			"altTitle" : {
				"XPATH_EXPRESSION" : "./filemaker:field[@name='AlternativeTitle']"
				},
			"accPref" : {
				"XPATH_EXPRESSION" : "./filemaker:field[@name='AccessionNumberPrefix']"
				},
			"accDepos" : {
				"XPATH_EXPRESSION" : "./filemaker:field[@name='AccessionNumberDepositorNumber']"
				},
			"accItem" : {
				"XPATH_EXPRESSION" : "./filemaker:field[@name='AccessionNumberItemNumber']"
				},
			"projGrp" : {
				"XPATH_EXPRESSION" : "./filemaker:field[@name='ProjectGroupTitle']"
				},
			"country" : {
				"XPATH_EXPRESSION" : "./filemaker:field[@name='m_257a_Country']"
				},
			"releaseYear" : {
				"XPATH_EXPRESSION" : "./filemaker:field[@name='m_260c_ReleaseYear']"
				},
			"directorsNames" : {
				"XPATH_EXPRESSION" : "./filemaker:field[@name='ct_DirectorsNames']"
				},
			"credits" : {
				"XPATH_EXPRESSION" : "./filemaker:field[@name='Credits']"
				},
			"generalNotes" : {
				"XPATH_EXPRESSION" : "./filemaker:field[@name='GeneralNotes']"
				},
			"conditionNote" : {
				"XPATH_EXPRESSION" : "./filemaker:field[@name='m_945z_GeneralConditionNotes']"
				},
			"Barcode" : {
				"XPATH_EXPRESSION" : "./filemaker:field[@name='Barcode']"
				},
			"language" : {
				"XPATH_EXPRESSION" : "./filemaker:field[@name='m_546a_Language']"
				},
			"soundCharacteristics" : {
				"XPATH_EXPRESSION" : "./filemaker:field[@name='SoundCharacteristics']"
				},
			"color" : {
				"XPATH_EXPRESSION" : "./filemaker:field[@name='ColorCharacteristics']"
				},
			"runningTime" : {
				"XPATH_EXPRESSION" : "./filemaker:field[@name='RunningTime']"
				},
			"frameRateTRTdetails" : {
				"XPATH_EXPRESSION" : "./filemaker:field[@name='RunningTimeDescription']"
				},
			"medium" : {
				"XPATH_EXPRESSION" : "./filemaker:field[@name='m_245h_Medium']"
				},
			"dimensions" : {
				"XPATH_EXPRESSION" : "./filemaker:field[@name='m_300c_Dimensions']"
				},
			"videoFormat" : {
				"XPATH_EXPRESSION" : "./filemaker:field[@name='VideoFormat']"
				},
			"videoStandard" : {
				"XPATH_EXPRESSION" : "./filemaker:field[@name='VideoStandard']"
				}
			}
		},
	"PFA_Recordings" : {
		"NAMESPACE" : {"filemaker":"http://www.filemaker.com/xml/fmresultset"},
		"FIELDS": {
			"PFAfilmSeries" : {
				"XPATH_EXPRESSION" : "./filemaker:field[@name='recordingPFASeries']"
				},
			"recordingDigitalStatus" : {
				"XPATH_EXPRESSION" : "./filemaker:field[@name='recordingDigitalStatusValue']"
				},
			"digitizer" : {
				"XPATH_EXPRESSION" : "./filemaker:field[@name='recordingIDPadded']"
				},
			"locationOfRecording" : {
				"XPATH_EXPRESSION" : "./filemaker:field[@name='recordingIDPadded']"
				},
			"speakerInterviewee" : {
				"XPATH_EXPRESSION" : "./filemaker:field[@name='ct_Speakers']"
				},
			"filmTitleSubjects" : {
				"XPATH_EXPRESSION" : "./filemaker:field[@name='ct_FilmTitles']"
				},
			"restrictionsOnUse" : {
				"XPATH_EXPRESSION" : "./filemaker:field[@name='recordingPermissions']"
				},
			"description" : {
				"XPATH_EXPRESSION" : "./filemaker:field[@name='recordingEventNotes']"
				},
			"eventTitle" : {
				"XPATH_EXPRESSION" : "./filemaker:field[@name='recordingEventTitle']"
				},
			"restrictionsOnUse" : {
				"XPATH_EXPRESSION" : "./filemaker:field[@name='recordingPermissions']"
				},
			# BELOW HERE STILL NEEDS TO BE ADDED TO RESOURCESPACE & PBCORE MAP
			"recordingAnalogTechnicalNotes" : {
				"XPATH_EXPRESSION" : "./filemaker:field[@name='recordingEventRecordingNotes']"
				},
			"audioRecordingID" : {
				"XPATH_EXPRESSION" : "./filemaker:field[@name='recordingIDPadded']"
				},
			"recordingPermissionsNotes" : {
				"XPATH_EXPRESSION" : "./filemaker:field[@name='recordingPermissionsNotes']"
				},
			"analogTapeNumber" : {
				"XPATH_EXPRESSION" : "./filemaker:field[@name='recordingTapeNumber']"
				},
			"analogTapeSide" : {
				"XPATH_EXPRESSION" : "./filemaker:field[@name='recordingTapeSide']"
				},
			"digitizationQCNotes" : {
				"XPATH_EXPRESSION" : "./filemaker:field[@name='Digitization Notes']"
				}
			}
		}
}