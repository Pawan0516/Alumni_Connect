from .views import CollegeViewSet
from django.urls import path, include
from organization import views

urlpatterns = [
    path('colleges/', views.CollegeViewSet.as_view(), name='colleges'),
]