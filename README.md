Welcome to the Social Media Platform project built using Django! This project aims to create a basic social media platform where users can register, log in, post updates, connect with friends, and more. The platform provides a foundation that you can extend and customize to create your own unique social media experience.

Table of Contents
Features
Getting Started
Prerequisites
Installation
Usage
Contributing
Features
User registration and authentication
User profiles with profile pictures and bio
News feed displaying posts from friends
Post creation and deletion
Like on posts
Follow to a user & see its post on home feed
unfollow to a user
User search functionality
Responsive and user-friendly design
Getting Started
Prerequisites
Before you begin, ensure you have the following installed:

Python (version 3.6 or higher)
Django (version 3.2 or higher)
Git
Installation
Clone the repository:

git clone https://github.com/Ayushsav/social-media.git
Navigate to the project directory:

cd social-media
Create a virtual environment (recommended):

virtualenv venv
Activate the virtual environment:

On Windows:

venv\Scripts\activate
On macOS and Linux:

source venv/bin/activate
Install the project dependencies:

pip install pillow
Perform database migrations:

python manage.py migrate
Create a superuser account for administrative access:

python manage.py createsuperuser
Run the development server:

python manage.py runserver
Access the application in your web browser at http://127.0.0.1:8000/.

Usage
Register a new account or log in with an existing account.
Customize your profile by adding a profile picture and bio.
Search for other users.
Create and delete your own posts.
Like on posts from friends.
Follow to a user & see its post on home feed
unfollow to a user
Explore the news feed to see posts from friends.
Log out when you're done using the platform.
Contributing
Contributions to this project are welcome! To contribute, follow these steps:

Fork the repository.
Create a new branch for your feature or bug fix: git checkout -b feature-name.
Make your changes and commit them: git commit -m "Add feature".
Push to the branch: git push origin feature-name.
Open a pull request describing your changes.
