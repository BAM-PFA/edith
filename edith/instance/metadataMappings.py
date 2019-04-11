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
				"SOURCE_FIELD_NAME" : "m_245a_CompleteTitle",
				"DISPLAY_NAME": "Title"
				},
			"altTitle" : {
				"RS_FIELD_ID" : 84,
				"SOURCE_FIELD_NAME" : "AlternativeTitle",
				"DISPLAY_NAME": ""
				},
			"accPref" : {
				"RS_FIELD_ID" : 86,
				"SOURCE_FIELD_NAME" : "AccessionNumberPrefix",
				"DISPLAY_NAME": ""
				},
			"accDepos" : {
				"RS_FIELD_ID" : 87,
				"SOURCE_FIELD_NAME" : "AccessionNumberDepositorNumber",
				"DISPLAY_NAME": ""
				},
			"accItem" : {
				"RS_FIELD_ID" : 88,
				"SOURCE_FIELD_NAME" : "AccessionNumberItemNumber",
				"DISPLAY_NAME": ""
				},
			"projGrp" : {
				"RS_FIELD_ID" : 90,
				"SOURCE_FIELD_NAME" : "ProjectGroupTitle",
				"DISPLAY_NAME": ""
				},
			"country" : {
				"RS_FIELD_ID" : 3,
				"SOURCE_FIELD_NAME" : "m_257a_Country",
				"DISPLAY_NAME": ""
				},
			"releaseYear" : {
				"RS_FIELD_ID" : 85,
				"SOURCE_FIELD_NAME" : "m_260c_ReleaseYear",
				"DISPLAY_NAME": ""
				},
			"directorsNames" : {
				"RS_FIELD_ID" : 91,
				"SOURCE_FIELD_NAME" : "ct_DirectorsNames",
				"DISPLAY_NAME": ""
				},
			"credits" : {
				"RS_FIELD_ID" : 92,
				"SOURCE_FIELD_NAME" : "Credits",
				"DISPLAY_NAME": ""
				},
			"generalNotes" : {
				"RS_FIELD_ID" : 93,
				"SOURCE_FIELD_NAME" : "GeneralNotes",
				"DISPLAY_NAME": ""
				},
			"conditionNote" : {
				"RS_FIELD_ID" : 94,
				"SOURCE_FIELD_NAME" : "m_945z_GeneralConditionNotes",
				"DISPLAY_NAME": ""
				},
			"Barcode" : {
				"RS_FIELD_ID" : 98,
				"SOURCE_FIELD_NAME" : "Barcode",
				"DISPLAY_NAME": ""
				},
			"language" : {
				"RS_FIELD_ID" : 99,
				"SOURCE_FIELD_NAME" : "m_546a_Language",
				"DISPLAY_NAME": ""
				},
			"soundCharacteristics" : {
				"RS_FIELD_ID" : 100,
				"SOURCE_FIELD_NAME" : "SoundCharacteristics",
				"DISPLAY_NAME": ""
				},
			"color" : {
				"RS_FIELD_ID" : 101,
				"SOURCE_FIELD_NAME" : "ColorCharacteristics",
				"DISPLAY_NAME": ""
				},
			"runningTime" : {
				"RS_FIELD_ID" : 102,
				"SOURCE_FIELD_NAME" : "RunningTime",
				"DISPLAY_NAME": ""
				},
			"frameRateTRTdetails" : {
				"RS_FIELD_ID" : 121,
				"SOURCE_FIELD_NAME" : "RunningTimeDescription",
				"DISPLAY_NAME": ""
				},
			"medium" : {
				"RS_FIELD_ID" : 103,
				"SOURCE_FIELD_NAME" : "m_245h_Medium",
				"DISPLAY_NAME": ""
				},
			"dimensions" : {
				"RS_FIELD_ID" : 104,
				"SOURCE_FIELD_NAME" : "m_300c_Dimensions",
				"DISPLAY_NAME": ""
				},
			"videoFormat" : {
				"RS_FIELD_ID" : 105,
				"SOURCE_FIELD_NAME" : "VideoFormat",
				"DISPLAY_NAME": ""
				},
			"videoStandard" : {
				"RS_FIELD_ID" : 106,
				"SOURCE_FIELD_NAME" : "VideoStandard",
				"DISPLAY_NAME": ""
				}
			}
		},
	"PFA_Recordings" : {
		"NAMESPACE" : {"filemaker":"http://www.filemaker.com/xml/fmresultset"},
		"FIELDS": {
			"PFAfilmSeries" : {
				"RS_FIELD_ID" : 127,
				"SOURCE_FIELD_NAME" : "recordingPFASeries",
				"DISPLAY_NAME": ""
				},
			"recordingDate" : {
				"RS_FIELD_ID" : 128,
				"SOURCE_FIELD_NAME" : "ct_RecordingDate",
				"DISPLAY_NAME": ""
				},
			"digitizedBornDigital" : {
				"RS_FIELD_ID" : 129,
				"SOURCE_FIELD_NAME" : "recordingDigitalStatusValue",
				"DISPLAY_NAME": ""
				},
			"digitizer" : {
				"RS_FIELD_ID" : 130,
				"SOURCE_FIELD_NAME" : "recordingDigitizer",
				"DISPLAY_NAME": ""
				},
			"locationOfRecording" : {
				"RS_FIELD_ID" : 131,
				"SOURCE_FIELD_NAME" : "recordingLocation",
				"DISPLAY_NAME": ""
				},
			"speakerInterviewee" : {
				"RS_FIELD_ID" : 132,
				"SOURCE_FIELD_NAME" : "ct_Speakers",
				"DISPLAY_NAME": ""
				},
			"filmTitleSubjects" : {
				"RS_FIELD_ID" : 133,
				"SOURCE_FIELD_NAME" : "ct_FilmTitles",
				"DISPLAY_NAME": ""
				},
			"restrictionsOnUse" : {
				"RS_FIELD_ID" : 119,
				"SOURCE_FIELD_NAME" : "recordingPermissions",
				"DISPLAY_NAME": ""
				},
			"description" : {
				"RS_FIELD_ID" : 113,
				"SOURCE_FIELD_NAME" : "recordingEventDescription",
				"DISPLAY_NAME": ""
				},
			"eventTitle" : {
				"RS_FIELD_ID" : 107,
				"SOURCE_FIELD_NAME" : "recordingEventTitle",
				"DISPLAY_NAME": ""
				},
			"recordingAnalogTechnicalNotes" : {
				"RS_FIELD_ID" : 135,
				"SOURCE_FIELD_NAME" : "recordingEventRecordingNotes",
				"DISPLAY_NAME": ""
				},
			"audioRecordingID" : {
				"RS_FIELD_ID" : 136,
				"SOURCE_FIELD_NAME" : "recordingIDPadded",
				"DISPLAY_NAME": ""
				},
			"recordingPermissionsNotes" : {
				"RS_FIELD_ID" : 137,
				"SOURCE_FIELD_NAME" : "recordingPermissionsNotes",
				"DISPLAY_NAME": ""
				},
			"analogTapeNumber" : {
				"RS_FIELD_ID" : 138,
				"SOURCE_FIELD_NAME" : "recordingTapeNumber",
				"DISPLAY_NAME": ""
				},
			"analogTapeSide" : {
				"RS_FIELD_ID" : 139,
				"SOURCE_FIELD_NAME" : "recordingTapeSide",
				"DISPLAY_NAME": ""
				},
			"digitizationQCNotes" : {
				"RS_FIELD_ID" : 140,
				"SOURCE_FIELD_NAME" : "DigitizationNotes",
				"DISPLAY_NAME": ""
				}
			}
		},
	"non-database" : {
		"NAMESPACE" : None,
		"FIELDS": {
			"creator" : {
				"RS_FIELD_ID" : 114,
				"SOURCE_FIELD_NAME" : "",
				"DISPLAY_NAME": ""
				},
			"sourceInputType" : {
				"RS_FIELD_ID" : 141,
				"SOURCE_FIELD_NAME" : "",
				"DISPLAY_NAME": "Source input type"
				},
			"canonicalName" : {
				"RS_FIELD_ID" : 142,
				"SOURCE_FIELD_NAME" : "",
				"DISPLAY_NAME": "Source canonical name"
				},
			"etc" : {
				"RS_FIELD_ID" : 999,
				"SOURCE_FIELD_NAME" : "",
				"DISPLAY_NAME": ""
				}
			}
		}
}
