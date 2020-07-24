from django.shortcuts import render
from .serializers import RegisterStudent, RegisterTeacher, DoubtSerializer
# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from django.http import JsonResponse
from .models import User, Doubt
from rest_framework.decorators import api_view
from django.contrib.auth.models import auth
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import APIView
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from .permissions import IsTeacher, IsStudent
@api_view(['POST', ])
def register_student(request):

	if request.method == 'POST':
		serializer = RegisterStudent(data = request.data)
		data = {}
		if serializer.is_valid():
			user = serializer.save()
			data['response'] = 'successfully registered new user.'
			data['email'] = user.email
			data['username'] = user.username
			token = Token.objects.get(user=user).key
			data['token'] = token
		else:
			data = serializer.errors
		return Response(data)

@api_view(['POST', ])
def register_teacher(request):

	if request.method == 'POST':
		serializer = RegisterTeacher(data = request.data)
		data = {}
		if serializer.is_valid():
			user = serializer.save()
			data['response'] = 'successfully registered new user.'
			data['email'] = user.email
			data['username'] = user.username
			token = Token.objects.get(user=user).key
			data['token'] = token
		else:
			data = serializer.errors
		return Response(data)

@api_view(['POST', ])
def user_login(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = auth.authenticate(username = username, password = password)
		if user:
			auth.login(request,user)
			data = {
				'message' : "Logged In"
			}
		else:
			data = {
				'message' : "Incorrect username or password"
			}
		return Response(data)

	


class Logout(APIView):
    def get(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response({'message': "Logged Out"}, status=status.HTTP_200_OK)

class ListDoubt(generics.ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsTeacher]
    serializer_class = DoubtSerializer
    def get_queryset(self):
        user = self.request.user
        return Doubt.objects.filter(teacher = user.id)

class AskViewDoubt(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsStudent]
    def get(self,request):
        doubt = Doubt.objects.filter(student = request.user.id)
        serializer = DoubtSerializer(doubt, many = True)
        return Response(serializer.data)
    
    def post(self,request):
        try:
            t = request.data['teacher']
            try:
                teacher = User.objects.get(username=t)
                if teacher.is_teacher and 'picture' in request.data:
                    data = {
                        "questions" : request.data["questions"],
                        "picture" : request.data["picture"],
                        "student" : request.user.id,
                        "teacher": teacher.id
                    }
                    serializer = DoubtSerializer(data = data) 
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data)
                    else:
                        return Response(serializer.errors)
                elif teacher.is_teacher and "picture" not in request.data:
                    data = {
                        "questions" : request.data["questions"],
                        "student" : request.user.id,
                        "teacher": teacher.id
                    }
                    serializer = DoubtSerializer(data = data)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data)
                    else:
                        return Response(serializer.errors)
                else:
                    return Response({'message' : "Teacher not Found."})
            except:
                return Response({'message' : "Not a User Instance."})
        except:
            return Response({'message' : 'Teacher field needs to be filled.'})