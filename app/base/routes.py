# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask import jsonify, render_template, redirect, request, url_for, abort
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user
)

from app import db, login_manager
from app.base import blueprint
from app.base.forms import LoginForm, CreateAccountForm
from app.base.models import User

from app.base.util import verify_pass

from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import sys
from api_cred import *

client = Client(account_sid, auth_token)

number_Id = []
messaging_service = 'test'

@blueprint.route('/')
def route_default():
    return redirect(url_for('base_blueprint.login'))

## Login & Registration

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if 'login' in request.form:
        
        # read form data
        username = request.form['username']
        password = request.form['password']

        # Locate user
        user = User.query.filter_by(username=username).first()
        
        # Check the password
        if user and verify_pass( password, user.password):

            login_user(user)
            return redirect(url_for('base_blueprint.route_default'))

        # Something (user or pass) is not ok
        return render_template( 'accounts/login.html', msg='Wrong user or password', form=login_form)

    if not current_user.is_authenticated:
        return render_template( 'accounts/login.html',
                                form=login_form)
    return redirect(url_for('home_blueprint.index'))

@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    login_form = LoginForm(request.form)
    create_account_form = CreateAccountForm(request.form)
    if 'register' in request.form:

        username  = request.form['username']
        email     = request.form['email'   ]

        # Check usename exists
        user = User.query.filter_by(username=username).first()
        if user:
            return render_template( 'accounts/register.html', 
                                    msg='Username already registered',
                                    success=False,
                                    form=create_account_form)

        # Check email exists
        user = User.query.filter_by(email=email).first()
        if user:
            return render_template( 'accounts/register.html', 
                                    msg='Email already registered', 
                                    success=False,
                                    form=create_account_form)

        # else we can create the user
        user = User(**request.form)
        db.session.add(user)
        db.session.commit()

        return render_template( 'accounts/register.html', 
                                msg='User created please <a href="/login">login</a>', 
                                success=True,
                                form=create_account_form)

    else:
        return render_template( 'accounts/register.html', form=create_account_form)

@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('base_blueprint.login'))

@blueprint.route('/shutdown')
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return 'Server shutting down...'

#1. Provision twilio sub-account

@blueprint.route('/provision', methods=['POST'])
def provision():
    global client
    global number_Id
    #reset number ID
    number_Id = []
    client = Client(account_sid, auth_token)
    username = request.get_json(force=True).get('username')
    #If user name is blank, abort with 401
    if not username:
        abort(401)

    account = client.api.accounts.create(friendly_name=username)
    client = Client(account.sid, account.auth_token)
    SID = {'sid': account.sid}

    return jsonify(SID);

#2. Purchase phone number

@blueprint.route('/purchase', methods=['POST'])
def purchase():
     global number_Id
     area = request.get_json(force=True).get('area')
     print(area, file=sys.stderr)
     local = client.available_phone_numbers('US').local.list(
         area_code=area,
         limit=1
     )

     #Return error if no phone numbers retured in list (area code not available)
     print(local, file=sys.stderr)
     if not local:
         number = {'number': 'No numbers in this area code avilable. Please wait or try with a different area code.'}
         return jsonify(number)

     for record in local:
        number = {'number': record.friendly_name}
        incoming_phone_number = client.incoming_phone_numbers \
            .create(phone_number=record.phone_number)
        print(incoming_phone_number.sid, file=sys.stderr)
        number_Id.append(incoming_phone_number.sid)
     return jsonify(number)


#3. Provision messaging service
@blueprint.route('/provision_m', methods=['POST'])

def provision_m():
     global messaging_service
     service_name = request.get_json(force=True).get('service_name')
     print(service_name, file=sys.stderr)
     service = client.messaging \
         .services \
         .create(
         status_callback='http://requestb.in/1234abcd',
         #5. programatically assign inbound request url.
         inbound_request_url='http://54.191.230.228:5001/sms',
         #7. disabled sticky sender
         sticky_sender = 'false',
         friendly_name=service_name
     )
     messaging_service=service.sid
     print(messaging_service, file=sys.stderr)
     service_name = {'service_name': service_name}
     return jsonify(service_name)


#4. Assign phone numbers to messaging service
@blueprint.route('/assign', methods=['POST'])
def assign_n():
    global messaging_service

    for record in number_Id:
     phone_number = client.messaging \
            .services(messaging_service) \
            .phone_numbers \
            .create(
            phone_number_sid=record
        )

     print(phone_number.sid, file=sys.stderr)
     status = 'All numbers added successfully'
     service_name = {'status': status}
     return jsonify(service_name)

#6 Webhook. (Callback URL has been set before)

@blueprint.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    """Respond to incoming message with a simple text message."""
    # Start our TwiML response
    resp = MessagingResponse()

    # Add a message
    resp.message("The Robots are coming! Head for the hills!")

    return str(resp)

#8 Send outbound SMS
@blueprint.route("/send", methods=['GET', 'POST'])
def send():
    global messaging_service
    send = request.get_json(force=True).get('send')
    print(send, file=sys.stderr)
    message = client.messages \
    .create(
         body='Revenge of the Sith was clearly the best of the prequel trilogy.',
         messaging_service_sid=messaging_service,
         to=send
     )

    status = 'Message sent successfully'
    service_name = {'status': status}
    return jsonify(service_name)
## Errors

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('page-403.html'), 403

@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('page-403.html'), 403

@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('page-404.html'), 404

@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('page-500.html'), 500
