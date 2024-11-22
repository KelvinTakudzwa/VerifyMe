from django.contrib import admin
from .models import UserProfile,Employee,Role,VerificationRequest,Document

admin.site.register([UserProfile,Employee,Role,VerificationRequest,Document])