from django.utils import timezone
from datetime import datetime
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from services.decomposition_objectifs import decompose_objective
from tasks.models import SubManager, PonctualTask, Action, Task, Reward
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ..serializers import SubManagerSerializer, TaskSerializer, PonctualTaskSerializer, RewardSerializer
from tasks.models import Task, PonctualTask, Reward, Action

@swagger_auto_schema(
    method='post',
    operation_summary='Décomposer un objectif en tâches',
    operation_description='Décompose un objectif en tâches. Nécessite l\'authentification.',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'objectif': openapi.Schema(type=openapi.TYPE_STRING, description='Objectif à décomposer'),
            'nb_tasks': openapi.Schema(type=openapi.TYPE_INTEGER, description='Nombre de tâches à générer (optionnel, défaut 7)')
        },
        required=['objectif']
    ),
    responses={
        200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'taches': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_OBJECT, properties={'name': openapi.Schema(type=openapi.TYPE_STRING)})
                )
            }
        ),
        400: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={'error': openapi.Schema(type=openapi.TYPE_STRING)}
        )
    }
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def decompose_objective_api(request):
    objectif = request.data.get('objectif')
    nb_tasks = int(request.data.get('nb_tasks', 7))
    result = decompose_objective(objectif, nb_tasks)
    if result['erreur']:
        return Response({'error': result['erreur']}, status=400)
    return Response({'taches': result['taches']})

@swagger_auto_schema(
    method='post',
    operation_summary='Ajouter des tâches à un sous-gestionnaire',
    operation_description='Ajoute des tâches à un sous-gestionnaire. Nécessite l\'authentification.',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'tasks': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'name': openapi.Schema(type=openapi.TYPE_STRING, description='Nom de la tâche'),
                        'date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, description='Date de la tâche (AAAA-MM-JJ)'),
                        'coins_number': openapi.Schema(type=openapi.TYPE_INTEGER, description='Nombre de pièces')
                    },
                    required=['name', 'date', 'coins_number']
                )
            )
        },
        required=['tasks']
    ),
    responses={
        200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'submanager': openapi.Schema(type=openapi.TYPE_OBJECT),
                'tasks': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_OBJECT)
                ),
                'ponctual_tasks': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_OBJECT)
                ),
                'rewards': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_OBJECT)
                ),
                'daily_coins': openapi.Schema(type=openapi.TYPE_INTEGER),
                'daily_objective': openapi.Schema(type=openapi.TYPE_INTEGER)
            }
        ),
        400: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={'error': openapi.Schema(type=openapi.TYPE_STRING)}
        ),
        404: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={'error': openapi.Schema(type=openapi.TYPE_STRING)}
        )
    }
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_tasks_to_submanager(request, submanager_id):
    try:
        submanager = SubManager.objects.get(id=submanager_id, user=request.user)
    except SubManager.DoesNotExist:
        return Response({'error': 'SubManager not found'}, status=404)

    tasks_data = request.data.get('tasks')
    if not tasks_data:
        return Response({'error': 'Tasks data is missing'}, status=400)

    for task_data in tasks_data:
        tache_name = task_data.get('name')
        tache_date_str = task_data.get('date')
        coins_number_str = task_data.get('coins_number')

        try:
            tache_date = datetime.strptime(tache_date_str, '%Y-%m-%d').date()
            coins_number = int(coins_number_str)
        except (ValueError, TypeError) as e:
            return Response({'error': f"Error parsing task data: {e}"}, status=400)

        tache_date_aware = timezone.make_aware(datetime.combine(tache_date, datetime.min.time()))
        PonctualTask.objects.create(name=tache_name, sub_manager=submanager, date=tache_date_aware, coins_number=coins_number) # type: ignore

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
