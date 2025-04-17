import re
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from tasks.models import Task, PonctualTask, TaskType, SubManager
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from ..serializers import TaskSerializer, PonctualTaskSerializer, RewardSerializer, TaskTypeSerializer
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.exceptions import ValidationError
from rest_framework import serializers

@swagger_auto_schema(
    method='post',
    operation_summary='Create a new task',
    operation_description='Creates a new task.  Can be a recurring task or a punctual task.',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING, description='Name of the task'),
            'coins_number': openapi.Schema(type=openapi.TYPE_INTEGER, description='Number of coins for the task'),
            'type_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the task type'),
            'sub_manager_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the sub manager'),
            'is_ponctual': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='True if the task is punctual, False otherwise'),
            'date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description='Date of the punctual task (YYYY-MM-DD HH:mm:ss)', example='2024-04-17 16:30:00')
        },
        required=['name', 'coins_number', 'is_ponctual']
    ),
    responses={
        201: openapi.Response(description='Task created successfully', schema=openapi.Schema(type=openapi.TYPE_OBJECT, properties={'id': openapi.Schema(type=openapi.TYPE_INTEGER)})),
        400: openapi.Response(description='Bad Request'),
        404: openapi.Response(description='Task type not found')
    }
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_task(request):
    try:
        data = request.data
        name = data.get('name')
        coins_number = data.get('coins_number')
        type_id = data.get('type_id')
        sub_manager_id = data.get('sub_manager_id')
        is_ponctual = data.get('is_ponctual')
        date_str = data.get('date')

        if not name or not coins_number or is_ponctual is None:
            if is_ponctual:
                if not sub_manager_id:
                    raise ValidationError("sub_manager_id is required for punctual tasks")
            else:
                if not type_id:
                    raise ValidationError("type_id is required for non-punctual tasks")

            raise ValidationError("Missing required fields")

        if is_ponctual:
            if not date_str or not sub_manager_id:
                raise ValidationError("Date and sub_manager_id are required for punctual tasks")
            try:
                date = timezone.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                return Response({'error': 'Invalid date format. Please use YYYY-MM-DD HH:mm:ss'}, status=status.HTTP_400_BAD_REQUEST)
            try:
                sub_manager = SubManager.objects.get(pk=sub_manager_id)
            except SubManager.DoesNotExist:
                return Response({'error': 'Sub manager not found'}, status=status.HTTP_404_NOT_FOUND)
            ponctual_task = PonctualTask.objects.create(
                name=name,
                coins_number=coins_number,
                sub_manager=sub_manager,
                date=date
            )
            serializer = PonctualTaskSerializer(ponctual_task)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            if not type_id:
                raise ValidationError("type_id is required for non-punctual tasks")
            try:
                task_type = TaskType.objects.get(pk=type_id)
            except TaskType.DoesNotExist:
                return Response({'error': 'Task type not found'}, status=status.HTTP_404_NOT_FOUND)
            task = Task.objects.create(
                name=name,
                coins_number=coins_number,
                type=task_type
            )
            serializer = TaskSerializer(task)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
