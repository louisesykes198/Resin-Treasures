# Resin Treasures

![image](docs/all-devices-black.png)

# Deployment

## Setting Up PostgreSQL

To configure your Django project to use PostgreSQL instead of SQLite, follow these steps:

### 1. Install PostgreSQL Adapter

Install the PostgreSQL adapter by adding `psycopg2-binary` to your project dependencies. After installation, update your `requirements.txt` file:
Put these in the terminal one after the other.

pip install psycopg2-binary

pip freeze > requirements.txt

2. Update settings.py

In your Django settings.py, import the necessary modules at the top of the file:

import dj_database_url
import os

Replace the existing DATABASES configuration with:

DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600
    )
}

This setup will allow Django to use the DATABASE_URL environment variable to connect to your PostgreSQL database.

3. Create and Set Your Environment Variable

If working locally, create a .env file and add the following:

DATABASE_URL=postgres://yourusername:yourpassword@yourhost:5432/yourdatabase

Make sure this .env file is not committed to version control by adding it to your .gitignore.

4. Run Migrations

Once your database is connected, apply migrations:

python manage.py migrate

This will set up your database schema using PostgreSQL.

5. Ready for Deployment

Once your PostgreSQL database is working locally, follow the steps in the Heroku Deployment section to complete deployment using Heroku's PostgreSQL add-on.

## Heroku Deployment

Deploying the crochet-files Django App to Heroku
Note: These instructions assume you have a verified Heroku account and an Eco Dynos plan via the GitHub Student Developer Pack.

1. Create a New Heroku App
Go to your Heroku Dashboard and click "New" > "Create new app".

Choose a unique app name and region, then click "Create app".

2. Configure Environment Variables
In your app dashboard, go to the Settings tab.

Click "Reveal Config Vars".

Add the following key-value pair:

Key: DISABLE_COLLECTSTATIC

Value: 1

Click Add.

This disables automatic static file collection during deployment, which we’ll configure manually later when HTML/CSS are in place.

3. Install a Production Web Server
Install Gunicorn:

Run pip3 install gunicorn~=20.1.

Add it to your requirements.txt:

Run pip3 freeze --local > requirements.txt.

Gunicorn is a production-ready WSGI server, replacing runserver for live environments.

4. Create a Procfile
At the root of your project directory (same level as requirements.txt), create a file named Procfile (no extension).

Inside, add:

web: gunicorn my_project.wsgi

Replace my_project with your Django project’s actual name (the one with settings.py).

5. Update Django Settings
Open settings.py and make the following changes:

a. Add Heroku to Allowed Hosts:

ALLOWED_HOSTS = ['.herokuapp.com', '127.0.0.1']

Adjust the list if you see a DisallowedHost error with a different address.

b. Turn off Debug Mode:

DEBUG = False

Required for security in production environments.

6. Commit and Push Changes to GitHub
Run git add .

Run git commit -m "Prepare project for Heroku deployment"

Run git push.

7. Connect GitHub to Heroku
Go back to your Heroku app dashboard and open the Deploy tab.

Under Deployment Method, select GitHub and click Connect to GitHub.

Search for your repository by name, then click Connect.

8. Deploy the App
Scroll to the bottom of the Deploy page and click Deploy Branch.

Wait for the build to complete. You can monitor progress under the Activity tab.

9. Set Up Dyno and Remove Postgres
Go to the Resources tab.

Could you make sure at least one Eco Dyno is enabled?

If there's a Heroku Postgres add-on (not needed for this project), click the three dots next to it and choose Delete Add-on.

10. View Your Live App
Click the Open app at the top right of your dashboard.

## Cloudinary Integration

This project uses Cloudinary to manage and serve image uploads. Follow these steps to integrate Cloudinary with your Django app:

Install Required Packages
Install the necessary Python packages:
pip3 install cloudinary~=1.36.0 dj3-cloudinary-storage~=0.0.6 urllib3~=1.26.15
(Also run pip install cloudinary if needed)

Add to requirements.txt
Run: pip3 freeze --local > requirements.txt

Sign Up for Cloudinary
Create an account at cloudinary.com. Choose "Developer" if asked. Verify your email if required.

Copy the CLOUDINARY_URL
From your Cloudinary dashboard, copy the API Environment Variable.

Set Environment Variable
In your env.py, add:
os.environ.setdefault("CLOUDINARY_URL", "<your copied URL>")
(Remove CLOUDINARY_URL= from the start of the string and keep it in quotes.)

Update settings.py
Add the following to INSTALLED_APPS (in this order):
'django.contrib.staticfiles'
'cloudinary_storage'
'django.contrib.sites'
'django_summernote'
'cloudinary'
'blog'
'about'

Update the Blog Model
In blog/models.py:

Add: from cloudinary.models import CloudinaryField

Add the image field to your Post model:
featured_image = CloudinaryField('image', default='placeholder')

Make and Apply Migrations
Run:
python3 manage.py makemigrations
python3 manage.py migrate

Update Template to Display Images
In blog/templates/blog/index.html, use this inside the .image-container:

{% if "placeholder" in post.featured_image.url %}
  <img class="card-img-top" src="{% static 'images/default.jpg' %}"alt="placeholder image">
{% else %}
  <img class="card-img-top" src="{{ post.featured_image.url }}"alt="{{ post.title }}">
{% endif %}
Add {% load static %} at the top of the file.

Prepare for Deployment

Set DEBUG = False in settings.py

Run:
git add --all
git commit -m "Enable serving of image files"
git push origin main

Add CLOUDINARY_URL to Heroku
In Heroku:

Go to Settings → Reveal Config Vars

Add a new variable:
Key: CLOUDINARY_URL
Value: (Paste the same URL from env.py)

Deploy
In the Deploy tab on Heroku, select the main branch and click Deploy Branch.

Test Your Live App
Open your deployed app in Heroku. Images should now be served via Cloudinary.

