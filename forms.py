from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateTimeLocalField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Length

class EventForm(FlaskForm):
    title = StringField('Event Title', validators=[DataRequired(), Length(max=200)])
    start_time = DateTimeLocalField('Start Time', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    end_time = DateTimeLocalField('End Time', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    description = TextAreaField('Description')

class ResourceForm(FlaskForm):
    resource_name = StringField('Resource Name', validators=[DataRequired(), Length(max=200)])
    resource_type = SelectField('Resource Type', choices=[
        ('room', 'Room'),
        ('instructor', 'Instructor'),
        ('equipment', 'Equipment'),
        ('other', 'Other')
    ], validators=[DataRequired()])

class AllocationForm(FlaskForm):
    event_id = SelectField('Event', coerce=int, validators=[DataRequired()])
    resource_ids = SelectMultipleField('Resources', coerce=int, validators=[DataRequired()])

class ReportForm(FlaskForm):
    start_date = DateTimeLocalField('Start Date', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    end_date = DateTimeLocalField('End Date', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
