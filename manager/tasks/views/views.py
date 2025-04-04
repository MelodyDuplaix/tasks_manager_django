from datetime import date
from django.contrib import messages  # type: ignore
from django.contrib.auth.decorators import login_required  # type: ignore
from django.shortcuts import render, redirect  # type: ignore

from tasks.forms import SubManagerForm  # type: ignore
from tasks.models import SubManager, Reward, Action, TaskType, Task  # type: ignore

@login_required
def options(request):
    """
    Display the main page which lists all sub-managers and others sub-pages.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The rendered options page with a list of sub-managers.
    """
    # Filtrer les SubManager pour l'utilisateur connecté
    submanagers = SubManager.objects.filter(user=request.user)

    # Filtrer les actions pour l'utilisateur connecté
    history = Action.objects.filter(coins_number__gt=0, date__date=date.today(), sub_manager__user=request.user)
    total_history = Action.objects.filter(sub_manager__user=request.user)
    # filtrer les actions total

    # Calculer le total des coins et objectifs
    total_total_coins = sum(action.coins_number for action in total_history if action.sub_manager.active)
    total_coins = sum(action.coins_number for action in history if action.sub_manager.active)
    daily_objectif = sum(submanager.daily_objectif for submanager in submanagers if submanager.active)
    percentage = (total_coins / daily_objectif * 100) if daily_objectif else 0

    return render(request, 'tasks/home.html',
                  {'submanagers': submanagers,
                   'total_coins': total_coins,
                   'daily_objectif': daily_objectif,
                   'percentage': percentage,
                   'user': request.user,
                   'total_total_coins': total_total_coins})



@login_required
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


@login_required
def delete_action(request, submanager_id, action_id):
    """
    Delete the action with the given ID from the database.

    Args:
        request: The HTTP request object.
        submanager_id: The submanager which belongs the action
        action_id: The ID of the Action to be deleted.

    Returns:
        HttpResponseRedirect: A redirect to the sub-manager options page.
    """
    try:
        action = Action.objects.get(id=action_id)
    except:
        messages.error(request, 'Action non trouvée')
        return redirect('history', submanager_id=submanager_id)
    action.delete()
    return redirect('history', submanager_id=submanager_id)


@login_required
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

