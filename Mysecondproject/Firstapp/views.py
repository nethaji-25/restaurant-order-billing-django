
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def Nethaji(request):
    a="Welcome to my home"
    return HttpResponse(a)

def Webpage(request):
    name="Nethaji"
    return render(request,template_name="first/Homepage.html",context={"name":name})


def Loginpage(request):
    a="Login to the application"
    return HttpResponse(a)

def Supportpage(request):
    a="Contact us at 9597364696 for any assistance"
    return HttpResponse(a)


