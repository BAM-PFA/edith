from flask_wtf import FlaskForm
import wtforms
from wtforms.validators import DataRequired, Email

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
        userMD_2_eventFullDate = wtforms.StringField("Full date of event",default='')
        userMD_2_eventLocation = wtforms.StringField("Event location",default='')
        userMD_2_eventOrganizer = wtforms.StringField("Event organizer",default='')
        userMD_2_eventRelatedExhibition = wtforms.StringField("Related exhibition",default='')
        userMD_2_eventSeries = wtforms.StringField("Event series",default='')
        userMD_2_eventTitle = wtforms.StringField("Event title",default='')
        userMD_2_eventYear = wtforms.StringField("Event year",default='')
        userMD_2_PFAfilmSeries = wtforms.StringField("Related PFA film series",default='')
        userMD_3_additionalCredits = wtforms.StringField("Additional credits",default='')
        userMD_3_assetExternalSource = wtforms.StringField("Source (if not BAMPFA staff)",default='')
        userMD_3_copyrightStatement = wtforms.StringField("Copyright statement",default='')
        userMD_3_description = wtforms.StringField("Description",default='')
        userMD_3_generation = wtforms.StringField("Generation",default='')
        userMD_3_nameSubjects = wtforms.StringField("Name subjects",default='')
        userMD_3_postProcessing = wtforms.SelectField("Raw or post processed",default='',choices=[('',''),('raw','Raw'),('processed','Post processed')])
        userMD_3_restrictionsOnUse = wtforms.StringField("Restrictions on use",default='')
        userMD_3_tags = wtforms.StringField("Tags (comma separated)",default='')
        userMD_3_title = wtforms.StringField("Main title of a work",default='')
        userMD_3_topicalSubjects = wtforms.StringField("Subject(s): Topics",default='')
        userMD_3_digitizedBornDigital = wtforms.SelectField("Digitized or Born-digital?",default='',choices=[('',''),('digitized','Digitized'),('born digital','Born-digital')])
        userMD_3_recordingDate = wtforms.StringField("Date of recording",default='')
        userMD_3_digitizer = wtforms.StringField("Name of digitizer",default='')
        userMD_3_locationOfRecording = wtforms.StringField("Location of recording or event",default='')
        userMD_3_speakerInterviewee = wtforms.StringField("Speaker/Interviewee",default='')
        userMD_3_filmTitleSubjects = wtforms.StringField("Subject(s): Film title(s)",default='')
        userMD_3_country = wtforms.StringField("Country of production",default='')
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
