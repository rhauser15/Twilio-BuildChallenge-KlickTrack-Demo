# Not my front end (Template), find it here: [Flask Dashboard - Argon Design](https://appseed.us/admin-dashboards/flask-boilerplate-dashboard-argon)


<h3> Installation: </h3>


```bash
$ # Get the code
$ git clone https://github.com/app-generator/flask-boilerplate-dashboard-argon.git
$ cd flask-boilerplate-dashboard-argon
$
$ # Virtualenv modules installation (Unix based systems)
$ virtualenv env
$ source env/bin/activate
$
$ # Virtualenv modules installation (Windows based systems)
$ # virtualenv env
$ # .\env\Scripts\activate
$
$ # Install modules - SQLite Database
$ pip3 install -r requirements.txt
$
$ # OR with PostgreSQL connector
$ # pip install -r requirements-pgsql.txt
$
$ # Set the FLASK_APP environment variable
$ (Unix/Mac) export FLASK_APP=run.py
$ (Windows) set FLASK_APP=run.py
$ (Powershell) $env:FLASK_APP = ".\run.py"
$
$ # Set up the DEBUG environment
$ # (Unix/Mac) export FLASK_ENV=development
$ # (Windows) set FLASK_ENV=development
$ # (Powershell) $env:FLASK_ENV = "development"
$
$ # Start the application (development mode)
$ # --host=0.0.0.0 - expose the app on all network interfaces (default 127.0.0.1)
$ # --port=5000    - specify the app port (default 5000)  
$ flask run --host=0.0.0.0 --port=5000
$
$ # Access the dashboard in browser: http://127.0.0.1:5000/
```

> Note: To use the app, please access the registration page and create a new user. After authentication, the app will unlock the private pages.


1. Once cloned create a file called api_cred.py with the following format: 

```
account_sid = "AC129dd7x"
auth_token  = "dxxxx"

```

2. Navigate to app/base/routes.py and modify the below function. Put your own public IP address in place of the 54.x.x

```

         #5. programatically assign inbound request url.
         inbound_request_url='http://54.x.x.228:5001/sms',
         
```

This ensures the webhook works correctly for responding to inbound messages. 

3. Type ```flask run```

4. Create a user name and login.

5. Navigate to the marketing page on the side bar. Step through provisioning a sub account, purcasing numbers, creating messaging service, assigning numbers. 

6. Send an outbound message using the messaging service. 

7. Respond to the message to confirm the webhook is working. 
