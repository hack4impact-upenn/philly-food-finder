# Necessary set-up.
from app import db
from app.models import Address, User, TimeSlot, FoodResource
from datetime import time

# Drop all database tables.
db.drop_all()

# Create new database tables.
db.create_all()

# Create a Farmers' Market FoodResource.
f0 = FoodResource() 
f0.name = "Clark Park"
f0.phone_number = "123-456-7890"
f0.description = "Open year round"
f0.location_type = "FARMERS_MARKET"
a0 = Address()
a0.line1 = "43rd Street and Baltimore Avenue"
a0.city = "Philadelphia"
a0.state = "PA"
a0.zip_code = "19104"
f0.address = a0
timeslots_list_0 = \
    [TimeSlot(day_of_week = 0, start_time = time(8,0), 
        end_time = time(18,30)),
    TimeSlot(day_of_week = 1, start_time = time(7,0), 
        end_time = time(19,30)),
    TimeSlot(day_of_week = 2, start_time = time(7,30), 
        end_time = time(18,30)),
    TimeSlot(day_of_week = 3, start_time = time(8,0), 
        end_time = time(19,30)),
    TimeSlot(day_of_week = 4, start_time = time(10,0), 
        end_time = time(5,30)),
    TimeSlot(day_of_week = 5, start_time = time(8,15), 
        end_time = time(18,45)),
    TimeSlot(day_of_week = 6, start_time = time(9,0), 
        end_time = time(20,45))]
f0.timeslots = timeslots_list_0

# Add each new object to session and commit session. 
db.session.add(f0)
db.session.add(a0)
for timeslot in timeslots_list_0:
	db.session.add(timeslot)
db.session.commit()

# Create a Meals On Wheels FoodResource.
f1 = FoodResource() 
f1.name = "Northeast Meals On Wheels"
f1.phone_number = "888-888-8888"
f1.description = "Fresh fruit and veggies!"
f1.location_type = "MEALS_ON_WHEELS"
a1 = Address()
a1.line1 = "6500 Tabor Ave"
a1.city = "Philadelphia"
a1.state = "PA"
a1.zip_code = "19111"
f1.address = a1
timeslots_list_1 = \
    [TimeSlot(day_of_week = 0, start_time = time(8,0), 
        end_time = time(18,30)),
    TimeSlot(day_of_week = 1, start_time = time(7,0), 
        end_time = time(19,30)),
    TimeSlot(day_of_week = 2, start_time = time(7,30), 
        end_time = time(18,30)),
    TimeSlot(day_of_week = 3, start_time = time(8,0), 
        end_time = time(19,30)),
    TimeSlot(day_of_week = 4, start_time = time(10,0), 
        end_time = time(5,30)),
    TimeSlot(day_of_week = 5, start_time = time(8,15), 
        end_time = time(18,45)),
    TimeSlot(day_of_week = 6, start_time = time(9,0), 
        end_time = time(20,45))]
f1.timeslots = timeslots_list_1

# Add each new object to session and commit session. 
db.session.add(f1)
db.session.add(a1)
for timeslot in timeslots_list_1:
	db.session.add(timeslot)
db.session.commit()

# Create a Food Cupboard FoodResource.
f2 = FoodResource() 
f2.name = "Sample Food Cupboard"
f2.phone_number = "777-777-7777"
f2.description = "Food cupboard description"
f2.location_type = "FOOD_CUPBOARD"
a2 = Address()
a2.line1 = "1000 Locust St"
a2.city = "Philadelphia"
a2.state = "PA"
a2.zip_code = "19107"
f2.address = a2
timeslots_list_2 = \
    [TimeSlot(day_of_week = 0, start_time = time(8,0), 
        end_time = time(18,30)),
    TimeSlot(day_of_week = 1, start_time = time(7,0), 
        end_time = time(19,30)),
    TimeSlot(day_of_week = 2, start_time = time(7,30), 
        end_time = time(18,30)),
    TimeSlot(day_of_week = 3, start_time = time(8,0), 
        end_time = time(19,30)),
    TimeSlot(day_of_week = 4, start_time = time(10,0), 
        end_time = time(5,30)),
    TimeSlot(day_of_week = 5, start_time = time(8,15), 
        end_time = time(18,45)),
    TimeSlot(day_of_week = 6, start_time = time(9,0), 
        end_time = time(20,45))]
f2.timeslots = timeslots_list_2

