from app import db

class Address(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    line1 = db.Column(db.String(100))
    line2 = db.Column(db.String(100))
    city = db.Column(db.String(35))
    state = db.Column(db.String(2))
    zip_code = db.Column(db.String(5))

class Resource(db.Model):
	location_type_enums = ('FARMER_MARKET','MEALS_ON_WHEELS','FOOD_CUPBOARDS_LIST','SHARE','SOUP_KITCHEN','WIC_OFFICES')
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50))
    address = db.Column(Address)
    phone = db.Column(db.String(35))
    timeslot_0 = db.Column(TimeSlot)
    timeslot_1 = db.Column(TimeSlot)
    timeslot_2 = db.Column(TimeSlot)
    timeslot_3 = db.Column(TimeSlot)
    timeslot_4 = db.Column(TimeSlot)
    timeslot_5 = db.Column(TimeSlot)
    timeslot_6 = db.Column(TimeSlot)
    description = db.Column(db.String(500))
    location_type = db.Column(Enum(*location_type_enums))

class TimeSlot(db.Model):
	day_of_week = dbColumn(db.Ingeger)
	start_time = dbColumn(db.Time)
	end_time = dbColumn(db.Time)
