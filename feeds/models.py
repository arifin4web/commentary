import json
from django.db import models
from django.template.defaultfilters import linebreaks_filter
from django.utils.six import python_2_unicode_compatible
from channels import Group


@python_2_unicode_compatible
class Event(models.Model):
    # Event title
    title = models.CharField(max_length=255)
    # Slug for routing (both HTML pages and WebSockets)
    slug = models.SlugField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """
        Returns the URL to view the Event.
        """
        return "/event/%s/" % self.slug

    @property
    def group_name(self):
        """
        Returns the Channels Group name to use for sending notifications.
        """
        return "event-%s" % self.id


@python_2_unicode_compatible
class Feed(models.Model):

    event = models.ForeignKey(Event, related_name="feeds")
    comment = models.TextField()
    user_name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "#%i: %s" % (self.id, self.body_intro())

    def body_intro(self):
        """
        Short first part of the body to show in the admin or other compressed
        views to give you some idea of what this is.
        """
        return self.comment[:50]

    def html_body(self):
        """
        Returns the rendered HTML body to show to browsers.
        You could change this method to instead render using RST/Markdown,
        or make it pass through HTML directly (but marked safe).
        """
        return linebreaks_filter(self.comment)

    def send_notification(self):
        """
        Sends a notification to everyone in our Event's group with our
        content.
        """
        # Make the payload of the notification. We'll JSONify this, so it has
        # to be simple types, which is why we handle the datetime here.
        notification = {
            "id": self.id,
            "user_name": self.user_name,
            "html": self.html_body(),
            "created": self.created.strftime("%a %d %b %Y %H:%M"),
        }
        # Encode and send that message to the whole channels Group for our
        # Event. Note how you can send to a channel or Group from any part
        # of Django, not just inside a consumer.
        Group(self.event.group_name).send({
            # WebSocket text frame, with JSON content
            "text": json.dumps(notification),
        })

    def save(self, *args, **kwargs):
        """
        Hooking send_notification into the save of the object
        """
        result = super(Feed, self).save(*args, **kwargs)
        self.send_notification()
        return result
