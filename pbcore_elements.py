'''
Python dicts that list PBCore elements and their attributes as
defined in the PBCore documentation:
http://pbcore.org/elements/
An excercise to get more familiar w the documentation
and hopefully will be useful to me!
'''
ROOT_ELEMENTS = {
	"pbcoreCollection":{
		"definition":("pbcoreCollection groups multiple pbcoreDescriptionDocument XML into one container element to allow for a serialized output. Uses might include API returns or other web service output."),
		"attributes":{
			"xmlns":{
				"required":True
			},
			"xsi":{
				"required":True
			},
			"schemaLocation":{
				"required":True
			},
			"collectionTitle":{
				"required":False
			},
			"collectionDescription":{
				"required":False
			},
			"collectionSource":{
				"required":False
			},
			"collectionRef":{
				"required":False
			},
			"collectionDate":{
				"required":False
			}
		},
		"best practice":("This element is not intended to be equivalent "
			"to the archive/library concept of a \"collection.\" Please "
			"see pbcoreAssetType for information on how PBCore can be "
			"used to express information about collections. The element "
			"is only applicable to XML expressions of PBCore. This "
			"container enables a similar function to RSS; "
			"pbcoreCollection would be similar to rss:channel and "
			"pbcoreDescription document to rss:item."),
		"usage":{
			"required":False,
			"repeatable":False,
			"usage note":("")
		},
		"subelements":{
			"pbcoreDescriptionDocument":{
				"required":True,
				"description":(" A root XML element for the expression "
					"of an indvidual PBCore record. "
					"pbcoreDescriptionDocument can be used to express "
					"intellectual content only (e.g. a series or "
					"collection level record with no associated "
					"instantiations), or intellectual content with one "
					"or more instantiations (e.g. an episode of a "
					"program with copies/instantiations on videotape and "
					"digital file). This element is only applicable to "
					"XML expressions of PBCore.")
			},
		"documentation":"http://pbcore.org/pbcorecollection/"
		}
	},
	"pbcoreDescriptionDocument":{
		"definition":("pbcoreDescriptionDocument is a root XML element for the expression of an individual PBCore record. pbcoreDescriptionDocument can be used to express intellectual content only (e.g. a series or collection level record with no associated instantiations), or intellectual content with one or more instantiations (e.g. an episode of a program with copies/instantiations on videotape and digital file). This element is only applicable to XML expressions of PBCore."),
		"attributes":{
			"xmlns":{
				"required":True
			},
			"xsi":{
				"required":True
			},
			"schemaLocation":{
				"required":True
			}
		},
		"best practice":(""),
		"usage":{
			"required":False,
			"repeatable":True,
			"usage note":"pbcoreDescriptionDocument can only be contained by pbcoreCollection. Only repeatable within pbcoreCollection"
		},
		"subelements":{
			"pbcoreAssetType":{
				"required":False,
				"description":("The pbcoreAssetType element is a broad definition of the type of intellectual content being described.  Asset types might include those without associated instantiations (a collection or series), or those with instantiations (programs, episodes, clips, etc.)")
			},
			"pbcoreAssetDate":{
				"required":False,
				"description":("The pbcoreAssetDate element is intended to reflect dates associated with the Intellectual Content.")
			},
			"pbcoreIdentifier":{
				"required":True,
				"description":("The pbcoreIdentifier element is an identifier that can apply to the asset. This identifier should not be limited to a specific instantiation, but rather all instantiations of an asset. It can also hold a URL or URI that points to the asset.")
			},
			"pbcoreTitle":{
				"required":True,
				"description":("The pbcoreTitle element is a name or label relevant to the asset.")
			},
			"pbcoreSubject":{
				"required":False,
				"description":("The pbcoreSubject element is used to assign topic headings or keywords that portray the intellectual content of the asset. A subject is expressed by keywords, key phrases, or even specific classification codes. Controlled vocabularies, authorities, formal classification codes, as well as folksonomies and user-generated tags, may be employed when assigning descriptive subject terms.")
			},
			"pbcoreDescription":{
				"required":True,
				"description":("The pbcoreDescription element uses free-form text or a narrative to report general notes, abstracts, or summaries about the intellectual content of an asset. The information may be in the form of an individual program description, anecdotal interpretations, or brief content reviews. The description may also consist of outlines, lists, bullet points, rundowns, edit decision lists, indexes, or tables of content.")
			},
			"pbcoreGenre":{
				"required":False,
				"description":("The pbcoreGenre element describes the Genre of the asset, which can be defined as a categorical description informed by the topical nature or a particular style or form of the content.")
			},
			"pbcoreRelation":{
				"required":False,
				"description":("The pbcoreRelation element contains the pbcoreRelationType and pbcoreRelationIdentifier elements. In order to properly use these two elements they must be nested with the pbcoreRelation element, and pbcoreRelation must contain both pbcoreRelationType and pbcoreRelationIdentifier if it is included.")
			},
			"pbcoreCoverage":{
				"required":False,
				"description":("The pbcoreCoverage element is a container for subelements coverage and coverageType.")
			},
			"pbcoreAudienceLevel":{
				"required":False,
				"description":("The pbcoreAudienceLevel element identifies a type of audience, viewer, or listener for whom the media item is primarily designed or educationally useful.")
			},
			"pbcoreAudienceRating":{
				"required":False,
				"description":("The pbcoreAudienceRating element designates the type of users for whom the intellectual content of a media item is intended or judged appropriate. This element differs from the element pbcoreAudienceLevel in that it utilizes standard ratings that have been crafted by the broadcast television and film industries and that are used as flags for audience or age-appropriate materials.")
			},
			"pbcoreCreator":{
				"required":False,
				"description":(" The pbcoreCreator element is a container for sub-elements creator and creatorRole.")
			},
			"pbcoreContributor":{
				"required":False,
				"description":(" The pbcoreContributor element is a container for sub-elements contributor and contributorRole.")
			},
			"pbcorePublisher":{
				"required":False,
				"description":("The pbcorePublisher element is a container for sub-elements publisher and publisherRole.")
			},
			"pbcoreRightsSummary":{
				"required":False,
				"description":("The pbcoreRightsSummary element is a container for sub-elements \'rightsSummary\', \'rightsLink\' and \'rightsEmbedded\' used to describe Rights for the asset. ")
			},
			"pbcoreInstantiation":{
				"required":False,
				"description":("The pbcoreInstantiation element contains subelements that describe a single instantiation of an asset. The definition is malleable but it should be thought of as any discreet and tangible unit that typically (though not always) comprises a whole representation of the asset. For example, an original master videotape, a preservation master video file, and a low-bitrate access copy would all be considered Instantiations of a single video program. All of the sub-elements held by this element are used to describe the intantiation specifically, not necessarily the asset as a whole.")
			},
			"pbcoreAnnotation":{
				"required":False,
				"description":("The pbcoreAnnotation element allows the addition of any supplementary information about the metadata used to describe the PBCore record. pbcoreAnnotation clarifies element values, terms, descriptors, and vocabularies that may not be otherwise sufficiently understood.")
			},
			"pbcorePart":{
				"required":False,
				"description":("The pbcorePart element may be used to split up a single asset so as to enable the use of all available elements at the pbcoreDescriptionDocument level to describe the intellectual content of individual segments of an asset.")
			},
			"pbcoreExtension":{
				"required":False,
				"description":("The pbcoreExtension element can be used as either a wrapper containing a specific element from another standard OR embedded xml containing the extension. ")
			}
		},
		"documentation":"http://pbcore.org/pbcoreDescriptionDocument/"
	},
	"pbcoreInstantiationDocument":{
		"definition":("pbcoreInstantiationDocument is the equivalent of the instantiation element, but used for the expression of an instantiation record at the root of an XML document. This is most commonly used when referenced from other schemas, or if you want to create and express a single, stand-alone instantiation."),
		"attributes":{
			"startTime":{
				"required":False
			},
			"endTime":{
				"required":False
			},
			"timeAnnotation":{
				"required":False
			}
		},
		"best practice":("This is most commonly used when Intellectual Content (in other words, descriptive metadata) is not expressed using PBCore, but rather another standard such as MODS or Dublin Core."),
		"usage":{
			"required":False,
			"repeatable":False,
			"usage note":("")
		},
		"subelements":{
			"instantiationIdentifier":{
				"required":True,
				"description":("The instantiationIdentifier element contains an unambiguous reference or identifier for a particular instantiation of an asset.")
				},
			"instantiationDate":{
				"required":False,
				"description":("A date associated with an instantiation.")
				},
			"instantiationPhysical":{
				"required":False,
				"description":("Use the element instantiationPhysical to identify the format of a particular instantiation as it exists in a physical form that occupies physical space (e.g., a tape on a shelf). This includes physical digital media, such as a DV tape, audio CD or authored DVD, as well as analog media.")
				},
			"instantiationDigital":{
				"required":False,
				"description":("Use the element instantiationDigital to identify the format of a particular instantiation of an asset as it exists as a digital file on a server, hard drive, or other digital storage medium. Digital instantiations should be expressed as a formal Internet MIME types.")
				},
			"instantiationStandard":{
				"required":False,
				"description":(" If the instantiation is a physical item, instantiationStandard can be used to refer to the broadcast standard of the video signal (e.g. NTSC, PAL), or the audio encoding (e.g. Dolby A, vertical cut). If the instantiation is a digital item, instantiationStandard should be used to express the container format of the digital file (e.g. MXF).")
				},
			"instantiationLocation":{
				"required":True,
				"description":(" instantiationLocation may contain information about a specific location for an instantiation, such as an organization\'s name, departmental name, shelf ID and contact information. The instantiationLocation for a digital file should include domain, path or URI to the file.")
				},
			"instantiationMediaType ":{
				"required":False,
				"description":("This element identifies the general, high level nature of the content of an instantiation. It uses categories that show how content is presented to an observer, e.g., as a sound, text or moving image.")
				},
			"instantiationGeneration":{
				"required":False,
				"description":(" The instantiationGeneration element identifies the use type and provenance of the instantiation. The generation of a video tape may be an “Original Master” or “Dub”, the generation of a film reel may be an “Original Negative” or “Composite Positive”, an audiotape may be a “Master” or “Mix Element”, an image may be a “Photograph” or a “Photocopy”.")
				},
			"instantiationFileSize ":{
				"required":False,
				"description":("This element indicates the file size of a digital instantiation. It should contain only numerical values. As a standard, express the file size in bytes. Units of Measure should be declared in the unitsOfMeasure attribute.")
				},
			"instantiationTimeStart ":{
				"required":False,
				"description":("This element describes the point at which playback begins for a time-based instantiation. It is likely that the content on a tape may begin an arbitrary amount of time after the beginning of the instantiation. Best practice is to use a timestamp format such as HH:MM:SS[:|;]FF or HH:MM:SS.mmm or S.mmm.")
				},
			"instantiationDuration":{
				"required":False,
				"description":("The element instantiationDuration provides a timestamp for the overall length or duration of a time-based media item. It represents the playback time. Best practice is to use a timestamp format such as HH:MM:SS[:|;]FF or HH:MM:SS.mmm or S.mmm")
				},
			"instantiationDataRate":{
				"required":False,
				"description":("The element instantiationDataRate expresses the amount of data in a digital media file that is encoded, delivered or distributed, for every second of time. This should be expressed as numerical data, with the units of measure declared in the unitsOfMeasure attribute. For example, if the audio file is 56 kilobits/second, then 56 should be the value of instantiationDataRate and the attribute unitsOfMeasure should be kilobits/second.")
				},
			"instantiationColors":{
				"required":False,
				"description":("The element instantiationColors indicates the overall color, grayscale, or black and white nature of the presentation of an instantiation, as a single occurrence or combination of occurrences in or throughout the instantiation.")
				},
			"instantiationTracks":{
				"required":False,
				"description":("The element instantiationTracks is simply intended to indicate the number and type of tracks that are found in a media item, whether it is analog or digital. (e.g. 1 video track, 2 audio tracks, 1 text track, 1 sprite track, etc.) Other configuration information specific to these identified tracks should be described using instantiationChannelConfiguration.")
				},
			"instantiationChannelConfiguration":{
				"required":False,
				"description":("The element instantiationChannelConfiguration is designed to indicate, at a general narrative level, the arrangement or configuration of specific channels or layers of information within an instantiation\'s tracks. Examples are 2-track mono, 8- track stereo, or video track with alpha channel.")
				},
			"instantiationLanguage":{
				"required":False,
				"description":("The element language identifies the primary language of the instantiation\'s audio or text. Alternative audio or text tracks and their associated languages should be identified using the element instantiationAlternativeModes.")
				},
			"instantiationAlternativeModes":{
				"required":False,
				"description":(" The element instantiationAlternativeModes is a catch-all metadata element that identifies equivalent alternatives to the primary visual, sound or textual information that exists in an instantiation. These are modes that offer alternative ways to see, hear, and read the content of an instantiation. Examples include DVI (Descriptive Video Information), SAP (Supplementary Audio Program), ClosedCaptions, OpenCaptions, Subtitles, Language Dubs, and Transcripts. For each instance of available alternativeModes, the mode and its associated language should be identified together, if applicable. Examples include \'SAP in English,\' \'SAP in Spanish,\' \'Subtitle in French,\' \'OpenCaption in Arabic.\'")
				},
			"instantiationEssenceTrack":{
				"required":False,
				"description":(" The instantiationEssenceTrack element is an XML container element that allows for grouping of related essenceTrack elements and their repeated use. Use instantiationEssenceTrack element to describe the individual streams that comprise an instantiation, such as audio, video, timecode, etc.")
				},
			"instantiationRelation":{
				"required":False,
				"description":("The instantiationRelation element is a container for sub-elements instantiationRelationType and instantiationRelationIdentifier to describe relationships to other instantiations.")
				},
			"instantiationRights":{
				"required":False,
				"description":(" The instantiationRights element is a container for sub-elements rightsSummary, rightsLink and rightsEmbedded to describe rights particular to this instantiation.")
				},
			"instantiationAnnotation":{
				"required":False,
				"description":("The instantiationAnnotation element is used to add any supplementary information about an instantiation of the instantiation or the metadata used to describe it. It clarifies element values, terms, descriptors, and vocabularies that may not be otherwise sufficiently understood.")
				},
			"instantiationPart":{
				"required":False,
				"description":("InstantiationPart is a container that allows the instantiation to be split into multiple parts, which can describe the parts of a multi-section instantiation, e.g., a multi-disk DVD or vitagraph record and 35mm reel that are intended for synchronous playback. It contains all of the elements that a pbcoreInstantiation element would typically contain.")
				},
			"instantiationExtension":{
				"required":False,
				"description":("Extensions are either a wrapper containing a specific element from another standard OR embedded xml containing the extension.")
				},
			"element":{
				"required":False,
				"description":("")
				}
		},
		"documentation":"http://pbcore.org/pbcoreinstantiationdocument/"
	}
}

