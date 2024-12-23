import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from tasks.models import SubManager, TaskType, Task, PonctualTask, Reward, Action

@pytest.mark.django_db
def test_create_submanager():
    user = User.objects.create_user('testuser', 'test@example.com', 'password')
    submanager = SubManager.objects.create(name='Test Submanager', user=user)
    assert submanager.name == 'Test Submanager'
 
@pytest.mark.django_db
def test_create_task():
    tasktype = TaskType.objects.create(name='Test Task Type')
    task = Task.objects.create(name='Test Task', type=tasktype, coins_number=10)
    assert task.name == 'Test Task'
    assert task.type == tasktype

@pytest.mark.django_db
def test_create_ponctualtask():
    ponctualtask = PonctualTask.objects.create(name='Test Ponctual Task', coins_number=10)
    assert ponctualtask.name == 'Test Ponctual Task'

@pytest.mark.django_db
def test_create_reward():
    reward = Reward.objects.create(name='Test Reward', coins_number=10)
    assert reward.name == 'Test Reward'

@pytest.mark.django_db
def test_create_action():
    tasktype = TaskType.objects.create(name='Test Task Type')
    action = Action.objects.create(name='Test Action', type=tasktype, coins_number=10)
    assert action.name == 'Test Action'
    assert action.type == tasktype