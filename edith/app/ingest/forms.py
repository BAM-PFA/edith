from flask_wtf import FlaskForm
import wtforms
from wtforms.validators import DataRequired, Email

class MetadataForm(FlaskForm):
        '''
        Fields for additional metadata
        '''
        userMD_event_title = wtforms.StringField("Event title",default='')
        userMD_event_year = wtforms.StringField("Event year",default='')
        userMD_event_full_date = wtforms.StringField("Full date of event",default='')
        userMD_event_series = wtforms.StringField("Event series",default='')
        userMD_related_exhibition = wtforms.StringField("Related exhibition",default='')
        userMD_event_location = wtforms.StringField("Event location",default='')
        userMD_description = wtforms.StringField("Description",default='')
        userMD_name_subjects = wtforms.StringField("Name subjects",default='')
        userMD_topical_subjects = wtforms.StringField("Topical subjects",default='')
        userMD_event_organizer = wtforms.StringField("Event organizer",default='')
        userMD_external_source = wtforms.StringField("Source (if not BAMPFA staff)",default='')
        userMD_copyright_statement = wtforms.StringField("Copyright statement",default='')
        userMD_use_restrictions = wtforms.StringField("Restrictions on use",default='')
        userMD_generation = wtforms.StringField("Generation",default='')
        userMD_platform_outlet = wtforms.StringField("Media platform or outlet",default='')
        userMD_edit_sequence_settings = wtforms.StringField("Settings/framing of NLE sequence",default='')
        userMD_post_processing = wtforms.SelectField("Raw or post processed",default='',choices=[('',''),('raw','Raw'),('processed','Post processed')])
        userMD_additional_credits = wtforms.StringField("Additional credits",default='')
        userMD_export_publish_date = wtforms.StringField("Date of export or publishing",default='')
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
