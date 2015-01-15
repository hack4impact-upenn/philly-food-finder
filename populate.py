# Necessary set-up.
from app import db
from app.models import *
from datetime import time, date
from app.utils import *

# Drop all database tables.
db.drop_all()

# Create new database tables.
db.create_all()

# Create colored pins.
cp_yellow = ColoredPin(
    color_name="Yellow",
    hex_color="fdd800", 
    pin_image_name="mbb_yellow.png"
)
db.session.add(cp_yellow)

cp_green = ColoredPin(
    color_name="Green",
    hex_color="009933", 
    pin_image_name="mbb_green.png"
)
db.session.add(cp_green)

cp_blue = ColoredPin(
    color_name="Blue",
    hex_color="0f85c7", 
    pin_image_name="mbb_blue.png"
)
db.session.add(cp_blue)

cp_red = ColoredPin(
    color_name="Red",
    hex_color="ef3d23", 
    pin_image_name="mbb_red.png"
)
db.session.add(cp_red)

cp_orange = ColoredPin(
    color_name="Orange",
    hex_color="f8a11d", 
    pin_image_name="mbb_orange.png"
)
db.session.add(cp_orange)

cp_purple = ColoredPin(
    color_name="Purple",
    hex_color="84459b", 
    pin_image_name="mbb_purple.png"
)
db.session.add(cp_purple)

cp_aqua = ColoredPin(
    color_name="Aqua",
    hex_color="82D1DA", 
    pin_image_name="mbb_aqua.png"
)
db.session.add(cp_aqua)

cp_grey = ColoredPin(
    color_name="Grey",
    hex_color="CCCCCC", 
    pin_image_name="mbb_grey.png"
)
db.session.add(cp_grey)

cp_lavender = ColoredPin(
    color_name="Lavender",
    hex_color="6F6AB0", 
    pin_image_name="mbb_lavender.png"
)
db.session.add(cp_lavender)

cp_light_green = ColoredPin(
    color_name="Light Green",
    hex_color="BFD849", 
    pin_image_name="mbb_light_green.png"
)
db.session.add(cp_light_green)

cp_magenta = ColoredPin(
    color_name="Magenta",
    hex_color="B86CAC", 
    pin_image_name="mbb_magenta.png"
)
db.session.add(cp_magenta)

cp_maroon = ColoredPin(
    color_name="Maroon",
    hex_color="8B181B", 
    pin_image_name="mbb_maroon.png"
)
db.session.add(cp_maroon)

cp_navy = ColoredPin(
    color_name="Navy",
    hex_color="2D4FA0", 
    pin_image_name="mbb_navy.png"
)
db.session.add(cp_navy)

cp_periwinkle = ColoredPin(
    color_name="Periwinkle",
    hex_color="A099CB", 
    pin_image_name="mbb_periwinkle.png"
)
db.session.add(cp_periwinkle)

cp_pink = ColoredPin(
    color_name="Pink",
    hex_color="F69799", 
    pin_image_name="mbb_pink.png"
)
db.session.add(cp_pink)

cp_sky_blue = ColoredPin(
    color_name="Sky Blue",
    hex_color="9FC9EB", 
    pin_image_name="mbb_sky_blue.png"
)
db.session.add(cp_sky_blue)

cp_turquoise = ColoredPin(
    color_name="Turquoise",
    hex_color="039B81", 
    pin_image_name="mbb_turquoise.png"
)
db.session.add(cp_turquoise)

# Create food resource types.
frt_farmers_market = FoodResourceType(
    name_singular="Farmers' Market",
    name_plural="Farmers' Markets",
    colored_pin=cp_yellow)

frt_food_cupboard = FoodResourceType(
    name_singular="Food Cupboard",
    name_plural="Food Cupboards",
    colored_pin=cp_green)

frt_senior_meals = FoodResourceType(
    name_singular="Senior Meals",
    name_plural="Senior Meals",
    colored_pin=cp_blue)

frt_share_host_site = FoodResourceType(
    name_singular="SHARE Host Site",
    name_plural="SHARE Host Sites",
    colored_pin=cp_red)

