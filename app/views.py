"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file contains the routes for your application.
"""

import os
import uuid
from app import app, db
from flask import render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from app.models import Property
from app.forms import PropertyForm


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")


@app.route('/properties/create', methods=['GET', 'POST'])
def create_property():
    """Display form to add a new property and handle submission."""
    form = PropertyForm()
    if form.validate_on_submit():
        # Save the uploaded photo
        photo_file = form.photo.data
        ext = os.path.splitext(secure_filename(photo_file.filename))[1]
        unique_filename = f"{uuid.uuid4().hex}{ext}"
        upload_folder = app.config['UPLOAD_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)
        photo_file.save(os.path.join(upload_folder, unique_filename))

        # Create the property record
        new_property = Property(
            title=form.title.data,
            description=form.description.data,
            no_of_rooms=form.no_of_rooms.data,
            no_of_bathrooms=form.no_of_bathrooms.data,
            price=form.price.data,
            property_type=form.property_type.data,
            location=form.location.data,
            photo=unique_filename
        )
        db.session.add(new_property)
        db.session.commit()
        flash('Property was successfully added!', 'success')
        return redirect(url_for('list_properties'))

    return render_template('property_create.html', form=form)


@app.route('/properties')
def list_properties():
    """Display a list of all properties."""
    properties = Property.query.all()
    return render_template('properties.html', properties=properties)


@app.route('/properties/<int:propertyid>')
def view_property(propertyid):
    """Display an individual property."""
    prop = Property.query.get_or_404(propertyid)
    return render_template('property_view.html', property=prop)


###
# The functions below should be applicable to all Flask apps.
###

@app.template_filter('currency')
def format_currency(value):
    try:
        # Remove existing $, commas, spaces
        clean_value = str(value).replace('$', '').replace(',', '').strip()
        num = float(clean_value)
        return "${:,.0f}".format(num)
    except (ValueError, TypeError):
        return value

# Display Flask WTF errors as Flash messages
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404
