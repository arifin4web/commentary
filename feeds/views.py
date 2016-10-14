from django.shortcuts import render, get_object_or_404
from django.db.models import Max
from .models import Event, Feed
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse
import json


def home(request):
    """
    Root page view. Just shows a list of Events.
    """
    # Get a list of events, ordered by the date of their most recent
    # post, descending (so ones with stuff happening are at the top)
    events = Event.objects.annotate(
        max_created=Max("feeds__created")
    ).order_by("-max_created")

    # Render that in the index template
    return render(request, "home.html", {
        "events": events,
    })


def event(request, slug):
    """
    Shows an individual event page.
    """
    # Get the event by slug
    event = get_object_or_404(Event, slug=slug)

    # Render it with the posts ordered in descending order.
    # If the user has JavaScript enabled, the template has JS that will
    # keep it updated.
    return render(request, "event.html", {
        "event": event,
        "feeds": event.feeds.order_by("-created"),
    })


@csrf_protect
def comment(request):
    data={}
    data["message"] = "Invalid Request"
    status_code=500

    if request.POST:
        try:
            feed = Feed()
            feed.event = Event.objects.get(id=request.POST.get("event"))
            feed.comment = request.POST.get("comment")
            feed.user_name = request.POST.get("name")
            feed.save()
            data["message"] = 'Successfull'
            status_code=200
        except exception as e:
            print(e)
            data["message"] = str(e)
            status_code=500
    return HttpResponse(json.dumps(data),content_type="application/json",status=status_code)
