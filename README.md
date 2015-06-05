The application is up and running at http://www.phillyfoodfinder.org.

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
In Philadelphia county, 22% of residents are food-insecure. While there are food assistance programs -- including food pantries, soup kitchens, and senior meal sites -- available to Philadelphians, such resources may be difficult for those in need to learn about or find. Our task was to develop a central web-based tool where individuals can find all food resources that are available within their zip code.

Philly Food Finder, our final web application, offers an intuitive map-based interface that visitors use to search for food resources by zip code and other optional criteria. We also developed a suite of administrative functions which allow the Philadelphia Food Policy Advisory Council (FPAC) to easily add and update food resources and other content on the website without writing any code. Moreover, managers of food resources within Philadelphia can submit their food resource’s information for inclusion in the website’s database. In order to develop Philly Food Finder, our team met weekly for three hours. Each team member also worked on their own for at least three hours per week. We divided weekly tasks between front- and back-end development. We hope that Philly Food Finder will be a great asset to FPAC and the greater Philadelphia community!

##Technologies Used For This Project 
+ [Flask](http://flask.pocoo.org) 
+ [Foundation](http://foundation.zurb.com)
+ [SQLAlchemy](http://www.sqlalchemy.org)
+ [jQuery](http://jquery.com/)
+ [gmaps.js](https://hpneo.github.io/gmaps/)
+ [CKEditor.js](http://ckeditor.com/)
+ [Dropzone.js](http://www.dropzonejs.com/)
+ [Remodal](http://vodkabears.github.io/remodal/)

##Languages Used For This Project 
+ Python
+ JavaScript
+ HTML
+ CSS

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
