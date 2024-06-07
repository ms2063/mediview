from django.urls import path
from .views import search, get_contraindications

urlpatterns = [
    path('search/', search, name='search'),
    path('get_contraindications/<int:제품코드>/', get_contraindications, name='get_contraindications'),
]