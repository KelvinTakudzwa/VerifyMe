from django.urls import path
from . import views
from .views import add_employee, search_employee, get_employee_by_employer, update_employee_api

urlpatterns = [
    path('', views.employee_list, name='employee_list'),  # URL for employee list view
    path('update/<int:pk>/', views.update_employee, name='update_employee'),  # URL for update employee view
    path('bulk_update/', views.bulk_update_employees, name='bulk_update_employees'),  # URL for bulk update view
    path('search/', views.employee_search, name='employee_search'),  # URL for employee search form view
    path('api/employees/', add_employee, name='add_employee'),  # URL for adding employees via API
    path('api/employees/search/', search_employee, name='search_employee'),  # URL for searching employees via API
    path('api/employees/by-employer/', get_employee_by_employer, name='get_employee_by_employer'),  # URL for fetching employee by employer's username or first name
    path('api/employees/<int:pk>/', update_employee_api, name='update_employee_api'),  # URL for updating employee via API
    # Add other URLs as needed for your project
]
