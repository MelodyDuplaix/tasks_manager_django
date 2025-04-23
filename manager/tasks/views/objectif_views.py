from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from tasks.forms import TaskForm, PonctualTaskForm
from tasks.models import Task, PonctualTask, SubManager
from services.decomposition_objectifs import decompose_objective
from django.contrib import messages
from datetime import datetime
from django.utils import timezone

@login_required
def create_objective(request, submanager_id):
    if request.method == 'POST':
        objectif = request.POST.get('objectif')
        nb_tasks = int(request.POST.get('nb_tasks', 7))

        result = decompose_objective(objectif, nb_tasks)

        if result['erreur']:
            messages.error(request, f"Erreur lors de la décomposition de l'objectif: {result['erreur']}")
            return redirect('create_objective', submanager_id=submanager_id)

        context = {'taches': result['taches'], 'objectif': objectif, 'submanager_id': submanager_id}
        return render(request, 'tasks/create_objective.html', context)

    return render(request, 'tasks/create_objective.html')


@login_required
def save_tasks(request, submanager_id):
    if request.method == 'POST':
        objectif = request.POST.get('objectif')
        try:
            submanager = SubManager.objects.get(id=submanager_id)
            num_tasks = len(request.POST) // 3  # Assuming 3 fields per task: name, date, coins
            for i in range(num_tasks):
                tache_name = request.POST.get(f'tache_name_{i}')
                tache_date_str = request.POST.get(f'tache_date_{i}')
                coins_number_str = request.POST.get(f'coins_number_{i}')

                try:
                    tache_date = datetime.strptime(tache_date_str, '%Y-%m-%d').date()
                    coins_number = int(coins_number_str)
                except (ValueError, TypeError) as e:
                    messages.error(request, f"Erreur lors de la création de la tâche {i+1}: {e}")
                    return redirect('create_objective', submanager_id=submanager_id)
                tache_date_aware = timezone.make_aware(datetime.combine(tache_date, datetime.min.time()))

                PonctualTask.objects.create(name=tache_name, sub_manager=submanager, date=tache_date_aware, coins_number=coins_number)
            messages.success(request, "Objectif décomposé et tâches créées avec succès !")
            return redirect('submanager_detail', submanager_id=submanager_id)
        except SubManager.DoesNotExist:
            messages.error(request, "SubManager not found. Please create one.")
            return redirect('home')
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {e}")
            return redirect('home')

    return HttpResponse("Erreur")
