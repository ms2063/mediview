from django.urls import path
from users.views import login_view, logout_view, signup, profile

urlpatterns = [
    path('login/',login_view),
    path('logout/',logout_view),
    path('signup/',signup),
    path('profile/',profile,name='profile'),
]
