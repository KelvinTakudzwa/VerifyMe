from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from cryptography.fernet import Fernet
from django.conf import settings

# Function to encrypt data
def encrypt_data(data):
    cipher_suite = Fernet(settings.ENCRYPTION_KEY)
    return cipher_suite.encrypt(data.encode('utf-8'))

# Function to decrypt data
def decrypt_data(data):
    cipher_suite = Fernet(settings.ENCRYPTION_KEY)
    return cipher_suite.decrypt(data).decode('utf-8')

class UserProfile(AbstractUser):
    birth_date = models.DateField(null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)
    
    # Field for storing encrypted SSN
    encrypted_ssn = models.BinaryField(null=True, blank=True)

    # Adding related_name to avoid clashes
    groups = models.ManyToManyField(Group, related_name='user_profiles', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='user_profiles', blank=True)

    def save(self, *args, **kwargs):
        # Assuming ssn is provided and needs encryption
        if hasattr(self, 'ssn') and self.ssn:
            self.encrypted_ssn = encrypt_data(self.ssn)
        super().save(*args, **kwargs)

    @property
    def ssn(self):
        return decrypt_data(self.encrypted_ssn) if self.encrypted_ssn else None

    def __str__(self):
        return self.username

class Employee(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    department = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    employer = models.CharField(max_length=255, blank=True)  # New field: employer
    year_started = models.CharField(max_length=4, blank=True)  # New field: year_started

    def __str__(self):
        return self.user.username

class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class VerificationRequest(models.Model):
    requester = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='verification_requests')
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], default='pending')
    result = models.TextField(blank=True)

    def __str__(self):
        return f"Verification Request #{self.id} by {self.requester.username}"

class Document(models.Model):
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='uploaded_documents')
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name
