import requests
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect

from config import settings

APP_ID = settings.config['facebook']['app_id']


def login(request):
    context = {
        'app_id': APP_ID,
    }
    return render(request, 'member/login.html', context)


def logout(request):
    logout(request)
    return redirect('index')


def login_facebook(request):
    REDIRECT_URI = 'http://localhost:8080/member/login/facebook/'
    SECRET_CODE = settings.config['facebook']['secret_code']
    APP_ACCESS_TOKEN = '{app_id}|{secret_code}'.format(
        app_id=APP_ID,
        secret_code=SECRET_CODE
    )

    # Redirect Facebook loign from login()
    # Once logged in, 'code' parameter is added to request.GET
    # Return to login_facebook() using 'redirect_uri'
    # Then...
    if request.GET.get('code'):
        CODE = request.GET.get('code')

        # Request access_token using received 'code'
        url_request_access_token = 'https://graph.facebook.com/v2.9/oauth/access_token'
        params = {
            'client_id': APP_ID,
            'redirect_uri': REDIRECT_URI,
            'client_secret': SECRET_CODE,
            'code': CODE,
        }
        r = requests.get(url_request_access_token, params=params)
        dict_access_token = r.json()
        USER_ACCESS_TOKEN = dict_access_token['access_token']

        # Authenticate token using user_access_token and app_access_token
        url_debug_token = 'https://graph.facebook.com/debug_token'
        params = {
            'input_token': USER_ACCESS_TOKEN,
            'access_token': APP_ACCESS_TOKEN
        }
        r = requests.get(url_debug_token, params=params)
        dict_debug_token = r.json()
        USER_ID = dict_debug_token['data']['user_id']

        # Authenticate with only FB ID then return to index page
        user = authenticate(facebook_id=USER_ID)
        login(request, user)
        return redirect('index')