frt_soup_kitchen = FoodResourceType(
    name_singular="Soup Kitchen",
    name_plural="Soup Kitchens",
    colored_pin=cp_orange)

frt_wic_office = FoodResourceType(
    name_singular="WIC Office",
    name_plural="WIC Offices",
    colored_pin=cp_purple)

db.session.add(frt_farmers_market)
db.session.add(frt_food_cupboard)
db.session.add(frt_senior_meals)
db.session.add(frt_share_host_site)
db.session.add(frt_soup_kitchen)
db.session.add(frt_wic_office)
db.session.commit()

# Create a Farmers' Market FoodResource.
f0 = FoodResource() 
f0.name = "Clark Park"
num0 = PhoneNumber(number = "123-456-7890")
f0.phone_numbers.append(num0)
db.session.add(num0)
f0.phone_number = "123-456-7890"
f0.description = "Open year round"
f0.location_type = "FARMERS_MARKET"
f0.food_resource_type = frt_farmers_market
f0.are_hours_available = True

a0 = Address()
a0.line1 = "43rd Street and Baltimore Avenue"
a0.city = "Philadelphia"
a0.state = "PA"
a0.zip_code = "19104"
a0.createLatAndLong()
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
        end_time = time(19,30)),
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

# Create a Senior Meals FoodResource.
f1 = FoodResource() 
f1.name = "Senior Meal #1"
num1 = PhoneNumber(number = "123-456-7890")
f1.phone_numbers.append(num1)
db.session.add(num1)
f1.description = "Fresh fruit and veggies!"
f1.location_type = "SENIOR_MEAL"
f1.food_resource_type = frt_senior_meals
f1.are_hours_available = True

a1 = Address()
a1.line1 = "3160 Chestnut Street"
a1.city = "Philadelphia"
a1.state = "PA"
a1.zip_code = "19104"
a1.createLatAndLong()
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
        end_time = time(15,30)),
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
num2 = PhoneNumber(number = "123-456-7890")
f2.phone_numbers.append(num2)
db.session.add(num2)
f2.description = "Food cupboard description"
f2.location_type = "FOOD_CUPBOARD"
f2.food_resource_type = frt_food_cupboard
f2.are_hours_available = True

a2 = Address()
a2.line1 = "3560 Spruce St"
a2.city = "Philadelphia"
a2.state = "PA"
a2.zip_code = "19104"
a2.createLatAndLong()
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
        end_time = time(19,30)),
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
num3 = PhoneNumber(number = "123-456-7890")
f3.phone_numbers.append(num3)
db.session.add(num3)
f3.description = "A description"
f3.location_type = "SHARE"
f3.food_resource_type = frt_share_host_site
f3.are_hours_available = True

a3 = Address()
a3.line1 = "1610 Sansom St"
a3.city = "Philadelphia"
a3.state = "PA"
a3.zip_code = "19103"
a3.createLatAndLong()
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
        end_time = time(19,30)),
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
num4 = PhoneNumber(number = "123-456-7890")
f4.phone_numbers.append(num4)
db.session.add(num4)
f4.description = "Another description"
f4.location_type = "SOUP_KITCHEN"
f4.food_resource_type = frt_soup_kitchen
f4.are_hours_available = True

a4 = Address()
a4.line1 = "2146 E Susquehanna Ave"
a4.city = "Philadelphia"
a4.state = "PA"
a4.zip_code = "19125"
a4.createLatAndLong()
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
        end_time = time(19,30)),
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
num5 = PhoneNumber(number = "123-456-7890")
f5.phone_numbers.append(num5)
db.session.add(num5)
f5.description = "Another another description"
f5.location_type = "WIC_OFFICE"
f5.food_resource_type = frt_wic_office
f5.are_hours_available = True

a5 = Address()
a5.line1 = "1300 W Lehigh Ave"
a5.city = "Philadelphia"
a5.state = "PA"
a5.zip_code = "19132"
a5.createLatAndLong()
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
        end_time = time(15,30)),
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

