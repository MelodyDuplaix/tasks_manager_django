from datetime import datetime, timedelta, date

from django.contrib import messages  # type: ignore
from django.contrib.auth import login  # type: ignore
from django.contrib.auth.decorators import login_required  # type: ignore
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail  # type: ignore
from django.db.models import Sum
from django.shortcuts import render, get_object_or_404, redirect  # type: ignore
from django.urls import reverse_lazy
from django.utils import timezone  # type: ignore
from django.utils.timezone import make_aware  # type: ignore
from tasks.forms import SubManagerForm, TaskForm, RewardForm, TypeForm, PonctualTaskForm, PasswordResetForm, \
    CustomUserCreationForm  # type: ignore
from tasks.models import SubManager, Reward, Action, TaskType, Task, PonctualTask  # type: ignore


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'registration/password_reset.html'
    email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject.txt'
    success_message = "Nous vous avons envoyé par e-mail des instructions pour définir votre mot de passe, " \
                      "si un compte existe avec l'email que vous avez saisi. Vous devriez les recevoir sous peu." \
                      " Si vous ne recevez pas d'e-mail, " \
                      "assurez-vous d'avoir saisi l'adresse avec laquelle vous vous êtes inscrit et vérifiez votre dossier spam."
    success_url = reverse_lazy('login')


def signup(request):
    """
    Display the signup page.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The rendered signup page.
    """

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Inscription reussie')
            return redirect('home')  # Redirige vers la page de connexion après l'inscription
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


def profile(request):
    """
    Redirect to the home page.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The rendered home page.
    """
    return redirect('home')


def password_reset(request):
    """
    Display the password reset page.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The rendered password reset page.
    """
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            send_mail(
                "Réinitialisation de mot de passe",
                f"Pour réinitiliser votre mot de passe, veuillez accéder à cette page :",
                from_email="melo.surseine@gmail.com",
                fail_silently=False,
                recipient_list=[email],
            )
            messages.success(request, 'Un email vous a ete envoye')
            return redirect('login')
    else:
        form = PasswordResetForm()

    return render(request, 'registration/password_reset.html', {'form': form})


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
    total_history = Action.objects.filter(coins_number__gt=0, sub_manager__user=request.user)

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
    historique = Action.objects.filter(sub_manager=submanager, date__date=timezone.now().date()).values_list(
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
    action = Action(name=reward.name, type=None, date=timezone.now(), coins_number=-reward.coins_number,
                    sub_manager=reward.sub_manager)
    action.save()
    return redirect('submanager_page', submanager_id=reward.sub_manager.id)


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
def history(request, submanager_id):
    """
    Display the page with the history of actions for the given sub-manager.

    Args:
        request: The HTTP request object.
        submanager_id: The ID of the SubManager to be displayed.

    Returns:
        HttpResponse: The rendered history page with the list of actions.
    """
    submanager = get_object_or_404(SubManager, id=submanager_id)
    actions = Action.objects.filter(sub_manager=submanager)

    date = request.GET.get('date')
    date_start = request.GET.get('date_start')
    date_end = request.GET.get('date_end')
    current_order = request.GET.get('order_by', '-date')

    if date:
        actions = actions.filter(date__date=datetime.strptime(date, "%Y-%m-%d").date())
    else:
        if date_start:
            start_datetime = make_aware(datetime.strptime(date_start, "%Y-%m-%d"))
            actions = actions.filter(date__gte=start_datetime)
        if date_end:
            end_datetime = make_aware(datetime.strptime(date_end, "%Y-%m-%d")) + timedelta(days=1)
            actions = actions.filter(date__lt=end_datetime)

    actions = actions.order_by(current_order)

    total_coins = actions.aggregate(total=Sum('coins_number'))['total'] or 0

    filters = {
        'date_start': date_start or '',
        'date_end': date_end or '',
        'order_by': current_order,
        'reverse_order_name': 'name' if current_order == '-name' else '-name',
        'reverse_order_date': 'date' if current_order == '-date' else '-date',
        'reverse_order_type': 'type' if current_order == '-type' else '-type',
        'reverse_order_coins_number': 'coins_number' if current_order == '-coins_number' else '-coins_number',
    }

    return render(request, 'tasks/history.html', {
        'submanager': submanager,
        'history': actions,
        'filters': filters,
        'total_coins': total_coins,
    })


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


@login_required
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
    submanagers = SubManager.objects.filter(user=request.user, active=True)

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


@login_required
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
    submanagers = SubManager.objects.filter(active=True, user=request.user)

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


@login_required
def yearly(request):
    """
    Display a page with the total of coins for each sub-manager for the current year.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The rendered yearly page with the data for each sub-manager.
    """
    current_year_start = date.today().replace(month=1, day=1)
    current_year_end = current_year_start + timedelta(days=365)
    submanagers = SubManager.objects.filter(active=True, user=request.user)

    data_by_submanager = {}
    for submanager in submanagers:
        actions = Action.objects.filter(
            sub_manager=submanager,
            date__date__range=(current_year_start, current_year_end),
            coins_number__gt=0
        )
        if not actions:
            data_by_submanager[submanager] = {
                'total_coins': 0,
                'objectif_yearly': submanager.yearly_objectif,
                'percentage': 0
            }
            continue
        total_coins = sum(action.coins_number for action in actions)

        objectif_yearly = submanager.yearly_objectif

        percentage = (total_coins / objectif_yearly * 100) if objectif_yearly else 0

        data_by_submanager[submanager] = {
            'total_coins': total_coins,
            'objectif_yearly': objectif_yearly,
            'percentage': percentage
        }

    if not any(data_by_submanager.values()):
        all_data = {
            'total_coins': 0,
            'objectif_yearly': 0,
            'percentage': 0
        }
    else:
        all_data = {
            'total_coins': sum(data['total_coins'] for data in data_by_submanager.values()),
            'objectif_yearly': sum(data['objectif_yearly'] for data in data_by_submanager.values()),
            'percentage': sum(data['percentage'] for data in data_by_submanager.values()) / len(data_by_submanager)
        }

    return render(request, 'tasks/yearly.html', {'data_by_submanager': data_by_submanager, 'all_data': all_data})


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
