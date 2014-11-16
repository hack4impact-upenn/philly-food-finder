import os, random, string
from datetime import time

# Function to generate a random password of given length 
def generate_password(length):
	chars = string.ascii_letters + string.digits + '!@#$%&'
	random.seed = (os.urandom(1024))
	return ''.join(random.choice(chars) for i in range(length-2)) + '1A'

# Takes strings of the form '8-00-am' or '1-15-pm' and returns an equivalent 
# time object
def get_time(time_string):
	first_dash = time_string.index("-")
	second_dash = time_string.index("-", first_dash+1)
	time_hour = int(time_string[:first_dash])
	time_minute = int(time_string[first_dash+1:second_dash])
	am_or_pm = time_string[second_dash+1:]
	if (am_or_pm == "pm" and time_hour != 12):
		time_hour += 12
	return time(time_hour, time_minute)
