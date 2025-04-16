from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from tasks.models import Task, PonctualTask
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from ..serializers import TaskSerializer, PonctualTaskSerializer, RewardSerializer
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

@swagger_auto_schema(
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING, description='Name of the task'),
            'coins_number': openapi.Schema(type=openapi.TYPE_INTEGER, description='Number of coins for the task'),
            'type_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the task type'),
            'is_ponctual': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Is the task ponctual?'),
            'date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, description='Date of the ponctual task (YYYY-MM-DD)')
        },
        required=['name', 'coins_number', 'type_id', 'is_ponctual']
    ),
    responses={201: 'Task created successfully'},
    method='POST'
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_task(request):
    is_ponctual = request.data.get('is_ponctual')
    if is_ponctual:
        serializer = PonctualTaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Ponctual task created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Task created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
