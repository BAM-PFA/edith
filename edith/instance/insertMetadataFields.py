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
		try:
			databaseID = models.Data_Source.query.filter_by(dbName=database).first().id
			databaseID = int(databaseID)
		except:
			databaseID = None

		for field,details in stuff['FIELDS'].items():
			fieldUniqueName = field
			rsFieldID = details['RS_FIELD_ID']
			fieldSourceName = details['SOURCE_FIELD_NAME']
			try:
				fieldDisplayName = details['DISPLAY_NAME'] 
			except:
				fieldDisplayName = None
			try:
				description = details['DESCRIPTION']
			except:
				description = None

			print(fieldUniqueName,rsFieldID,fieldSourceName,fieldDisplayName,description,database)

			_field = models.Metadata_Field(
				fieldName = fieldDisplayName,
				fieldUniqueName = fieldUniqueName,
				fieldSourceName = fieldSourceName,
				dataSource_id = databaseID,
				rsFieldID = rsFieldID,
				description = description
				)

			try:
				db.session.add(_field)
			except Exception as e:
				print(e)
			db.session.commit()
