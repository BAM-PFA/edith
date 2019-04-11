# non-standard libraries
from flask_wtf import FlaskForm
import wtforms
from wtforms.validators import DataRequired, Email
from wtforms.ext.sqlalchemy.fields import QuerySelectField

# local imports
from ..models import Data_Source


class MetadataForm(FlaskForm):
	'''
	Fields for additional metadata
	userMD_1 = Communications
	userMD_2 = Event
	userMD_3 = General
	'''
	userMD_1_editSequenceSettings = wtforms.StringField("Settings/framing of NLE sequence",default='')
	userMD_1_exportPublishDate = wtforms.StringField("Date of export or publishing",default='')
	userMD_1_platformOutlet = wtforms.StringField("Media platform or outlet",default='')
	# userMD_2_eventFullDate = wtforms.StringField("Full date of event",default='')
	# userMD_2_eventLocation = wtforms.StringField("Event location",default='')

	userMD_2_locationOfRecording = wtforms.StringField("Location of recording or event",default='')
	userMD_2_eventOrganizer = wtforms.StringField("Event organizer",default='')
	userMD_2_eventSeries = wtforms.StringField("Event series",default='')
	userMD_2_eventRelatedExhibition = wtforms.StringField("Related BAMPFA exhibition",default='')
	# userMD_2_eventYear = wtforms.StringField("Event year",default='')
	userMD_2_PFAfilmSeries = wtforms.StringField("Related PFA film series",default='')

	userMD_3_altTitle = wtforms.StringField("Alternative title for a work",default='')
	userMD_3_additionalCredits = wtforms.StringField("Additional credits",default='')
	userMD_3_country = wtforms.StringField("Country of production",default='')
	userMD_3_language = wtforms.StringField("Language",default='')
	userMD_3_description = wtforms.StringField("Description",default='')
	userMD_3_generalNotes = wtforms.StringField("General notes",default='')
	userMD_3_generation = wtforms.StringField("Generation",default='')
	userMD_3_medium = wtforms.StringField("Source format/medium (for digitized works)",default='')
	userMD_3_tags = wtforms.StringField("Tags (comma separated)",default='')
	userMD_3_assetExternalSource = wtforms.StringField("Source (if not BAMPFA staff)",default='')
	userMD_3_copyrightStatement = wtforms.StringField("Copyright statement",default='')
	userMD_3_restrictionsOnUse = wtforms.StringField("Restrictions on use",default='')
	userMD_3_postProcessing = wtforms.SelectField("Raw or edited work",default='',choices=[('',''),('raw','Raw'),('edited','Edited work')])
	userMD_3_digitizedBornDigital = wtforms.SelectField("Digitized or Born-digital?",default='',choices=[('',''),('digitized','Digitized'),('born digital','Born-digital')])
	userMD_3_digitizer = wtforms.StringField("Name of digitizer",default='')
	userMD_3_nameSubjects = wtforms.StringField("Name subjects",default='')
	userMD_3_filmTitleSubjects = wtforms.StringField("Subject(s): Film title(s)",default='')
	userMD_3_topicalSubjects = wtforms.StringField("Subject(s): Topics",default='')

	userMD_4_title = wtforms.StringField("Main title of a work",default='')
	userMD_4_directorsNames = wtforms.StringField("Director(s)/Filmmaker(s)",default='')
	userMD_4_releaseDate = wtforms.StringField("Release date",default='')
	userMD_4_eventTitle = wtforms.StringField("Event title",default='')
	userMD_4_recordingDate = wtforms.StringField("Date of recording",default='')
	userMD_4_speakerInterviewee = wtforms.StringField("Speaker/Interviewee",default='')
	userMD_4_creator = wtforms.StringField("Creator (unspecified role)",default='')
	# userMD_ = wtforms.StringField("",default='')

class ObjectForm(FlaskForm):
	"""
	Fields for an individual object
	"""
	targetPath = wtforms.HiddenField('objectPath')
	targetBase = wtforms.HiddenField('objectBase')
	runIngest = wtforms.BooleanField('Ingest?',default='')
	doConcat = wtforms.BooleanField("Concatenate reels?",default='')

	# https://stackoverflow.com/questions/46921823/dynamic-choices-wtforms-flask-selectfield?rq=1
	metadataSource = wtforms.SelectField('Metadata Source',coerce=int,default='')
	metadataForm = wtforms.FormField(MetadataForm)
	

class IngestForm(FlaskForm):
	'''
	General input form
	'''
	suchChoices = wtforms.HiddenField(default='default choices')
	submit = wtforms.SubmitField('Submit')
