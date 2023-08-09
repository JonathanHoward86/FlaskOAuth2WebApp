"""
This is my webapp for eve oauth2 and chris's dashboard display
"""

import base64
import os
import uuid
import logging
from urllib.parse import urlencode
import requests
from flask import Flask, render_template, redirect, request, session


app = Flask(__name__)

eve_client_id = os.environ.get("EVE_CLIENT_ID")
eve_client_secret = os.environ.get("EVE_CLIENT_SECRET")
eve_client_scope = os.environ.get("EVE_CLIENT_SCOPE")
app.secret_key = os.environ.get("APP_SECRET_KEY")
logging.basicConfig(level=logging.INFO)
logging.info('This is an informational message')


@app.route('/', methods=['GET', 'POST'])
def home():
    """
    Home
    """
    if request.method == 'POST':
        session['character_id'] = request.form.get('character_id')
        session['corporation_id'] = request.form.get('corporation_id')
        return redirect('/pre_auth')
    return render_template("home.html", show_auth_button=False)


@app.route('/pre_auth', methods=['GET', 'POST'])
def pre_auth():
    """
    Pre-authentication screen, shows the authorization button
    """
    return render_template("home.html", show_auth_button=True)


@app.route('/authenticate', methods=['GET', 'POST'])
def authenticate():
    """
    Authenticate
    """
    state = uuid.uuid4().hex
    session['state'] = state

    params = {
        'response_type': 'code',
        'redirect_uri': 'https://evecorpauthentication.azurewebsites.net/'
        'callback/',
        'client_id': eve_client_id,
        'scope': eve_client_scope,
        'state': state,
    }
    url = 'https://login.eveonline.com/v2/oauth/authorize/?' + urlencode(
        params
    )

    return redirect(url)


@app.route("/callback/", methods=['GET', 'POST'])
def callback():
    """
    Callback
    """
    token = None
    refresh = None

    if request.args.get('state') != session.get('state'):
        return redirect('/failure')

    code = request.args.get('code')
    app_auth = base64.b64encode(
        (eve_client_id + ':' + eve_client_secret).encode('utf-8')
        ).decode('utf-8')

    headers = {
        'Authorization': 'Basic ' + app_auth,
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'login.eveonline.com',
    }

    payload = {
        'grant_type': 'authorization_code',
        'code': code,
        }

    response = requests.post(
        'https://login.eveonline.com/v2/oauth/token',
        headers=headers,
        data=payload,
        timeout=1000
    )
    token = response.json().get('access_token')
    refresh = response.json().get('refresh_token')

    if token:
        session['token'] = token
        session['refresh'] = refresh

        headers = {
            'Authorization': 'Bearer ' + token,
        }

        return redirect("/authorized")

    else:
        return redirect("/failure")


@app.route("/authorized", methods=['GET', 'POST'])
def authorization_successful():
    """
    Authorized
    """
    return render_template('authorized.html', token=session.get('token'))


@app.route("/data", methods=['GET', 'POST'])
def data_presentation():
    """
    Data Presentation
    """
    token = session.get('token')
    character_id = session.get('character_id')
    corporation_id = session.get('corporation_id')

    if not token:
        return redirect('/failure')

    headers = {
        'Authorization': 'Bearer ' + token,
    }

    urls = [
        f'https://esi.evetech.net/latest/corporations/{corporation_id}/fw/stats/?datasource=tranquility',
        f'https://esi.evetech.net/latest/characters/{character_id}/fw/stats/?datasource=tranquility'
    ]

    data = {}
    for url in urls:
        response = requests.get(url, headers=headers, timeout=1000)
        url_data = response.json()
        data[url] = url_data

    avatar_response = requests.get(
        f'https://esi.evetech.net/latest/characters/{character_id}/portrait/?datasource=tranquility',
        headers=headers,
        timeout=1000
    )
    avatar_url = None
    if avatar_response.status_code == 200:
        avatar_json = avatar_response.json()
        avatar_url = avatar_json.get('px128x128')

    session['data'] = data

    return render_template('data.html', data=data, character_id=character_id, avatar_url=avatar_url)


@app.route("/failure")
def handle_failure():
    """
    Failure!
    """
    return render_template("failure.html")


if not app.debug:
    app.config.update(
        SESSION_COOKIE_SECURE=True,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE='None',
    )
