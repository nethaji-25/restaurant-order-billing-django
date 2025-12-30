from django.shortcuts import render, redirect

from .models import Employeedetails
from .form import Employeeform
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages


from django.db.models import Q

# Create your views here.

@login_required(login_url='logincrud')
def Getemployees(request):
    e=Employeedetails.objects.all()
    return render(request,template_name="CRUD/empdetails.html",context={"e":e})

def Addemployees(request):
    form=Employeeform()
    if request.method=="POST":
        e=Employeeform(request.POST)
        if e.is_valid():
            e.save()
            return redirect("crudget")

    return render(request,template_name="CRUD/Register.html",context={"form":form})

def Deleteemployee(request,id):
    e=Employeedetails.objects.get(id=id)
    e.delete()
    return redirect("crudget")

def Updateemployee(request,id):
    e=Employeedetails.objects.get(id=id)
    if request.method=="POST":
        a=Employeeform(request.POST,instance=e)
        if a.is_valid():
            a.save()
            return redirect('crudget')
    return render(request,template_name="CRUD/update.html",context={"e":e})


def Searchemployee(request):
    a=request.GET.get("details")
    if a:
        e=Employeedetails.objects.filter(Q(Empname__icontains=a) | Q(Empid__icontains=a) | Q(Empcity__icontains=a))
    else:
        e=Employeedetails.objects.all()
    return render(request,template_name="CRUD/empdetails.html",context={"e":e})





def loginuser(request):
    if request.user.is_authenticated:
        return redirect('crudget')
    if request.method=="POST":
        usr=request.POST.get("loginid")
        passi=request.POST.get("password")

        a=authenticate(request,username=usr,password=passi)
        if a is not None:
            login(request,a)
            return redirect('crudget')
        else:
            messages.error(request,"Invalid username or password")

    return render(request,template_name="CRUD/Homepage.html")

def logoutuser(request):
    logout(request)
    return redirect('logincrud')

