#About Us
[Hack4Impact](http://hack4impact.weebly.com) is a student organization 
at the University of Pennsylvania that connects nonprofits with student software 
developers. Through semester-long projects, we build webapps to help 
socially-oriented organizations accomplish their goals even better. Inspired by 
technology's huge potential to empower activists and humanitarians, our mission 
is to foster the wider adoption of software as a tool for social impact.

#About Our Client
Founded in 1996, the [Greater Philadelphia Coalition Against Hunger](http://www.hungercoalition.org/about-us) strives to build a community where all people have the food they 
need to lead healthy lives. The Coalition connects people with food assistance 
programs and nutrition education; provides resources to a network of food 
pantries; and educates the public and policymakers about responsible solutions 
that prevent people from going hungry. 
#About The Project
##Technologies Used For This Project 
+ [Flask](http://flask.pocoo.org) 
+ [Foundation](http://foundation.zurb.com)
+ [SQLAlchemy](http://www.sqlalchemy.org)

##Languages Used For This Project 
+ Python
+ HTML/CSS
+ JavaScript

#How to get started with this project

1. `cd` to the directory where this project will be stored.

		cd path/to/directory

2. Create a local git repository and set up this repo as your remote repo.
	
		git init
		git remote add origin https://github.com/hack4impact/gpcah

3. Pull the project onto your local machine. This will give you copies of all 
files in the project.

		git pull origin master

4. Install [`virtualenv`](http://virtualenv.readthedocs.org/en/latest/virtualenv.html). 

5. Create a virtual environment. This will create a directory called `ENV/` that 
will hold any libraries you install.

		virtualenv ENV

6. Activate your virtual environment.

		source ENV/bin/activate

7. Install the project's requirements.
		
		pip install -r requirements.txt

8. Run the site.

		python run.py

9. Head on over to http://0.0.0.0:5000/!