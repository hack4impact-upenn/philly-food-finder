from app import db

class Address(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	line1 = db.Column(db.String(100))
	line2 = db.Column(db.String(100))
	city = db.Column(db.String(35))
	state = db.Column(db.String(2))
	zip_code = db.Column(db.String(5))
	resource_id = db.Column(db.Integer, db.ForeignKey('food_resource.id'))

class TimeSlot(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	day_of_week = db.Column(db.Integer)
	start_time = db.Column(db.Time)
	end_time = db.Column(db.Time)
	resource_id = db.Column(db.Integer, db.ForeignKey('food_resource.id'))

class FoodResource(db.Model):
	food_resource_type_enums = ('FARMERS_MARKET','MEALS_ON_WHEELS','FOOD_CUPBOARD','SHARE','SOUP_KITCHEN','WIC_OFFICE')
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(50))
	address = db.relationship('Address', backref='food_resource', lazy='select', uselist=False)
	phone = db.Column(db.String(35))
	timeslots = db.relationship('TimeSlot', backref='food_resource', lazy='select', uselist=True)
	description = db.Column(db.String(500))
	location_type = db.Column(db.Enum(*food_resource_type_enums))


