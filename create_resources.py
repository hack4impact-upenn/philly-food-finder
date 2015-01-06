import csv 
from app import db
from app.models import *
from app.utils import *
from string import strip

def main():
	# Delete all existing food resources
	for food_resource in FoodResource.query.all():
		db.session.delete(food_resource)
		db.session.commit()

	with open('all_resources.csv', 'rU') as csvfile:
		spamreader = csv.reader(csvfile)
		for i, row in enumerate(spamreader):
			'''if i == 1:
				for j, item in enumerate(row):
					print str(j) + ": " + str(item) + "\n"'''
			if i >= 2: 
				# Extract food resource's location type.
				location_type = row[1] # Required.

				# Ignore any rows that don't have a food resource type.
				if location_type:

					# Create food resource's FoodResourceType.
					location_type = FoodResourceType.query \
						.filter_by(enum=location_type).first() 

					#print "row = " + str(i) + "\n"

					# Extract food resource's name.
					name = str(row[2]) # Required.
					required("name", name, i)

					# Extract food resource's address.
					address_line1 = str(row[3]) # Required.
					required("address_line1", address_line1, i)
					address_line2 = str(row[4]) # Optional.
					address_city = str(row[5]) # Required.
					required("address_city", address_city, i)
					address_state = str(row[6]) # Required.
					required("address_state", address_state, i)
					address_zip_code = str(row[7]) # Required.
					required("address_zip_code", address_zip_code, i)

					# Create food resource's Address.
					address = Address(
						line1=address_line1, 
						line2=address_line2,
						city=address_city,
						state=address_state,
						zip_code=address_zip_code)
					db.session.add(address)

					# Extract food resource's phone number.
					phone_numbers = []
					number = str(row[8])
					phone_number = PhoneNumber(number=number)
					phone_numbers.append(phone_number)
					db.session.add(phone_number)

					# Extract food resource's website.
					website = str(row[9])

					# Extract food resource's description.
					description = str(row[10])

					# Extract food resource's boolean characteristics.
					is_for_family_and_children = convert_string_to_boolean(str(row[11]))
					is_for_seniors = convert_string_to_boolean(str(row[12])) 
					is_wheelchair_accessible = convert_string_to_boolean(str(row[13]))
					is_accepts_snap = convert_string_to_boolean(str(row[14]))
					is_accepts_fmnp = convert_string_to_boolean(str(row[15]))
					is_accepts_philly_food_bucks = convert_string_to_boolean(str(row[16]))
					are_hours_available = convert_string_to_boolean(str(row[17]))

					# Extract the days on which the food resource is open.
					days_open = []
					for j in range(18, 25): # [18, 25)
						days_open.append(convert_string_to_boolean(str(row[j]))) 

					# Extract the food resource's hours of operation.
					daily_hours = []
					for j in range(25, 39): # [25, 39)
						time_string = str(row[j]).strip()
						if not time_string:
							daily_hours.append("")
						else:
							daily_hours.append(get_time_from_string(time_string))

					# Create food resource's timeslots.
					timeslots = []
					for j, day_is_open in enumerate(days_open):
						if day_is_open:
							opening_time_1 = daily_hours[j*2]
							closing_time_1 = daily_hours[j*2+1]
							if opening_time_1 and closing_time_1:
								if opening_time_1 >= closing_time_1:
									throw_exception("Opening time must be before closing time", i)
								timeslot = TimeSlot(
									day_of_week=j, 
									start_time=opening_time_1, 
									end_time=closing_time_1
								)
								db.session.add(timeslot)
								timeslots.append(timeslot)

					# Create food resource.
					food_resource = FoodResource(
						name = name, 
						phone_numbers = phone_numbers,
						url = website,
						description = description,
						food_resource_type = location_type,
						address = address,
						are_hours_available = are_hours_available,
						timeslots = timeslots,
						is_for_family_and_children = is_for_family_and_children,
						is_for_seniors = is_for_seniors,
						is_wheelchair_accessible = is_wheelchair_accessible,
						is_accepts_snap = is_accepts_snap
					)

					# Commit all database changes. 
					db.session.add(food_resource)
					db.session.commit()

def convert_string_to_boolean(row_slot):
	if row_slot == "Yes":
		return True
	return False

def required(field_name, field_val, row_index):
	field_val = field_val.strip()
	if not field_val:
		raise Exception("Error: " + field_name + " is a required field (row " \
			+ str(row_index) + ").\n")

def throw_exception(exception_text, row_index):
	raise Exception("Error: " + exception_text + " (row " + str(row_index) \
		+ "\n")

if __name__ == "__main__": 
	main()