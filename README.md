
# Authentication in Django with EMail OTP Verification

The implemented authentication features in the Django application provide user registration, login, logout, and email verification functionalities. Here's a brief explanation of each feature and how to use them:

#### 1. User Registration (register view):
        Users can register by providing a unique username, email, and password.
        The system checks for existing usernames and emails to ensure uniqueness.
        After successful registration, an OTP (One-Time Password) is generated and sent to the user's email for verification.
        Upon verification, the user gains access to the site.

Url Route:
```bash
http://127.0.0.1:8000/register/
```

#### 2. Email Verification (verify_otp view):
        Users receive an OTP via email after registration.
        They can enter the OTP on the verification page to confirm their email address.
        If the OTP matches the one sent, the user's email is marked as verified, granting them full access to the site.

Url Route:
```bash
http://127.0.0.1:8000/verify_otp/
```

#### 3.Login (login view):
        Existing users can log in using their username and password.
        Upon successful authentication, users are redirected to the homepage.
        If authentication fails, appropriate error messages are displayed.

Url Route:
```bash
http://127.0.0.1:8000/login/
```

#### 4. Logout (logout view):
        Users can log out from their current session.
        This feature clears the user's session and redirects them to the login page.

Url Route:
```bash
http://127.0.0.1:8000/logout/
```

#### 2. Access Control (aeditProfile View):
        Certain views, such as the edit profile page, are restricted to logged-in users.
        Additionally, access to sensitive functionalities may require email verification.

Url Route:
```bash
http://127.0.0.1:8000/editProfile/
```

#### To use these features:

To register, users navigate to the registration page (/register) and fill out the required fields. They will receive an email with an OTP for verification.


After registering, users verify their email by entering the OTP on the verification page (/verify_otp).


Once verified, users can log in using their credentials on the login page (/login) and access the site's features.


Users can log out at any time by clicking the logout link, which clears their session and redirects them to the login page.

These authentication features ensure secure user registration, login, and access control, enhancing the overall security and usability of the application.






## Documentation





### Prerequisites

Before you begin, ensure you have the following installed on your computer:

    Python (version 3.X or higher)
    pip (Python package manager)


### Installation

1. Clone the project repository from https://github.com/herohit/Day-1.
```bash
    git clone https://github.com/herohit/Day-1
```
2. Navigate to the project directory i.e Day-1.
```bash
    cd project-directory
```


3. Create a virtual environment .
```bash
    python -m venv env
```
4. Activate the virtual environment.
```bash
    On Windows:  .\env\Scripts\activate
```

```bash
On macOS and Linux:  source env/bin/activate
```
5. Install project dependencies.

```bash
pip install -r requirements.txt
```


## Configuration

1. Open the settings.py file in the following  directory.

```bash
Day-1/EmailAuth/EmailAuth
```

2. Update the following settings as necessary:

    DATABASES: Configure database settings (if applicable).

```bash
    DATABASES['default'] =dj_database_url.parse( 'ENTER YOUR DATABASE EXTERNAL URL')
```

3. Create database tables by running migrations.
```bash
python manage.py migrate
```

### Local Database Setup
3. If using local database you needed to install PostgreSQL.

* Download and install PostgreSQL from the official website: PostgreSQL Downloads.
* Follow the installation instructions provided for your operating system.

4. Create Database:
* Open the PostgreSQL command-line interface (psql) or a graphical client like pgAdmin.
* Log in to your PostgreSQL server as a superuser or a user with administrative privileges.
* Create a new database for your Django project.

5 Database Configuration:

* Open the settings.py file in your Django project's directory (project-name/project-name).
* Update the DATABASES setting to use PostgreSQL:

```bash
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_database_name',
        'USER': 'your_database_username',
        'PASSWORD': 'your_database_password',
        'HOST': 'localhost',  # Or the hostname where your PostgreSQL server is running
        'PORT': '5432',       # Default PostgreSQL port
    }
}
```

4. Apply Migrations:

```bash
python manage.py migrate
```



## Setup SMTP

1. In your settings.py file, include a template for SMTP configuration. You can define placeholders for user-specific values such as email host, port, username, password, etc.

For example:
```bash
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'your_smtp_host'
EMAIL_PORT = 'your_smtp_port'
EMAIL_HOST_USER = 'your_smtp_username'
EMAIL_HOST_PASSWORD = 'your_smtp_password'
EMAIL_USE_TLS = True  # Or False depending on your SMTP server settings
```

2. Navigate to authentication/views.py and in register view uncomment the following line:

```bash
if not send_otp_email(email, otp):
    Failed to send email, handle error
    return HttpResponse('Failed to send OTP email. Please try again later.')
```

3. Go to models.py and uncomment this line marked as #.
```bash
def set_email_verification_code(self):
        other code here
        # send_otp_email(self.email, self.email_verification_code)
```
## Running the Project

1. Navigate to the project_directory where the manage.py is located and Start the development server.

```bash
python manage.py runserver
```

2. Open a web browser and navigate to http://127.0.0.1:8000/ (or the specified URL and port).

3. You should now see the homepage of the project.

4. You now need to register for an account and all set.


## Support

If you encounter any issues or have questions about the project setup, please don't hesitate to contact Rohit Negi at rohitnegi323@gmail.com.