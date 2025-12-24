from django.urls import path

from . import views


app_name = 'loader'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('import-excel/', views.ExcelImportView.as_view(), name='import_excel'),
]
