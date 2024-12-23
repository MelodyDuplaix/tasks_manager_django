# manager/test/test_forms.py

import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from tasks.forms import SubManagerForm, TaskForm, RewardForm, TypeForm, PonctualTaskForm
from tasks.models import SubManager, TaskType, Task, Reward, PonctualTask

@pytest.mark.django_db
def test_submanager_form_valid():
    user = User.objects.create_user('testuser', 'test@example.com', 'password')
    form = SubManagerForm({'name': 'Test Submanager', 'daily_objectif': 10, 'monthly_objectif': 10, 'weekly_objectif': 10, 'yearly_objectif': 10})
    assert form.is_valid()

@pytest.mark.django_db
def test_submanager_form_invalid():
    form = SubManagerForm({'name': ''})
    assert not form.is_valid()

@pytest.mark.django_db
def test_task_form_valid():
    tasktype = TaskType.objects.create(name='Test Task Type')
    form = TaskForm({'name': 'Test Task', 'type': tasktype.id, 'coins_number': 10})
    assert form.is_valid()

@pytest.mark.django_db
def test_task_form_invalid():
    form = TaskForm({'name': ''})
    assert not form.is_valid()

@pytest.mark.django_db
def test_reward_form_valid():
    form = RewardForm({'name': 'Test Reward', 'coins_number': 10})
    assert form.is_valid()

@pytest.mark.django_db
def test_reward_form_invalid():
    form = RewardForm({'name': ''})
    assert not form.is_valid()

@pytest.mark.django_db
def test_type_form_valid():
    submanager = SubManager.objects.create(name='Test Submanager', user=User.objects.create_user('testuser', 'test@example.com', 'password'))
    form = TypeForm({'name': 'Test Task Type', 'sub_manager': submanager.id})
    assert form.is_valid()

@pytest.mark.django_db
def test_type_form_invalid():
    form = TypeForm({'name': ''})
    assert not form.is_valid()

@pytest.mark.django_db
def test_ponctualtask_form_valid():
    submanager = SubManager.objects.create(name='Test Submanager', user=User.objects.create_user('testuser', 'test@example.com', 'password'))
    form = PonctualTaskForm({'name': 'Test Ponctual Task', 'coins_number': 10, 'sub_manager': submanager.id})
    assert form.is_valid()

@pytest.mark.django_db
def test_ponctualtask_form_invalid():
    form = PonctualTaskForm({'name': ''})
    assert not form.is_valid()