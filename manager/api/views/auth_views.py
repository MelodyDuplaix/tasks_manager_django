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
from django.utils import timezone
from tasks.models import Action
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from ..serializers import (
    UserSerializer,
    LoginSerializer,
    PasswordResetSerializer,
    PasswordChangeSerializer,
)

@api_view(['POST'])
def login_view(request):
    """
    Log in a user.

    Args:
        request: The request object containing username and password.

    Returns:
        Response: 
            - 200 OK: Contains refresh and access tokens, and user data.
            - 400 BAD REQUEST: If the request data is invalid.
            - 401 UNAUTHORIZED: If the credentials are invalid.

    Example Request:
    ```json
    {
        "username": "testuser",
        "password": "password"
    }
    ```

    Example Response (Success):
    ```json
    {
        "refresh": "your_refresh_token",
        "access": "your_access_token",
        "user": {
            "id": 1,
            "username": "testuser",
            "email": "testuser@example.com"
        }
    }
    ```

    Example Response (Error):
    ```json
    {
        "error": "Invalid credentials"
    }
    ```
    """
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
    """
    Initiate a password reset request.

    Args:
        request: The request object containing the user's email.

    Returns:
        Response:
            - 200 OK: If the email was sent successfully.
            - 400 BAD REQUEST: If the request data is invalid.
            - 500 INTERNAL SERVER ERROR: If BASE_URL is not set in settings.

    Example Request:
    ```json
    {
        "email": "testuser@example.com"
    }
    ```

    Example Response (Success):
    ```json
    {
        "message": "Password reset email sent."
    }
    ```

    Example Response (Error):
    ```json
    {
        "error": "Invalid data"
    }
    ```
    """
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
    """
    Change the user's password.

    Args:
        request: The request object containing old and new passwords.

    Returns:
        Response:
            - 200 OK: If the password was changed successfully.
            - 400 BAD REQUEST: If the request data is invalid or old password is incorrect.

    Example Request:
    ```json
    {
        "old_password": "oldpassword",
        "new_password1": "newpassword",
        "new_password2": "newpassword"
    }
    ```

    Example Response (Success):
    ```json
    {
        "message": "Password changed successfully."
    }
    ```

    Example Response (Error):
    ```json
    {
        "error": "Invalid old password"
    }
    ```
    """
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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_id(request):
    """
    Retrieve the ID of the currently authenticated user.

    Args:
        request: The request object.

    Returns:
        Response: Contains the user's ID.  Example: `{"id": 1}`
    """
    return Response({'username': request.user.username})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_submanagers(request):
    """
    Retrieve a list of SubManagers associated with the currently authenticated user.

    Args:
        request: The request object.

    Returns:
        Response: A list of SubManager objects.
    """
    from tasks.models import SubManager
    from ..serializers import SubManagerSerializer
    submanagers = SubManager.objects.filter(user=request.user)
    serializer = SubManagerSerializer(submanagers, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_daily_total_points(request):
    """
    Retrieve the total points earned today by all submanagers associated with the user.

    Args:
        request: The request object.

    Returns:
        Response: An object containing the total points earned today and the total daily objective.
    """
    from tasks.models import SubManager, Action
    total_coins_today = 0
    total_daily_objectif = 0
    submanagers = SubManager.objects.filter(user=request.user)
    for submanager in submanagers:
        historique = Action.objects.filter(sub_manager=submanager, date__date=timezone.now().date(), coins_number__gt=0).values_list(
            'coins_number', flat=True)
        total_coins_today += sum(historique)
        total_daily_objectif += submanager.daily_objectif
    return Response({'total_coins_today': total_coins_today, 'total_daily_objectif': total_daily_objectif})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_total_points(request):
    """
    Retrieve the total points earned by all active submanagers associated with the user.

    Args:
        request: The request object.

    Returns:
        Response: An object containing the total points earned.
    """
    from tasks.models import Action
    total_history = Action.objects.filter(sub_manager__user=request.user)
    total_coins = sum(action.coins_number for action in total_history if getattr(action.sub_manager, 'active', False))
    return Response({'total_coins': total_coins})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_total_points_submanager(request, submanager_id):
    """
    Retrieve the total points earned by a specific submanager.

    Args:
        request: The request object.
        submanager_id: The ID of the submanager.

    Returns:
        Response: An object containing the total points earned by the submanager.
    """
    from tasks.models import SubManager, Action
    submanager = SubManager.objects.select_related('user').get(id=submanager_id)
    historique_total = Action.objects.filter(sub_manager=submanager).values_list('coins_number', flat=True)
    total_coins = sum(historique_total)
    return Response({'total_coins': total_coins})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_submanager_data(request, submanager_id):
    """
    Retrieve data for a specific submanager, including tasks, punctual tasks, rewards, and daily coins.

    Args:
        request: The request object.
        submanager_id: The ID of the submanager.

    Returns:
        Response: An object containing submanager data, tasks, punctual tasks, rewards, daily coins, and daily objective.
    """
    from tasks.models import SubManager, Task, PonctualTask, Reward, Action
    from ..serializers import SubManagerSerializer, TaskSerializer, PonctualTaskSerializer, RewardSerializer
    try:
        submanager = SubManager.objects.get(id=submanager_id, user=request.user)
    except SubManager.DoesNotExist:
        return Response({'error': 'SubManager not found'}, status=status.HTTP_404_NOT_FOUND)

    tasks = Task.objects.filter(type__sub_manager=submanager)
    task_serializer = TaskSerializer(tasks, many=True)
    
    submanager_serializer = SubManagerSerializer(submanager)

    ponctual_tasks = PonctualTask.objects.filter(sub_manager=submanager)
    ponctual_task_serializer = PonctualTaskSerializer(ponctual_tasks, many=True)

    rewards = Reward.objects.filter(sub_manager=submanager)
    reward_serializer = RewardSerializer(rewards, many=True)

    total_coins_today = 0
    historique = Action.objects.filter(sub_manager=submanager, date__date=timezone.now().date(), coins_number__gt=0).values_list(
        'coins_number', flat=True)
    total_coins_today += sum(historique)

    daily_objective = getattr(submanager, 'daily_objectif', 0)

    data = {
        'submanager': submanager_serializer.data,
        'tasks': task_serializer.data,
        'ponctual_tasks': ponctual_task_serializer.data,
        'rewards': reward_serializer.data,
        'daily_coins': total_coins_today,
        'daily_objective': daily_objective,
    }

    return Response(data)
