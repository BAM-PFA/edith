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
				"DISPLAY_NAME": "Alternative title"
				},
			"accPref" : {
				"RS_FIELD_ID" : 86,
				"SOURCE_FIELD_NAME" : "AccessionNumberPrefix",
				"DISPLAY_NAME": "Accession number - prefix"
				},
			"accDepos" : {
				"RS_FIELD_ID" : 87,
				"SOURCE_FIELD_NAME" : "AccessionNumberDepositorNumber",
				"DISPLAY_NAME": "Accession number - depositor number"
				},
			"accItem" : {
				"RS_FIELD_ID" : 88,
				"SOURCE_FIELD_NAME" : "AccessionNumberItemNumber",
				"DISPLAY_NAME": "Accession number - item number"
				},
			"accFull" : {
				"RS_FIELD_ID" : 89,
				"SOURCE_FIELD_NAME" : "m_099a_PFAAccessionNumber",
				"DISPLAY_NAME": "Accession number - complete"
				},
			"projGrp" : {
				"RS_FIELD_ID" : 90,
				"SOURCE_FIELD_NAME" : "ProjectGroupTitle",
				"DISPLAY_NAME": "Project/Group"
				},
			"country" : {
				"RS_FIELD_ID" : 3,
				"SOURCE_FIELD_NAME" : "m_257a_Country",
				"DISPLAY_NAME": "Country"
				},
			"releaseDate" : {
				"RS_FIELD_ID" : 85,
				"SOURCE_FIELD_NAME" : "m_260c_ReleaseYear",
				"DISPLAY_NAME": "Release date"
				},
			"directorsNames" : {
				"RS_FIELD_ID" : 91,
				"SOURCE_FIELD_NAME" : "ct_DirectorsNames",
				"DISPLAY_NAME": "Director(s)/Filmmaker(s)"
				},
			"credits" : {
				"RS_FIELD_ID" : 92,
				"SOURCE_FIELD_NAME" : "Credits",
				"DISPLAY_NAME": "Credits statement"
				},
			"generalNotes" : {
				"RS_FIELD_ID" : 93,
				"SOURCE_FIELD_NAME" : "GeneralNotes",
				"DISPLAY_NAME": "General notes"
				},
			"conditionNote" : {
				"RS_FIELD_ID" : 94,
				"SOURCE_FIELD_NAME" : "m_945z_GeneralConditionNotes",
				"DISPLAY_NAME": "Condition note (of physical item)"
				},
			"Barcode" : {
				"RS_FIELD_ID" : 98,
				"SOURCE_FIELD_NAME" : "Barcode",
				"DISPLAY_NAME": "Barcode"
				},
			"language" : {
				"RS_FIELD_ID" : 99,
				"SOURCE_FIELD_NAME" : "m_546a_Language",
				"DISPLAY_NAME": "Language"
				},
			"soundCharacteristics" : {
				"RS_FIELD_ID" : 100,
				"SOURCE_FIELD_NAME" : "SoundCharacteristics",
				"DISPLAY_NAME": "Sound characteristics (silent/sound)"
				},
			"color" : {
				"RS_FIELD_ID" : 101,
				"SOURCE_FIELD_NAME" : "ColorCharacteristics",
				"DISPLAY_NAME": "Color characteristics (b&w/color)"
				},
			"runningTime" : {
				"RS_FIELD_ID" : 102,
				"SOURCE_FIELD_NAME" : "RunningTime",
				"DISPLAY_NAME": "Running time"
				},
			"frameRateTRTdetails" : {
				"RS_FIELD_ID" : 121,
				"SOURCE_FIELD_NAME" : "RunningTimeDescription",
				"DISPLAY_NAME": "Running time details"
				},
			"medium" : {
				"RS_FIELD_ID" : 103,
				"SOURCE_FIELD_NAME" : "m_245h_Medium",
				"DISPLAY_NAME": "Medium of original"
				},
			"dimensions" : {
				"RS_FIELD_ID" : 104,
				"SOURCE_FIELD_NAME" : "m_300c_Dimensions",
				"DISPLAY_NAME": "Dimensions of original"
				},
			"videoFormat" : {
				"RS_FIELD_ID" : 105,
				"SOURCE_FIELD_NAME" : "VideoFormat",
				"DISPLAY_NAME": "Video format of original"
				},
			"videoStandard" : {
				"RS_FIELD_ID" : 106,
				"SOURCE_FIELD_NAME" : "VideoStandard",
				"DISPLAY_NAME": "Video standard of original"
				},
			"generation" : {
				"RS_FIELD_ID" : 105,
				"SOURCE_FIELD_NAME" : "m_300_3_Generation",
				"DISPLAY_NAME": "Generation of original"
				}
			}
		},
	"PFA_Recordings" : {
		"NAMESPACE" : {"filemaker":"http://www.filemaker.com/xml/fmresultset"},
		"FIELDS": {
			"PFAfilmSeries" : {
				"RS_FIELD_ID" : 127,
				"SOURCE_FIELD_NAME" : "recordingPFASeries",
				"DISPLAY_NAME": "Related PFA film series"
				},
			"recordingDate" : {
				"RS_FIELD_ID" : 128,
				"SOURCE_FIELD_NAME" : "ct_RecordingDate",
				"DISPLAY_NAME": "Date of recording"
				},
			"digitizedBornDigital" : {
				"RS_FIELD_ID" : 129,
				"SOURCE_FIELD_NAME" : "recordingDigitalStatusValue",
				"DISPLAY_NAME": "Digitized/Born-digital"
				},
			"digitizer" : {
				"RS_FIELD_ID" : 130,
				"SOURCE_FIELD_NAME" : "recordingDigitizer",
				"DISPLAY_NAME": "Digitizer"
				},
			"locationOfRecording" : {
				"RS_FIELD_ID" : 131,
				"SOURCE_FIELD_NAME" : "recordingLocation",
				"DISPLAY_NAME": "Location of recording"
				},
			"speakerInterviewee" : {
				"RS_FIELD_ID" : 132,
				"SOURCE_FIELD_NAME" : "ct_Speakers",
				"DISPLAY_NAME": "Speaker/Interviewee"
				},
			"filmTitleSubjects" : {
				"RS_FIELD_ID" : 133,
				"SOURCE_FIELD_NAME" : "ct_FilmTitles",
				"DISPLAY_NAME": "Film titles as subjects"
				},
			"restrictionsOnUse" : {
				"RS_FIELD_ID" : 119,
				"SOURCE_FIELD_NAME" : "recordingPermissions",
				"DISPLAY_NAME": "Restrictions on use/Permissions"
				},
			"description" : {
				"RS_FIELD_ID" : 113,
				"SOURCE_FIELD_NAME" : "recordingEventDescription",
				"DISPLAY_NAME": "Description"
				},
			"eventTitle" : {
				"RS_FIELD_ID" : 107,
				"SOURCE_FIELD_NAME" : "recordingEventTitle",
				"DISPLAY_NAME": "Event title"
				},
			"recordingAnalogTechnicalNotes" : {
				"RS_FIELD_ID" : 135,
				"SOURCE_FIELD_NAME" : "recordingEventRecordingNotes",
				"DISPLAY_NAME": "Event recording quality notes"
				},
			"audioRecordingID" : {
				"RS_FIELD_ID" : 136,
				"SOURCE_FIELD_NAME" : "recordingIDPadded",
				"DISPLAY_NAME": "Recording database ID"
				},
			"recordingPermissionsNotes" : {
				"RS_FIELD_ID" : 137,
				"SOURCE_FIELD_NAME" : "recordingPermissionsNotes",
				"DISPLAY_NAME": "Notes: recording permissions"
				},
			"analogTapeNumber" : {
				"RS_FIELD_ID" : 138,
				"SOURCE_FIELD_NAME" : "recordingTapeNumber",
				"DISPLAY_NAME": "Analog tape number"
				},
			"analogTapeSide" : {
				"RS_FIELD_ID" : 139,
				"SOURCE_FIELD_NAME" : "recordingTapeSide",
				"DISPLAY_NAME": "Analog tape side"
				},
			"digitizationQCNotes" : {
				"RS_FIELD_ID" : 140,
				"SOURCE_FIELD_NAME" : "DigitizationNotes",
				"DISPLAY_NAME": "Digitization/QC notes"
				}
			}
		},
	"non-database" : {
		"NAMESPACE" : None,
		"FIELDS": {
			"creator" : {
				"RS_FIELD_ID" : 114,
				"SOURCE_FIELD_NAME" : "",
				"DISPLAY_NAME": "Creator"
				},
			"sourceInputType" : {
				"RS_FIELD_ID" : 141,
				"SOURCE_FIELD_NAME" : "",
				"DISPLAY_NAME": "Source input type",
				"DESCRIPTION":"NOT MAPPED TO PBCORE"
				},
			"canonicalName" : {
				"RS_FIELD_ID" : 142,
				"SOURCE_FIELD_NAME" : "",
				"DISPLAY_NAME": "Source canonical name",
				"DESCRIPTION":"NOT MAPPED TO PBCORE"
				},
			"tags" : {
				"RS_FIELD_ID" : 1,
				"SOURCE_FIELD_NAME" : "",
				"DISPLAY_NAME": "Tags"
				},
			"assetExternalSource" : {
				"RS_FIELD_ID" : 117,
				"SOURCE_FIELD_NAME" : "",
				"DISPLAY_NAME": "External (non-BAMPFA) source of asset"
				},
			"copyrightStatement" : {
				"RS_FIELD_ID" : 118,
				"SOURCE_FIELD_NAME" : "",
				"DISPLAY_NAME": "Copyright Statement"
				},
			"postProcessing" : {
				"RS_FIELD_ID" : 125,
				"SOURCE_FIELD_NAME" : "",
				"DISPLAY_NAME": "Raw footage or edited work"
				},
			"nameSubjects" : {
				"RS_FIELD_ID" : 29,
				"SOURCE_FIELD_NAME" : "",
				"DISPLAY_NAME": "Name subjects"
				},
			"topicalSubjects" : {
				"RS_FIELD_ID" : 134,
				"SOURCE_FIELD_NAME" : "",
				"DISPLAY_NAME": "Topical subjects"
				},
			"editSequenceSettings" : {
				"RS_FIELD_ID" : 123,
				"SOURCE_FIELD_NAME" : "",
				"DISPLAY_NAME": "Export/edit settings from NLE",
				"DESCRIPTION":"NOT MAPPED TO PBCORE"
				},
			"exportPublishDate" : {
				"RS_FIELD_ID" : 126,
				"SOURCE_FIELD_NAME" : "",
				"DISPLAY_NAME": "Date of export/publishing"
				},
			"platformOutlet" : {
				"RS_FIELD_ID" : 122,
				"SOURCE_FIELD_NAME" : "",
				"DISPLAY_NAME": "Platform/media outlet"
				},
			"eventOrganizer" : {
				"RS_FIELD_ID" : 116,
				"SOURCE_FIELD_NAME" : "",
				"DISPLAY_NAME": "Event organizer"
				},
			"eventSeries" : {
				"RS_FIELD_ID" : 110,
				"SOURCE_FIELD_NAME" : "",
				"DISPLAY_NAME": "Event series title"
				},
			"eventRelatedExhibition" : {
				"RS_FIELD_ID" : 111,
				"SOURCE_FIELD_NAME" : "",
				"DISPLAY_NAME": "Related BAMPFA exhibition"
				},
			"ingestUUID" : {
				"RS_FIELD_ID" : 95,
				"SOURCE_FIELD_NAME" : "",
				"DISPLAY_NAME": "Ingest process unique identifier"
				},
			"frameRateProxy" : {
				"RS_FIELD_ID" : 111,
				"SOURCE_FIELD_NAME" : "",
				"DISPLAY_NAME": "Frame rate of access file",
				"DESCRIPTION":"NOT MAPPED TO PBCORE"
				}
			}
		}
}
