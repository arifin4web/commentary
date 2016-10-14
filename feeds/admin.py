from django.contrib import admin
from .models import Event, Feed


admin.site.register(
    Event,
    list_display=["id", "title", "slug"],
    list_display_links=["id", "title"],
    ordering=["title"],
    prepopulated_fields={"slug": ("title",)},
)


admin.site.register(
    Feed,
    list_display=["id", "event", "user_name","created", "body_intro"],
    ordering=["-id"],
)
