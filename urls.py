from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='hostcheckr_index'),
    path('fix_optimization/', views.fix_optimization, name='hostcheckr_fix'),
]
