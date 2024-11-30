from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from tasks.models import SubManager, Reward, Objectif, Action, TaskType, Task
from tasks.forms import SubManagerForm
import datetime

import unicodedata

def options(request):
    """
    Display the options page which lists all sub-managers.
    
    Args:
        request: The HTTP request object.
    
    Returns:
        HttpResponse: The rendered options page with a list of sub-managers.
    """
    submanagers = SubManager.objects.all()
    return render(request, 'tasks/options.html', {'submanagers': submanagers})

def update_submanager(request, submanager_id):
    """
    Update the details of an existing sub-manager.

    Args:
        request: The HTTP request object, expected to be a POST request for 
            form submission.
        submanager_id: The ID of the SubManager to be updated.

    Returns:
        HttpResponse: The rendered update sub-manager page with the form to 
        edit the sub-manager details.
    """
    submanager = SubManager.objects.get(id=submanager_id)
    if request.method == 'POST':
        form = SubManagerForm(request.POST, instance=submanager)
        if form.is_valid():
            form.save()
            return redirect('options')
    else:
        form = SubManagerForm(instance=submanager)
    return render(request, 'tasks/update_sub_manager.html', {'submanager': submanager, 'form': form})

def add_submanager(request):
    """
    Add a new sub-manager to the database.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The rendered add sub-manager page with the form to add a new
        sub-manager.
    """
    if request.method == 'POST':
        form = SubManagerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('options')
    else:
        form = SubManagerForm()
    return render(request, 'tasks/add_sub_manager.html', {'form': form})

def delete_submanager(request, submanager_id):
    """
    Delete the sub-manager with the given ID from the database.

    Args:
        request: The HTTP request object.
        submanager_id: The ID of the SubManager to be deleted.

    Returns:
        HttpResponse: A redirect to the options page.
    """
    submanager = SubManager.objects.get(id=submanager_id)
    submanager.delete()
    return redirect('home')


def submanager_page(request, submanager_id):
    """
    Display the page for a specific sub-manager with its name and details.

    Args:
        request: The HTTP request object.
        submanager_id: The ID of the SubManager to be displayed.

    Returns:
        HttpResponse: The rendered sub-manager page with its name and details.
    """
    submanager = SubManager.objects.get(id=submanager_id)
    daily_objectif = Objectif.objects.get(name='quotidien')
    historique = Action.objects.all().filter(sub_manager=submanager, date__date=datetime.date.today(), coins_number__gt=0)
    total_coins_today = sum(action.coins_number for action in historique)
    daily_objectif_percentage = (total_coins_today / daily_objectif.coins_number) * 100
    tasks = Task.objects.all().filter(type__sub_manager=submanager)
    rewards = Reward.objects.all().filter(sub_manager=submanager)
    types = TaskType.objects.all().filter(sub_manager=submanager)
    historique_total = Action.objects.all().filter(sub_manager=submanager)
    total_coins = sum(historique_total.values_list('coins_number', flat=True))
    return render(request, 'tasks/submanager_page.html', 
                  {'submanager': submanager, 
                   'daily_objectif_percentage': daily_objectif_percentage, 
                   'daily_objectif': daily_objectif.coins_number,
                   'total_coins_today': total_coins_today,
                   'tasks': tasks,
                   'rewards': rewards,
                   'types': types,
                   'total_coins': total_coins}) 

def task_action(request, task_id):
    """
    Register the action for the task with the given ID.

    Args:
        request: The HTTP request object.
        task_id: The ID of the Task to be registered as an action.

    Returns:
        HttpResponse: The rendered sub-manager page with its name and details.
    """
    task = Task.objects.get(id=task_id)
    action = Action(name=task.name, type=task.type, date=datetime.datetime.now(), coins_number=task.coins_number, sub_manager=task.type.sub_manager)
    action.save()
    return redirect('submanager_page', submanager_id=task.type.sub_manager.id)

def reward_action(request, reward_id):
    """
    Register the action for the reward with the given ID.

    Args:
        request: The HTTP request object.
        reward_id: The ID of the Reward to be registered as an action.

    Returns:
        HttpResponse: The rendered sub-manager page with its name and details.
    """
    reward = Reward.objects.get(id=reward_id)
    action = Action(name=reward.name, type=None, date=datetime.datetime.now(), coins_number= -reward.coins_number, sub_manager=reward.sub_manager)
    action.save()
    return redirect('submanager_page', submanager_id=reward.sub_manager.id)

def sub_manager_option(request, submanager_id):
    submanager = SubManager.objects.get(id=submanager_id)
    return render(request, 'tasks/sub_manager_options.html', {'submanager': submanager})