from django import forms
from .models import Employee, UserProfile

class EmployeeForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    employer = forms.CharField(max_length=100, required=True)
    year_started = forms.IntegerField(required=True)
    year_left = forms.IntegerField(required=False)

    class Meta:
        model = Employee
        fields = ['username', 'email', 'first_name', 'last_name', 'department', 'position', 'employer', 'year_started', 'year_left']

    def save(self, commit=True):
        employee = super(EmployeeForm, self).save(commit=False)
        user_profile, created = UserProfile.objects.get_or_create(
            username=self.cleaned_data['username'],
            defaults={
                'email': self.cleaned_data['email'],
                'first_name': self.cleaned_data['first_name'],
                'last_name': self.cleaned_data['last_name'],
            }
        )
        employee.user = user_profile
        employee.employer = self.cleaned_data['employer']
        employee.year_started = self.cleaned_data['year_started']
        employee.year_left = self.cleaned_data['year_left']
        if commit:
            employee.save()
        return employee

class EmployeeSearchForm(forms.Form):
    username = forms.CharField(required=False)
    employer = forms.CharField(required=False)
    position = forms.CharField(required=False)
    department = forms.CharField(required=False)
    year_started = forms.IntegerField(required=False)
    year_left = forms.IntegerField(required=False)
