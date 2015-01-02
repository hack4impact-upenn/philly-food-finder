import os, random, string, datetime
from datetime import time, datetime, timedelta
from pytz import timezone
from models import *
import os, random, string
from datetime import time
from pytz import timezone
from models import *
import re
import csv

def get_underscored_string(string_to_convert):
	string = string_to_convert.lower().replace(" ", "_")
	string = re.sub(r'[^a-zA-Z0-9_]','', string)
	return string 

def get_hyphenated_string(string_to_convert):
	string = string_to_convert.lower().replace(" ", "-")
	string = re.sub(r'[^a-zA-Z0-9\-]','', string)
	return string 

def get_enum(string_to_convert):
	return get_underscored_string(string_to_convert).upper()

# Function to generate a random password of given length 
def generate_password(length):
	chars = string.ascii_letters + string.digits + '!@#$%&'
	random.seed = (os.urandom(1024))
	return ''.join(random.choice(chars) for i in range(length-2)) + '1A'

# Takes strings of the form '08:00' or '17:30' and returns an equivalent 
# time object
def get_time_from_string(time_string):
	colon_index = time_string.index(":")
	time_hour = int(time_string[:colon_index])
	time_minute = int(time_string[colon_index+1:])
	return time(time_hour, time_minute)

def is_open(resource, current_date = None):
	month_pairs = resource.open_month_pairs
	timeslots = resource.timeslots

	if(current_date is None):
		eastern = timezone('US/Eastern')
		current_date = datetime.now(eastern)
	
	pair_bool = False
	for pair in month_pairs:
		start_month = pair.start_month
		end_month = pair.end_month
		pair_bool = pair_bool or (current_date.month <= end_month and current_date.month >= start_month)

	if(not pair_bool):
		return False

	weekday = 0
	if current_date.weekday() == 0:
		weekday = 1
	if current_date.weekday() == 1:
		weekday = 2
	if current_date.weekday() == 2:
		weekday = 3
	if current_date.weekday() == 3:
		weekday = 4
	if current_date.weekday() == 5:
		weekday = 6
	if current_date.weekday() == 6:
		weekday = 0

	today_timeslot_list = [slot for slot in timeslots if slot.day_of_week == weekday]

	if(len(today_timeslot_list) == 0): #This means it must be closed all day today
		return False
	else:
		today_timeslot = today_timeslot_list[0]
		time = current_date.time()
		if(time < today_timeslot.start_time or time > today_timeslot.end_time):
			return False

	return True

def get_possible_opening_times():
	opening_times = []
	# Year, month, and day are arbitrary, as only the time is needed.
	opening_time = datetime( 
		year=2014, 	# Arbitrary.
		month=1, 	# Arbitrary.
		day=1,		# Arbitrary.
		hour=7, 	# First opening time is 7:00 AM.
		minute=0)
	final_opening_time = datetime( 
		year=2014,	# Arbitrary.
		month=1, 	# Arbitrary.
		day=1,		# Arbitrary.
		hour=17,	# Final opening time is 5:00 PM.
		minute=0)
	while opening_time != final_opening_time:
		opening_times.append(
			(
				opening_time.time().strftime("%H:%M"), # 8:00 AM or 1:OO PM
				opening_time.time().strftime("%I:%M %p") # 8:00 or 13:00
			)
		)
		# Opening time is incremented in 15-minute intervals.
		opening_time += timedelta(0, 15*60) # Number of seconds in 15 minutes.
	return opening_times

def get_possible_closing_times():
	closing_times = []
	# Year, month, and day are arbitrary, as only the time is needed.
	closing_time = datetime( 
		year=2014, 	# Arbitrary.
		month=1, 	# Arbitrary.
		day=1,		# Arbitrary.
		hour=11, 	# First closing time is 11:00 AM.
		minute=0)
	final_closing_time = datetime( 
		year=2014,	# Arbitrary.
		month=1, 	# Arbitrary.
		day=1,		# Arbitrary.
		hour=21,	# Final closing time is 9:00 PM.
		minute=0)
	while closing_time != final_closing_time:
		closing_times.append(
			(
				closing_time.time().strftime("%H:%M"), # 8:00 AM or 1:OO PM
				closing_time.time().strftime("%I:%M %p") # 8:00 or 13:00
			)
		)
		# Closing time is incremented in 15-minute intervals.
		closing_time += timedelta(0, 15*60) # Number of seconds in 15 minutes.
	return closing_times

def get_food_resources_by_location_type(list_to_populate, location_type):
	for food_resource in db.session.query(FoodResource) \
		.join(FoodResource.address) \
		.filter(
			FoodResource.food_resource_type==location_type,
			FoodResource.is_approved==True) \
		.order_by(FoodResource.name).all():
		list_to_populate.append(food_resource)

def get_food_resources_by_location_type_and_zip_code(list_to_populate, 
	location_type, 
	zip_code):
	for food_resource in db.session.query(FoodResource) \
		.join(FoodResource.address) \
		.filter(
			Address.zip_code==zip_code,
			FoodResource.food_resource_type==location_type,
			FoodResource.is_approved==True) \
		.order_by(FoodResource.name).all():
		list_to_populate.append(food_resource)

def filter_food_resources(list_to_filter, has_families_and_children_filter, 
	has_seniors_filter, has_wheelchair_accessible_filter,
	has_accepts_snap_filter):
	for food_resource in list(list_to_filter):
		if has_families_and_children_filter and \
			food_resource.is_for_family_and_children == False:
			list_to_filter.remove(food_resource)
		elif has_seniors_filter and \
			food_resource.is_for_seniors == False:
			list_to_filter.remove(food_resource)
		elif has_wheelchair_accessible_filter and \
			food_resource.is_wheelchair_accessible == False:
			list_to_filter.remove(food_resource)
		elif has_accepts_snap_filter and \
			food_resource.is_accepts_snap == False:
			list_to_filter.remove(food_resource)

def import_file(file):

	# Helper functions
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

	with open(file.filename, 'rU') as csvfile:
	#with file.stream as csvfile:

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
				
				# Commits only after completing iteration
				db.session.commit()