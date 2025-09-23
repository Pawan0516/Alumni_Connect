from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from accounts import views

urlpatterns = [
    path('login/', views.LoginViewSet.as_view(), name='login'),

    path("changepassword/", views.ChangePasswordView.as_view(), name="change-password"),
    path("refresh/", TokenRefreshView.as_view(), name="refresh-token"),
    
    path("profile/", views.ProfileViewSet.as_view(), name="profile"),
]