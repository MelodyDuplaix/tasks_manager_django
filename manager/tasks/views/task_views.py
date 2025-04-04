from tasks.forms import TaskForm  # type: ignore
from tasks.models import SubManager, Action, TaskType, Task  # type: ignore
from django.contrib import messages  # type: ignore
from django.contrib.auth.decorators import login_required  # type: ignore
from django.shortcuts import render, redirect  # type: ignore
from django.utils import timezone  # type: ignore

from tasks.forms import TaskForm, PonctualTaskForm  # type: ignore
from tasks.models import SubManager, Action, TaskType, Task, PonctualTask  # type: ignore


@login_required
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
        form.submanager_id = submanager_id
        form.fields['type'].queryset = TaskType.objects.filter(sub_manager=submanager)

        if form.is_valid():
            task = form.save(commit=False)
            task.save()
            return redirect('sub_manager_options', submanager_id=submanager_id)
    else:
        form = TaskForm()
        form.submanager_id = submanager_id
        form.fields['type'].queryset = TaskType.objects.filter(sub_manager=submanager)

    return render(request, 'tasks/add_task.html', {'form': form, 'submanager': submanager})


@login_required
def update_task(request, submanager_id, task_id):
    """
    Update the details of an existing task.

    Args:
        request: The HTTP request object, expected to be a POST request for
            form submission.
        submanager_id: The submanager which belongs the task
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
    submanager = task.type.sub_manager if task.type else None
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


@login_required
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


@login_required
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


@login_required
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
    action = Action(name=task.name, type=task.type, date=timezone.now(), coins_number=task.coins_number,
                    sub_manager=task.type.sub_manager)
    action.save()
    return redirect('submanager_page', submanager_id=task.type.sub_manager.id)

@login_required
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
    action = Action(name=task.name, type=None, date=timezone.now(), coins_number=task.coins_number,
                    sub_manager=task.sub_manager)
    action.save()
    task.delete()
    return redirect('submanager_page', submanager_id=submanager.id)

@login_required
def update_ponctual_task(request, submanager_id, task_id):
    """
    Update the details of an existing ponctual task.

    Args:
        request: The HTTP request object, expected to be a POST request for
            form submission.
        submanager_id: The submanager which belongs the task
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

@login_required
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

@login_required
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

@login_required
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