# Create a Farmers' Market FoodResource.
f6 = FoodResource() 
f6.name = "Food Trust"
num6 = PhoneNumber(number = "215-575-0444")
f6.phone_numbers.append(num6)
db.session.add(num6)
f6.phone_number = "215-575-0444"
f6.description = "Everyone deserves healthy food"
f6.food_resource_type = frt_farmers_market
a6 = Address()
a6.line1 = "1617 John F. Kennedy Blvd."
a6.city = "Philadelphia"
a6.state = "PA"
a6.zip_code = "19103"
a6.createLatAndLong()
f6.address = a6
timeslots_list_6 = \
    [TimeSlot(day_of_week = 0, start_time = time(8,0), 
        end_time = time(18,30)),
    TimeSlot(day_of_week = 1, start_time = time(7,0), 
        end_time = time(19,30)),
    TimeSlot(day_of_week = 2, start_time = time(7,30), 
        end_time = time(18,30)),
    TimeSlot(day_of_week = 3, start_time = time(8,0), 
        end_time = time(19,30)),
    TimeSlot(day_of_week = 4, start_time = time(10,0), 
        end_time = time(19,30)),
    TimeSlot(day_of_week = 5, start_time = time(8,15), 
        end_time = time(18,45)),
    TimeSlot(day_of_week = 6, start_time = time(9,0), 
        end_time = time(20,45))]
f6.timeslots = timeslots_list_6
f6.are_hours_available = True

# Add each new object to session and commit session. 
db.session.add(f6)
db.session.add(a6)
for timeslot in timeslots_list_6:
    db.session.add(timeslot)
db.session.commit()

# Create a Senior Meals FoodResource.
f7 = FoodResource() 
f7.name = "Senior Meal #2"
num7 = PhoneNumber(number = "888-998-6325")
f7.phone_numbers.append(num7)
db.session.add(num7)
f7.description = "Fresh foods!"
f7.food_resource_type = frt_senior_meals
a7 = Address()
a7.line1 = "8446 Bayard Street"
a7.city = "Philadelphia"
a7.state = "PA"
a7.zip_code = "19150"
a7.createLatAndLong()
f7.address = a7
timeslots_list_7 = \
    [TimeSlot(day_of_week = 0, start_time = time(8,0), 
        end_time = time(18,30)),
    TimeSlot(day_of_week = 1, start_time = time(7,0), 
        end_time = time(19,30)),
    TimeSlot(day_of_week = 2, start_time = time(7,30), 
        end_time = time(18,30)),
    TimeSlot(day_of_week = 3, start_time = time(8,0), 
        end_time = time(19,30)),
    TimeSlot(day_of_week = 4, start_time = time(10,0), 
        end_time = time(19,30)),
    TimeSlot(day_of_week = 5, start_time = time(8,15), 
        end_time = time(18,45)),
    TimeSlot(day_of_week = 6, start_time = time(9,0), 
        end_time = time(20,45))]
f7.timeslots = timeslots_list_7
f7.are_hours_available = True

# Add each new object to session and commit session. 
db.session.add(f7)
db.session.add(a7)
for timeslot in timeslots_list_7:
    db.session.add(timeslot)
db.session.commit()

# Create a Food Cupboard FoodResource.
f8 = FoodResource() 
f8.name = "St. Francis Inn Ministries"
num8 = PhoneNumber(number = "215-925-4584")
f8.phone_numbers.append(num8)
db.session.add(num8)
f8.description = "Food cupboard description"
f8.food_resource_type = frt_food_cupboard
a8 = Address()
a8.line1 = "2441 Kensington Avenue"
a8.city = "Philadelphia"
a8.state = "PA"
a8.zip_code = "19125"
a8.createLatAndLong()
f8.address = a8
timeslots_list_8 = \
    [TimeSlot(day_of_week = 0, start_time = time(8,0), 
        end_time = time(18,30)),
    TimeSlot(day_of_week = 1, start_time = time(7,0), 
        end_time = time(19,30)),
    TimeSlot(day_of_week = 2, start_time = time(7,30), 
        end_time = time(18,30)),
    TimeSlot(day_of_week = 3, start_time = time(8,0), 
        end_time = time(19,30)),
    TimeSlot(day_of_week = 4, start_time = time(10,0), 
        end_time = time(19,30)),
    TimeSlot(day_of_week = 5, start_time = time(8,15), 
        end_time = time(18,45)),
    TimeSlot(day_of_week = 6, start_time = time(9,0), 
        end_time = time(20,45))]
