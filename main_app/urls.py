from django.urls import path
from . import views

app_name = 'main_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('get-total/', views.get_total_value, name='get_total'),
    path('test-data/', views.test_data, name='test_data'),
]