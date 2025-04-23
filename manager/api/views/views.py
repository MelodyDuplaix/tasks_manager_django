from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from tasks.models import Reward, Task, PonctualTask
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from ..serializers import RewardSerializer, TaskSerializer, PonctualTaskSerializer
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db.models import Sum
from tasks.models import Action

@swagger_auto_schema(
    method='post',
    operation_summary='Validate a reward',
    operation_description='Validates a reward if the user has enough coins. Requires authentication.',
    responses={
        200: openapi.Response(
            description='Reward validated successfully',
            examples={
                'application/json': {
                    'message': 'Reward validated successfully.'
                }
            }
        ),
        400: openapi.Response(
            description='Not enough coins to claim this reward',
            examples={
                'application/json': {
                    'error': 'Not enough coins to claim this reward.'
                }
            }
        ),
        404: openapi.Response(
            description='Reward not found',
            examples={
                'application/json': {
                    'error': 'Reward not found'
                }
            }
        )
    }
)
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
    method='post',
    operation_summary='Mark a task as done',
    operation_description='Marks a task as done and creates an action. Requires authentication.',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'is_ponctual': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Is the task a ponctual task?')
        },
        required=['is_ponctual']
    ),
    responses={
        200: openapi.Response(
            description='Task marked as done and action created',
            examples={
                'application/json': {
                    'message': 'Task marked as done and action created.'
                }
            }
        ),
        400: openapi.Response(
            description='Bad Request: Task type is None',
            examples={
                'application/json': {
                    'error': 'Task type is None'
                }
            }
        ),
        404: openapi.Response(
            description='Task not found',
            examples={
                'application/json': {
                    'error': 'Task not found'
                }
            }
        )
    }
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