f8.timeslots = timeslots_list_8
f8.are_hours_available = True

# Add each new object to session and commit session. 
db.session.add(f8)
db.session.add(a8)
for timeslot in timeslots_list_8:
    db.session.add(timeslot)
db.session.commit()

# Create a SHARE Food Site FoodResource.
f9 = FoodResource() 
f9.name = "Sample SHARE Food Site"
num9 = PhoneNumber(number = "123-456-7890")
f9.phone_numbers.append(num9)
db.session.add(num9)
f9.description = "A description"
f9.food_resource_type = frt_share_host_site
a9 = Address()
a9.line1 = "2901 Hunting Park Avenue"
a9.city = "Philadelphia"
a9.state = "PA"
a9.zip_code = "19129"
a9.createLatAndLong()
f9.address = a9
timeslots_list_9 = \
    [TimeSlot(day_of_week = 0, start_time = time(8,0), 
        end_time = time(18,30)),
    TimeSlot(day_of_week = 1, start_time = time(7,0), 
        end_time = time(19,30)),
    TimeSlot(day_of_week = 2, start_time = time(7,30), 
        end_time = time(18,30)),
    TimeSlot(day_of_week = 3, start_time = time(8,0), 
        end_time = time(19,30)),
    TimeSlot(day_of_week = 4, start_time = time(10,0), 
        end_time = time(19,30)),
    TimeSlot(day_of_week = 5, start_time = time(8,15), 
        end_time = time(18,45)),
    TimeSlot(day_of_week = 6, start_time = time(9,0), 
        end_time = time(20,45))]
f9.timeslots = timeslots_list_9
f9.are_hours_available = True

# Add each new object to session and commit session. 
db.session.add(f9)
db.session.add(a9)
for timeslot in timeslots_list_9:
    db.session.add(timeslot)
db.session.commit()

# Create a Soup Kitchen FoodResource.
f10 = FoodResource() 
f10.name = "Philabundance"
num10 = PhoneNumber(number = "215-739-7394")
f10.phone_numbers.append(num10)
db.session.add(num10)
f10.description = "Another description"
f10.food_resource_type = frt_soup_kitchen
a10 = Address()
a10.line1 = "3616 S Galloway St"
a10.city = "Philadelphia"
a10.state = "PA"
a10.zip_code = "19148"
a10.createLatAndLong()
f10.address = a10
timeslots_list_10 = \
    [TimeSlot(day_of_week = 0, start_time = time(8,0), 
        end_time = time(18,30)),
    TimeSlot(day_of_week = 1, start_time = time(7,0), 
        end_time = time(19,30)),
    TimeSlot(day_of_week = 2, start_time = time(7,30), 
        end_time = time(18,30)),
    TimeSlot(day_of_week = 3, start_time = time(8,0), 
        end_time = time(19,30)),
    TimeSlot(day_of_week = 4, start_time = time(10,0), 
        end_time = time(19,30)),
    TimeSlot(day_of_week = 5, start_time = time(8,15), 
        end_time = time(18,45)),
    TimeSlot(day_of_week = 6, start_time = time(9,0), 
        end_time = time(20,45))]
f10.timeslots = timeslots_list_10
f10.are_hours_available = True

# Add each new object to session and commit session. 
db.session.add(f10)
db.session.add(a10)
for timeslot in timeslots_list_10:
    db.session.add(timeslot)
db.session.commit()

