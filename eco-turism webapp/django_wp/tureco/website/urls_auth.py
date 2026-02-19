from django.urls import path
from .views import (
    signup_view, login_view, 
    logout_view, customer_signup,
    customer_login, customer_logout, customer_dashboard,
    manager_dashboard,
)


urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    # Customer system
    path("customer/signup/", customer_signup, name="customer_signup"),
    path("customer/login/", customer_login, name="customer_login"),
    path("customer/logout/", customer_logout, name="customer_logout"),
    path("customer/dashboard/", customer_dashboard, name="customer_dashboard"),
    
    # Manager dashboard (also accessible via website:manager_dashboard)
    path("manager/dashboard/", manager_dashboard, name="manager_dashboard"),
]