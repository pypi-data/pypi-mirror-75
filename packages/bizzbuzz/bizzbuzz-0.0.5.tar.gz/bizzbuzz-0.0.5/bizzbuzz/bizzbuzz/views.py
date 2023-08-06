from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from bizzbuzz.models import Preferences
from bizzbuzz.models import News
from bizzbuzz.forms import PrefForm
import time
from django.core import management
from bizzbuzz.management.commands import update_db
from datetime import datetime, time, timedelta


def index_view(request):
    return render(request,'bizzbuzz/index.html')

def login_view(request):
    if request.method == 'GET':
        return render(request, 'bizzbuzz/login.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:    #gets username and password, logs the user in
            login(request, user)
            #if they've never logged in before, go to select channels
            return redirect('home')
        else:
            messages.error(request, 'Username or password is incorrect')
            return render(request, 'bizzbuzz/login.html')

def logout_view(request):
    logout(request)
    return redirect('index')

def signup_view(request):
    if request.method == 'GET':
        return render(request, 'bizzbuzz/signup.html')
    elif request.method == 'POST':
        if request.POST.get('username') and request.POST.get('password'):
            #gets the fields from the form in signup.html and puts into database
            username = request.POST.get('username')
            password = request.POST.get('password')
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username, None, password)
                user.save()

                preference = Preferences(username=username)
                preference.save()
                #run 'SELECT * from auth_user' in query console to see contents of this table
                return redirect('login')
            else:
                messages.error(request, 'Username is already taken')
                return render(request, 'bizzbuzz/signup.html')
        else:
            messages.error(request, 'Please enter a valid username and password')
            return render(request, 'bizzbuzz/signup.html')

def home_view(request):
    if not request.user.is_authenticated or not Preferences.objects.get(username=request.user.username):
        return redirect('login')
    if request.method == 'POST' and 'run_script' in request.POST:
        # calls update_db.py in bizzbuzz/management/commands to update the database
        management.call_command('update_db')
        # go back to home page with new articles showing
        return redirect('home')

    else:
        # gather user's preferences to use in search later
        username = request.user.username
        preference = Preferences.objects.get(username=username)
        companies = ['apple', 'google', 'facebook', 'microsoft', 'amazon', 'samsung', 'ibm', 'twitter', 'netflix',
                     'oracle', 'sap', 'salesforce', 'tesla', 'spacex']
        if request.method == 'GET':
            preferred = []
            for i in companies: #gets the current values of each company, puts in appropriate list, and passes lists to HTML
                value = getattr(preference, i)
                if value is True:
                    preferred.append(i.upper())

        titles= []
        urls = []
        summaries = []
        indices = []
        sources = []
        dates = []
        i = 1

        for pref in preferred:
            #filter articles containing relevant company name
            news = News.objects.filter(company__icontains=pref)
            #hard coded 'applebee's' exception, can make more generic if other exceptions arise
            if pref.lower() == 'apple':
                news=news.exclude(title__icontains="applebee's")
            for n in news:
                #check for duplicate urls
                if getattr(n, 'url') not in urls:
                    titles.append(getattr(n, 'title'))
                    urls.append(getattr(n, 'url'))
                    summaries.append(getattr(n, 'summary'))
                    # dates.append(getattr(n, 'expiration_date'))
                    if str(datetime.now().date()) == str(getattr(n, 'expiration_date'))[0:10]:
                        dates.append(True)
                    else:
                        dates.append(False)
                    indices.append(i)
                    i+=1
                    #update with extra sources once we implement them
                    if 'nytimes.com' in getattr(n, 'url').lower():
                        sources.append('NYTIMES')
                    elif 'techtimes.com' in getattr(n, 'url').lower():
                        sources.append('TECH_TIMES')
                    elif 'forbes.com' in getattr(n, 'url').lower():
                        sources.append('FORBES')
                    else:
                        sources.append('BI')
        #zip together titles, urls, summaries, sources, and send to home.html
        return render(request, 'bizzbuzz/home.html', {'name': username, 'articles' : zip(titles, urls, summaries, sources, indices, dates), 'articles2' : zip(titles, urls, summaries, sources, indices, dates)})

def selectchannel_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    username = request.user.username
    preference = Preferences.objects.get(username=username) #.values_list('apple', 'microsoft', 'google', 'facebook')
    companies = ['apple', 'google', 'facebook', 'microsoft', 'amazon', 'samsung', 'ibm', 'twitter', 'netflix',
                 'oracle', 'sap', 'salesforce', 'tesla', 'spacex']
    if request.method == 'GET':
        preferred = []
        not_preferred = []
        for i in companies: #gets the current values of each company, puts in appropriate list, and passes lists to HTML
            value = getattr(preference, i)
            if value is False:
                not_preferred.append(i.upper())
            else:
                preferred.append(i.upper())

        return render(request,'bizzbuzz/selectchannel.html', {'name': request.user.username, 'preferred': preferred, 'not_preferred': not_preferred, 'preference': preference})
    elif request.method == 'POST':
        MyPrefForm = PrefForm(request.POST)
        changePref = Preferences.objects.get(username=username)
        if MyPrefForm.is_valid():
            changePref.amazon = True if "amazon" in request.POST else False
            changePref.apple = True if "apple" in request.POST else False
            changePref.facebook = True if "facebook" in request.POST else False
            changePref.google = True if "google" in request.POST else False
            changePref.ibm = True if "ibm" in request.POST else False
            changePref.microsoft = True if "microsoft" in request.POST else False
            changePref.netflix = True if "netflix" in request.POST else False
            changePref.oracle = True if "oracle" in request.POST else False
            changePref.salesforce = True if "salesforce" in request.POST else False
            changePref.samsung = True if "samsung" in request.POST else False
            changePref.sap = True if "sap" in request.POST else False
            changePref.spacex = True if "spacex" in request.POST else False
            changePref.tesla = True if "tesla" in request.POST else False
            changePref.twitter = True if "twitter" in request.POST else False
            changePref.save()
        return redirect('selectchannel')