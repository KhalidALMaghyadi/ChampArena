from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib import messages
from datetime import datetime
from .forms import ActivityForm
from .models import Activity, ActivityName, ActivityCategory

def new_activity_view(request: HttpRequest):
    if not request.user.is_authenticated:
        messages.warning(request, "You have to log in first!", "alert-warning")
        return redirect("main:home_page_view")

    today = datetime.now().strftime('%Y-%m-%dT%H:%M')
    activity_form = ActivityForm()  
    activity_categories = ActivityCategory.objects.all()
    activity_names = ActivityName.objects.none()

    if request.method == "POST":
        activity_form = ActivityForm(request.POST, request.FILES)
        print(request.POST['name'])
        if activity_form.is_valid():
            activity = activity_form.save(commit=False)
            activity.created_by = request.user
            activity.save()

            messages.success(request, "Created activity successfully! Waiting for approval.", "alert-success")
            return redirect("main:home_page_view")
        else:
            print(activity_form.errors)
            messages.error(request, "There was an error with your form. Please try again.", "alert-danger")

    return render(request, "activities/new_activity.html", context={
        "form": activity_form,
        "categories": activity_categories,
        "activities_name": activity_names,
        "today": today
    })

def get_activities(request:HttpRequest, category_id):
    activities = ActivityName.objects.filter(category_id=category_id)
    return JsonResponse({'activities': list(activities.values('id', 'name'))})
