from django.contrib import messages  # type: ignore
from django.contrib.auth.decorators import login_required  # type: ignore
from django.shortcuts import render, redirect  # type: ignore

from tasks.forms import TypeForm  # type: ignore
from tasks.models import SubManager, TaskType  # type: ignore

@login_required
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


@login_required
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


@login_required
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


@login_required
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
