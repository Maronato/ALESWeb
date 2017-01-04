# ALES's Website
Website that serves as a database and framework for the ALES Project

# Instructions to run locally

## Setting up

1. [Install Python 3](https://www.python.org/downloads/)
2. [Install virtualenv](https://virtualenv.pypa.io/en/stable/) (Accomplish this by running `pip3 install virtualenv`)
3. [Install Postgres](https://devcenter.heroku.com/articles/heroku-postgresql#local-setup)
4. Open a terminal window at the project's root:
 1. `virtualenv -p python3 venv` to create a virtual machine for the website
 * `source venv/bin/activate` to activate the virtual machine
 * `pip install -r requirements.txt` to install the requirements
 * `python manage.py migrate` to migrate the database
 * `python manage.py createsuperuser` to create the website's admin. Take note of the username and password for later
 * `python manage.py runserver` to start the server

Now you should have a version of the website running locally

## Local settings

Now you need to setup some local settings.

Go to project/settings.py and change the following:

### General settings
`SECRET_KEY` Django's signing key. No need to change it if running with `DEBUG = True`

`SITE_URL` is the website's domain. If running locally, yours wil probably be something like `http://localhost:8000`

### Email settings
To properly sign users in the website uses a email verification system.

You'll need a valid email account to serve as host

`DEFAULT_FROM_EMAIL` the default email address to be used as 'from' field

`EMAIL_HOST_USER` email address that'll be used as host

`EMAIL_HOST_PASSWORD` the password of the above host

You can leave `EMAIL_USE_TLS`, `EMAIL_HOST` and `EMAIL_PORT` as is if you are using gmail

`SERVER_EMAIL` the email address that django will use when sending error reports

`ADMINS` List of tuples with admin names and emails. Used when sending error reports

Now you are all set.

# Using the website

Start by going to the index page and clicking Login

Use your admin username and password to login

Now you'll see some options. Start at the top and create a City.

Proceed by creating schools, courses, etc. Create as many as you want.

Whenever you create a Teacher or a Student, a confirmation email is sent to them. Within it you'll find a unique confirmation url. Use it to activate and set a password for the teacher or student.

You'll now be able to login as the activated teacher or student and do some other things as them, like enroll in courses or create events.

# TODO

### Main
Finish the main app so that:

* The main page is complete with realtime data about the number of students, courses, teachers, etc
* there is a working Contact tab to email us
* There is a working 'Inscreva-se' tab that embeds a google form for students and teachers to apply
* There is a working 'Escoals' subtab at the index page that shows the current schools and cities we are working with, and the number of students and teachers working at them

### Blog
Finish the blog app so that:

* teachers can:
 * create, edit and delete their own posts
* visitants see a list of posts at /blog
* visitants can see the post in detail
* list of posts supports pagination
* visitants can search for posts
* posts are posted on the facebook page automagically

### Pictures
Finish the pictures app so that:

* admins can create albums
* admins can upload pictures within said albums
* pictures are uploaded to S3
* pictures are thumbnailed
* deleting a picture deletes the file in S3
* visitants can see albuns at /albums
* visitants can see the pictures within each album
* lists need not be paginated

### Videos
Finish the videos app so that:

* admins can create, edit and delete videos
* vidos should be hosted on youtube
* visitants can see a list of videos at /videos
* list need not be paginated

### Press - (?)
Finish the press app so that

* admins can create, edit and delete press posts
* visitants can see a paginated list of press posts
* BONUS - press data is collected by a snippet bot

### Courses

* create view to show courses details for everyone to see
* do the same for events
* create 'category' model to assign events (?)
* propagate categories a little better accross views(like telling students what category the event is)

### Teachers

* Finish 'my info' dashboard tab so that teachers can change their passwords, emails, unsubscribe from reminders and see what info we have about them
* create a command for reminding teachers about their events

### Schools

* Finish 'my info' dashboard tab so that students can change their passwords, emails, unsubscribe from reminders and see what info we have about them
* make it so the schools' principals can see stats about their students
* make it so parents can see stats about their kids, or make it so the kids themselves can see the stats and parents can login as their kids

### Misc

* Are there any other ways to interact with facebook?
* Finish the change password and email views/forms for students and teachers
* create a custom template for the reset-password view
* change reminder command so that it sends emails for events that are exactly X days away, so that we can send multiple emails for each event
* fix the footer so that it is sticky
* make the welcome email a little nicer, since people are going to apply and not know when we are going to accept them. Make it sound like it is a big deal to be accepted
* make the email templates a little nicer
