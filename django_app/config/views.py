from django.shortcuts import redirect


# Redirect to login screen.
def index(request):
    return redirect('member:login')
