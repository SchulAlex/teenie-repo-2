from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, ValidationError


IMAGE_EXTENSIONS = ['jpg', 'jpeg', 'png', 'gif', 'webp']


class StoryForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=100)])
    author = StringField('Your name (optional)', validators=[Optional(), Length(max=100)])
    content = TextAreaField('Content', validators=[DataRequired()])
    image = FileField('Picture (optional, max. 5 MB)',
                      validators=[Optional(), FileAllowed(IMAGE_EXTENSIONS, 'Only JPG, PNG, GIF or WEBP images are allowed.')])
    submit = SubmitField('Submit')


class PollForm(FlaskForm):
    question = StringField('Question', validators=[DataRequired(), Length(max=200)])
    options = StringField('Options (comma separated)', validators=[DataRequired()])
    image = FileField('Picture (optional, max. 5 MB)',
                      validators=[Optional(), FileAllowed(IMAGE_EXTENSIONS, 'Only JPG, PNG, GIF or WEBP images are allowed.')])
    submit = SubmitField('Create Poll')

    def validate_options(self, field):
        options = self.parsed_options(field.data)
        if len(options) < 2:
            raise ValidationError('Please enter at least two options, separated by commas.')
        if any(len(o) > 100 for o in options):
            raise ValidationError('Each option may have at most 100 characters.')

    @staticmethod
    def parsed_options(raw):
        return [o.strip() for o in (raw or '').split(',') if o.strip()]


class FeedbackForm(FlaskForm):
    name = StringField('Your Name', validators=[Length(max=50)])
    feedback = TextAreaField('Feedback', validators=[DataRequired()])
    submit = SubmitField('Send Feedback')
