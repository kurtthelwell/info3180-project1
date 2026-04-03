from app import db


class Property(db.Model):
    __tablename__ = 'properties'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=False)
    description = db.Column(db.Text, nullable=False)
    no_of_rooms = db.Column(db.String(10), nullable=False)
    no_of_bathrooms = db.Column(db.String(10), nullable=False)
    price = db.Column(db.String(50), nullable=False)
    property_type = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(256), nullable=False)
    photo = db.Column(db.String(256))

    def __repr__(self):
        return f'<Property {self.id}: {self.title}>'
