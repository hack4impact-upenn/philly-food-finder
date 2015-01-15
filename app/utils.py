import os, random, string, datetime
#from datetime import datetime, timedelta
#import datetime
from pytz import timezone
from models import *
import os, random, string
#from datetime import date
from pytz import timezone
from models import *
import re
import csv
from app import db

def getFilteredFoodResources(has_zip_code_filter, zip_code, has_open_now_filter, booleans_array):
	# Create empty arrays to hold food resources.
	all_resources = []
	food_resource_types = FoodResourceType.query \
		.order_by(FoodResourceType.name_plural).all()

	# Zip code is one of the filters.
	if has_zip_code_filter:

		# Iterate through all food resource types.
		for i, food_resource_type in enumerate(food_resource_types):

			# Filter for each kind of food resource with a specific zip code.
			all_resources.append([])
			get_food_resources_by_location_type_and_zip_code(
				all_resources[i], # List to populate.
				food_resource_type, # Location type by which to filter.
				zip_code # Zip code by which to filter.
			)

	# Zip code is not one of the filters. 
	else: 

		# Iterate through all food resource types.
		for i, food_resource_type in enumerate(food_resource_types):

			# Filter for each kind of food resource without a specific zip code.
			all_resources.append([])
			get_food_resources_by_location_type(
				all_resources[i], # List to populate.
				food_resource_type # Location type by which to filter.
			)

	# Filter each list by other boolean criteria.
	for list_to_filter in all_resources:
		filter_food_resources(list_to_filter, has_open_now_filter, 
			booleans_array)

	return all_resources

def get_first_day_of_month(day):
	return datetime.date(day.year, day.month, 1)

def get_last_day_of_previous_month(day):
	first = get_first_day_of_month(day)
	last = first - datetime.timedelta(days=1)
	return last

def get_first_day_of_previous_month(day):
	last = get_last_day_of_previous_month(day)
	return get_first_day_of_month(last)

def get_food_resource_booleans():
	booleans = []
	booleans.append(FoodResourceBoolean(
		description_question="Requires a photo ID?", 
		description_statement="Does this food resource require a photo ID?"
	))
	booleans.append(FoodResourceBoolean(
		description_question="Requires proof of address?", 
		description_statement="Does this food resource require proof of address?"
	))
	booleans.append(FoodResourceBoolean(
		description_question="Requires proof of income?", 
		description_statement="Does this food resource require proof of income?"
    ))
	booleans.append(FoodResourceBoolean(
		description_question="Requires a Social Security card?", 
		description_statement="Does this food resource require a Social Security card?"
	))
	booleans.append(FoodResourceBoolean(
		description_question="Requires a referral?", 
		description_statement="Does this food resource require a referral?"
    ))
	booleans.append(FoodResourceBoolean(
		description_question="Accepts SNAP?", 
		description_statement="Does this food resource accept SNAP?"
	))
	booleans.append(FoodResourceBoolean(
		description_question="Accepts FMNP Vouchers?", 
		description_statement="Does this food resource accept FMNP Vouchers?"
	))
	booleans.append(FoodResourceBoolean(
		description_question="Accepts Philly Food Bucks?", 
		description_statement="Does this food resource accept Philly Food Bucks?"
		))
	booleans.append(FoodResourceBoolean(
		description_question="Wheelchair accessible?", 
		description_statement="Is this food resource wheelchair accessible?"
	))
	# Add any new booleans to END of list.
	return booleans

