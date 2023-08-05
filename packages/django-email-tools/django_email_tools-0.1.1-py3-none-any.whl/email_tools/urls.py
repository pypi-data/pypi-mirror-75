from django.urls import path

from email_tools.views import EmailPreviewView


app_name = "email_tools"

urlpatterns = [path("", EmailPreviewView.as_view(), name="emailpreview")]
