import os, random, string

def generate_password(length):
	chars = string.ascii_letters + string.digits + '!@#$%^&*()'
	random.seed = (os.urandom(1024))
	return '1A'.join(random.choice(chars) for i in range(length))