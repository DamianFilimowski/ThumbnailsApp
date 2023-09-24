# Tournament Application

Welcome to the Tournament Application! This Django app allows you to manage tournaments, teams, matches, and scorers for
different events.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)


## Features

- logged user can upload images via HTTP request in PNG or JPG format.
- there are three builtin account tiers: Basic, Premium and Enterprise:

1. users that have "Basic" plan after uploading an image get: 

* a link to a thumbnail that's 200px in height
2. Users that have "Premium" plan get:

* a link to a thumbnail that's 200px in height

* a link to a thumbnail that's 400px in height

* a link to the originally uploaded image

3. Users that have "Enterprise" plan get

* a link to a thumbnail that's 200px in height

* a link to a thumbnail that's 400px in height

* a link to the originally uploaded image

* ability to fetch an expiring link to the image (the link expires after a given number of seconds (the user can specify any number between 300 and 30000))

Admins are be able to create arbitrary tiers with the following things configurable:
- arbitrary thumbnail sizes
- presence of the link to the originally uploaded file
- ability to generate expiring links

## Installation

1. Clone this repository:

   git clone https://github.com/DamianFilimowski/ThumbnailsApp

   cd ThumbnailsApp

2. Create a virtual environment:
    
    python3 -m venv venv

3. Activate the virtual environment:
    
    On macOS and Linux:

        source venv/bin/activate

4. Install the required packages:

    pip install -r requirements.txt

5. Apply database migrations:

    python manage.py migrate

6. Run the development server:
    
    python manage.py runserver

## Usage

Access the Django admin panel by visiting http://localhost:8000/admin/. Log in using your superuser credentials or
create account.

- at http://localhost:8000/api/obtain-auth-token/ you can obtain authentication token
- at http://localhost:8000/api/upload-image/<str:filename>/ you can upload images via HTTP request
add your authorization token in headers, image in body
- at http://localhost:8000/api/image-list/ you can see list of your images, and links to them/thumbnails
depending on your plan
- at http://localhost:8000/api/get-exp-link/ you can obtain expiring link if your plan allows you to do so

