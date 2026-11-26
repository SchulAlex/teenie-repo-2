from flask_wtf import FlaskForm
<<<<<<< HEAD
from flask_wtf.file import FileAllowed, FileField
=======
>>>>>>> 2e30b332e272c2b4ba395f0b61e71434b00f2dfb
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, ValidationError


<<<<<<< HEAD
IMAGE_EXTENSIONS = ['jpg', 'jpeg', 'png', 'gif', 'webp']


=======
>>>>>>> 2e30b332e272c2b4ba395f0b61e71434b00f2dfb
class StoryForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=100)])
    author = StringField('Your name (optional)', validators=[Optional(), Length(max=100)])
    content = TextAreaField('Content', validators=[DataRequired()])
<<<<<<< HEAD
    image = FileField('Picture (optional, max. 5 MB)',
                      validators=[Optional(), FileAllowed(IMAGE_EXTENSIONS, 'Only JPG, PNG, GIF or WEBP images are allowed.')])
=======
>>>>>>> 2e30b332e272c2b4ba395f0b61e71434b00f2dfb
    submit = SubmitField('Submit')


class PollForm(FlaskForm):
    question = StringField('Question', validators=[DataRequired(), Length(max=200)])
    options = StringField('Options (comma separated)', validators=[DataRequired()])
<<<<<<< HEAD
    image = FileField('Picture (optional, max. 5 MB)',
                      validators=[Optional(), FileAllowed(IMAGE_EXTENSIONS, 'Only JPG, PNG, GIF or WEBP images are allowed.')])
=======
>>>>>>> 2e30b332e272c2b4ba395f0b61e71434b00f2dfb
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
