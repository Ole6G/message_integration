from django.shortcuts import render


def index(request):
    return render(request, 'email_integration/index.html')
