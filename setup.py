# Necessary set-up.
from app import db
from app.models import *
from app.utils import *
import datetime
import time

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
p1 = HTML(page = 'edit-page', value = 'Administrators will put content here.')
p2 = HTML(page = 'about-page', value = 'Administrators will put content here.')
p3 = HTML(page = 'map-announcements', value = 'Administrators will put announcements here.')
p4 = HTML(page = 'wic-info-page', value = 'Administrators will put content here.')
p5 = HTML(page = 'snap-info-page', value = 'Administrators will put content here.')
p6 = HTML(page = 'summer-info-page', value = 'Administrators will put content here.')
p7 = HTML(page = 'seniors-info-page', value = 'Administrators will put content here.')
p8 = HTML(page = 'contact-page', value = 'Administrators will put contact information here.')
p9 = HTML(page = 'farmers-info-page', value = 'Administrators will put content here.')
p10 = HTML(page = 'neighborhood-info-page', value = 'Administrators will put content here.')
p11 = HTML(page = 'share-info-page', value = 'Administrators will put content here.')

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