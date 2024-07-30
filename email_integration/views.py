from django.shortcuts import render
from django.http import JsonResponse
from .models import Message


def index(request):
    return render(request, 'email_integration/index.html')


def get_messages(request):
    messages = Message.objects.all().values()
    return JsonResponse(list(messages), safe=False)
