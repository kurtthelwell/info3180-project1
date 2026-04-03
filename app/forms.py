from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, TextAreaField, SelectField
from wtforms.validators import DataRequired

# Add New Property Form
class PropertyForm(FlaskForm):
    title = StringField('Property Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    no_of_rooms = StringField('No. of Bedrooms', validators=[DataRequired()])
    no_of_bathrooms = StringField('No. of Bathrooms', validators=[DataRequired()])
    price = StringField('Price', validators=[DataRequired()])
    property_type = SelectField(
        'Property Type',
        choices=[('House', 'House'), ('Apartment', 'Apartment')],
        validators=[DataRequired()]
    )
    location = StringField('Location', validators=[DataRequired()])
    photo = FileField(
        'Photo',
        validators=[
            FileRequired(),
            FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')
        ]
    )