def create_food_resource_from_form(form, additional_errors):
	food_resource_type = form.location_type.data
	all_timeslots = []

	if form.are_hours_available.data == "yes":
		are_hours_available = True
	else:
		are_hours_available = False

	# Create the food resource's timeslots.
	num_timeslots_checked_per_day = [0] * 7
	are_timeslots_valid = True
	if are_hours_available: 
		for i, timeslots in enumerate(form.daily_timeslots):
			for timeslot in timeslots.timeslots:
				# Check if food resource is open on the i-th day of the 
				# week.
				is_open = True
				if form.is_open[i].is_open.data == "closed":
					is_open = False

				# Check if all relevant timeslots have already been checked
				are_all_timeslots_checked = False
				day_of_week_index = i
				if num_timeslots_checked_per_day[day_of_week_index] == \
					int(form.daily_timeslots[day_of_week_index] \
						.num_timeslots.data):
					are_all_timeslots_checked = True

				# Create timeslots only if the food resource is open on the
				# i-th day of the week.
				if is_open and not are_all_timeslots_checked:
					num_timeslots_checked_per_day[day_of_week_index] += 1
					start_time = \
						get_time_from_string(timeslot.starts_at.data)
					end_time = get_time_from_string(timeslot.ends_at.data)
					timeslot = TimeSlot(day_of_week=i, 
						start_time=start_time, end_time=end_time)
					all_timeslots.append(timeslot)

					# Check that timeslot is valid.
					if start_time >= end_time: 
						are_timeslots_valid = False
						additional_errors.append("Opening time must be \
							before closing time.")
					else:
						db.session.add(timeslot)

	# Create the food resource's remaining attributes. 
	if are_timeslots_valid:

		# Create food resource's address.
		address = Address(line1=form.address_line1.data, 
			line2=form.address_line2.data, 
			city=form.address_city.data, 
			state=form.address_state.data, 
			zip_code=form.address_zip_code.data)
		address.createLatAndLong()
		db.session.add(address)

		# Create food resource's phone number.
		phone_numbers = []
		home_number = PhoneNumber(number=form.phone_number.data)
		db.session.add(home_number)
		phone_numbers.append(home_number)

		# Create food resource's type.
		enum = form.location_type.data
		food_resource_type = FoodResourceType.query.filter_by(enum=enum) \
			.first()

		# Create food resource and store all data in it.
		food_resource = FoodResource()
		food_resource.name = form.name.data
		food_resource.phone_numbers = phone_numbers
		food_resource.description = form.additional_information.data
		food_resource.timeslots = all_timeslots
		food_resource.address = address
		food_resource.are_hours_available = are_hours_available
		food_resource.food_resource_type = food_resource_type
		form_booleans = form.get_booleans()
		for food_resource_boolean in food_resource.booleans:
			for key, value in form_booleans.iteritems():
				if food_resource_boolean.hyphenated_id == key:
					food_resource_boolean.value = value
					db.session.add(food_resource_boolean)
		return food_resource

def get_string_of_all_food_resource_types():
	possible_types_text = ""
	food_resource_types = FoodResourceType.query.all()
	# There is 1 food resource type.
	if len(food_resource_types) == 1:
		possible_types_text = food_resource_types[0].enum
	# There are 2 food resource types.
	elif len(food_resource_types) == 2:
		possible_types_text = food_resource_types[0].enum + " or " \
			+ food_resource_types[1].enum
	# There are 3 or more food resource types.
	else:
		for i, food_resource_type in enumerate(food_resource_types):
			# Last item in the list.
			if (i == len(food_resource_types) - 1):
				possible_types_text += food_resource_type.enum
			# Second-to-last item in list.
			elif (i == len(food_resource_types) - 2):
				possible_types_text += food_resource_type.enum + ", or "
			# All other items in list.
			else:
				possible_types_text += food_resource_type.enum + ", "
	return possible_types_text

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
	return datetime.time(time_hour, time_minute)

def is_open(resource, current_date = None):
	timeslots = resource.timeslots

	if(current_date is None):
		eastern = timezone('US/Eastern')
		current_date = datetime.now(eastern)

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

	if(len(today_timeslot_list) == 0): # This means it must be closed all day today
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
	opening_time = datetime.datetime( 
		year=2014, 	# Arbitrary.
		month=1, 	# Arbitrary.
		day=1,		# Arbitrary.
		hour=0, 	# First opening time is 12:00 AM.
		minute=0)
	final_opening_time = datetime.datetime( 
		year=2014,	# Arbitrary.
		month=1, 	# Arbitrary.
		day=2,		# Arbitrary.
		hour=0,		# Final opening time is 11:45 PM.
		minute=0)
	while opening_time != final_opening_time:
		opening_times.append(
			(
				opening_time.time().strftime("%H:%M"), # 8:00 AM or 1:OO PM
				opening_time.time().strftime("%I:%M %p") # 8:00 or 13:00
			)
		)
		# Opening time is incremented in 15-minute intervals.
		opening_time += datetime.timedelta(0, 15*60) # Number of seconds in 15 minutes.
	return opening_times

def get_possible_closing_times():
	closing_times = []
	# Year, month, and day are arbitrary, as only the time is needed.
	closing_time = datetime.datetime( 
		year=2014, 	# Arbitrary.
		month=1, 	# Arbitrary.
		day=1,		# Arbitrary.
		hour=0, 	# First closing time is 12:00 AM.
		minute=0)
	final_closing_time = datetime.datetime( 
		year=2014,	# Arbitrary.
		month=1, 	# Arbitrary.
		day=2,		# Arbitrary.
		hour=0,		# Final closing time is 11:45 PM.
		minute=0)
	while closing_time != final_closing_time:
		closing_times.append(
			(
				closing_time.time().strftime("%H:%M"), # 8:00 AM or 1:OO PM
				closing_time.time().strftime("%I:%M %p") # 8:00 or 13:00
			)
		)
		# Closing time is incremented in 15-minute intervals.
		closing_time += datetime.timedelta(0, 15*60) # Number of seconds in 15 minutes.
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

