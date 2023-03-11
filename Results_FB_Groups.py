import requests
from bs4 import BeautifulSoup
import os

# Login credentials
email = os.getenv('fb_email')
password = os.getenv('fb_password')

# URL of the Facebook login page
login_url = 'https://www.facebook.com/login.php'

# Create a session object
session = requests.session()

# Get the login page and parse the HTML with Beautiful Soup
login_page = session.get(login_url)
soup = BeautifulSoup(login_page.content, 'html.parser')

# Extract the input fields from the login form
inputs = soup.select('form#login_form input')

# Create a dictionary to store the login form data
login_data = {}
for inp in inputs:
    name = inp.get('name')
    value = inp.get('value')
    if name:
        login_data[name] = value

# Add the email and password to the login form data
login_data['email'] = email
login_data['pass'] = password

# Send a post request to the login page with the login form data
response = session.post(login_url, data=login_data)

# Now you can make requests to Facebook as an authenticated user
fairy_floss_url = 'https://www.facebook.com/groups/117412174975402'
fairy_floss_content_raw = session.get(fairy_floss_url)
print(response.content)
