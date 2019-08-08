from django.urls import path

from django.contrib import admin

admin.autodiscover()

import hello.views
import ifttt.views

# To add a new path, first import the app:
# import blog
#
# Then add the new path:
# path('blog/', blog.urls, name="blog")
#
# Learn more here: https://docs.djangoproject.com/en/2.1/topics/http/urls/

urlpatterns = [
    path("", hello.views.index, name="index"),
    path("ifttt/v1/status", ifttt.views.status, name="status"),
    path("ifttt/v1/actions/update", ifttt.views.update, name="update"),
    path("ifttt/v1/triggers/state", ifttt.views.state, name="state"),
    path("ifttt/v1/test/setup", ifttt.views.test_setup, name="test_setup"),
]
