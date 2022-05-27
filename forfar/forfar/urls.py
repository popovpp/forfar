from django.contrib import admin
from django.urls import path

from receipt.views import CreateChecksView, NewChecksView, CheckView


urlpatterns = [
    path(r'admin/', admin.site.urls),
    path(r'create_checks/', CreateChecksView.as_view()),
    path(r'new_checks/', NewChecksView.as_view()),
    path(r'check/', CheckView.as_view()),
]
