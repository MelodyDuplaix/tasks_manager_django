from datetime import datetime, timedelta, date
import pandas as pd
from django.contrib.auth.decorators import login_required  # type: ignore
from django.db.models import Sum
from django.shortcuts import render, get_object_or_404  # type: ignore
from django.utils.timezone import make_aware
import plotly.express as px  # type: ignore
from django.utils.safestring import mark_safe

from tasks.models import SubManager, Action  # type: ignore




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
    
    
    all_submanager = SubManager.objects.filter(user=request.user)

    return render(request, 'tasks/history.html', {
        'submanager': submanager,
        'history': actions,
        'filters': filters,
        'total_coins': total_coins,
        'all_submanager': all_submanager
    })


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
def statistics(request, submanager_id):
    """
    View function to generate and display statistics for a given submanager.
    Args:
        request (HttpRequest): The HTTP request object.
        submanager_id (int): The ID of the submanager for which statistics are to be generated.
    Returns:
        HttpResponse: The rendered HTML page with the statistics.
    """
    submanager = SubManager.objects.get(id=submanager_id)
    actions = Action.objects.filter(sub_manager__id=submanager_id).order_by('date')

    if actions.exists():
        df = pd.DataFrame(list(actions.values('name', 'date')))
        stats = {}
        stats['most_frequent_actions'] = mark_safe(df.groupby('name').size().reset_index(name='count')\
            .sort_values('count', ascending=False)\
            .head(10)
            .rename(columns={'name': 'Nom de l\'action','count': 'Nombre d\'actions'})
            .to_html(classes="table table-striped", index=False))
            
        daily_tasks = df.groupby(df['date'].dt.date).size().reset_index(name='count')
        print(daily_tasks)
        fig = px.line(daily_tasks, x='date', y='count', 
                     labels={'date': 'Date', 'count': 'Nombre de tâches'})
        graph_html = fig.to_html(full_html=False)
        stats['daily_tasks_graph'] = mark_safe(graph_html)
        
        stats['daily_tasks_frequency'] = mark_safe(df.groupby('name')['date'].count().div(len(df['date'].dt.date.unique())).reset_index()
                                                   .rename(columns={'name': 'Nom de la tâche', 'date': 'Fréquence moyenne par jour'})
                                                   .sort_values('Fréquence moyenne par jour', ascending=False)
                                                   .to_html(classes="table table-striped", index=False))
        
    else:
        stats = {}
        graph_html = None

    all_submanager = SubManager.objects.filter(user=request.user)
    
    return render(request, 'tasks/statistics.html', {
        'submanager': submanager,
        'stats': stats,
        'all_submanager': all_submanager
    })
