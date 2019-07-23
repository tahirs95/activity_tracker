from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from .models import ActivityTracker, Activity
import json
from datetime import timedelta, datetime, date
month = datetime.now() - timedelta(days=30)
week = datetime.now() - timedelta(days=7)
today = date.today()

# dateStr = today.strftime("%d %b %Y ")

def get_records(request, *args, **kwargs):
    daily_activities_dict = {}
    weekly_activities_dict = {}
    monthly_activities_dict = {}
    date_entry = "2019,7,22"
    y, m, d = map(int, date_entry.split(','))
    custom_date = datetime(y, m, d)

    custom_date_activities = ActivityTracker.objects.filter(date=custom_date)

    daily_activities = ActivityTracker.objects.filter(date=today)
    weekly_activities = ActivityTracker.objects.filter(date__gte=datetime.date(week))
    monthly_activities = ActivityTracker.objects.filter(date__gte=datetime.date(month))

    for i, daily_activity in enumerate(daily_activities):
        daily_activities_dict[i] = {
            "date":daily_activity.date.strftime("%d %b %Y"),
            "start_time":daily_activity.start_time.strftime("%H:%M"),
            "end_time":daily_activity.end_time.strftime("%H:%M"),
            "activity":daily_activity.activity.name,
            "elapsed_time":daily_activity.elapsed_time
            }
        
    for i, weekly_activity in enumerate(weekly_activities):
        weekly_activities_dict[i] = {
            "date":weekly_activity.date.strftime("%d %b %Y"),
            "start_time":weekly_activity.start_time.strftime("%H:%M"),
            "end_time":weekly_activity.end_time.strftime("%H:%M"),
            "activity":weekly_activity.activity.name,
            "elapsed_time":weekly_activity.elapsed_time

            }
    
    for i, monthly_activity in enumerate(monthly_activities):
        monthly_activities_dict[i] = {
            "date":monthly_activity.date.strftime("%d %b %Y"),
            "start_time":monthly_activity.start_time.strftime("%H:%M"),
            "end_time":monthly_activity.end_time.strftime("%H:%M"),
            "activity":monthly_activity.activity.name,
            "elapsed_time":monthly_activity.elapsed_time

            }

    return JsonResponse({"daily_dict":daily_activities_dict, "week_dict":weekly_activities_dict, "month_dict":monthly_activities_dict})

@csrf_exempt
def add_record(request):
    request_data = json.loads(request.body)

    # loading request data
    date = request_data["date"]
    start_time = request_data["start_time"]
    end_time = request_data["end_time"]
    activity_id = request_data["activity"]
    elapsed_time = request_data["elapsed_time"]

    # date_entry = "2019,7,22"
    y, m, d = map(int, date.split(','))
    custom_date = datetime(y, m, d)

    activity = Activity.objects.get(id = activity_id)
    row = ActivityTracker(date=custom_date, start_time=start_time, end_time=end_time, activity=activity, elapsed_time=elapsed_time)
    row.save()
    return JsonResponse({"status":"True", "message":"Activity has been added."})

