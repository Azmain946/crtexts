
from django.contrib import admin
from django.urls import path, include
from new_routine import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    #path('routine/', views.routine_page, name="routine"),
    path('<str:institute>/<str:dept>/<str:batch>/<str:section>/routine/', views.routine_page, name="routine"),
    path('ajax/load-departments/', views.load_departments, name='ajax_load_departments'),
    path('ajax/load-batches/', views.load_batches, name='ajax_load_batches'),
    path('ajax/load-sections/', views.load_sections, name='ajax_load_sections'),
    path('custom-admin/', include('custom_admin.urls')),
]
