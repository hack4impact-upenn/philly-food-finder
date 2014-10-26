from app import db

class Address(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	line1 = db.Column(db.String(100))
	line2 = db.Column(db.String(100))
	city = db.Column(db.String(35))
	state = db.Column(db.String(2))
	zip_code = db.Column(db.String(5))
	resource_id = db.Column(db.Integer, db.ForeignKey('resource.id'))

class TimeSlot(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	day_of_week = db.Column(db.Integer)
	start_time = db.Column(db.Time)
	end_time = db.Column(db.Time)
	resource_id = db.Column(db.Integer, db.ForeignKey('resource.id'))

class Resource(db.Model):
	location_type_enums = ('FARMER_MARKET','MEALS_ON_WHEELS','FOOD_CUPBOARDS_LIST','SHARE','SOUP_KITCHEN','WIC_OFFICES')
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(50))
	address = db.relationship('Address', backref='resource', lazy='select', uselist=False)
	phone = db.Column(db.String(35))
	timeslots = db.relationship('TimeSlot', backref='resource', lazy='select', uselist=True)
	description = db.Column(db.String(500))
	location_type = db.Column(db.Enum(*location_type_enums))


