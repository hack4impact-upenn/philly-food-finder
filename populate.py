# Necessary set-up.
from app import db
from app.models import *
from datetime import time

# Drop all database tables.
db.drop_all()

# Create new database tables.
db.create_all()

# Create a Farmers' Market FoodResource.
f0 = FoodResource() 
f0.name = "Clark Park"
num0 = PhoneNumber(number = "123-456-7890")
f0.phone_numbers.append(num0)
db.session.add(num0)
f0.phone_number = "123-456-7890"
f0.description = "Open year round"
f0.location_type = "FARMERS_MARKET"
f0.is_for_family_and_children = True
f0.is_for_seniors = True

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
f1.is_for_family_and_children = False
f1.is_for_seniors = True

a1 = Address()
a1.line1 = "3160 Chestnut Street"
a1.city = "Philadelphia"
a1.state = "PA"
a1.zip_code = "19104"
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
f2.is_for_family_and_children = False
f2.is_for_seniors = True

a2 = Address()
a2.line1 = "3560 Spruce St"
a2.city = "Philadelphia"
a2.state = "PA"
a2.zip_code = "19104"
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
f3.is_for_family_and_children = False
f3.is_for_seniors = True

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
f4.is_for_family_and_children = False
f4.is_for_seniors = True

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
f5.is_for_family_and_children = False
f5.is_for_seniors = True

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
f6.location_type = "FARMERS_MARKET"
a6 = Address()
a6.line1 = "1617 John F. Kennedy Blvd."
a6.city = "Philadelphia"
a6.state = "PA"
a6.zip_code = "19103"
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
f7.location_type = "SENIOR_MEAL"
a7 = Address()
a7.line1 = "8446 Bayard Street"
a7.city = "Philadelphia"
a7.state = "PA"
a7.zip_code = "19150"
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
f8.location_type = "FOOD_CUPBOARD"
a8 = Address()
a8.line1 = "2441 Kensington Avenue"
a8.city = "Philadelphia"
a8.state = "PA"
a8.zip_code = "19125"
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
f9.location_type = "SHARE"
a9 = Address()
a9.line1 = "2901 Hunting Park Avenue"
a9.city = "Philadelphia"
a9.state = "PA"
a9.zip_code = "19129"
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
f10.location_type = "SOUP_KITCHEN"
a10 = Address()
a10.line1 = "3616 S Galloway St"
a10.city = "Philadelphia"
a10.state = "PA"
a10.zip_code = "19148"
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
f11.location_type = "WIC_OFFICE"
a11 = Address()
a11.line1 = "2100 Arch Street"
a11.city = "Philadelphia"
a11.state = "PA"
a11.zip_code = "19103"
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
p3 = HTML(page = 'faq-page', value = 'Hello faq!')
p4 = HTML(page = 'wic-info-page', value = 'Hello WIC!')
p5 = HTML(page = 'snap-info-page', value = 'Hello SNAP!')
p6 = HTML(page = 'summer-info-page', value = 'Hello Summer!')
p7 = HTML(page = 'seniors-info-page', value = 'Hello Seniors!')

# Add each new object to session and commit session. 
db.session.add(p1)
db.session.add(p2)
db.session.add(p3)
db.session.add(p4)
db.session.add(p5)
db.session.add(p6)
db.session.add(p7)
db.session.commit()

# Create food resource types.
frt0 = FoodResourceType(
    enum="FARMERS_MARKET",
    name_singular="Farmers' Market",
    name_plural="Farmers' Markets",
    hypenated_id_singular="farmers-market",
    hypenated_id_plural="farmers-markets",
    underscored_id_singular="farmers_market",
    underscored_id_plural="farmers_markets",
    hex_color="fdd800",
    pin_image_name="mb_yellow.png")

frt1 = FoodResourceType(
    enum="FOOD_CUPBOARD",
    name_singular="Food Cupboard",
    name_plural="Food Cupboards",
    hypenated_id_singular="food-cupboard",
    hypenated_id_plural="food-cupboards",
    underscored_id_singular="food_cupboard",
    underscored_id_plural="food_cupboards",
    hex_color="009933",
    pin_image_name="mbb_green.png")

frt2 = FoodResourceType(
    enum="SENIOR_MEAL",
    name_singular="Senior Meals",
    name_plural="Senior Meals",
    hypenated_id_singular="senior-meals",
    hypenated_id_plural="senior-meals",
    underscored_id_singular="senior_meals",
    underscored_id_plural="senior_meals",
    hex_color="0f85c7",
    pin_image_name="mbb_blue.png")

frt3 = FoodResourceType(
    enum="SHARE",
    name_singular="SHARE Host Site",
    name_plural="SHARE Host Sites",
    hypenated_id_singular="share-host-site",
    hypenated_id_plural="share-host-sites",
    underscored_id_singular="share_host_site",
    underscored_id_plural="share_host_sites",
    hex_color="ef3d23",
    pin_image_name="mbb_red.png")

frt4 = FoodResourceType(
    enum="SOUP_KITCHEN",
    name_singular="Soup Kitchen",
    name_plural="Soup Kitchens",
    hypenated_id_singular="soup-kitchen",
    hypenated_id_plural="soup-kitchens",
    underscored_id_singular="soup_kitchen",
    underscored_id_plural="soup_kitchens",
    hex_color="f8a11d",
    pin_image_name="mbb_orange.png")

frt5 = FoodResourceType(
    enum="WIC_OFFICE",
    name_singular="WIC Office",
    name_plural="WIC Offices",
    hypenated_id_singular="wic-office",
    hypenated_id_plural="wic-offices",
    underscored_id_singular="wic_office",
    underscored_id_plural="wic_offices",
    hex_color="84459b",
    pin_image_name="mbb_purple.png")

db.session.add(frt0)
db.session.add(frt1)
db.session.add(frt2)
db.session.add(frt3)
db.session.add(frt4)
db.session.add(frt5)
db.session.commit()