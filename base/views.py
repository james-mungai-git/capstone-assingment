from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import UserProfile, BlogPost
from .serializers import (
    UserProfileSerializer,
    BlogPostSerializer,
    RegisterUserSerializer,
    LoginSerializer,
)
from rest_framework.authtoken.models import Token
from rest_framework import generics
from django.shortcuts import get_object_or_404


class RegisterViewSet(generics.CreateAPIView):
    serializer_class = RegisterUserSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        token, created = Token.objects.get_or_create(user=user)

        return Response(
            {
                "user": RegisterUserSerializer(user).data,
                "token": token.key,
            },
            status=status.HTTP_201_CREATED,
        )


class LoginViewSet(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data
        token, created = Token.objects.get_or_create(user=user)

        return Response(
            {
                "user": RegisterUserSerializer(user).data,
                "token": token.key,
            },
            status=status.HTTP_200_OK,
        )


class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all().order_by("-published_date")
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "author__username"]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        limit = int(self.request.GET.get('limit',10))
        posts = BlogPost.objects.all()[:limit]
        
        data = [
                    {'id': p.id, 'title': p.title, 'content': p.content}
                    for p in posts
        ]
        return Response(data, status=status.HTTP_201_CREATED)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise permissions.PermissionDenied("You cannot edit this post")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise permissions.PermissionDenied("You cannot delete this post")
        instance.delete()


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["get"])
    def maintenance_calories(self, request):
        profile = get_object_or_404(UserProfile, user=request.user)
        calories = profile.maintenance_calories()
        return Response({"maintenance_calories": calories}, status=status.HTTP_200_OK)