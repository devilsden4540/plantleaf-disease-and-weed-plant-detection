from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from .models import *
from django.db.models import Q
# Create your views here.


def index(request):
    return render(request, "index.html")


def userreg(request):
    msg = ''
    if request.method == "POST":
        name = request.POST['txtName']
        address = request.POST['txtAddress']
        email = request.POST['txtEmail']
        contact = request.POST['txtContact']
        pwd = request.POST['txtPwd']
        dist = request.POST['dist']
        pin = request.POST['pin']
        user = CustomUser.objects.create_user(
            username=email, password=pwd, user_type='User')
        user.save()
        customer = Users.objects.create(
            name=name, email=email, phone=contact, address=address, district=dist, pin=pin, user=user)
        customer.save()
        msg = "Registration successful"
    return render(request, "userreg.html", {"msg": msg})


def officerreg(request):
    msg = ''
    if request.method == "POST":
        name = request.POST['txtName']
        address = request.POST['txtAddress']
        email = request.POST['txtEmail']
        contact = request.POST['txtContact']
        pwd = request.POST['txtPwd']
        dist = request.POST['dist']
        pin = request.POST['pin']
        try:
            user = CustomUser.objects.create_user(
                username=email, password=pwd, user_type='Officer', is_active=0)
            user.save()
            park = Officer.objects.create(
                name=name, email=email, phone=contact, address=address, district=dist, pin=pin, user=user)
            park.save()
        except:
            msg = "Some Error Occured"
    return render(request, "officerreg.html", {"msg": msg})


def login(request):
    msg = ""
    if (request.POST):
        email = request.POST.get("txtUname")
        password = request.POST.get("txtPwd")
        user = authenticate(username=email, password=password)
        print(user)
        if user is not None:
            if user.user_type == 'Admin':
                return redirect("/adminhome")
            elif user.user_type == 'User':
                request.session['uid'] = user.id
                return redirect('/userhome')
            elif user.user_type == 'Officer':
                request.session['uid'] = user.id
                return redirect('/officerhome')
        else:
            msg = "Invalid Credentials"

    return render(request, "commonlogin.html", {"msg": msg})


def adminhome(request):

    return render(request, "adminhome.html")


def adminofficer(request):
    data = Officer.objects.filter(
        user__is_active=1).order_by("user__is_active")
    if "sts" in request.GET:
        data = Officer.objects.filter(
            user__is_active=0).order_by("user__is_active")

    return render(request, "adminofficer.html", {"data": data})


def updateuser(request):
    id = request.GET['id']
    status = int(request.GET['status'])
    if status == 1:
        rest = CustomUser.objects.get(id=id)
        rest.is_active = 1
        rest.save()
    elif status == -1:
        rest = CustomUser.objects.get(id=id)
        rest.delete()
    return redirect("/adminofficer")


def admincustomer(request):
    rest = Users.objects.all()
    return render(request, "adminusers.html", {"data": rest})


def officerhome(request):
    uid = request.session['uid']
    pid = Officer.objects.get(user=uid)
    request.session['pid'] = pid.id
    return render(request, "officerhome.html")


def userhome(request):
    uid = request.session['uid']
    cid = Users.objects.get(user=uid)
    request.session['cid'] = cid.id
    return render(request, "userhome.html")
