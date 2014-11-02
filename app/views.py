from app import app, db
from models import Address

@app.route('/')
def index():
    return "Hello World!"

