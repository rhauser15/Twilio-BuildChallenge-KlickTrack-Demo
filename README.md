# FRONT END DESIGN/TEMPLATE: [Argon Dashboard Flask](https://www.creative-tim.com/product/argon-dashboard-flask) [![Tweet](https://img.shields.io/twitter/url/http/shields.io.svg?style=social&logo=twitter)]#


<h3>This project is up and running on AWS here:# </h3>


<h4> Installation: </h4>

$ cd Twilio-BuildChallenge-KlickTrack-Demo
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


1. Create a new account or loging with credentials user:test/pass:test. 

2. Navigate to marketing tab on left. 

3. Step through to provision subaccount, purchase numbers, create a messaging service, assign numbers to messaging service and send message to number. 

4. Text the message back to test webhook functionality. 
