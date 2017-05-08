import requests
from django.shortcuts import render

from config import settings

app_id = settings.config['facebook']['app_id']


def login(request):
    context = {
        'app_id': app_id,
    }
    return render(request, 'member/login.html', context)


def login_facebook(request):
    redirect_uri = 'http://localhost:8080/member/login/facebook/'
    secret_code = settings.config['facebook']['secret_code']
    app_access_token = '{app_id}|{secret_code}'.format(
        app_id=app_id,
        secret_code=secret_code
    )

    # Redirect Facebook loign from login()
    # Once logged in, 'code' parameter is added to request.GET
    # Return to login_facebook() using 'redirect_uri'
    # Then...
    if request.GET.get('code'):
        code = request.GET.get('code')

        # Request access_token using received 'code'
        url_request_access_token = 'https://graph.facebook.com/v2.9/oauth/access_token'
        params = {
            'client_id': app_id,
            'redirect_uri': redirect_uri,
            'client_secret': secret_code,
            'code': code,
        }
        r = requests.get(url_request_access_token, params=params)
        dict_access_token = r.json()
        user_access_token = dict_access_token['access_token']

        # Authenticate token using user_access_token and app_access_token
        url_debug_token = 'https://graph.facebook.com/debug_token'
        params = {
            'input_token': user_access_token,
            'access_token': app_access_token
        }
        r = requests.get(url_debug_token, params=params)
        dict_debug_token = r.jsoin()
        user_id = dict_debug_token['data']['user_id']
