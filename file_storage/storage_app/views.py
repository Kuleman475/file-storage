from django.http import HttpResponse


def index(request):
    return HttpResponse("This is a simple Django-powered file storage web app. Users will be able to upload files, view a list of uploaded files, and download them anytime. The project also includes pages like Home, About, and Contact to explain what the app does and how to get in touch.")

def login(request):
    return HttpResponse("LOGIN PAGE")