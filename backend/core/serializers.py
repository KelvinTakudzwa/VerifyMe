from rest_framework import serializers
from .models import Employee, UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'first_name', 'last_name', 'birth_date', 'bio', 'profile_picture']

class EmployeeSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()

    class Meta:
        model = Employee
        fields = ['user', 'department', 'position', 'employer', 'year_started']  # Removed 'year_left'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserProfile.objects.create(**user_data)
        employee = Employee.objects.create(user=user, **validated_data)
        return employee

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        user = instance.user

        instance.department = validated_data.get('department', instance.department)
        instance.position = validated_data.get('position', instance.position)
        instance.employer = validated_data.get('employer', instance.employer)
        instance.year_started = validated_data.get('year_started', instance.year_started)
        instance.save()

        if user_data:
            user.username = user_data.get('username', user.username)
            user.email = user_data.get('email', user.email)
            user.first_name = user_data.get('first_name', user.first_name)
            user.last_name = user_data.get('last_name', user.last_name)
            user.birth_date = user_data.get('birth_date', user.birth_date)
            user.bio = user_data.get('bio', user.bio)
            user.profile_picture = user_data.get('profile_picture', user.profile_picture)
            user.save()

        return instance
