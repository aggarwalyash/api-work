from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from django.http import HttpResponse
from rest_framework.generics import (
    CreateAPIView,DestroyAPIView,ListAPIView,UpdateAPIView,RetrieveAPIView,RetrieveUpdateAPIView
    )
from rest_framework.permissions import (
    AllowAny,IsAuthenticated,IsAdminUser,IsAuthenticatedOrReadOnly,
    )
from .models import *

User = get_user_model()

from .serializers import (
    UserCreateSerializer,UserLoginSerializer,UsersSerializer,ProfileCreateUpdateSerializer
    )


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]


class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            new_data['error'] = 'null'
            new_data['status'] = 200,
            new_data['message'] = 'Welcome back, ' + new_data['username']
            return Response(new_data, status=HTTP_200_OK)

        return Response(serializers.data, status=HTTP_400_BAD_REQUEST)

class UsersAPIView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = UsersSerializer
    queryset = User.objects.all()


class ProfileAPIView(RetrieveUpdateAPIView):
    permission_classes = [AllowAny]
    queryset = Profile.objects.all()
    serializer_class = ProfileCreateUpdateSerializer

    def get(self, request, *args, **kwargs):
        try:
            profile = Profile.objects.get(user=self.kwargs['pk'])
            # return self.retrieve(request, *args, **kwargs)
            return Response({
                'status': 200,
                'message': 'Welcome, '+profile.user.username,
                'error': 'null',
                'data': {
                    'email': profile.user.email,
                    'nationality': profile.nationality,
                    'gender': profile.gender,
                    'updated_at': profile.updated,
                    'address': profile.address
                }
            })
        except:
            return Response({
                'status':400,
                'message':'User does not exist',
                'error':'Not found'
                })

    def put(self, request, *args, **kwargs):
        self.update(request, *args, **kwargs)
        profile = Profile.objects.get(user=self.kwargs['pk'])
        return Response({
            'status': 200,
            'message': 'Successfully updated , '+profile.user.username+' profile',
            'error': 'null',
            'data': {
                'email': profile.user.email,
                'nationality': profile.nationality,
                'gender': profile.gender,
                'updated_at': profile.updated,
                'address': profile.address
            }
        })
