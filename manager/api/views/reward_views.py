from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from tasks.models import Reward, SubManager

from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from ..serializers import RewardSerializer

@swagger_auto_schema(
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING, description='Name of the reward'),
            'coins_number': openapi.Schema(type=openapi.TYPE_INTEGER, description='Number of coins for the reward'),
            'sub_manager_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the sub manager')
        },
        required=['name', 'coins_number', 'sub_manager_id']
    ),
    responses={
        201: openapi.Response(
            description='Reward created successfully',
            examples={
                'application/json': {
                    'message': 'Reward created successfully',
                    'reward': {
                        'id': 1,
                        'name': 'Example Reward',
                        'coins_number': 100,
                        'sub_manager_id': 1
                    }
                }
            }
        ),
        400: openapi.Response(
            description='Bad Request: Invalid data or SubManager not found',
            examples={
                'application/json': {
                    'error': 'Invalid sub_manager_id'
                }
            }
        )
    },
    operation_summary='Create a new reward',
    operation_description='Creates a new reward associated with a specific sub manager. Requires authentication.',
    method='POST'
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_reward(request):
    serializer = RewardSerializer(data=request.data)
    if serializer.is_valid() and isinstance(serializer.validated_data, dict) and serializer.validated_data:
        sub_manager_id = serializer.validated_data.get('sub_manager_id')
        if sub_manager_id is not None and isinstance(sub_manager_id, int):
            try:
                sub_manager = SubManager.objects.get(id=sub_manager_id, user=request.user)
                reward = serializer.save(sub_manager=sub_manager)
                return Response({'message': 'Reward created successfully', 'reward': RewardSerializer(reward).data}, status=status.HTTP_201_CREATED)
            except SubManager.DoesNotExist:
                return Response({'error': 'SubManager not found or not authorized'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Invalid sub_manager_id', "submanager_id": serializer.validated_data}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING, description='Name of the reward'),
            'coins_number': openapi.Schema(type=openapi.TYPE_INTEGER, description='Number of coins for the reward'),
            'sub_manager_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the sub manager')
        }
    ),
    responses={
        200: openapi.Response(
            description='Reward updated successfully',
            examples={
                'application/json': {
                    'message': 'Reward updated successfully',
                    'reward': {
                        'id': 1,
                        'name': 'Updated Reward Name',
                        'coins_number': 150,
                        'sub_manager_id': 1
                    }
                }
            }
        ),
        400: openapi.Response(
            description='Bad Request: Invalid data or SubManager not found',
            examples={
                'application/json': {
                    'error': 'Invalid sub_manager_id'
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
        ),
        403: openapi.Response(
            description='Forbidden: Not authorized to update this reward',
            examples={
                'application/json': {
                    'error': 'Not authorized to update this reward'
                }
            }
        )
    },
    operation_summary='Update an existing reward',
    operation_description='Updates an existing reward. Requires authentication and authorization.',
    method='PUT'
)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_reward(request, reward_id):
    try:
        reward = Reward.objects.get(pk=reward_id)
        
        # Check if user has permission to update this reward
        if request.user and reward and reward.sub_manager and reward.sub_manager.user:
            if reward.sub_manager.user != request.user:
                return Response({'error': 'Not authorized to update this reward'}, status=status.HTTP_403_FORBIDDEN)
        
        data = request.data.copy()
        
        # Handle sub_manager_id separately
        sub_manager_id = data.pop('sub_manager_id', None)
        if sub_manager_id:
            try:
                sub_manager = SubManager.objects.get(id=sub_manager_id, user=request.user)
                reward.sub_manager = sub_manager
            except SubManager.DoesNotExist:
                return Response({'error': 'SubManager not found or not authorized'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Update other fields
        serializer = RewardSerializer(reward, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Reward updated successfully', 'reward': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    except Reward.DoesNotExist:
        return Response({'error': 'Reward not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(
    responses={
        204: openapi.Response(description='Reward deleted successfully'),
        404: openapi.Response(
            description='Reward not found',
            examples={
                'application/json': {
                    'error': 'Reward not found'
                }
            }
        ),
        403: openapi.Response(
            description='Forbidden: Not authorized to delete this reward',
            examples={
                'application/json': {
                    'error': 'Not authorized to delete this reward'
                }
            }
        )
    },
    operation_summary='Delete a reward',
    operation_description='Deletes a reward. Requires authentication and authorization.',
    method='DELETE'
)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_reward(request, reward_id):
    try:
        reward = Reward.objects.get(pk=reward_id)
        
        # Check if user has permission to delete this reward
        if request.user and reward and reward.sub_manager and reward.sub_manager.user:
            if reward.sub_manager.user != request.user:
                return Response({'error': 'Not authorized to delete this reward'}, status=status.HTTP_403_FORBIDDEN)
        
        reward.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    except Reward.DoesNotExist:
        return Response({'error': 'Reward not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
