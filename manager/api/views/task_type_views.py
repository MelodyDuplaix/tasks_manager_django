from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from tasks.models import TaskType, SubManager
from ..serializers import TaskTypeSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.exceptions import ValidationError
from django.http import Http404

@swagger_auto_schema(
    method='post',
    operation_summary='Create a new task type',
    operation_description='Creates a new task type for a specific submanager.',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING, description='Name of the task type'),
            'sub_manager_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the submanager')
        },
    ),
    responses={
        201: openapi.Response(description='Task type created successfully', schema=TaskTypeSerializer),
        400: openapi.Response(description='Bad Request'),
        404: openapi.Response(description='Submanager not found')
    }
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_task_type(request): 
    try:
        data = request.data
        name = data.get('name')
        sub_manager_id = data.get('sub_manager_id')

        if not name or not sub_manager_id:
            raise ValidationError("Missing required fields")

        sub_manager = SubManager.objects.get(pk=sub_manager_id)
        task_type = TaskType.objects.create(name=name, sub_manager=sub_manager)
        serializer = TaskTypeSerializer(task_type)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    except SubManager.DoesNotExist:
        return Response({'error': 'Submanager not found'}, status=status.HTTP_404_NOT_FOUND)
    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(
    method='get',
    operation_summary='Get task types for a specific submanager',
    operation_description='Returns a list of task types for the given submanager ID.',
    manual_parameters=[
        openapi.Parameter(
            'sub_manager_id',
            openapi.IN_PATH,
            description='ID of the submanager',
            type=openapi.TYPE_INTEGER,
            required=True
        )
    ],
    responses={
        200: openapi.Response(description='List of task types', schema=openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_OBJECT, properties={'id': openapi.Schema(type=openapi.TYPE_INTEGER), 'name': openapi.Schema(type=openapi.TYPE_STRING)}))),
        404: openapi.Response(description='Submanager not found')
    }
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_task_types(request, sub_manager_id):
    try:
        sub_manager = SubManager.objects.get(pk=sub_manager_id)
        task_types = TaskType.objects.filter(sub_manager=sub_manager)
        serializer = TaskTypeSerializer(task_types, many=True)
        return Response(serializer.data)
    except SubManager.DoesNotExist:
        raise Http404
