from django.contrib import messages  # type: ignore
from django.contrib.auth.decorators import login_required  # type: ignore
from django.db.models import Sum
from django.shortcuts import render, redirect  # type: ignore
from django.utils import timezone  # type: ignore

from tasks.forms import RewardForm  # type: ignore
from tasks.models import SubManager, Reward, Action  # type: ignore
import pandas as pd
from django.contrib import messages  # type: ignore
from django.contrib.auth.decorators import login_required  # type: ignore
from django.db.models import Sum
from django.shortcuts import render, redirect  # type: ignore
from django.utils import timezone  # type: ignore

@login_required
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
    submanager = reward.sub_manager
    actions = Action.objects.filter(sub_manager=submanager)
    total_coins = actions.aggregate(total=Sum('coins_number'))['total'] or 0
    print(total_coins, reward.coins_number)
    if total_coins >= reward.coins_number:
        action = Action(name=reward.name, type=None, date=timezone.now(), coins_number=-reward.coins_number,
                        sub_manager=reward.sub_manager)
        action.save()
    else:
        messages.error(request, 'Nombre de pièce insuffisant')
    return redirect('submanager_page', submanager_id=reward.sub_manager.id) # type: ignore


@login_required
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

@login_required
def update_reward(request, submanager_id, reward_id):
    """
    Update the details of an existing reward.

    Args:
        request: The HTTP request object, expected to be a POST request for
            form submission.
        submanager_id: The submanager which belongs the reward
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



@login_required
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

@login_required
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