INTELLECTUAL_CONTENT_ELEMENTS = {
	"pbcoreAssetType":{
		"definition":("pbcoreAssetType is a broad definition of the type of intellectual content being described. Asset types might include those without associated instantiations (a collection or series), or those with instantiations (programs, episodes, clips, etc.)"),
		"attributes":{
			"ref":{
				"required":False,
				"usage note":("Use attribute ref to supply a source’s URI for the value of the element. Attribute ref can be used to point to a term in a controlled vocabulary, or a URI associated with a source.")
			},
			"source":{
					"required":False,
					"usage note":("Attribute source provides the name of the authority used to declare the value of the element. Different elements will use the source attribute slightly differently.  For example, identifier source (required) should be the name of the organization, institution, system or namespace that the identifier came from, such as \'PBS NOLA Code\' or an institutional database identifier.  For other elements, this might be the name of a controlled vocabulary, namespace or authority list, such as Library of Congress Subject Headings.  We recommend a consistent and human readable use.")
				},
			"version":{
					"required":False,
					"usage note":(" Attribute version identifies any version information about the authority or convention used to express data of this element.")
				},
			"annotation":{
					"required":False,
					"usage note":("Attribute annotation includes narrative information intended to clarify the nature of data used in the element. Can be used as a notes field to include any additional information about the element or associated attributes")
				}
		},
		"best practice":("The asset type should broadly describe all related instantiations -- for example, if an asset includes many instantiations representing different generations of a program, the asset type ‘program’ remains accurate for all of them."),
		"usage":{
			"required":False,
			"repeatable":True,
			"usage note":("")
		},
		"subelements":{
			"":""
		},
		"documentation":"http://pbcore.org/pbcoreassettype/"
	},
	"pbcoreAssetDate":{
		"definition":("pbcoreAssetDate is intended to reflect dates associated with the Intellectual Content."),
		"attributes":{
			"dateType":{
				"required":False,
				"usage note":(" Attribute dateType classifies by named type the date-related data of the element e.g., created, broadcast, dateAvailableStart. Used to clarify how the assetDate is related to the asset. Date Created may be the most common, but the element could also be used to describe the Date Accessioned or Date Deaccessioned, for example.")
			},
			"ref":{
				"required":False,
				"usage note":("Use attribute ref to supply a source’s URI for the value of the element. Attribute ref can be used to point to a term in a controlled vocabulary, or a URI associated with a source.")
			},
			"source":{
					"required":False,
					"usage note":("Attribute source provides the name of the authority used to declare the value of the element. Different elements will use the source attribute slightly differently.  For example, identifier source (required) should be the name of the organization, institution, system or namespace that the identifier came from, such as \'PBS NOLA Code\' or an institutional database identifier.  For other elements, this might be the name of a controlled vocabulary, namespace or authority list, such as Library of Congress Subject Headings.  We recommend a consistent and human readable use.")
				},
			"version":{
					"required":False,
					"usage note":(" Attribute version identifies any version information about the authority or convention used to express data of this element.")
				},
			"annotation":{
					"required":False,
					"usage note":("Attribute annotation includes narrative information intended to clarify the nature of data used in the element. Can be used as a notes field to include any additional information about the element or associated attributes")
				}
		},
		"best practice":("By contrast, instantiationDate is intended to reflect date information for the specific instance. For instance, if you have a VHS copy of Gone With The Wind, the pbcoreAssetDate would be 1939, while the instantiationDate of the VHS copy could be 1985. pbcoreAssetDate may also be used to reflect availability dates, etc. Date types should be specified using the @dateType attribute.  Dates or time-based events related to the content of the asset, on the other hand, would be described in the \'coverage\' element — so, while the storyline of Gone with the Wind takes place in the nineteenth century, this information should be noted in the Coverage field, not the assetDate field.  Best practice is to use ISO 8601 or some other date/time standard if possible."),
		"usage":{
			"required":False,
			"repeatable":True,
			"usage note":("")
		},
		"subelements":{
			"":""
		},
		"documentation":"http://pbcore.org/pbcoreassetdate/"
	},
	"pbcoreIdentifier":{
		"definition":("pbcoreIdentifier is an identifier that can apply to the asset. This identifier should not be limited to a specific instantiation, but rather all instantiations of an asset. It can also hold a URL or URI that points to the asset."),
		"attributes":{
			"ref":{
				"required":False,
				"usage note":("Use attribute ref to supply a source’s URI for the value of the element. Attribute ref can be used to point to a term in a controlled vocabulary, or a URI associated with a source.")
			},
			"source":{
					"required":True,
					"usage note":("Attribute source provides the name of the authority used to declare the value of the element. Different elements will use the source attribute slightly differently.  For example, identifier source (required) should be the name of the organization, institution, system or namespace that the identifier came from, such as \'PBS NOLA Code\' or an institutional database identifier.  For other elements, this might be the name of a controlled vocabulary, namespace or authority list, such as Library of Congress Subject Headings.  We recommend a consistent and human readable use.")
				},
			"version":{
					"required":False,
					"usage note":(" Attribute version identifies any version information about the authority or convention used to express data of this element.")
				},
			"annotation":{
					"required":False,
					"usage note":("Attribute annotation includes narrative information intended to clarify the nature of data used in the element. Can be used as a notes field to include any additional information about the element or associated attributes")
				}
		},
		"best practice":("Best practice is to identify the media item (whether analog or digital) by means of an unambiguous string or number corresponding to an established or formal identification system if one exists. Otherwise, use an identification method that is in use within your agency, station, production company, office, or institution."),
		"usage":{
			"required":True,
			"repeatable":True,
			"usage note":("")
		},
		"subelements":{
			"":""
		},
		"documentation":"http://pbcore.org/pbcoreidentifier/"
	},
	"pbcoreTitle":{
		"definition":("pbcoreTitle is a name or label relevant to the asset."),
		"attributes":{
			"titleType":{
				"required":False,
				"usage note":("Use the attribute titleType to indicate the type of title being assigned to the asset, such as series title, episode title or project title. Has a PBCore controlled vocabulary (recommended).")
			},
			"titleTypeSource":{
				"required":False,
				"usage note":("Attribute titleTypeSource provides the name of the authority used to declare data value of the titleType attribute. This might be the name of a controlled vocabulary, namespace or authority list, such as the official PBCore vocabulary. We recommend a consistent and human readable use.")
			},
			"titleTypeRef":{
				"required":False,
				"usage note":(". Use attribute titleTypeRef to supply a source’s URI for the value of the attribute titleTypeSource. Attribute titleTypeRef can be used to point to a term in a controlled vocabulary, or a URI associated with a source.")
			},
			"titleTypeVersion":{
				"required":False,
				"usage note":("Attribute titleTypeVersion identifies any version information about the authority or convention used to express data of this element.")
			},
			"titleTypeAnnotation":{
				"required":False,
				"usage note":("Attribute titleTypeAnnotation includes narrative information intended to clarify the nature of data used in the element. Can be used as a notes field to include any additional information about the element or associated attributes.")
			},
			"startTime":{
				"required":False,
				"usage note":("Attribute startTime combines with the endTime attribute to define a specific media segment within a broader timeline of an asset and/or instantiation. Used to talk generally about the start/end time of a segment (e.g. \'30 minutes\'), or by providing a timestamp to a specific point in an instantiation. If you\'re doing that for element at the asset level, we suggest referencing the instantiation ID you are referring to in timeAnnotation. One example would be if a six-hour long tape was broken into multiple programs, and each instantiation might have its start time labeled as when the instantiation began in the timeline of the broader tape. Another example for this usage might be a digital file created from a VHS tape that contains multiple segments. In the digital copy, color bars are removed from the beginning, and black from the end of the digital instantiation. Time references referring to the segments on the physical VHS are no longer relevant; therefore it\'s important to tie start and end time references to a specific instantiation, e.g. use the asset ID and timestamp.")
			},
			"endTime":{
				"required":False,
				"usage note":(" Attribute endTime combines with a similar value in the startTime attribute to define a specific media segment within a broader timeline of an asset and/or instantiation.")
			},
			"timeAnnotation":{
				"required":False,
				"usage note":("Attribute timeAnnotation includes narrative information intended to clarify the nature of data used in the element.")
			},
			"ref":{
				"required":False,
				"usage note":("Use attribute ref to supply a source’s URI for the value of the element. Attribute ref can be used to point to a term in a controlled vocabulary, or a URI associated with a source.")
			},
			"source":{
				"required":True,
				"usage note":("Attribute source provides the name of the authority used to declare the value of the element. Different elements will use the source attribute slightly differently.  For example, identifier source (required) should be the name of the organization, institution, system or namespace that the identifier came from, such as \'PBS NOLA Code\' or an institutional database identifier.  For other elements, this might be the name of a controlled vocabulary, namespace or authority list, such as Library of Congress Subject Headings.  We recommend a consistent and human readable use.")
			},
			"version":{
				"required":False,
				"usage note":(" Attribute version identifies any version information about the authority or convention used to express data of this element.")
			},
			"annotation":{
				"required":False,
				"usage note":("Attribute annotation includes narrative information intended to clarify the nature of data used in the element. Can be used as a notes field to include any additional information about the element or associated attributes")
			}
		},
		"best practice":("There may be many types of titles an asset may have, such as a series title, episode title, segment title, or project title, therefore the element is repeatable."),
		"usage":{
			"required":True,
			"repeatable":True,
			"usage note":("")
		},
		"subelements":{
			"":""
		},
		"documentation":"http://pbcore.org/pbcoretitle/"
	},
	"pbcoreSubject":{
		"definition":(""),
		"attributes":{
			"attribute":{
				"required":False,
				"usage note":("")
			}
		},
		"best practice":(""),
		"usage":{
			"required":False,
			"repeatable":False,
			"usage note":("")
		},
		"subelements":{
			"element":{
				"required":False,
				"description":("")
			}
		},
		"documentation":""
	},
	"pbcoreDescription":{
		"definition":(""),
		"attributes":{
			"attribute":{
				"required":False,
				"usage note":("")
			}
		},
		"best practice":(""),
		"usage":{
			"required":False,
			"repeatable":False,
			"usage note":("")
		},
		"subelements":{
			"element":{
				"required":False,
				"description":("")
			}
		},
		"documentation":""
	},
	"pbcoreGenre":{
		"definition":(""),
		"attributes":{
			"attribute":{
				"required":False,
				"usage note":("")
			}
		},
		"best practice":(""),
		"usage":{
			"required":False,
			"repeatable":False,
			"usage note":("")
		},
		"subelements":{
			"element":{
				"required":False,
				"description":("")
			}
		},
		"documentation":""
	},
	"pbcoreRelation":{
		"definition":(""),
		"attributes":{
			"attribute":{
				"required":False,
				"usage note":("")
			}
		},
		"best practice":(""),
		"usage":{
			"required":False,
			"repeatable":False,
			"usage note":("")
		},
		"subelements":{
			"element":{
				"required":False,
				"description":("")
			}
		},
		"documentation":""
	},
	"pbcoreRelationType":{
		"definition":(""),
		"attributes":{
			"attribute":{
				"required":False,
				"usage note":("")
			}
		},
		"best practice":(""),
		"usage":{
			"required":False,
			"repeatable":False,
			"usage note":("")
		},
		"subelements":{
			"element":{
				"required":False,
				"description":("")
			}
		},
		"documentation":""
	},
	"pbcoreRelationIdentifier":{
		"definition":(""),
		"attributes":{
			"attribute":{
				"required":False,
				"usage note":("")
			}
		},
		"best practice":(""),
		"usage":{
			"required":False,
			"repeatable":False,
			"usage note":("")
		},
		"subelements":{
			"element":{
				"required":False,
				"description":("")
			}
		},
		"documentation":""
	},
	"pbcoreCoverage":{
		"definition":(""),
		"attributes":{
			"attribute":{
				"required":False,
				"usage note":("")
			}
		},
		"best practice":(""),
		"usage":{
			"required":False,
			"repeatable":False,
			"usage note":("")
		},
		"subelements":{
			"element":{
				"required":False,
				"description":("")
			}
		},
		"documentation":""
	},
	"coverage":{
		"definition":(""),
		"attributes":{
			"attribute":{
				"required":False,
				"usage note":("")
			}
		},
		"best practice":(""),
		"usage":{
			"required":False,
			"repeatable":False,
			"usage note":("")
		},
		"subelements":{
			"element":{
				"required":False,
				"description":("")
			}
		},
		"documentation":""
	},
	"coverageType":{
		"definition":(""),
		"attributes":{
			"attribute":{
				"required":False,
				"usage note":("")
			}
		},
		"best practice":(""),
		"usage":{
			"required":False,
			"repeatable":False,
			"usage note":("")
		},
		"subelements":{
			"element":{
				"required":False,
				"description":("")
			}
		},
		"documentation":""
	},
	"pbcoreAudienceLevel":{
		"definition":(""),
		"attributes":{
			"attribute":{
				"required":False,
				"usage note":("")
			}
		},
		"best practice":(""),
		"usage":{
			"required":False,
			"repeatable":False,
			"usage note":("")
		},
		"subelements":{
			"element":{
				"required":False,
				"description":("")
			}
		},
		"documentation":""
	},
	"pbcoreAudienceRating":{
		"definition":(""),
		"attributes":{
			"attribute":{
				"required":False,
				"usage note":("")
			}
		},
		"best practice":(""),
		"usage":{
			"required":False,
			"repeatable":False,
			"usage note":("")
		},
		"subelements":{
			"element":{
				"required":False,
				"description":("")
			}
		},
		"documentation":""
	},
	"pbcoreAnnotation":{
		"definition":(""),
		"attributes":{
			"attribute":{
				"required":False,
				"usage note":("")
			}
		},
		"best practice":(""),
		"usage":{
			"required":False,
			"repeatable":False,
			"usage note":("")
		},
		"subelements":{
			"element":{
				"required":False,
				"description":("")
			}
		},
		"documentation":""
	}
}

