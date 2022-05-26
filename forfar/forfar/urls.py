from django.contrib import admin
from django.urls import path, re_path

from receipt.views import CreateChecksView, NewChecksView


urlpatterns = [
    re_path(r'admin/', admin.site.urls),
    re_path(r'create_checks/', CreateChecksView.as_view()),
    re_path(r'new_checks/', NewChecksView.as_view()),
]
