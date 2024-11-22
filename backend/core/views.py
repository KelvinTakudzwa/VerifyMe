from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Employee
from .forms import EmployeeForm, EmployeeSearchForm
import pandas as pd
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import EmployeeSerializer, UserProfileSerializer

@api_view(['POST'])
def add_employee(request):
    serializer = EmployeeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'detail': 'Employee added successfully.'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def search_employee(request):
    query = request.query_params.get('q', None)
    if query:
        employees = Employee.objects.filter(
            user__username__icontains=query
        ) | Employee.objects.filter(
            user__first_name__icontains=query
        ) | Employee.objects.filter(
            user__last_name__icontains=query
        ) | Employee.objects.filter(
            department__icontains=query
        ) | Employee.objects.filter(
            position__icontains=query
        ) | Employee.objects.filter(
            employer__icontains=query
        )
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)
    return Response({'detail': 'No query parameter provided.'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_employee_by_employer(request):
    username = request.query_params.get('username')
    first_name = request.query_params.get('first_name')
    
    if username:
        try:
            employee = Employee.objects.get(user__username=username)
            serializer = EmployeeSerializer(employee)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Employee.DoesNotExist:
            return Response({'error': 'Employee not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    elif first_name:
        try:
            employee = Employee.objects.get(user__first_name=first_name)
            serializer = EmployeeSerializer(employee)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Employee.DoesNotExist:
            return Response({'error': 'Employee not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    else:
        return Response({'error': 'Username or first name is required.'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_employee_api(request, pk):
    try:
        employee = Employee.objects.get(pk=pk)
    except Employee.DoesNotExist:
        return Response({'error': 'Employee not found.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = EmployeeSerializer(employee, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'detail': 'Employee updated successfully.'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmployeeListCreateAPIView(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]

class EmployeeDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]

def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'employee_list.html', {'employees': employees})

def update_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employee updated successfully!')
            return redirect('employee_list')
        else:
            messages.error(request, 'Error updating employee information. Please check the form and try again.')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'update_employee.html', {'form': form})

def bulk_update_employees(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        if not file:
            messages.error(request, 'No file uploaded')
            return redirect('bulk_update_employees')

        try:
            if file.name.endswith('.csv'):
                data = pd.read_csv(file)
            elif file.name.endswith('.xlsx'):
                data = pd.read_excel(file)
            else:
                messages.error(request, 'Unsupported file format')
                return redirect('bulk_update_employees')

            for _, row in data.iterrows():
                user_data = {
                    'username': row['username'],
                    'email': row['email'],
                    'first_name': row['first_name'],
                    'last_name': row['last_name'],
                    'birth_date': row['birth_date'],
                    'bio': row['bio'],
                    'profile_picture': row['profile_picture'],
                }
                user, created = UserProfile.objects.update_or_create(username=row['username'], defaults=user_data)
                employee_data = {
                    'department': row['department'],
                    'position': row['position'],
                    'employer': row['employer'],
                    'year_started': row['year_started'],
                }
                Employee.objects.update_or_create(user=user, defaults=employee_data)
            messages.success(request, 'Employees updated successfully!')
        except Exception as e:
            messages.error(request, f'Error processing file: {str(e)}')

        return redirect('employee_list')
    return render(request, 'bulk_update_employees.html')

def employee_search(request):
    if request.method == 'POST':
        form = EmployeeSearchForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            employer = form.cleaned_data.get('employer')
            position = form.cleaned_data.get('position')
            department = form.cleaned_data.get('department')
            year_started = form.cleaned_data.get('year_started')

            employees = Employee.objects.filter(
                user__username__icontains=name,
                employer__icontains=employer,
                position__icontains=position,
                department__icontains=department,
                year_started__gte=year_started
            ) 

            context = {
                'form': form,
                'employees': employees
            }
            return render(request, 'employee_search_results.html', context)
        else:
            messages.error(request, 'Error in search form. Please check the input fields.')
    else:
        form = EmployeeSearchForm()

    context = {
        'form': form
    }
    return render(request, 'search_employees.html', context)
