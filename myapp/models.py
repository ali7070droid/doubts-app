from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.conf import settings


class User(AbstractUser):
	is_teacher = models.BooleanField(default = False)
	is_student = models.BooleanField(default = False)

	def __Str__(self):
		return self.username

#class Teacher(models.Model):
#	user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
#
#class Student(modesl.Model):
#	user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)

class Doubt(models.Model):
	questions = models.TextField(max_length = 200)
	picture = models.ImageField(blank = True, null = True, upload_to='images')
	student = models.ForeignKey(User, related_name = 'student',  on_delete = models.CASCADE)
	teacher = models.ForeignKey(User, related_name = 'teacher',  on_delete = models.CASCADE)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)