# yak/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('step1/', views.step1, name='step1'),
    path('step2/<int:patient_id>/', views.step2, name='step2'),
    path('step3/<int:patient_id>/', views.step3, name='step3'),
    path('step4/<int:patient_id>/', views.step4, name='step4'),
    path('step5/<int:patient_id>/', views.step5, name='step5'),
    path('step6/<int:patient_id>/', views.step6, name='step6'),
    path('step7/<int:patient_id>/', views.step7, name='step7'),
    path('step8/<int:patient_id>/', views.step8, name='step8'),
    path('step9/<int:patient_id>/', views.step9, name='step9'),
    path('step10/<int:patient_id>/', views.step10, name='step10'),
    path('step11/<int:patient_id>/', views.step11, name='step11'),
    path('download_pdf/<int:patient_id>/', views.download_pdf, name='download_pdf'),
]
