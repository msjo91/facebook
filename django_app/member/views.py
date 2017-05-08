from django.shortcuts import render


def login(request):
    context = {}
    return render(request, 'member/login.html', context)
