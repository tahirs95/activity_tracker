from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from .models import ActivityTracker
import json
from datetime import timedelta, datetime, date
month = datetime.now() - timedelta(days=30)
week = datetime.now() - timedelta(days=7)
today = date.today()

# dateStr = today.strftime("%d %b %Y ")

def book(request, *args, **kwargs):
    daily_activities_dict = {}
    weekly_activities_dict = {}
    monthly_activities_dict = {}
    date_entry = "2019,7,22"
    y, m, d = map(int, date_entry.split(','))
    custom_date = datetime(y, m, d)

    custom_date_activities = ActivityTracker.objects.filter(date=custom_date)
    print(custom_date_activities)

    daily_activities = ActivityTracker.objects.filter(date=today)
    weekly_activities = ActivityTracker.objects.filter(date__gte=datetime.date(week))
    monthly_activities = ActivityTracker.objects.filter(date__gte=datetime.date(month))

    for i, daily_activity in enumerate(daily_activities):
        daily_activities_dict[i] = {
            "date":daily_activity.date.strftime("%d %b %Y"),
            "start_time":daily_activity.start_time.strftime("%H:%M"),
            "end_time":daily_activity.end_time.strftime("%H:%M"),
            "activity":daily_activity.activity.name
            }
        
    for i, weekly_activity in enumerate(weekly_activities):
        weekly_activities_dict[i] = {
            "date":weekly_activity.date.strftime("%d %b %Y"),
            "start_time":weekly_activity.start_time.strftime("%H:%M"),
            "end_time":weekly_activity.end_time.strftime("%H:%M"),
            "activity":weekly_activity.activity.name
            }
    
    for i, monthly_activity in enumerate(monthly_activities):
        monthly_activities_dict[i] = {
            "date":monthly_activity.date.strftime("%d %b %Y"),
            "start_time":monthly_activity.start_time.strftime("%H:%M"),
            "end_time":monthly_activity.end_time.strftime("%H:%M"),
            "activity":monthly_activity.activity.name
            }

    
    return render(request, "index.html", {'daily_dict':daily_activities_dict, 'week_dict':weekly_activities_dict, 'month_dict':monthly_activities_dict})

