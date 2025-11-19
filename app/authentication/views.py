from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from drf_spectacular.utils import extend_schema, OpenApiParameter
from .serializers import UserSerializer, RegisterSerializer, ChangePasswordSerializer
from .tasks import send_welcome_email


class RegisterView(generics.CreateAPIView):
    """
    Register a new user account
    """
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    @extend_schema(
        summary="Register a new user",
        description="Create a new user account and return authentication token",
        responses={201: UserSerializer}
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Create token for the new user
        token, created = Token.objects.get_or_create(user=user)

        # Send welcome email asynchronously
        send_welcome_email.delay(user.email, user.username)

        return Response({
            'user': UserSerializer(user).data,
            'token': token.key
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    """
    Login with username and password to get authentication token
    """
    permission_classes = (AllowAny,)

    @extend_schema(
        summary="Login",
        description="Authenticate user and return token",
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'username': {'type': 'string'},
                    'password': {'type': 'string'}
                }
            }
        },
        responses={200: UserSerializer}
    )
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response(
                {'error': 'Please provide both username and password'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(username=username, password=password)

        if not user:
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'user': UserSerializer(user).data,
            'token': token.key
        }, status=status.HTTP_200_OK)


class LogoutView(APIView):
    """
    Logout by deleting the authentication token
    """
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        summary="Logout",
        description="Delete user's authentication token",
        responses={200: None}
    )
    def post(self, request):
        # Delete the user's token
        request.user.auth_token.delete()
        return Response(
            {'message': 'Successfully logged out'},
            status=status.HTTP_200_OK
        )


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    Get or update the current user's profile
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    @extend_schema(
        summary="Get current user profile",
        description="Retrieve the authenticated user's profile information"
    )
    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @extend_schema(
        summary="Update current user profile",
        description="Update the authenticated user's profile information"
    )
    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @extend_schema(
        summary="Partially update current user profile",
        description="Partially update the authenticated user's profile information"
    )
    def patch(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ChangePasswordView(APIView):
    """
    Change password for the authenticated user
    """
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        summary="Change password",
        description="Change the authenticated user's password",
        request=ChangePasswordSerializer,
        responses={200: None}
    )
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user

        # Check old password
        if not user.check_password(serializer.data.get('old_password')):
            return Response(
                {'old_password': 'Wrong password'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Set new password
        user.set_password(serializer.data.get('new_password'))
        user.save()

        return Response(
            {'message': 'Password updated successfully'},
            status=status.HTTP_200_OK
        )