def filter_food_resources(list_to_filter, has_open_now_filter, booleans_array):
	for food_resource in list(list_to_filter):
		for i, boolean in enumerate(booleans_array):
			if boolean == True and food_resource.booleans[i].value == False:
				if food_resource in list_to_filter:
					list_to_filter.remove(food_resource)
		if food_resource in list_to_filter and has_open_now_filter and not \
			is_open(food_resource):
			list_to_filter.remove(food_resource)

def import_file(path, charset='utf-8'):

	# If there are errors, they will be returned to the user.
	errors = []

	# Helper functions
	def convert_string_to_boolean(row_slot, row_index):
		if row_slot == "Yes":
			return True
		elif row_slot is None or row_slot == "":
			return False
		else:
			make_error('\'' + str(row_slot) + '\' is invalid. Please put \'Yes\' or leave blank.', row_index)
			return False # To prevent program from breaking too early

	def required(field_name, field_val, row_index):
		field_val = field_val.strip()
		if not field_val:
			errors.append("'" + str(field_name) + "' is a required field (row " \
				+ str(row_index) + ").")

	def make_error(exception_text, row_index):
		errors.append(str(exception_text) + " (row " + str(row_index) + ").")

	def check_length(field_name, field_val, length, row_index):
		field_val = field_val.strip()
		if field_val and len(field_val) > length:
			errors.append(str(field_val) + " is longer than the max length of " \
				+ str(length) + " characters (row " + str(row_index) + ").")

	def check_time_format(field_val, row_index):
		check = re.compile('^\d{1,2}:\d{2}$')
		if check.match(field_val) is None:
			errors.append(str(field_val) + " is not a proper time format. Please " \
				+ "use military time - e.g., 8:00 or 17:00. (row " + str(row_index) + ").")
			return False
		colon_index = field_val.index(":")
		hours = int(field_val[0:colon_index])
		if hours < 0 or hours > 23:
			errors.append(str(field_val) + " has an invalid hour number. A \
				valid hour number is between 0 and 23. (row " + \
				str(row_index) + ").")
			return False
		minutes = int(field_val[colon_index+1:])
		if minutes < 0 or minutes > 59 or minutes % 15 != 0:
			errors.append(str(field_val) + " has an invalid minute number. A \
				valid minute number is either 0, 15, 30, or 45. (row " + \
				str(row_index) + ").")
			return False
		return True

	def decode_string(s, field_name, row_index):
		new = ""
		try:
			new = str(s).decode(charset)
		except Exception as e:
			make_error("The field '" + field_name + "' cannot be decoded. \
				To fix this problem, try retyping the contents of this field. \
				A common culprit for this kind of error is the aprostraphe \
				('). Make sure that all of your apostraphes are perfectly \
				vertically straight rather than curly. (Yes, these are \
				different characters.)", i)
		return new


	with open(path, 'rU') as csvfile:

		spamreader = csv.reader(csvfile)
		for i, row in enumerate(spamreader):
			if row:
				if i >= 2: 
					# Extract food resource's location type.
					location_type_table = decode_string(row[1], "location_type", i) # Required.

					# Extract food resource's name.
					name = decode_string(row[2], "name", i) # Required.			

					# If a row contains either a location type or a name, then the row will be 
					# analyzed for validity.
					if len(location_type_table.strip()) > 0 or len(name.strip()) > 0:
						
						# Verify that name and location type are valid.
						required("location_type", location_type_table, i)
						required("name", name, i)
						check_length("name", name, 100, i)

						# Create food resource's FoodResourceType.
						location_type = FoodResourceType.query \
							.filter_by(enum=location_type_table).first() 

						if location_type is None and location_type_table is not None:
							make_error('The location_type ' + location_type_table + ' is invalid', i)

						# Extract food resource's address.
						address_line1 = decode_string(row[3], "address_line1", i) # Required.
						required("address_line1", address_line1, i)
						check_length("address_line1", address_line1, 100, i)

						address_line2 = decode_string(row[4], "address_line2", i) # Optional.
						check_length("address_line2", address_line2, 100, i)

						address_city = decode_string(row[5], "address_city", i) # Required.
						required("address_city", address_city, i)
						check_length("address_city", address_city, 35, i)

						address_state = decode_string(row[6], "address_state", i) # Required.
						required("address_state", address_state, i)
						check_length("address_state", address_state, 2, i)

						address_zip_code = decode_string(row[7], "address_zip_code", i) # Required.
						required("address_zip_code", address_zip_code, i)

						# Ensures zip_code is exactly 5 digits.
						zip_code_strip = address_zip_code.strip()
						if zip_code_strip and len(zip_code_strip) is not 5:
							make_error('The zip_code ' + str(zip_code_strip) + ' is not the right length. \
								Please ensure that it is 5 digits.', i)

						# Create food resource's Address.
						address = Address(
							line1=address_line1, 
							line2=address_line2,
							city=address_city,
							state=address_state,
							zip_code=address_zip_code)
						address.createLatAndLong()
						db.session.add(address)

						# Extract food resource's phone number.
						phone_numbers = []
						number = decode_string(row[8], "phone_number", i)
						check_length("phone_number", number, 35, i)

						phone_number = PhoneNumber(number=number)
						phone_numbers.append(phone_number)
						db.session.add(phone_number)

						# Extract food resource's website.
						website = decode_string(row[9], "website", i)

						# Extract food resource's description.
						description = decode_string(row[10], "description", i)

						# Extract food resource's boolean characteristics.
						row_num = 11
						booleans = []
						food_resource_booleans = get_food_resource_booleans()
						for food_resource_boolean in food_resource_booleans:
							booleans.append(convert_string_to_boolean(str(row[row_num]), i))
							row_num += 1

						are_hours_available = convert_string_to_boolean(str(row[row_num]), i)
						row_num += 1

						# Extract the days on which the food resource is open.
						days_open = []
						first_day_open_column = row_num
						row_num += 7
						last_day_open_column = row_num
						for j in range(first_day_open_column, last_day_open_column): 
							days_open.append(convert_string_to_boolean(str(row[j]), i)) 

						# Extract the food resource's hours of operation.
						all_daily_hours = [None] * 7
						for j in range(0, 7):
							all_daily_hours[j] = []
						are_all_times_valid = True
						first_time_column = row_num
						row_num += 140
						last_time_column = row_num
						for j in range(first_time_column, last_time_column):
							time_string = str(row[j]).strip()
							day_of_week = (j - first_time_column) / 20
							if not time_string:
								all_daily_hours[day_of_week].append("")
							else:
								if check_time_format(time_string, i):
									all_daily_hours[day_of_week].append(get_time_from_string(time_string))
								else:
									are_all_times_valid = False

						# Create food resource's timeslots.
						timeslots = []
						if are_all_times_valid:
							# Iterate through all day of the week.
							for j, daily_hours in enumerate(all_daily_hours):
								if days_open[j]:
									# Iterate through 10 possible timeslots per day.
									for k in range(0, 10):
										opening_time = daily_hours[k*2]
										closing_time = daily_hours[k*2+1]
										if opening_time and closing_time:
											if opening_time >= closing_time:
												make_error("Opening time (" + \
													str(opening_time.strftime('%H:%M')) + \
													") must be before closing time (" + \
													str(closing_time.strftime('%H:%M')) + 
													")", i)
											timeslot = TimeSlot(
												day_of_week=j, 
												start_time=opening_time, 
												end_time=closing_time
											)
											db.session.add(timeslot)
											timeslots.append(timeslot)

						# Checks database to see if identical resource exists
						duplicate = db.session.query(FoodResource) \
							.join(FoodResource.address) \
							.filter(
								FoodResource.name==name, 
								FoodResource.url==website, 
								FoodResource.description==description,
								Address.line1==address_line1,
								Address.line2==address_line2,
								Address.city==address_city,
								Address.state==address_state,
								Address.zip_code==address_zip_code
								).first()

						if duplicate:
							make_error("Identical resource (" + 
								duplicate.name + ") already exists in database. \
							It may be either an approved food resource, a \
							pending food resource, or a food resource that's \
							in this spreadsheet.", i)

						# Create food resource.
						food_resource = FoodResource()
						food_resource.name = name
						food_resource.phone_numbers = phone_numbers
						food_resource.url = website
						food_resource.description = description
						food_resource.food_resource_type = location_type
						food_resource.address = address
						food_resource.are_hours_available = are_hours_available
						food_resource.timeslots = timeslots
						for j, boolean in enumerate(food_resource.booleans):
							boolean.value = booleans[j]

						# Stage database changes. 
						db.session.add(food_resource)
				
	# Commits only after completing iteration and if no errors
	if len(errors) is 0:
		db.session.commit()
		return None
	else:
		return errors