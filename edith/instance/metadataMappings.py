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
				"RS_FIELD_ID" : 8,
				"SOURCE_FIELD_NAME" : "m_245a_CompleteTitle"
				},
			"altTitle" : {
				"RS_FIELD_ID" : 84,
				"SOURCE_FIELD_NAME" : "AlternativeTitle"
				},
			"accPref" : {
				"RS_FIELD_ID" : 86,
				"SOURCE_FIELD_NAME" : "AccessionNumberPrefix"
				},
			"accDepos" : {
				"RS_FIELD_ID" : 87,
				"SOURCE_FIELD_NAME" : "AccessionNumberDepositorNumber"
				},
			"accItem" : {
				"RS_FIELD_ID" : 88,
				"SOURCE_FIELD_NAME" : "AccessionNumberItemNumber"
				},
			"projGrp" : {
				"RS_FIELD_ID" : 90,
				"SOURCE_FIELD_NAME" : "ProjectGroupTitle"
				},
			"country" : {
				"RS_FIELD_ID" : 3,
				"SOURCE_FIELD_NAME" : "m_257a_Country"
				},
			"releaseYear" : {
				"RS_FIELD_ID" : 85,
				"SOURCE_FIELD_NAME" : "m_260c_ReleaseYear"
				},
			"directorsNames" : {
				"RS_FIELD_ID" : 91,
				"SOURCE_FIELD_NAME" : "ct_DirectorsNames"
				},
			"credits" : {
				"RS_FIELD_ID" : 92,
				"SOURCE_FIELD_NAME" : "Credits"
				},
			"generalNotes" : {
				"RS_FIELD_ID" : 93,
				"SOURCE_FIELD_NAME" : "GeneralNotes"
				},
			"conditionNote" : {
				"RS_FIELD_ID" : 94,
				"SOURCE_FIELD_NAME" : "m_945z_GeneralConditionNotes"
				},
			"Barcode" : {
				"RS_FIELD_ID" : 98,
				"SOURCE_FIELD_NAME" : "Barcode"
				},
			"language" : {
				"RS_FIELD_ID" : 99,
				"SOURCE_FIELD_NAME" : "m_546a_Language"
				},
			"soundCharacteristics" : {
				"RS_FIELD_ID" : 100,
				"SOURCE_FIELD_NAME" : "SoundCharacteristics"
				},
			"color" : {
				"RS_FIELD_ID" : 101,
				"SOURCE_FIELD_NAME" : "ColorCharacteristics"
				},
			"runningTime" : {
				"RS_FIELD_ID" : 102,
				"SOURCE_FIELD_NAME" : "RunningTime"
				},
			"frameRateTRTdetails" : {
				"RS_FIELD_ID" : 121,
				"SOURCE_FIELD_NAME" : "RunningTimeDescription"
				},
			"medium" : {
				"RS_FIELD_ID" : 103,
				"SOURCE_FIELD_NAME" : "m_245h_Medium"
				},
			"dimensions" : {
				"RS_FIELD_ID" : 104,
				"SOURCE_FIELD_NAME" : "m_300c_Dimensions"
				},
			"videoFormat" : {
				"RS_FIELD_ID" : 105,
				"SOURCE_FIELD_NAME" : "VideoFormat"
				},
			"videoStandard" : {
				"RS_FIELD_ID" : 106,
				"SOURCE_FIELD_NAME" : "VideoStandard"
				}
			}
		},
	"PFA_Recordings" : {
		"NAMESPACE" : {"filemaker":"http://www.filemaker.com/xml/fmresultset"},
		"FIELDS": {
			"PFAfilmSeries" : {
				"RS_FIELD_ID" : 127,
				"SOURCE_FIELD_NAME" : "recordingPFASeries"
				},
			"recordingDate" : {
				"RS_FIELD_ID" : 128,
				"SOURCE_FIELD_NAME" : "ct_RecordingDate"
				},
			"digitizedBornDigital" : {
				"RS_FIELD_ID" : 129,
				"SOURCE_FIELD_NAME" : "recordingDigitalStatusValue"
				},
			"digitizer" : {
				"RS_FIELD_ID" : 130,
				"SOURCE_FIELD_NAME" : "recordingDigitizer"
				},
			"locationOfRecording" : {
				"RS_FIELD_ID" : 131,
				"SOURCE_FIELD_NAME" : "recordingLocation"
				},
			"speakerInterviewee" : {
				"RS_FIELD_ID" : 132,
				"SOURCE_FIELD_NAME" : "ct_Speakers"
				},
			"filmTitleSubjects" : {
				"RS_FIELD_ID" : 133,
				"SOURCE_FIELD_NAME" : "ct_FilmTitles"
				},
			"restrictionsOnUse" : {
				"RS_FIELD_ID" : 119,
				"SOURCE_FIELD_NAME" : "recordingPermissions"
				},
			"description" : {
				"RS_FIELD_ID" : 113,
				"SOURCE_FIELD_NAME" : "recordingEventDescription"
				},
			"eventTitle" : {
				"RS_FIELD_ID" : 107,
				"SOURCE_FIELD_NAME" : "recordingEventTitle"
				},
			# BELOW HERE STILL NEEDS TO BE ADDED TO RESOURCESPACE & PBCORE MAP
			"recordingAnalogTechnicalNotes" : {
				"RS_FIELD_ID" : None,
				"SOURCE_FIELD_NAME" : "recordingEventRecordingNotes"
				},
			"audioRecordingID" : {
				"RS_FIELD_ID" : None,
				"SOURCE_FIELD_NAME" : "recordingIDPadded"
				},
			"recordingPermissionsNotes" : {
				"RS_FIELD_ID" : None,
				"SOURCE_FIELD_NAME" : "recordingPermissionsNotes"
				},
			"analogTapeNumber" : {
				"RS_FIELD_ID" : None,
				"SOURCE_FIELD_NAME" : "recordingTapeNumber"
				},
			"analogTapeSide" : {
				"RS_FIELD_ID" : None,
				"SOURCE_FIELD_NAME" : "recordingTapeSide"
				},
			"digitizationQCNotes" : {
				"RS_FIELD_ID" : None,
				"SOURCE_FIELD_NAME" : "DigitizationNotes"
				}
			}
		}
}
