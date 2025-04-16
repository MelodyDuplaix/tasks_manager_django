from datetime import date
from django.db.models import Sum
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
from tasks.models import SubManager, Action
from .serializers import (
    UserSerializer,
    LoginSerializer,
    PasswordResetSerializer,
    PasswordChangeSerializer,
    SubManagerSerializer,
)
from tasks.models import SubManager, Task, PonctualTask, Reward
from .serializers import (
    UserSerializer,
    LoginSerializer,
    PasswordResetSerializer,
    PasswordChangeSerializer,
    SubManagerSerializer,
    TaskSerializer,
    PonctualTaskSerializer,
    RewardSerializer,
)
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def validate_reward(request, reward_id):
    """
    Validates a reward if the user has enough coins.
    """
    try:
        reward = Reward.objects.get(id=reward_id)
    except Reward.DoesNotExist:
        return Response({'error': 'Reward not found'}, status=status.HTTP_404_NOT_FOUND)

    submanager = reward.sub_manager
    actions = Action.objects.filter(sub_manager=submanager)
    total_coins = actions.aggregate(total=Sum('coins_number'))['total'] or 0

    if total_coins >= reward.coins_number:
        Action.objects.create(
            name=reward.name,
            type=None,
            date=timezone.now(),
            coins_number=-reward.coins_number,
            sub_manager=submanager
        )
        return Response({'message': 'Reward validated successfully.'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Not enough coins to claim this reward.'}, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'is_ponctual': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Is the task a ponctual task?'),
        },
        required=['is_ponctual']
    ),
    responses={200: 'Success message'},
    method='POST'
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_task_done(request, task_id):
    is_ponctual = request.data.get('is_ponctual', False)
    if is_ponctual:
        try:
            ponctual_task = PonctualTask.objects.get(id=task_id)
            submanager = ponctual_task.sub_manager
            Action.objects.create(
                name=f"{ponctual_task.name}",
                coins_number=ponctual_task.coins_number,
                sub_manager=submanager
            )
            ponctual_task.delete()
            return Response({'message': 'Ponctual Task marked as done, action created and task deleted.'}, status=status.HTTP_200_OK)
        except PonctualTask.DoesNotExist:
            return Response({'error': 'PonctualTask not found'}, status=status.HTTP_404_NOT_FOUND)
    else:
        try:
            task = Task.objects.get(id=task_id)
            if task.type is not None:
                submanager = task.type.sub_manager
                Action.objects.create(
                    name=f"{task.name}",
                    type=task.type,
                    coins_number=task.coins_number,
                    sub_manager=submanager
                )
                return Response({'message': 'Task marked as done and action created.'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Task type is None'}, status=status.HTTP_400_BAD_REQUEST)
        except Task.DoesNotExist:
            return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_id(request):
    return Response({'username': request.user.username})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_submanager_data(request, submanager_id):
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

    daily_objective = submanager.daily_objectif

    data = {
        'submanager': submanager_serializer.data,
        'tasks': task_serializer.data,
        'ponctual_tasks': ponctual_task_serializer.data,
        'rewards': reward_serializer.data,
        'daily_coins': total_coins_today,
        'daily_objective': daily_objective,
    }

    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_submanagers(request):
    submanagers = SubManager.objects.filter(user=request.user)
    serializer = SubManagerSerializer(submanagers, many=True)
    return Response(serializer.data)

@api_view(['POST'])
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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_daily_total_points(request):
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
    total_history = Action.objects.filter(sub_manager__user=request.user)
    total_coins = sum(action.coins_number for action in total_history if action.sub_manager.active)
    return Response({'total_coins': total_coins})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_total_points_submanager(request, submanager_id):
    submanager = SubManager.objects.select_related('user').get(id=submanager_id)
    historique_total = Action.objects.filter(sub_manager=submanager).values_list('coins_number', flat=True)
    total_coins = sum(historique_total)
    return Response({'total_coins': total_coins})

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
