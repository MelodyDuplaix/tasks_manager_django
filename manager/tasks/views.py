from django.shortcuts import render, get_object_or_404 # type: ignore
from django.http import HttpResponse # type: ignore
from django.shortcuts import redirect # type: ignore
from django.contrib import messages # type: ignore
from django.utils.timezone import make_aware # type: ignore
from django.utils import timezone #type: ignore
from tasks.models import SubManager, Reward, Action, TaskType, Task, PonctualTask
from tasks.forms import SubManagerForm, TaskForm, RewardForm, TypeForm, PonctualTaskForm
from datetime import datetime, timedelta, date

def options(request):
    """
    Display the main page which lists all sub-managers and others sub-pages.
    
    Args:
        request: The HTTP request object.
    
    Returns:
        HttpResponse: The rendered options page with a list of sub-managers.
    """
    submanagers = SubManager.objects.all()
    history = Action.objects.filter(coins_number__gt=0, date__date=date.today())
    total_coins = sum( action.coins_number for action in history if action.sub_manager.active)
    daily_objectif = sum( submanager.daily_objectif for submanager in submanagers if submanager.active)
    percentage = (total_coins / daily_objectif * 100) if daily_objectif else 0
    return render(request, 'tasks/home.html', 
                  {'submanagers': submanagers, 
                   'total_coins': total_coins, 
                   'daily_objectif': daily_objectif, 
                   'percentage': percentage})


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
    
    inactive_submanagers = SubManager.objects.filter(active=False)
    return render(request, 'tasks/add_sub_manager.html', {'form': form, 'inactive_submanagers': inactive_submanagers})

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
    if submanager:
        submanager.delete()
    else:
        messages.error(request, 'Sous manager non trouvé')
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
    try:
        submanager = SubManager.objects.get(id=submanager_id)
    except:
        return redirect('home')
    daily_objectif = submanager.daily_objectif
    historique = Action.objects.all().filter(sub_manager=submanager, date__date=date.today(), coins_number__gt=0)
    total_coins_today = sum(action.coins_number for action in historique)
    daily_objectif_percentage = (total_coins_today / daily_objectif) * 100
    tasks = Task.objects.all().filter(type__sub_manager=submanager)
    rewards = Reward.objects.all().filter(sub_manager=submanager)
    types = TaskType.objects.all().filter(sub_manager=submanager)
    historique_total = Action.objects.all().filter(sub_manager=submanager)
    total_coins = sum(historique_total.values_list('coins_number', flat=True))
    ponctuals = PonctualTask.objects.all().filter(sub_manager=submanager)
    return render(request, 'tasks/submanager_page.html', 
                  {'submanager': submanager, 
                   'daily_objectif_percentage': daily_objectif_percentage, 
                   'daily_objectif': daily_objectif,
                   'total_coins_today': total_coins_today,
                   'tasks': tasks,
                   'rewards': rewards,
                   'types': types,
                   'total_coins': total_coins,
                   'ponctuals': ponctuals}) 

def task_action(request, task_id):
    """
    Register the action for the task with the given ID.

    Args:
        request: The HTTP request object.
        task_id: The ID of the Task to be registered as an action.

    Returns:
        HttpResponse: The rendered sub-manager page with its name and details.
    """
    try:
        task = Task.objects.get(id=task_id)
    except:
        messages.error(request, 'Tache non trouvée')
        return redirect('home')
    action = Action(name=task.name, type=task.type, date=timezone.now(), coins_number=task.coins_number, sub_manager=task.type.sub_manager)
    action.save()
    return redirect('submanager_page', submanager_id=task.type.sub_manager.id)

def ponctual_task_action(request, task_id):
    """
    Register the action for the task with the given ID.

    Args:
        request: The HTTP request object.
        task_id: The ID of the Task to be registered as an action.

    Returns:
        HttpResponse: The rendered sub-manager page with its name and details.
    """
    try:
        task = PonctualTask.objects.get(id=task_id)
    except:
        messages.error(request, 'Tache non trouvée')
        return redirect('home')
    submanager = task.sub_manager
    action = Action(name=task.name, type=None, date=timezone.now(), coins_number=task.coins_number, sub_manager=task.sub_manager)
    action.save()
    task.delete()
    return redirect('submanager_page', submanager_id=submanager.id)

