from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from .models import CustomeUserModel
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomeUserModel.objects.all()

    def get_serializer_class(self):
        if self.action == 'register':
            return UserRegistrationSerializer

        elif self.action == 'login':
            return UserLoginSerializer

        else:
            return UserProfileSerializer

    @action(detail=False, methods=['POST'])
    def register(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({
            'user': UserProfileSerializer(user).data,
            'token': serializer.get_token(user)
        }, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['POST'])
    def login(self, request):
        serializer = UserLoginSerializer(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get('user')
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'user': UserProfileSerializer(user).data,
            'token': token.key
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET', 'PATCH'], permission_classes=[IsAuthenticated])
    def profile(self, request):
        if request.method == 'GET':
            serializer = UserProfileSerializer(request.data)
            return Response(serializer.data)
        serializer = UserProfileSerializer(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
