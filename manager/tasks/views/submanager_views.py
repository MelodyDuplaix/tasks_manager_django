from django.contrib import messages  # type: ignore
from django.contrib.auth.decorators import login_required  # type: ignore
from django.shortcuts import render, redirect  # type: ignore

from tasks.forms import SubManagerForm  # type: ignore
from tasks.models import SubManager  # type: ignore
from django.contrib import messages  # type: ignore
from django.contrib.auth.decorators import login_required  # type: ignore
from django.shortcuts import render, redirect  # type: ignore
from django.utils import timezone  # type: ignore

from tasks.forms import SubManagerForm  # type: ignore
from tasks.models import SubManager, Reward, Action, TaskType, Task, PonctualTask  # type: ignore


@login_required
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
            # Ajouter le sous-manager avec l'utilisateur connecté
            submanager = form.save(commit=False)
            submanager.user = request.user
            submanager.save()

            return redirect('home')
    else:
        form = SubManagerForm()

    inactive_submanagers = SubManager.objects.filter(active=False, user=request.user)

    return render(request, 'tasks/add_sub_manager.html', {'form': form, 'inactive_submanagers': inactive_submanagers})


@login_required
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


@login_required
def submanager_page(request, submanager_id):
    try:
        submanager = SubManager.objects.select_related('user').get(id=submanager_id)
    except SubManager.DoesNotExist:
        return redirect('home')

    daily_objectif = submanager.daily_objectif
    historique = Action.objects.filter(sub_manager=submanager, date__date=timezone.now().date(), coins_number__gt=0).values_list(
        'coins_number', flat=True)
    daily_objectif_percentage = (sum(historique) / daily_objectif) * 100 if daily_objectif else 0
    tasks = Task.objects.filter(type__sub_manager=submanager)
    rewards = Reward.objects.filter(sub_manager=submanager)
    types = TaskType.objects.filter(sub_manager=submanager)
    historique_total = Action.objects.filter(sub_manager=submanager).values_list('coins_number', flat=True)
    ponctuals = PonctualTask.objects.filter(sub_manager=submanager)
    all_submanager = SubManager.objects.filter(user=request.user)

    return render(request, 'tasks/submanager_page.html',
                  {'submanager': submanager,
                   'daily_objectif_percentage': daily_objectif_percentage,
                   'daily_objectif': daily_objectif,
                   'total_coins_today': sum(historique),
                   'tasks': tasks,
                   'rewards': rewards,
                   'types': types,
                   'total_coins': sum(historique_total),
                   'ponctuals': ponctuals,
                   'all_submanager': all_submanager})


@login_required
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


@login_required
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
