README

Introduction

This is a RESTful API system built with Django and Django Rest Framework. The system allows users to register, log in, and interact with restaurants, menus, and votes.
Components

The system consists of the following components:

Auth: Handles user authentication and registration
Employee: Manages employee data and interactions
Menu: Handles menu data and interactions
Restaurants: Manages restaurant data and interactions
Votes: Handles vote data and interactions
How it Works

Here is a high-level overview of how the system works:

User Registration: A user registers by sending a POST request to the /register/ endpoint with their email and password.
User Login: A user logs in by sending a POST request to the /login/ endpoint with their email and password.
Employee Management: Employees can be created, read, updated, or deleted by sending requests to the /employees/ endpoint.
Menu Management: Menus can be created, read, updated, or deleted by sending requests to the /menus/ endpoint.
Restaurant Management: Restaurants can be created, read, updated, or deleted by sending requests to the /restaurants/ endpoint.
Vote Management: Votes can be cast by sending a POST request to the /votes/ endpoint.
Endpoints

Here are the available endpoints:

/register/: Register a new user
/login/: Log in to the system
/employees/: Manage employees
/menus/: Manage menus
/restaurants/: Manage restaurants
/votes/: Cast a vote
Authentication

The system uses JSON Web Tokens (JWT) for authentication. When a user logs in, a JWT token is generated and returned in the response. This token must be included in the Authorization header of subsequent requests to authenticate the user.

Requirements

Python 3.8 or higher
Django 3.2 or higher
Django Rest Framework 3.12 or higher
pip
Installation

Clone the repository: git clone https://github.com/your-username/your-repo-name.git
Install the required packages: pip install -r requirements.txt
Create a new Django project: django-admin startproject projectname
Create a new Django app: python manage.py startapp restbas
Add the app to the project: python manage.py migrate
Run the development server: python manage.py runserver
Running the System

Open a web browser and navigate to http://localhost:8000/
Register a new user by sending a POST request to http://localhost:8000/register/ with the required fields (email, password, etc.)
Log in by sending a POST request to http://localhost:8000/login/ with the email and password
Interact with the system by sending requests to the various endpoints (e.g. http://localhost:8000/restaurants/, http://localhost:8000/menus/, etc.)
Endpoints

http://localhost:8000/register/: Register a new user
http://localhost:8000/login/: Log in to the system
http://localhost:8000/restaurants/: Create, read, update, or delete restaurants
http://localhost:8000/menus/: Create, read, update, or delete menus
http://localhost:8000/votes/: Create, read, update, or delete votes
Authentication

The system uses JSON Web Tokens (JWT) for authentication. When a user logs in, a JWT token is generated and returned in the response. This token must be included in the Authorization header of subsequent requests to authenticate the user.
