#!flask/bin/python
import unittest
import os
from app import app, db
from config import basedir
from app.models import Address

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

if __name__ == '__main__':
    unittest.main()

