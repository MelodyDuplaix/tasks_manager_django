from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages
from tasks.models import SubManager, Reward, Objectif, Action, TaskType, Task
from tasks.forms import SubManagerForm, ObjectifForm, TaskForm, RewardForm

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
    return render(request, 'tasks/home.html', {'submanagers': submanagers})

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
            return redirect('home')
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
            return redirect('home')
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
    """
    Display the page for managing a specific sub-manager with its options.

    Args:
        request: The HTTP request object.
        submanager_id: The ID of the SubManager to be displayed.

    Returns:
        HttpResponse: The rendered sub-manager options page with its options.
    """
    submanager = get_object_or_404(SubManager, id=submanager_id)
    objectifs = Objectif.objects.filter(sub_manager=submanager)
    tasks = Task.objects.filter(type__sub_manager=submanager)
    rewards = Reward.objects.filter(sub_manager=submanager)

    if request.method == 'POST':
        objectif_id = request.POST.get('objectif_id')
        objectif = get_object_or_404(Objectif, id=objectif_id, sub_manager=submanager)
        form = ObjectifForm(request.POST, instance=objectif)
        if form.is_valid():
            form.save()
            messages.success(request, f"L'objectif '{objectif.name}' a été mis à jour.")
            return redirect('sub_manager_options', submanager_id=submanager_id)
        else:
            messages.error(request, "Une erreur est survenue lors de la mise à jour.")

    forms = {objectif.id: ObjectifForm(instance=objectif) for objectif in objectifs}
    return render(request, 'tasks/sub_manager_options.html', {
        'submanager': submanager,
        'objectifs': objectifs,
        'forms': forms,
        'tasks': tasks,
        'rewards': rewards
    })

def history(request, submanager_id):
    """
    Display the page with the history of actions for the given sub-manager.

    Args:
        request: The HTTP request object.
        submanager_id: The ID of the SubManager to be displayed.

    Returns:
        HttpResponse: The rendered history page with the list of actions.
    """
    submanager = SubManager.objects.get(id=submanager_id)
    history = Action.objects.all().filter(sub_manager=submanager).order_by('-date')
    return render(request, 'tasks/history.html', {'submanager': submanager, 'history': history})

def add_task(request, submanager_id):
    """
    Add a new task to the database for the given sub-manager.

    Args:
        request: The HTTP request object.
        submanager_id: The ID of the SubManager to add the task to.

    Returns:
        HttpResponse: The rendered add task page with the form to add a new task.
    """
    submanager = SubManager.objects.get(id=submanager_id)
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():    
            task = form.save(commit=False)
            task.type = TaskType.objects.get(id=request.POST.get('type'))
            task.save()
            return redirect('sub_manager_options', submanager_id=submanager_id)
    else:
        form = TaskForm()
    return render(request, 'tasks/add_task.html', {'form': form, 'submanager': submanager})   


def add_reward(request, submanager_id):
    """
    Add a new reward to the database for the given sub-manager.

    Args:
        request: The HTTP request object.
        submanager_id: The ID of the SubManager to add the reward to.

    Returns:
        HttpResponse: The rendered add reward page with the form to add a new reward.
    """
    submanager = SubManager.objects.get(id=submanager_id)
    if request.method == 'POST':
        form = RewardForm(request.POST)
        if form.is_valid():
            reward = form.save(commit=False)
            reward.sub_manager = submanager
            reward.save()
            return redirect('sub_manager_options', submanager_id=submanager_id)
    else:
        form = RewardForm()
    return render(request, 'tasks/add_reward.html', {'form': form, 'submanager': submanager})

def update_task(request, submanager_id, task_id):
    """
    Update the details of an existing task. 

    Args:
        request: The HTTP request object, expected to be a POST request for 
            form submission.
        task_id: The ID of the Task to be updated.

    Returns:
        HttpResponse: The rendered update task page with the form to update the task.
    """
    task = get_object_or_404(Task, id=task_id)
    submanager = task.type.sub_manager
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('sub_manager_options', submanager_id=submanager_id)
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/update_task.html', {'form': form, 'task': task, 'submanager': submanager})

def update_reward(request, submanager_id, reward_id):
    """
    Update the details of an existing reward. 

    Args:
        request: The HTTP request object, expected to be a POST request for 
            form submission.
        reward_id: The ID of the Reward to be updated.

    Returns:
        HttpResponse: The rendered update reward page with the form to update the reward.
    """
    reward = get_object_or_404(Reward, id=reward_id)
    submanager = reward.sub_manager
    if request.method == 'POST':
        form = RewardForm(request.POST, instance=reward)
        if form.is_valid():
            form.save()
            return redirect('sub_manager_options', submanager_id=submanager_id)
    else:
        form = RewardForm(instance=reward)
    return render(request, 'tasks/update_reward.html', {'form': form, 'reward': reward, 'submanager': submanager})

def confirm_delete_task(request, submanager_id, task_id):
    """
    Display a confirmation page for deleting a task.

    Args:
        request: The HTTP request object.
        submanager_id: The ID of the SubManager the task belongs to.
        task_id: The ID of the Task to be deleted.

    Returns:
        HttpResponse: The rendered confirmation page for deleting the task.
    """
    task = Task.objects.get(id=task_id)
    submanager = task.type.sub_manager
    return render(request, 'tasks/confirm_delete_task.html', {'task': task, 'submanager': submanager})

def confirm_delete_reward(request, submanager_id, reward_id):
    """
    Display a confirmation page for deleting a reward.

    Args:
        request: The HTTP request object.
        submanager_id: The ID of the SubManager the reward belongs to.
        reward_id: The ID of the Reward to be deleted.

    Returns:
        HttpResponse: The rendered confirmation page for deleting the reward.
    """
    reward = Reward.objects.get(id=reward_id)
    submanager = reward.sub_manager
    return render(request, 'tasks/confirm_delete_reward.html', {'reward': reward, 'submanager': submanager})

def delete_task(request, submanager_id, task_id):
    """
    Delete the task with the given ID from the database.

    Args:
        request: The HTTP request object.
        submanager_id: The ID of the SubManager the task belongs to.
        task_id: The ID of the Task to be deleted.

    Returns:
        HttpResponse: A redirect to the sub-manager options page.
    """
    task = Task.objects.get(id=task_id)
    task.delete()
    return redirect('sub_manager_options', submanager_id=submanager_id)

def delete_reward(request, submanager_id, reward_id):
    """
    Delete the reward with the given ID from the database.

    Args:
        request: The HTTP request object.
        submanager_id: The ID of the SubManager the reward belongs to.
        reward_id: The ID of the Reward to be deleted.

    Returns:
        HttpResponse: A redirect to the sub-manager options page.
    """
    reward = Reward.objects.get(id=reward_id)
    reward.delete()
    return redirect('sub_manager_options', submanager_id=submanager_id)