INTELLECTUAL_PROPERTY_ELEMENTS = {
	"pbcoreCreator":{
		"definition":(""),
		"attributes":{
			"attribute":{
				"required":False,
				"usage note":("")
			}
		},
		"best practice":(""),
		"usage":{
			"required":False,
			"repeatable":False,
			"usage note":("")
		},
		"subelements":{
			"element":{
				"required":False,
				"description":("")
			}
		},
		"documentation":""
	},
	"creator":{
		"definition":(""),
		"attributes":{
			"attribute":{
				"required":False,
				"usage note":("")
			}
		},
		"best practice":(""),
		"usage":{
			"required":False,
			"repeatable":False,
			"usage note":("")
		},
		"subelements":{
			"element":{
				"required":False,
				"description":("")
			}
		},
		"documentation":""
	},
	"creatorRole":{
		"definition":(""),
		"attributes":{
			"attribute":{
				"required":False,
				"usage note":("")
			}
		},
		"best practice":(""),
		"usage":{
			"required":False,
			"repeatable":False,
			"usage note":("")
		},
		"subelements":{
			"element":{
				"required":False,
				"description":("")
			}
		},
		"documentation":""
	},
	"pbcoreContributor":{
		"definition":(""),
		"attributes":{
			"attribute":{
				"required":False,
				"usage note":("")
			}
		},
		"best practice":(""),
		"usage":{
			"required":False,
			"repeatable":False,
			"usage note":("")
		},
		"subelements":{
			"element":{
				"required":False,
				"description":("")
			}
		},
		"documentation":""
	},
	"contributor":{
		"definition":(""),
		"attributes":{
			"attribute":{
				"required":False,
				"usage note":("")
			}
		},
		"best practice":(""),
		"usage":{
			"required":False,
			"repeatable":False,
			"usage note":("")
		},
		"subelements":{
			"element":{
				"required":False,
				"description":("")
			}
		},
		"documentation":""
	},
	"contributorRole":{
		"definition":(""),
		"attributes":{
			"attribute":{
				"required":False,
				"usage note":("")
			}
		},
		"best practice":(""),
		"usage":{
			"required":False,
			"repeatable":False,
			"usage note":("")
		},
		"subelements":{
			"element":{
				"required":False,
				"description":("")
			}
		},
		"documentation":""
	},
	"pbcorePublisher":{
		"definition":(""),
		"attributes":{
			"attribute":{
				"required":False,
				"usage note":("")
			}
		},
		"best practice":(""),
		"usage":{
			"required":False,
			"repeatable":False,
			"usage note":("")
		},
		"subelements":{
			"element":{
				"required":False,
				"description":("")
			}
		},
		"documentation":""
	},
	"publisher":{
		"definition":(""),
		"attributes":{
			"attribute":{
				"required":False,
				"usage note":("")
			}
		},
		"best practice":(""),
		"usage":{
			"required":False,
			"repeatable":False,
			"usage note":("")
		},
		"subelements":{
			"element":{
				"required":False,
				"description":("")
			}
		},
		"documentation":""
	},
	"publisherRole":{
		"definition":(""),
		"attributes":{
			"attribute":{
				"required":False,
				"usage note":("")
			}
		},
		"best practice":(""),
		"usage":{
			"required":False,
			"repeatable":False,
			"usage note":("")
		},
		"subelements":{
			"element":{
				"required":False,
				"description":("")
			}
		},
		"documentation":""
	},
	"pbcoreRightsSummary":{
		"definition":(""),
		"attributes":{
			"attribute":{
				"required":False,
				"usage note":("")
			}
		},
		"best practice":(""),
		"usage":{
			"required":False,
			"repeatable":False,
			"usage note":("")
		},
		"subelements":{
			"element":{
				"required":False,
				"description":("")
			}
		},
		"documentation":""
	},
	"rightsSummary":{
		"definition":(""),
		"attributes":{
			"attribute":{
				"required":False,
				"usage note":("")
			}
		},
		"best practice":(""),
		"usage":{
			"required":False,
			"repeatable":False,
			"usage note":("")
		},
		"subelements":{
			"element":{
				"required":False,
				"description":("")
			}
		},
		"documentation":""
	},
	"rightsLink":{
		"definition":(""),
		"attributes":{
			"attribute":{
				"required":False,
				"usage note":("")
			}
		},
		"best practice":(""),
		"usage":{
			"required":False,
			"repeatable":False,
			"usage note":("")
		},
		"subelements":{
			"element":{
				"required":False,
				"description":("")
			}
		},
		"documentation":""
	},
	"rightsEmbedded":{
		"definition":(""),
		"attributes":{
			"attribute":{
				"required":False,
				"usage note":("")
			}
		},
		"best practice":(""),
		"usage":{
			"required":False,
			"repeatable":False,
			"usage note":("")
		},
		"subelements":{
			"element":{
				"required":False,
				"description":("")
			}
		},
		"documentation":""
	}
}

PBCORE_VERSION_2_1_ELEMENTS = {
	"ROOT_ELEMENTS":ROOT_ELEMENTS,
	"INTELLECTUAL_CONTENT_ELEMENTS":INTELLECTUAL_CONTENT_ELEMENTS,
	"INTELLECTUAL_PROPERTY_ELEMENTS":INTELLECTUAL_PROPERTY_ELEMENTS
}
