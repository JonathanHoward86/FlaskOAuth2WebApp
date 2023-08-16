# FlaskOAuth2WebApp

This web application allows users to authenticate through EVE Online's OAuth2 system and displays dashboard data retrieved from the EVE Online API. Users can provide their character ID and corporation ID to access their information.

Prerequisites

Python 3.x
Required Python packages (selenium, openpyxl, Flask, urllib3, requests, dash)

Installation

Clone or download this repository to your local machine.
Navigate to the project directory in your terminal.
Install the required Python packages using the following command:
pip install -r requirements.txt

Configuration

Set up environment variables for the following:
EVE_CLIENT_ID: Your EVE Online OAuth2 client ID.
EVE_CLIENT_SECRET: Your EVE Online OAuth2 client secret.
EVE_CLIENT_SCOPE: OAuth2 scope for accessing EVE Online API.
APP_SECRET_KEY: Secret key for Flask session management.
Adjust the OAuth2 redirect URI in the authenticate route to match your deployment URL.

Usage

Open a terminal and navigate to the project directory.
Run the application using the following command:
python app.py
Access the application in your web browser at http://127.0.0.1:5000/.

Routes and Functionality

/: Displays a form for users to enter their character ID and corporation ID.
/pre_auth: Pre-authentication screen showing the authorization button.
/authenticate: Initiates the OAuth2 authentication process.
/callback: Callback route for receiving the OAuth2 authorization code.
/authorized: Displays a success message and a button to proceed to data presentation.
/data: Displays dashboard data retrieved from the EVE Online API.
/failure: Displays an error message for authentication failures.

Templates

The application uses HTML templates for rendering pages. The templates can be found in the templates directory.

Logging

The application logs messages using the logging module. The log level is set to INFO.

Data Presentation

The /data route retrieves and displays dashboard data from the EVE Online API. The data is presented in HTML tables.

Security

If deploying this application to production, make sure to configure secure session cookies and use HTTPS.

Acknowledgments

The code in this repository were created with a little help from Chat GPT by Jonathan Howard, an aspiring software developer with expertise in Agile Software Development and proficiency in various programming languages.
