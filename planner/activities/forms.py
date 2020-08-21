from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class ActivityForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    link = StringField('Link URL')
    description = TextAreaField('Description', validators=[DataRequired()])
    category = StringField('Category', validators = [DataRequired()])
    # date_posted = 
    submit = SubmitField('Post')