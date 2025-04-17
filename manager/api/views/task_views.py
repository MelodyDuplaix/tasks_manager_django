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
            'is_ponctual': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='True if the task is punctual, False otherwise'),
            'date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description='Date of the punctual task (YYYY-MM-DD HH:mm:ss)')
        },
        required=['name', 'coins_number', 'type_id', 'is_ponctual']
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
        is_ponctual = data.get('is_ponctual')
        date_str = data.get('date')

        if not name or not coins_number or not type_id or is_ponctual is None:
            raise ValidationError("Missing required fields")

        task_type = TaskType.objects.get(pk=type_id)

        if is_ponctual:
            if not date_str:
                raise ValidationError("Date is required for punctual tasks")
            date = timezone.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
            ponctual_task = PonctualTask.objects.create(
                name=name,
                coins_number=coins_number,
                sub_manager=task_type.sub_manager,
                date=date
            )
            serializer = PonctualTaskSerializer(ponctual_task)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            task = Task.objects.create(
                name=name,
                coins_number=coins_number,
                type=task_type
            )
            serializer = TaskSerializer(task)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    except TaskType.DoesNotExist:
        return Response({'error': 'Task type not found'}, status=status.HTTP_404_NOT_FOUND)
    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
