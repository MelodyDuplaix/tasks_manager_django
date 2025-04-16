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
    responses={201: 'Reward created successfully', 400: 'Bad Request'},
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
