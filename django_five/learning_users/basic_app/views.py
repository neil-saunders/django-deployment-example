from django.shortcuts import render
from basic_app.forms import UserForm,UserProfileInfoForm

from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request,'basic_app/index.html')

@login_required
def special(request):
    return HttpResponse("You are logged in")


@login_required # decorator
def user_logout(request):
    logout(request) # built in logout function
    return HttpResponseRedirect(reverse('index'))

def register(request):

    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save() # grabbing user form + saving to database
            user.set_password(user.password) # hashing password - goes to settings.py and sets as hashing
            user.save()

            profile = profile_form.save(commit=False) # dont want to commit to database yet in case it collisions with the above
            profile.user = user # sets up 1 to 1 relationship (as in model OneToOneFIeld)

            if 'profile_pic' in request.FILES: # using request.FILES to find different media types
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered = True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request,'basic_app/registration.html',
                                        {'user_form':user_form,
                                        'profile_form':profile_form,
                                        'registered':registered})


def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username') # gets POST from username in HTML
        password = request.POST.get('password')

        user = authenticate(username=username,password=password) # django function to authenticate user for you

        if user:
            if user.is_active:
                login(request,user) # built in django function
                return HttpResponseRedirect(reverse('index')) # sends user back to homepage
            else:
                return HttpResponse("Account Not Active")
        else:
            print("Someone tried to login and failed!")
            print("Username: {} and password {}".format(username,password))
            return HttpResponse("invalid login details supplied")
    else:
        return render(request,'basic_app/login.html',{}) # send them to login page?
