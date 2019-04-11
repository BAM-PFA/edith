'''
Run this from `flask shell`
from instance import insertMetadataFields
insertMetadataFields.insert_fields()
'''
from . import metadataMappings
from app import models,db

metadata = metadataMappings.metadataMaps

def insert_fields():
	for database, stuff in metadataMappings.metadataMaps.items():
		print(database)
		databaseID = models.Data_Source.query.filter_by(dbName=database).first().id

		for field,details in stuff['FIELDS'].items():
			fieldUniqueName = field
			rsFieldID = details['RS_FIELD_ID']
			fieldSourceName = details['SOURCE_FIELD_NAME']
			fieldDisplayName = None #details['DISPLAY_NAME'] I SHOULD ADD THIS TO THE MAP?
			print(fieldUniqueName,rsFieldID,fieldSourceName,fieldDisplayName,database)

			_field = models.Metadata_Field(
				fieldName = fieldDisplayName,
				fieldUniqueName = fieldUniqueName,
				fieldSourceName = fieldSourceName,
				dataSource_id = int(databaseID),
				rsFieldID = rsFieldID
				)

			db.session.add(_field)
			db.session.commit()
