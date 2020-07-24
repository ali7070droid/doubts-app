from rest_framework import serializers
from .models import User, Doubt
from rest_framework import generics

class RegisterStudent(serializers.ModelSerializer):
	password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
	class Meta:
		model = User
		fields = ['email', 'username', 'password', 'password2']
		extra_kwargs = {
				'password': {'write_only': True},
		}
	def save(self):
		user = User(
			email=self.validated_data['email'],
			username=self.validated_data['username'],
			is_student=True
			)
		password = self.validated_data['password']
		password2 = self.validated_data['password2']
		if password != password2:
			raise serializers.ValidationError({'password': 'Passwords must match.'})
		user.set_password(password)
		user.save()
		return user

class RegisterTeacher(serializers.ModelSerializer):
	password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
	class Meta:
		model = User
		fields = ['email', 'username', 'password', 'password2']
		extra_kwargs = {
				'password': {'write_only': True},
		}
	def save(self):
		user = User(
			email=self.validated_data['email'],
			username=self.validated_data['username'],
			is_teacher=True
			)
		password = self.validated_data['password']
		password2 = self.validated_data['password2']
		if password != password2:
			raise serializers.ValidationError({'password': 'Passwords must match.'})
		user.set_password(password)
		user.save()
		return user

class DoubtSerializer(serializers.ModelSerializer):
	class Meta:
		model = Doubt
		fields = ['questions', 'picture', 'student', 'teacher']




