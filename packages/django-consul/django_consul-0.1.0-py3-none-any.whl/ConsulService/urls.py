from django.urls import re_path
from .views import healthy_check_view


urlpatterns = [
    re_path(r'healthy/', healthy_check_view),
]
