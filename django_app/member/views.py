from django.shortcuts import render

from config import settings


def login(request):
    facebook_app_id = settings.config['facebook']['app_id']
    context = {
        'facebook_app_id': facebook_app_id,
    }
    return render(request, 'member/login.html', context)


def login_facebook(request):
    print(request.GET)
