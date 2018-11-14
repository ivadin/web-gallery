from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .forms import UserRegisterForm, AddImage
from .models import Images

import os
from v2.settings import net


# Create your views here.

def home_page(request):
    if request.POST:
        username = request.POST.get("email", "")
        password = request.POST.get("password", "")
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/gallery')
        else:
            return render(request, 'home_page.html', {'login_error': True})
    else:
        html = render(request, "home_page.html")
        return HttpResponse(html)


def logout(request):
    auth.logout(request)
    return redirect('/')


def registration(request):
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        password = form.cleaned_data.get("password")
        user.set_password(password)
        user.save()
        new_user = auth.authenticate(username=user.username, password=password)
        auth.login(request, new_user)
        return redirect("../")
    context = {
        "form": form
    }
    return render(request, "registration.html", context)


def user_home(request):
    html = render(request, "user_home_page.html")
    return HttpResponse(html)


def images(request):
    curuser = request.user

    objects_to_page_list = Images.objects.filter(users_id=curuser.id).order_by("-timestamp")

    query = request.GET.get("query")
    if query:
        objects_to_page_list = objects_to_page_list.filter(
            Q(title__icontains=query)
        ).distinct()

    paginator = Paginator(objects_to_page_list, 12)
    page = request.GET.get('page')
    try:
        objects_to_page = paginator.page(page)
    except PageNotAnInteger:
        objects_to_page = paginator.page(1)
    except EmptyPage:
        objects_to_page = paginator.page(paginator.num_pages)

    context = {
        'image_db': objects_to_page
    }
    return render(request, "images.html", context)


def image(request, image_id=1):
    if request.POST:
        i = Images.objects.get(id=image_id)
        image_path = i.image.path
        Images.objects.filter(id=image_id).delete()
        os.remove(image_path)
        return redirect('/gallery')

    return render(request, 'image.html', {'image': Images.objects.get(id=image_id)})


def add_image(request):
    form = AddImage(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save()
        print("location:", instance.image.path)
        instance.title = net.detect(instance.image.path)
        instance.users = request.user
        instance.save()
        messages.success(request, "Successfully")
        return redirect("/gallery")
    context = {
        "form": form
    }
    return render(request, "add_image.html", context)
