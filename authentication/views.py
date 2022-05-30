from pstats import Stats
from django.shortcuts import render
from rest_framework.generics import GenericAPIView  
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import RegisterSerializer, LoginSerializer
from django.contrib.auth import authenticate


# Create your views here.
class AuthUserAPIView(GenericAPIView):

    permission_classes= (IsAuthenticated,)  

    def get(self, request):
        user = request.user
        serializer = RegisterSerializer(user)
        return Response({'user': serializer.data})

class RegistrationAPIView(GenericAPIView):

    authentication_classes=[]

    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(GenericAPIView):

    authentication_classes = []

    serializer_class=LoginSerializer

    def post(self,request):
        email= request.data.get("email", None)
        password = request.data.get("password", None)

        user = authenticate(username=email, password=password)

        if user:
            serializer = self.serializer_class(user)

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'message': "Invalid credentials. Try again!"}, status=status.HTTP_401_UNAUTHORIZED)