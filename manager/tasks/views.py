from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from tasks.models import SubManager
from tasks.forms import SubManagerForm

def hello(request):
    return HttpResponse('<h1>Hello Django!</h1>')

def options(request):
    submanagers = SubManager.objects.all()
    return render(request, 'tasks/options.html', {'submanagers': submanagers})

def update_submanager(request, submanager_id):
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
    if request.method == 'POST':
        form = SubManagerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('options')
    else:
        form = SubManagerForm()
    return render(request, 'tasks/add_sub_manager.html', {'form': form})

def delete_submanager(request, submanager_id):
    submanager = SubManager.objects.get(id=submanager_id)
    submanager.delete()
    return redirect('options')