from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib import messages
from datetime import datetime
from django.core.paginator import Paginator
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
            activity:Activity = activity_form.save(commit=False)
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

def update_activity_view(request:HttpRequest, activity_id):
    activity = Activity.objects.get(pk=activity_id)
    categories = ActivityCategory.objects.all()
    activity_names = ActivityName.objects.none()
    if request.method == 'POST':
        form = ActivityForm(request.POST,request.FILES, instance=activity)
        if form.is_valid():
            form.save()
            messages.success(request, 'Activity updated successfully!','danger')
            return redirect('main:home_page_view')
        else:
            messages.error(request, 'There was an error updating the activity.')

    else:
        form = ActivityForm(instance=activity)

    return render(request, 'activities/update_activity.html', {
        'form': form,
        'activity': activity,
        'categories': categories,
        "activities_name": activity_names,
    })


def get_activities(request:HttpRequest, category_id):
    activities = ActivityName.objects.filter(category_id=category_id)
    return JsonResponse({'activities': list(activities.values('id', 'name'))})


def detail_activity_view(request:HttpRequest,activity_id):

    activities=Activity.objects.get(pk=activity_id)
    
    return render(request,"activities/activity_detail.html",{"activities":activities})


def all_activities_view(request : HttpRequest):
    activities = Activity.objects.filter(status='approved').order_by('start_date')
    activities_category=ActivityCategory.objects.all()
    activities_name=ActivityName.objects.none()
    
    
    if "search" in request.GET and len(request.GET["search"]) >= 3:
        activities = Activity.objects.filter(title__contains=request.GET["search"])
        
    if "category" in request.GET and request.GET["category"]:

        activities = activities.filter(name__category__id=request.GET["category"])

    if "name" in request.GET and request.GET["name"]:
        activities = activities.filter(name__id=request.GET["name"])

    page_number = request.GET.get("page")  
    paginator = Paginator(activities,4)
    activities_page = paginator.get_page(page_number)
    return render(request,"activities/all_activities.html",context={"activities":activities_page,'categories':activities_category,'activities_name':activities_name})
