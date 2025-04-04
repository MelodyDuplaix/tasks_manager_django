from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import (
    UserSerializer,
    LoginSerializer,
    PasswordResetSerializer,
    PasswordChangeSerializer,
    SubManagerSerializer,
)
from tasks.models import SubManager

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_id(request):
    return Response({'username': request.user.username})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_submanagers(request):
    submanagers = SubManager.objects.filter(user=request.user)
    serializer = SubManagerSerializer(submanagers, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        validated_data = serializer.validated_data
        if isinstance(validated_data, dict) and 'username' in validated_data and 'password' in validated_data:
            user = authenticate(
                request, username=validated_data['username'], password=validated_data['password']
            )
            if user is not None:
                login(request, user)
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': UserSerializer(user).data,
                })
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_request(request):
    serializer = PasswordResetSerializer(data=request.data)
    if serializer.is_valid():
        validated_data = serializer.validated_data
        if isinstance(validated_data, dict) and 'email' in validated_data:
            email = validated_data['email']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({'message': 'Password reset email sent.'}, status=status.HTTP_200_OK)

            token = default_token_generator.make_token(user)
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            if hasattr(settings, 'BASE_URL'):
                reset_url = f"{settings.BASE_URL}/password/reset/confirm/{uidb64}/{token}/"  # Replace with your actual URL

                context = {
                    'reset_url': reset_url,
                    'user': user,
                }
                subject = render_to_string('registration/password_reset_subject.txt', context)
                message = render_to_string('registration/password_reset_email.html', context)

                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                )

                return Response({'message': 'Password reset email sent.'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'BASE_URL is not set in settings'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def password_change(request):
    serializer = PasswordChangeSerializer(data=request.data)
    if serializer.is_valid():
        validated_data = serializer.validated_data
        if isinstance(validated_data, dict) and 'old_password' in validated_data and 'new_password1' in validated_data:
            user = request.user
            if user.check_password(validated_data['old_password']):
                user.set_password(validated_data['new_password1'])
                user.save()
                update_session_auth_hash(request, user)  # To update session after password change
                return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid old password'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