# Add each new object to session and commit session. 
db.session.add(f2)
db.session.add(a2)
for timeslot in timeslots_list_2:
	db.session.add(timeslot)
db.session.commit()

# Create a SHARE Food Site FoodResource.
f3 = FoodResource() 
f3.name = "Sample SHARE Food Site"
f3.phone_number = "193-538-2842"
f3.description = "A description"
f3.location_type = "SHARE"
a3 = Address()
a3.line1 = "1610 Sansom St"
a3.city = "Philadelphia"
a3.state = "PA"
a3.zip_code = "19103"
f3.address = a3
timeslots_list_3 = \
    [TimeSlot(day_of_week = 0, start_time = time(8,0), 
        end_time = time(18,30)),
    TimeSlot(day_of_week = 1, start_time = time(7,0), 
        end_time = time(19,30)),
    TimeSlot(day_of_week = 2, start_time = time(7,30), 
        end_time = time(18,30)),
    TimeSlot(day_of_week = 3, start_time = time(8,0), 
        end_time = time(19,30)),
    TimeSlot(day_of_week = 4, start_time = time(10,0), 
        end_time = time(5,30)),
    TimeSlot(day_of_week = 5, start_time = time(8,15), 
        end_time = time(18,45)),
    TimeSlot(day_of_week = 6, start_time = time(9,0), 
        end_time = time(20,45))]
f3.timeslots = timeslots_list_3

# Add each new object to session and commit session. 
db.session.add(f3)
db.session.add(a3)
for timeslot in timeslots_list_3:
	db.session.add(timeslot)
db.session.commit()

# Create a Soup Kitchen FoodResource.
f4 = FoodResource() 
f4.name = "Sample Soup Kitchen"
f4.phone_number = "739-492-9359"
f4.description = "Another description"
f4.location_type = "SOUP_KITCHEN"
a4 = Address()
a4.line1 = "2146 E Susquehanna Ave"
a4.city = "Philadelphia"
a4.state = "PA"
a4.zip_code = "19125"
f4.address = a4
timeslots_list_4 = \
    [TimeSlot(day_of_week = 0, start_time = time(8,0), 
        end_time = time(18,30)),
    TimeSlot(day_of_week = 1, start_time = time(7,0), 
        end_time = time(19,30)),
    TimeSlot(day_of_week = 2, start_time = time(7,30), 
        end_time = time(18,30)),
    TimeSlot(day_of_week = 3, start_time = time(8,0), 
        end_time = time(19,30)),
    TimeSlot(day_of_week = 4, start_time = time(10,0), 
        end_time = time(5,30)),
    TimeSlot(day_of_week = 5, start_time = time(8,15), 
        end_time = time(18,45)),
    TimeSlot(day_of_week = 6, start_time = time(9,0), 
        end_time = time(20,45))]
f4.timeslots = timeslots_list_4

# Add each new object to session and commit session. 
db.session.add(f4)
db.session.add(a4)
for timeslot in timeslots_list_4:
	db.session.add(timeslot)
db.session.commit()

# Create a WIC Office FoodResource.
f5 = FoodResource() 
f5.name = "North Philadelphia WIC Office"
f5.phone_number = "573-910-5830"
f5.description = "Another another description"
f5.location_type = "WIC_OFFICE"
a5 = Address()
a5.line1 = "1300 W Lehigh Ave"
a5.city = "Philadelphia"
a5.state = "PA"
a5.zip_code = "19132"
f5.address = a5
timeslots_list_5 = \
    [TimeSlot(day_of_week = 0, start_time = time(8,0), 
        end_time = time(18,30)),
    TimeSlot(day_of_week = 1, start_time = time(7,0), 
        end_time = time(19,30)),
    TimeSlot(day_of_week = 2, start_time = time(7,30), 
        end_time = time(18,30)),
    TimeSlot(day_of_week = 3, start_time = time(8,0), 
        end_time = time(19,30)),
    TimeSlot(day_of_week = 4, start_time = time(10,0), 
        end_time = time(5,30)),
    TimeSlot(day_of_week = 5, start_time = time(8,15), 
        end_time = time(18,45)),
    TimeSlot(day_of_week = 6, start_time = time(9,0), 
        end_time = time(20,45))]
f5.timeslots = timeslots_list_5

# Add each new object to session and commit session. 
db.session.add(f5)
db.session.add(a5)
for timeslot in timeslots_list_5:
	db.session.add(timeslot)
db.session.commit()