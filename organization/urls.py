from django.urls import path
from organization import views

urlpatterns = [
    path("onboard/colleges/", views.OnboardCollegeAPIView.as_view(), name="college-onboard"),
    path("onboard/colleges/verify", views.EmailVerifyViewSet.as_view(), name="college-verify"),
    path("colleges/<str:handle>/", views.CollegeDetailAPIView.as_view(), name="college-detail"),
]