# Create a WIC Office FoodResource.
f11 = FoodResource() 
f11.name = "Mitzvah Food Project"
num11 = PhoneNumber(number = "215-832-0831")
f11.phone_numbers.append(num11)
db.session.add(num11)
f11.description = "Another another description"
f11.food_resource_type = frt_wic_office
a11 = Address()
a11.line1 = "2100 Arch Street"
a11.city = "Philadelphia"
a11.state = "PA"
a11.zip_code = "19103"
a11.createLatAndLong()
f11.address = a11
timeslots_list_11 = \
    [TimeSlot(day_of_week = 0, start_time = time(8,0), 
        end_time = time(18,30)),
    TimeSlot(day_of_week = 1, start_time = time(7,0), 
        end_time = time(19,30)),
    TimeSlot(day_of_week = 2, start_time = time(7,30), 
        end_time = time(18,30)),
    TimeSlot(day_of_week = 3, start_time = time(8,0), 
        end_time = time(19,30)),
    TimeSlot(day_of_week = 4, start_time = time(10,0), 
        end_time = time(19,30)),
    TimeSlot(day_of_week = 5, start_time = time(8,15), 
        end_time = time(18,45)),
    TimeSlot(day_of_week = 6, start_time = time(9,0), 
        end_time = time(20,45))]
f11.timeslots = timeslots_list_11
f11.are_hours_available = True

# Add each new object to session and commit session. 
db.session.add(f11)
db.session.add(a11)
for timeslot in timeslots_list_11:
    db.session.add(timeslot)
db.session.commit()

# Create 3 admin users
u1 = User(email='ben@ben.com', password = 'pass123', is_enabled = True,
            first_name = 'Ben', last_name = 'Sandler', 
            roles=[Role(name = 'Admin')])
u2 = User(email = 'steve@gmail.com', password = 'p@$$w0rd', is_enabled = True,
            first_name = 'Steve', 
            last_name = 'Smith', roles = [Role(name = 'Admin')])
u3 = User(email = 'sarah@gmail.com',
            password = '139rjf9i#@$#R$#!#!!!48939832984893rfcnj3@#%***^%$#@#$@#', 
            is_enabled = True, first_name = 'Sarah', last_name = 'Smith', 
            roles = [Role(name = 'Admin')])

u1.confirm_and_enable_debug()
u2.confirm_and_enable_debug()
u3.confirm_and_enable_debug()

# Add each new object to session and commit session. 
db.session.add(u1)
db.session.add(u2)
db.session.add(u3)
db.session.commit()

# Create HTML objects
p1 = HTML(page = 'edit-page', value = 'Hello world!')
p2 = HTML(page = 'about-page', value = 'Hello about!')
p3 = HTML(page = 'map-announcements', value = 'Hello announcements!')
p4 = HTML(page = 'wic-info-page', value = 'Hello WIC!')
p5 = HTML(page = 'snap-info-page', value = 'Hello SNAP!')
p6 = HTML(page = 'summer-info-page', value = 'Hello Summer!')
p7 = HTML(page = 'seniors-info-page', value = 'Hello Seniors!')
p8 = HTML(page = 'contact-page', value = 'Hello contact!')
p9 = HTML(page = 'farmers-info-page', value = 'Hello farmers!')
p10 = HTML(page = 'neighborhood-info-page', value = 'Hello neighborhood!')
p11 = HTML(page = 'share-info-page', value = 'Hello share!')

# Add each new object to session and commit session. 
db.session.add(p1)
db.session.add(p2)
db.session.add(p3)
db.session.add(p4)
db.session.add(p5)
db.session.add(p6)
db.session.add(p7)
db.session.add(p8)
db.session.add(p9)
db.session.add(p10)
db.session.add(p11)
db.session.commit()

# Create sample searches.
today = date.today()
# Searches from this month.
zip = ZipSearch(zip_code='19104', search_count=10, date=today)
db.session.add(zip)
zip = ZipSearch(zip_code='19103', search_count=7, date=today)
db.session.add(zip)
zip = ZipSearch(zip_code='19129', search_count=3, date=today)
db.session.add(zip)
db.session.commit()
# Searches from last month. 
first = get_first_day_of_previous_month(today)
last = get_last_day_of_previous_month(today)
second = first + timedelta(days=1)
zip = ZipSearch(zip_code='19104', search_count=10, date=first)
db.session.add(zip)
zip = ZipSearch(zip_code='02420', search_count=100, date=last)
db.session.add(zip)
zip = ZipSearch(zip_code='02420', search_count=3, date=first)
db.session.add(zip)
zip = ZipSearch(zip_code='11111', search_count=100, date=second)
db.session.add(zip)
db.session.commit()