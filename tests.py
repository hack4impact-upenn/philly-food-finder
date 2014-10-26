#!flask/bin/python
import unittest
import os
from datetime import time
from sqlalchemy.exc import IntegrityError
from app import app, db
from config import basedir
from app.models import Address, Resource, TimeSlot

class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_writing_reading_address(self):
    	a1 = Address(line1 = '1234 MB 1234', line2 = '3700 Spruce St', city = 'Philadelphia', state = 'PA', zip_code = '14109')
    	db.session.add(a1)
    	a2 = Address(line1 = '4567 MB 1234', line2 = '3600 Spruce St', city = 'Philadelphia', state = 'PA', zip_code = '14109')
    	db.session.add(a2)
    	db.session.commit()
    	assert len(Address.query.filter_by(zip_code = '14109').all()) == 2
    	assert len(Address.query.filter_by(zip_code = '14109', city = 'New York').all()) == 0

    def test_create_valid_resource(self):
        a1 = Address(line1 = '1234 MB 1234', line2 = '3700 Spruce St', city = 'Philadelphia', state = 'PA', zip_code = '14109')
        t0 = TimeSlot(day_of_week=0,start_time=time(8,0),end_time=time(18,30))
        t1 = TimeSlot(day_of_week=1,start_time=time(7,0),end_time=time(19,30))
        t2 = TimeSlot(day_of_week=2,start_time=time(7,30),end_time=time(18,30))
        t3 = TimeSlot(day_of_week=3,start_time=time(8,0),end_time=time(19,30))
        t4 = TimeSlot(day_of_week=4,start_time=time(10,0),end_time=time(5,30))
        t5 = TimeSlot(day_of_week=5,start_time=time(8,15),end_time=time(18,45))
        t6 = TimeSlot(day_of_week=6,start_time=time(9,0),end_time=time(20,45))
        desc = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec sem neque, vehicula ac nisl at, porta porttitor enim. Suspendisse nibh eros, pulvinar nec risus a, dignissim efficitur diam. Phasellus vestibulum posuere ex, vel hendrerit turpis molestie sit amet. Nullam ornare magna quis urna sodales, vel iaculis purus consequat. Mauris laoreet enim ipsum. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Nulla facilisi. In et dui ante. Morbi elementum dolor ligula, et mollis magna interdum non. Mauris ligula mi, mattis at ex ut, pellentesque porttitor elit. Integer volutpat elementum tristique. Ut interdum, mauris a feugiat euismod, tortor.'
        r1 = Resource(name='Test Resource 1',address=a1,phone='1234567898',timeslots=[t0,t1,t2,t3,t4,t5,t6],description=desc,location_type='FARMER_MARKET')
        db.session.add(r1)
        db.session.commit()
        assert len(Resource.query.filter_by(name = 'Test Resource 1').all()) == 1
        assert len(Resource.query.filter_by(address = a1).all()) == 1

    def test_create_invalid_enum_resource(self):
        a1 = Address(line1 = '1234 MB 1234', line2 = '3700 Spruce St', city = 'Philadelphia', state = 'PA', zip_code = '14109')
        t0 = TimeSlot(day_of_week=0,start_time=time(8,0),end_time=time(18,30))
        t1 = TimeSlot(day_of_week=1,start_time=time(7,0),end_time=time(19,30))
        t2 = TimeSlot(day_of_week=2,start_time=time(7,30),end_time=time(18,30))
        t3 = TimeSlot(day_of_week=3,start_time=time(8,0),end_time=time(19,30))
        t4 = TimeSlot(day_of_week=4,start_time=time(10,0),end_time=time(5,30))
        t5 = TimeSlot(day_of_week=5,start_time=time(8,15),end_time=time(18,45))
        t6 = TimeSlot(day_of_week=6,start_time=time(9,0),end_time=time(20,45))
        desc = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec sem neque, vehicula ac nisl at, porta porttitor enim. Suspendisse nibh eros, pulvinar nec risus a, dignissim efficitur diam. Phasellus vestibulum posuere ex, vel hendrerit turpis molestie sit amet. Nullam ornare magna quis urna sodales, vel iaculis purus consequat. Mauris laoreet enim ipsum. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Nulla facilisi. In et dui ante. Morbi elementum dolor ligula, et mollis magna interdum non. Mauris ligula mi, mattis at ex ut, pellentesque porttitor elit. Integer volutpat elementum tristique. Ut interdum, mauris a feugiat euismod, tortor.'
        self.assertRaises(IntegrityError, r1 = Resource(name='Test Resource 1',address=a1,phone='1234567898',timeslots=[t0,t1,t2,t3,t4,t5,t6],description=desc,location_type='WRONG_ENUM!!!!!!!!!!!!!'))

if __name__ == '__main__':
    unittest.main()