def reward_action(request, reward_id):
    """
    Register the action for the reward with the given ID.

    Args:
        request: The HTTP request object.
        reward_id: The ID of the Reward to be registered as an action.

    Returns:
        HttpResponse: The rendered sub-manager page with its name and details.
    """
    try:
        reward = Reward.objects.get(id=reward_id)
    except:
        messages.error(request, 'Récompense non trouvée')
        return redirect('home')
    action = Action(name=reward.name, type=None, date=timezone.now(), coins_number= -reward.coins_number, sub_manager=reward.sub_manager)
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
    try:
        submanager = SubManager.objects.get(id=submanager_id)
    except:
        messages.error(request, 'Sous manager non trouvée')
        return redirect('home')
    tasks = Task.objects.filter(type__sub_manager=submanager)
    rewards = Reward.objects.filter(sub_manager=submanager)
    tasks_type = TaskType.objects.filter(sub_manager=submanager)

    if request.method == 'POST':
        objectif_id = request.POST.get('objectif_id')
        form = SubManagerForm(request.POST, instance=submanager)
        if form.is_valid():
            form.save()
            messages.success(request, f"Les objectifs ont bien été mis à jour.")
            return redirect('sub_manager_options', submanager_id=submanager_id)
        else:
            messages.error(request, "Une erreur est survenue lors de la mise à jour.")

    form = SubManagerForm(instance=submanager)
    return render(request, 'tasks/sub_manager_options.html', {
        'submanager': submanager,
        'form': form,
        'tasks': tasks,
        'rewards': rewards,
        'tasks_type': tasks_type
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
    try:
        submanager = get_object_or_404(SubManager, id=submanager_id)
    except:
        messages.error(request, 'Sous manager non trouvée')
        return redirect('home')
    actions = Action.objects.filter(sub_manager=submanager)

    date = request.GET.get('date', '')
    date_start = request.GET.get('date_start', '') 
    date_end = request.GET.get('date_end', '') 
    current_order = request.GET.get('order_by', '-date')

    if date:
        date = datetime.strptime(date, "%Y-%m-%d").date()
        actions = actions.filter(date__date=date)
    elif date_end and date_start:
        start_datetime = make_aware(datetime.strptime(date_start, "%Y-%m-%d"))
        end_datetime = make_aware(datetime.strptime(date_end, "%Y-%m-%d")) + timedelta(days=1)
        actions = actions.filter(date__range=(start_datetime, end_datetime))
    elif date_start:
        start_datetime = make_aware(datetime.strptime(date_start, "%Y-%m-%d"))
        actions = actions.filter(date__gte=start_datetime)
    elif date_end:
        end_datetime = make_aware(datetime.strptime(date_end, "%Y-%m-%d")) + timedelta(days=1)
        actions = actions.filter(date__lt=end_datetime)

    reverse_order = current_order.lstrip('-')
    if current_order.startswith('-'):
        reverse_order = reverse_order
    else:
        reverse_order = f"-{reverse_order}"

    actions = actions.order_by(current_order)

    total_coins = sum(action.coins_number for action in actions)
    print("total de pièce : ",total_coins)

    return render(request, 'tasks/history.html', {
        'submanager': submanager,
        'history': actions,
        'filters': {
            'date_start': date_start,
            'date_end': date_end,
            'order_by': current_order,
            'reverse_order_name': 'name' if current_order == '-name' else '-name',
            'reverse_order_date': 'date' if current_order == '-date' else '-date',
            'reverse_order_type': 'type' if current_order == '-type' else '-type',
            'reverse_order_coins_number': 'coins_number' if current_order == '-coins_number' else '-coins_number'
        },
            'total_coins': total_coins
    })

def add_task(request, submanager_id):
    """
    Add a new task to the database for the given sub-manager.

    Args:
        request: The HTTP request object.
        submanager_id: The ID of the SubManager to add the task to.

    Returns:
        HttpResponse: The rendered add task page with the form to add a new task.
    """
    try:
        submanager = SubManager.objects.get(id=submanager_id)
    except:
        messages.error(request, 'Sous manager non trouvée')
        return redirect('home')
    if request.method == 'POST':
        form = TaskForm(request.POST)
        form.fields['type'].queryset = TaskType.objects.filter(sub_manager=submanager)

        if form.is_valid():
            task = form.save(commit=False)
            task.save()
            return redirect('sub_manager_options', submanager_id=submanager_id)
    else:
        form = TaskForm()
        form.fields['type'].queryset = TaskType.objects.filter(sub_manager=submanager)

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
    try:
        submanager = SubManager.objects.get(id=submanager_id)
    except:
        messages.error(request, 'Sous manager non trouvée')
        return redirect('home')
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
    try:
        task = Task.objects.get(id=task_id)
    except:
        messages.error(request, 'Tache non trouvée')
        return redirect('home')
    name = task.name
    type = task.type
    submanager = task.type.sub_manager
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        form.fields['type'].queryset = TaskType.objects.filter(sub_manager=submanager)
        history = Action.objects.filter(name=name, type=type, sub_manager=submanager)
        for action in history:
            action.name = form['name'].value()
            action.type = TaskType.objects.get(id=form['type'].value())
            action.save()
        if form.is_valid():
            form.save()
            return redirect('sub_manager_options', submanager_id=submanager_id)
    else:
        form = TaskForm(instance=task)
        form.fields['type'].queryset = TaskType.objects.filter(sub_manager=submanager)
    return render(request, 'tasks/update_task.html', {'form': form, 'task': task, 'submanager': submanager})

def update_ponctual_task(request, submanager_id, task_id):
    """
    Update the details of an existing ponctual task. 

    Args:
        request: The HTTP request object, expected to be a POST request for 
            form submission.
        task_id: The ID of the Task to be updated.

    Returns:
        HttpResponse: The rendered update task page with the form to update the task.
    """
    try:
        task = PonctualTask.objects.get(id=task_id)
    except:
        messages.error(request, 'Tache non trouvée')
        return redirect('home')
    submanager = task.sub_manager
    if request.method == 'POST':
        form = PonctualTaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('submanager_page', submanager_id=submanager_id)
    else:
        form = PonctualTaskForm(instance=task)
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
    try:
        reward = Reward.objects.get(id=reward_id)
    except:
        messages.error(request, 'Récompense non trouvée')
        return redirect('home')
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
    try:
        task = Task.objects.get(id=task_id)
    except:
        messages.error(request, 'Tache non trouvée')
        return redirect('home')
    submanager = task.type.sub_manager
    return render(request, 'tasks/confirm_delete_task.html', {'task': task, 'submanager': submanager})

def confirm_delete_ponctual_task(request, submanager_id, task_id):
    """
    Display a confirmation page for deleting a poncutal task.

    Args:
        request: The HTTP request object.
        submanager_id: The ID of the SubManager the task belongs to.
        task_id: The ID of the Task to be deleted.

    Returns:
        HttpResponse: The rendered confirmation page for deleting the task.
    """
    try:
        task = PonctualTask.objects.get(id=task_id)
    except:
        messages.error(request, 'Tache non trouvée')
        return redirect('home')
    submanager = task.sub_manager
    return render(request, 'tasks/confirm_delete_ponctual_task.html', {'task': task, 'submanager': submanager})

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
    try:
        reward = Reward.objects.get(id=reward_id)
    except:
        messages.error(request, 'Récompense non trouvée')
        return redirect('home')
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
    try:
        task = Task.objects.get(id=task_id)
    except:
        messages.error(request, 'Tache non trouvée')
        return redirect('home')
    task.delete()
    return redirect('sub_manager_options', submanager_id=submanager_id)

def delete_ponctual_task(request, submanager_id, task_id):
    """
    Delete the ponctual task with the given ID from the database.

    Args:
        request: The HTTP request object.
        submanager_id: The ID of the SubManager the task belongs to.
        task_id: The ID of the Task to be deleted.

    Returns:
        HttpResponse: A redirect to the sub-manager options page.
    """
    try:
        task = PonctualTask.objects.get(id=task_id)
    except:
        messages.error(request, 'Tache non trouvée')
        return redirect('home')
    task.delete()
    return redirect('submanager_page', submanager_id=submanager_id)

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
    try:
        reward = Reward.objects.get(id=reward_id)
    except:
        messages.error(request, 'Récompense non trouvée')
        return redirect('home')
    reward.delete()
    return redirect('sub_manager_options', submanager_id=submanager_id)

def weekly(request):
    """
    Display a page with the total of coins for each sub-manager for the current week.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The rendered weekly page with the data for each sub-manager.
    """
    current_week_start = date.today() - timedelta(days=date.today().weekday())
    current_week_end = current_week_start + timedelta(days=6)
    submanagers = SubManager.objects.filter(active=True)

    data_by_submanager = {}
    for submanager in submanagers:
        actions = Action.objects.filter(
            sub_manager=submanager,
            date__date__range=(current_week_start, current_week_end),
            coins_number__gt=0
        )
        if not actions:
            data_by_submanager[submanager] = {
                'total_coins': 0,
                'objectif_weekly': submanager.weekly_objectif,
                'percentage': 0
            }
            continue
        total_coins = sum(action.coins_number for action in actions)

        objectif_weekly = submanager.weekly_objectif

        percentage = (total_coins / objectif_weekly * 100) if objectif_weekly else 0

        data_by_submanager[submanager] = {
            'total_coins': total_coins,
            'objectif_weekly': objectif_weekly,
            'percentage': percentage
        }
    if not any(data_by_submanager.values()):
        all_data = {
            'total_coins': 0,
            'objectif_weekly': 0,
            'percentage': 0
        }
    else:
        all_data = {
            'total_coins': sum(data['total_coins'] for data in data_by_submanager.values()),
            'objectif_weekly': sum(data['objectif_weekly'] for data in data_by_submanager.values()),
            'percentage': sum(data['percentage'] for data in data_by_submanager.values()) / len(data_by_submanager)
        }

    return render(request, 'tasks/weekly.html', {'data_by_submanager': data_by_submanager, 'all_data': all_data})

def monthly(request):
    """
    Display a page with the total of coins for each sub-manager for the current month.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The rendered monthly page with the data for each sub-manager.
    """
    current_month_start = date.today().replace(day=1)
    current_month_end = current_month_start + timedelta(days=31)
    submanagers = SubManager.objects.filter(active=True)

    data_by_submanager = {}
    for submanager in submanagers:
        actions = Action.objects.filter(
            sub_manager=submanager,
            date__date__range=(current_month_start, current_month_end),
            coins_number__gt=0
        )
        if not actions:
            data_by_submanager[submanager] = {
                'total_coins': 0,
                'objectif_monthly': submanager.monthly_objectif,
                'percentage': 0
            }
            continue
        total_coins = sum(action.coins_number for action in actions)

        objectif_monthly = submanager.monthly_objectif

        percentage = (total_coins / objectif_monthly * 100) if objectif_monthly else 0

        data_by_submanager[submanager] = {
            'total_coins': total_coins,
            'objectif_monthly': objectif_monthly,
            'percentage': percentage
        }

    if not any(data_by_submanager.values()):
        all_data = {
            'total_coins': 0,
            'objectif_weekly': 0,
            'percentage': 0
        }
    else:
        all_data = {
            'total_coins': sum(data['total_coins'] for data in data_by_submanager.values()),
            'objectif_monthly': sum(data['objectif_monthly'] for data in data_by_submanager.values()),
            'percentage': sum(data['percentage'] for data in data_by_submanager.values()) / len(data_by_submanager)
        }

    return render(request, 'tasks/monthly.html', {'data_by_submanager': data_by_submanager, 'all_data': all_data})

def add_type(request, submanager_id):
    """
    Add a new type of task to the sub-manager with the given ID.

    Args:
        request: The HTTP request object.
        submanager_id: The ID of the SubManager to add the type to.

    Returns:
        HttpResponse: A redirect to the sub-manager options page.
    """
    try:
        submanager = SubManager.objects.get(id=submanager_id)
    except:
        messages.error(request, 'Sous manager non trouvée')
        return redirect('home')
    if request.method == 'POST':
        form = TypeForm(request.POST)
        if form.is_valid():
            type = form.save(commit=False)
            type.sub_manager = submanager
            type.save()    
            return redirect('sub_manager_options', submanager_id=submanager_id)
    else:
        form = TypeForm()
    return render(request, 'tasks/add_type.html', {'form': form, 'submanager': submanager})

def update_type(request, submanager_id, type_id):
    """
    Update the type of task with the given ID in the sub-manager with the given ID.

    Args:
        request: The HTTP request object.
        submanager_id: The ID of the SubManager the type belongs to.
        type_id: The ID of the Type to be updated.

    Returns:
        HttpResponse: A redirect to the sub-manager options page.
    """
    try:
        submanager = SubManager.objects.get(id=submanager_id)
    except:
        messages.error(request, 'Sous manager non trouvée') 
        return redirect('home')
    type = TaskType.objects.get(id=type_id)
    if not type:
        messages.error(request, 'Type de tâche non trouvée')
        return redirect('home')
    if request.method == 'POST':
        form = TypeForm(request.POST, instance=type)
        if form.is_valid():
            form.save()
            return redirect('sub_manager_options', submanager_id=submanager_id)
    else:
        form = TypeForm(instance=type)
    return render(request, 'tasks/update_type.html', {'form': form, 'submanager': submanager, 'type': type})

def delete_type(request, submanager_id, type_id):
    """
    Delete the type of task with the given ID from the sub-manager with the given ID.

    Args:
        request: The HTTP request object.
        submanager_id: The ID of the SubManager the type belongs to.
        type_id: The ID of the Type to be deleted.

    Returns:
        HttpResponse: A redirect to the sub-manager options page.
    """
    try:
        type = TaskType.objects.get(id=type_id)
    except:
        messages.error(request, 'Type de tâche non trouvée')
        return redirect('home')
    type.delete()
    return redirect('sub_manager_options', submanager_id=submanager_id)

def confirm_delete_type(request, submanager_id, type_id):
    """
    Confirm the deletion of the type of task with the given ID from the sub-manager with the given ID.

    Args:
        request: The HTTP request object.
        submanager_id: The ID of the SubManager the type belongs to.
        type_id: The ID of the Type to be deleted.

    Returns:
        HttpResponse: A redirect to the sub-manager options page.
    """
    try:
        submanager = SubManager.objects.get(id=submanager_id)
    except:
        messages.error(request, 'Sous manager non trouvée')
        return redirect('home')
    type = TaskType.objects.get(id=type_id)
    return render(request, 'tasks/confirm_delete_type.html', {'submanager': submanager, 'type': type})


def add_ponctual_task(request, submanager_id):
    """
    Add a new ponctual task to the sub-manager with the given ID.

    Args:
        request: The HTTP request object.
        submanager_id: The ID of the SubManager to add the task to.

    Returns:
        HttpResponse: A redirect to the sub-manager options page.
    """
    try:
        submanager = SubManager.objects.get(id=submanager_id)
    except:
        messages.error(request, 'Sous manager non trouvée')
        return redirect('home')
    if request.method == 'POST':
        form = PonctualTaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.sub_manager = submanager
            task.save()
            return redirect('submanager_page', submanager_id=submanager_id)
    else:
        form = PonctualTaskForm()
    return render(request, 'tasks/add_ponctual_task.html', {'form': form, 'submanager': submanager})

def activate_submanager(request, submanager_id):
    """
    Activate the sub-manager with the given ID.

    Args:
        request: The HTTP request object.
        submanager_id: The ID of the SubManager to be activated.

    Returns:
        HttpResponse: A redirect to the sub-manager options page.
    """
    try:
        submanager = SubManager.objects.get(id=submanager_id)
    except:
        messages.error(request, 'Sous manager non trouvée')
        return redirect('home')
    submanager.active = True
    submanager.save()
    return redirect('submanager_page', submanager_id=submanager_id)

def desactivate_submanager(request, submanager_id):
    """
    Deactivate the sub-manager with the given ID.

    Args:
        request: The HTTP request object.
        submanager_id: The ID of the SubManager to be deactivated.

    Returns:
        HttpResponse: A redirect to the sub-manager options page.
    """
    try:
        submanager = SubManager.objects.get(id=submanager_id)
    except:
        messages.error(request, 'Sous manager non trouvée')
        return redirect('home')
    submanager.active = False
    submanager.save()
    return redirect('home')

def delete_action(request, submanager_id, action_id):
    """ 
    Delete the action with the given ID from the database.

    Args:
        request: The HTTP request object.
        action_id: The ID of the Action to be deleted.

    Returns:
        HttpResponse: A redirect to the sub-manager options page.
    """
    try:
        action = Action.objects.get(id=action_id)
    except:
        messages.error(request, 'Action non trouvée')
        return redirect('history', submanager_id=submanager_id)
    action.delete()
    return redirect('history', submanager_id=submanager_id)

def confirm_delete_action(request, submanager_id, action_id):
    """
    Confirm the deletion of the action with the given ID from the sub-manager with the given ID.

    Args:
        request: The HTTP request object.
        submanager_id: The ID of the SubManager the action belongs to.
        action_id: The ID of the Action to be deleted.

    Returns:
        HttpResponse: A redirect to the sub-manager options page.
    """
    try:
        submanager = SubManager.objects.get(id=submanager_id)
        action = Action.objects.get(id=action_id)
    except:
        messages.error(request, 'Sous manager ou action non trouvée')
        return redirect('home')
    return render(request, 'tasks/confirm_delete_action.html', {'submanager': submanager, 'action': action})