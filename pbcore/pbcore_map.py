import pbcore_elements

pbCoreIntelContentAndProp = []
for item in list(pbcore_elements.INTELLECTUAL_CONTENT_ELEMENTS.keys()):
	pbCoreIntelContentAndProp.append(item)
for item in list(pbcore_elements.INTELLECTUAL_PROPERTY_ELEMENTS.keys()):
	pbCoreIntelContentAndProp.append(item)

PBCORE_MAP = {
	"accFull":{
		"instantiationIdentifier":{
			"LEVEL":"INSTANTIATION",
			"ATTRIBUTES":{
				"source":"PFA accession number"
			},
			"TEXT":"value"
		}
	},
	"title":{
		"pbcoreTitle":{
			"LEVEL":"WORK",
			"ATTRIBUTES":{
				"titleType":"Main"
			},
			"TEXT":"value"
		}
	},
	"altTitle":{
		"pbcoreTitle":{
			"LEVEL":"WORK",
			"ATTRIBUTES":{
				"titleType":"Alternative Main"
			},
			"TEXT":"value"
		}
	},
	"releaseYear":{
		"pbcoreAssetDate":{
			"LEVEL":"WORK",
			"ATTRIBUTES":{
				"dateType":"Released"
			},
			"TEXT":"value"
		}
	},
	"conditionNote":{
		"instantiationAnnotation":{
			"LEVEL":"INSTANTIATION",
			"ATTRIBUTES":{
				"annotationType":"Condition note"
			},
			"TEXT":"value"
		}
	},
	"country":{
		"coverage":{
			"LEVEL":"WORK",
			"TEXT":"value",
			"SIBLING_FIELD":{
				"coverageType":{
					"ATTRIBUTES":{
						"ref":"http://metadataregistry.org/concept/show/id/2522.html"
					},
					"TEXT":"Spatial"
				}
			}
		}
	},
	"directorsNames":{
		"pbcoreCreator":{
			"LEVEL":"WORK",
			"TEXT":"",
			"SUBELEMENTS":{
				"creator":{
					"TEXT":"value"
				},
				"creatorRole":{
					"ATTRIBUTES":{
						"source":"PBCore creatorRole",
						"ref":"http://metadataregistry.org/concept/show/id/1303.html"
					},
					"TEXT":"Director(s)"
				}
			}
		}
	},
	"Barcode":{
		"instantiationIdentifier":{
			"LEVEL":"INSTANTIATION",
			"ATTRIBUTES":{
				"source":"PFA barcode"
			},
			"TEXT":"value"
		}
	},
	"generalNotes":{
		"instantiationAnnotation":{
			"LEVEL":"INSTANTIATION",
			"ATTRIBUTES":{
				"annotationType":"General note"
			},
			"TEXT":"value"
		}
	},
	"credits":{
		"pbcoreRightsSummary":{
			"LEVEL":"WORK",
			"TEXT":"",
			"SUBELEMENTS":{
				"rightsSummary":{
					"ATTRIBUTES":{
						"annotation":"Credits statement"
					},
					"TEXT":"value"
				}
			}
		}
	},
	"projGrp":{
		"instantiationExtension":{
			"LEVEL":"INSTANTIATION",
			"TEXT":"",
			"SUBELEMENTS":{
				"extensionWrap":{
					"TEXT":"",
					"SUBELEMENTS":{
						"extensionElement":{
							"TEXT":"isPartOf"
						},
						"extensionValue":{
							"TEXT":"value"
						},
						"extensionAuthorityUsed":{
							"TEXT":"DCMI Metadata Terms"
						}
					},
				}
			}
		}
	},
	"ingestUUID":{
		"instantiationAnnotation":{
			"LEVEL":"INSTANTIATION",
			"ATTRIBUTES":{
				"annotationType":"PFA ingest process unique identifier"
			},
			"TEXT":"value"
		}
	},
	"BAMPFAlocation":{
		"instantiationLocation":{
			"LEVEL":"INSTANTIATION",
			"ATTRIBUTES":{
				"annotation":"may either be 'BAMPFA Digital Repository or LTO Tape ID"
			},
			"TEXT":"value"
		}
	},
	"eventTitle":{
		"pbcoreTitle":{
			"LEVEL":"WORK",
			"ATTRIBUTES":{
				"titleType":"Event",
				"titleTypeAnnotation":"BAMPFA metadata definition"
			},
			"TEXT":"value"
		}
	},
	"eventYear":{
		"pbcoreAssetDate":{
			"LEVEL":"WORK",
			"ATTRIBUTES":{
				"dateType":"Event",
				"annotation":"Year of a recorded event. Describes BAMPFA non-collection assets."
			},
			"TEXT":"value"
		}
	},
	"eventFullDate":{
		"pbcoreAssetDate":{
			"LEVEL":"WORK",
			"ATTRIBUTES":{
				"dateType":"Event",
				"annotation":"Full date of a recorded event. Describes BAMPFA non-collection assets."
			},
			"TEXT":"value"
		}
	},
	"generation":{
		"instantiationGenerations":{
			"LEVEL":"INSTANTIATION",
			"ATTRIBUTES":{
				"source":"BAMPFA controlled vocabulary"
			},
			"TEXT":"value"
		}
	},
	"language":{
		"instantiationLanguage":{
			"LEVEL":"INSTANTIATION",
			"ATTRIBUTES":{
				"source":"IS0 639.2",
				"ref":""
			},
			"TEXT":"value"
		}
	},
	"soundCharacteristics":{
		"instantiationAnnotation":{
			"LEVEL":"INSTANTIATION",
			"ATTRIBUTES":{
				"annotation":"Sound or silent"
			},
			"TEXT":"value"
		}
	},
	"colorCharacteristics":{
		"instantiationColors":{
			"LEVEL":"INSTANTIATION",
			"ATTRIBUTES":{
				"source":"BAMPFA controlled vocabulary"
			},
			"TEXT":"value"
		}
	},
	"runningTime":{
		"instantiationDuration":{
			"LEVEL":"INSTANTIATION",
			"ATTRIBUTES":{
				"annotation":"May be specific to BAMPFA projectors, scan rates, etc."
			},
			"TEXT":"value"
		}
	},
	"medium":{
		"instantiationMediaType":{
			"LEVEL":"INSTANTIATION",
			"ATTRIBUTES":{
				"source":"BAMPFA controlled vocabulary",
				"annotation":"BAMPFA source material medium."
			},
			"TEXT":"value"
		}
	},
	"dimensions":{
		"instantiationDimensions":{
			"LEVEL":"INSTANTIATION",
			"ATTRIBUTES":{
				"source":"BAMPFA controlled vocabulary"
			},
			"TEXT":"value"
		}
	},
	"videoFormat":{
		"instantiationPhysical":{
			"LEVEL":"INSTANTIATION",
			"ATTRIBUTES":{
				"source":"BAMPFA controlled vocabulary"
			},
			"TEXT":"value"
		}
	},
	"videoStandard":{
		"instantiationStandard":{
			"LEVEL":"INSTANTIATION",
			"ATTRIBUTES":{
				"source":"PBCore instantiationStandard/video",
				"ref":"http://pbcore.org/vocabularies/instantiationStandard/video%23ntsc"
			},
			"TEXT":"value"
		}
	},
	"BAMPFA_FIELD":{
		"PBCORE_ELEMENT":{
			"LEVEL":"WORK_OR_INSTANTIATION",
			"ATTRIBUTE":"DEFAULT_VALUE",
			"TEXT":"Null",
			"SUBELEMENTS":{
				"PBCORE_FIELD":{
					"ATTRIBUTE":"DEFAULT_VALUE",
					"TEXT":"Null"
				}
			},
			"SIBLING_FIELD":{
				"PBCORE_FIELD":{
					"ATTRIBUTE":"DEFAULT_VALUE"
				}
			}
		}
	}
}

BAMPFA_FIELDS = list(PBCORE_MAP.keys())