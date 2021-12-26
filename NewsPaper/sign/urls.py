from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
# from .views import BaseRegisterView  # 9.3
from .views import upgrade_me
urlpatterns = [
    path('login/', LoginView.as_view(template_name='sign/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='sign/logout.html'), name='logout'),
    # 9.3
    # path('signup/', BaseRegisterView.as_view(template_name='sign/signup.html'), name='signup'),
    # # 13.9
    path('upgrade/', upgrade_me, name='upgrade'),
            ]
