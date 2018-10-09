from flask_wtf import FlaskForm
import wtforms
from wtforms.validators import DataRequired, Email

class MetadataForm(FlaskForm):
        '''
        Fields for additional metadata
        '''
        userMD_eventTitle = wtforms.StringField("Event title",default='')
        userMD_eventYear = wtforms.StringField("Event year",default='')
        userMD_eventFullDate = wtforms.StringField("Full date of event",default='')
        userMD_eventSeries = wtforms.StringField("Event series",default='')
        userMD_eventRelatedExhibition = wtforms.StringField("Related exhibition",default='')
        userMD_eventLocation = wtforms.StringField("Event location",default='')
        userMD_description = wtforms.StringField("Description",default='')
        userMD_nameSubjects = wtforms.StringField("Name subjects",default='')
        userMD_topicalSubjects = wtforms.StringField("Topical subjects",default='')
        userMD_eventOrganizer = wtforms.StringField("Event organizer",default='')
        userMD_assetExternalSource = wtforms.StringField("Source (if not BAMPFA staff)",default='')
        userMD_copyrightStatement = wtforms.StringField("Copyright statement",default='')
        userMD_restrictionsOnUse = wtforms.StringField("Restrictions on use",default='')
        userMD_generation = wtforms.StringField("Generation",default='')
        userMD_platformOutlet = wtforms.StringField("Media platform or outlet",default='')
        userMD_editSequenceSettings = wtforms.StringField("Settings/framing of NLE sequence",default='')
        userMD_postProcessing = wtforms.SelectField("Raw or post processed",default='',choices=[('',''),('raw','Raw'),('processed','Post processed')])
        userMD_additionalCredits = wtforms.StringField("Additional credits",default='')
        userMD_exportPublishDate = wtforms.StringField("Date of export or publishing",default='')
        # userMD_ = wtforms.StringField("",default='')

class ObjectForm(FlaskForm):
	"""
	Fields for an individual object
	"""
	targetPath = wtforms.HiddenField('objectPath')
	targetBase = wtforms.HiddenField('objectBase')
	runIngest = wtforms.BooleanField('Ingest?',default='')
	#testselect = wtforms.SelectField("Raw or post processed",default='',choices=[('raw','Raw'),('processed','Post processed')])
	#doProres = wtforms.BooleanField("make prores?",default='')
	#proresToDave = wtforms.BooleanField("deliver prores to dave?",default='')
	doConcat = wtforms.BooleanField("Concatenate reels?",default='')
	metadataForm = wtforms.FormField(MetadataForm)
	#metadataFields = wtforms.FieldList(StringField('metadata1'))

class IngestForm(FlaskForm):
	'''
	General input form
	'''
	suchChoices = wtforms.HiddenField(default='default choices')
	user = wtforms.StringField('Please enter your email address:',validators=[DataRequired(), Email()])
	submit = wtforms.SubmitField('Submit')
