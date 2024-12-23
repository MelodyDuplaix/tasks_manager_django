import pytest
from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User
from tasks.models import SubManager, Reward, Action, TaskType, Task, PonctualTask

@pytest.mark.django_db
def test_reset_password_view():
    client = Client()
    response = client.get(reverse('password_reset'))
    assert response.status_code == 200
    assert 'registration/password_reset.html' in [template.name for template in response.templates]

@pytest.mark.django_db
def test_signup_view():
    client = Client()
    response = client.get(reverse('signup'))
    assert response.status_code == 200
    assert 'registration/signup.html' in [template.name for template in response.templates]

    data = {'username': 'newuser', 'email': 'newuser@example.com', 'password1': 'testitesta', 'password2': 'testitesta'}
    response = client.post(reverse('signup'), data)
    assert response.status_code == 302
    assert response.url == reverse('home')

@pytest.mark.django_db
def test_profile_view():
    client = Client()
    response = client.get(reverse('profile'))
    assert response.status_code == 302
    assert response.url == reverse('home')

@pytest.mark.django_db
def test_password_reset_view():
    client = Client()
    response = client.get(reverse('password_reset'))
    assert response.status_code == 200
    assert 'registration/password_reset.html' in [template.name for template in response.templates]

    data = {'email': 'test@example.com'}
    response = client.post(reverse('password_reset'), data)
    assert response.status_code == 302
    assert response.url == reverse('login')

@pytest.mark.django_db
def test_options_view():
    client = Client()
    user = User.objects.create_user('testuser', 'test@example.com', 'password')
    client.login(username='testuser', password='password')
    response = client.get(reverse('home'))
    assert response.status_code == 200
    assert 'tasks/home.html' in [template.name for template in response.templates]

@pytest.mark.django_db
def test_add_submanager_view():
    client = Client()
    user = User.objects.create_user('testuser', 'test@example.com', 'password')
    client.login(username='testuser', password='password')
    response = client.get(reverse('add_submanager'))
    assert response.status_code == 200
    assert 'tasks/add_sub_manager.html' in [template.name for template in response.templates]

    data = {'name': 'New SubManager', 'daily_objectif': 100, 'monthly_objectif': 100, 'weekly_objectif': 100, 'yearly_objectif': 100}
    response = client.post(reverse('add_submanager'), data)
    assert response.status_code == 302
    assert response.url == reverse('home')

@pytest.mark.django_db
def test_delete_submanager_view():
    client = Client()
    user = User.objects.create_user('testuser', 'test@example.com', 'password')
    client.login(username='testuser', password='password')
    submanager = SubManager.objects.create(name='Test SubManager', user=user)
    response = client.get(reverse('delete_submanager', args=[submanager.id]))
    assert response.status_code == 302
    assert response.url == reverse('home')

@pytest.mark.django_db
def test_submanager_page_view():
    client = Client()
    user = User.objects.create_user('testuser', 'test@example.com', 'password')
    client.login(username='testuser', password='password')
    submanager = SubManager.objects.create(name='Test SubManager', user=user)
    response = client.get(reverse('submanager_page', args=[submanager.id]))
    assert response.status_code == 200
    assert 'tasks/submanager_page.html' in [template.name for template in response.templates]
    
@pytest.mark.django_db
def test_task_action_view():
    client = Client()
    user = User.objects.create_user('testuser', 'testuser@example.com', 'password')
    submanager = SubManager.objects.create(name='Test SubManager', user=user)
    task_type = TaskType.objects.create(name='Test Task Type', sub_manager=submanager)
    client.force_login(user)
    task = Task.objects.create(name='Test Task', type=task_type, coins_number=10)
    response = client.get(reverse('task_action', args=[task.id]))
    assert response.status_code == 302
    assert Action.objects.count() == 1

@pytest.mark.django_db
def test_ponctual_task_action_view():
    client = Client()
    user = User.objects.create_user('testuser', 'testuser@example.com', 'password')
    submanager = SubManager.objects.create(name='Test SubManager', user=user)
    client.force_login(user)
    task = PonctualTask.objects.create(name='Test Task', sub_manager=submanager, coins_number=10)
    response = client.get(reverse('ponctual_task_action', args=[task.id]))
    assert response.status_code == 302
    assert Action.objects.count() == 1
    assert PonctualTask.objects.count() == 0

@pytest.mark.django_db
def test_reward_action_view():
    client = Client()
    user = User.objects.create_user('testuser', 'testuser@example.com', 'password')
    submanager = SubManager.objects.create(name='Test SubManager', user=user)
    client.force_login(user)
    reward = Reward.objects.create(name='Test Reward', sub_manager=submanager, coins_number=10)
    response = client.get(reverse('reward_action', args=[reward.id]))
    assert response.status_code == 302
    assert Action.objects.count() == 1

@pytest.mark.django_db
def test_sub_manager_option_view():
    client = Client()
    user = User.objects.create_user('testuser', 'testuser@example.com', 'password')
    client.force_login(user)
    submanager = SubManager.objects.create(name='Test SubManager', user=user)
    response = client.get(reverse('sub_manager_options', args=[submanager.id]))
    assert response.status_code == 200
    assert 'tasks/sub_manager_options.html' in [template.name for template in response.templates]

@pytest.mark.django_db
def test_history_view():
    client = Client()
    user = User.objects.create_user('testuser', 'testuser@example.com', 'password')
    client.force_login(user)
    submanager = SubManager.objects.create(name='Test SubManager', user=user)
    action = Action.objects.create(name='Test Action', sub_manager=submanager, coins_number=10)
    response = client.get(reverse('history', args=[submanager.id]))
    assert response.status_code == 200
    assert 'tasks/history.html' in [template.name for template in response.templates]

@pytest.mark.django_db
def test_add_task_view():
    client = Client()
    user = User.objects.create_user('testuser', 'testuser@example.com', 'password')
    client.force_login(user)
    submanager = SubManager.objects.create(name='Test SubManager', user=user)
    task_type = TaskType.objects.create(name='Test Task Type', sub_manager=submanager)
    response = client.get(reverse('add_task', args=[submanager.id]))
    assert response.status_code == 200
    assert 'tasks/add_task.html' in [template.name for template in response.templates]

    data = {'name': 'Test Task', 'type': task_type.id, 'coins_number': 10}
    response = client.post(reverse('add_task', args=[submanager.id]), data)
    assert response.status_code == 302
    assert Task.objects.count() == 1

@pytest.mark.django_db
def test_add_reward_view():
    client = Client()
    user = User.objects.create_user('testuser', 'testuser@example.com', 'password')
    client.force_login(user)
    submanager = SubManager.objects.create(name='Test SubManager', user=user)
    response = client.get(reverse('add_reward', args=[submanager.id]))
    assert response.status_code == 200
    assert 'tasks/add_reward.html' in [template.name for template in response.templates]

    data = {'name': 'Test Reward', 'coins_number': 10}
    response = client.post(reverse('add_reward', args=[submanager.id]), data)
    assert response.status_code == 302
    assert Reward.objects.count() == 1

@pytest.mark.django_db
def test_update_task_view():
    client = Client()
    user = User.objects.create_user('testuser', 'testuser@example.com', 'password')
    submanager = SubManager.objects.create(name='Test SubManager', user=user)
    task_type = TaskType.objects.create(name='Test Task Type', sub_manager=submanager)
    client.force_login(user)
    task = Task.objects.create(name='Test Task', type=task_type, coins_number=10)
    response = client.get(reverse('update_task', args=[submanager.id, task.id]))
    assert response.status_code == 200
    assert 'tasks/update_task.html' in [template.name for template in response.templates]

    data = {'name': 'Test Task Updated', 'type': task_type.id, 'coins_number': 20}
    response = client.post(reverse('update_task', args=[submanager.id, task.id]), data)
    assert response.status_code == 302
    assert Task.objects.count() == 1
    assert Task.objects.first().name == 'Test Task Updated'
    assert Task.objects.first().type.id == task_type.id

@pytest.mark.django_db
def test_update_ponctual_task_view():
    client = Client()
    user = User.objects.create_user('testuser', 'testuser@example.com', 'password')
    submanager = SubManager.objects.create(name='Test SubManager', user=user)
    client.force_login(user)
    task = PonctualTask.objects.create(name='Test Task', sub_manager=submanager, coins_number=10)
    response = client.get(reverse('update_ponctual_task', args=[submanager.id, task.id]))
    assert response.status_code == 200
    assert 'tasks/update_task.html' in [template.name for template in response.templates]

    data = {'name': 'Test Task Updated', 'coins_number': 20}
    response = client.post(reverse('update_ponctual_task', args=[submanager.id, task.id]), data)
    assert response.status_code == 302
    assert PonctualTask.objects.count() == 1
    assert PonctualTask.objects.first().name == 'Test Task Updated'
    
@pytest.mark.django_db
def test_update_reward_view():
    client = Client()
    user = User.objects.create_user('testuser', 'testuser@example.com', 'password')
    submanager = SubManager.objects.create(name='Test SubManager', user=user)
    reward = Reward.objects.create(name='Test Reward', sub_manager=submanager, coins_number=10)
    client.force_login(user)
    response = client.get(reverse('update_reward', args=[submanager.id, reward.id]))
    assert response.status_code == 200
    assert 'tasks/update_reward.html' in [template.name for template in response.templates]

    data = {'name': 'Test Reward Updated', 'coins_number': 20}
    response = client.post(reverse('update_reward', args=[submanager.id, reward.id]), data)
    assert response.status_code == 302
    assert Reward.objects.count() == 1
    assert Reward.objects.first().name == 'Test Reward Updated'


@pytest.mark.django_db
def test_confirm_delete_task_view():
    client = Client()
    user = User.objects.create_user('testuser', 'testuser@example.com', 'password')
    submanager = SubManager.objects.create(name='Test SubManager', user=user)
    task_type = TaskType.objects.create(name='Test Task Type', sub_manager=submanager)
    task = Task.objects.create(name='Test Task', type=task_type, coins_number=10)
    client.force_login(user)
    response = client.get(reverse('confirm_delete_task', args=[submanager.id, task.id]))
    assert response.status_code == 200
    assert 'tasks/confirm_delete_task.html' in [template.name for template in response.templates]


@pytest.mark.django_db
def test_confirm_delete_ponctual_task_view():
    client = Client()
    user = User.objects.create_user('testuser', 'testuser@example.com', 'password')
    submanager = SubManager.objects.create(name='Test SubManager', user=user)
    task = PonctualTask.objects.create(name='Test Ponctual Task', sub_manager=submanager, coins_number=10)
    client.force_login(user)
    response = client.get(reverse('confirm_delete_ponctual_task', args=[submanager.id, task.id]))
    assert response.status_code == 200
    assert 'tasks/confirm_delete_ponctual_task.html' in [template.name for template in response.templates]


@pytest.mark.django_db
def test_confirm_delete_reward_view():
    client = Client()
    user = User.objects.create_user('testuser', 'testuser@example.com', 'password')
    submanager = SubManager.objects.create(name='Test SubManager', user=user)
    reward = Reward.objects.create(name='Test Reward', sub_manager=submanager, coins_number=10)
    client.force_login(user)
    response = client.get(reverse('confirm_delete_reward', args=[submanager.id, reward.id]))
    assert response.status_code == 200
    assert 'tasks/confirm_delete_reward.html' in [template.name for template in response.templates]


@pytest.mark.django_db
def test_delete_task_view():
    client = Client()
    user = User.objects.create_user('testuser', 'testuser@example.com', 'password')
    submanager = SubManager.objects.create(name='Test SubManager', user=user)
    task_type = TaskType.objects.create(name='Test Task Type', sub_manager=submanager)
    task = Task.objects.create(name='Test Task', type=task_type, coins_number=10)
    client.force_login(user)
    response = client.get(reverse('delete_task', args=[submanager.id, task.id]))
    assert response.status_code == 302
    assert Task.objects.count() == 0


@pytest.mark.django_db
def test_delete_ponctual_task_view():
    client = Client()
    user = User.objects.create_user('testuser', 'testuser@example.com', 'password')
    submanager = SubManager.objects.create(name='Test SubManager', user=user)
    task = PonctualTask.objects.create(name='Test Ponctual Task', sub_manager=submanager, coins_number=10)
    client.force_login(user)
    response = client.get(reverse('delete_ponctual_task', args=[submanager.id, task.id]))
    assert response.status_code == 302
    assert PonctualTask.objects.count() == 0


@pytest.mark.django_db
def test_delete_reward_view():
    client = Client()
    user = User.objects.create_user('testuser', 'testuser@example.com', 'password')
    submanager = SubManager.objects.create(name='Test SubManager', user=user)
    reward = Reward.objects.create(name='Test Reward', sub_manager=submanager, coins_number=10)
    client.force_login(user)
    response = client.get(reverse('delete_reward', args=[submanager.id, reward.id]))
    assert response.status_code == 302
    assert Reward.objects.count() == 0


@pytest.mark.django_db
def test_weekly_view():
    client = Client()
    user = User.objects.create_user('testuser', 'testuser@example.com', 'password')
    client.force_login(user)
    response = client.get(reverse('weekly'))
    assert response.status_code == 200
    assert 'tasks/weekly.html' in [template.name for template in response.templates]


@pytest.mark.django_db
def test_monthly_view():
    client = Client()
    user = User.objects.create_user('testuser', 'testuser@example.com', 'password')
    client.force_login(user)
    response = client.get(reverse('monthly'))
    assert response.status_code == 200
    assert 'tasks/monthly.html' in [template.name for template in response.templates]


@pytest.mark.django_db
def test_yearly_view():
    client = Client()
    user = User.objects.create_user('testuser', 'testuser@example.com', 'password')
    client.force_login(user)
    response = client.get(reverse('yearly'))
    assert response.status_code == 200
    assert 'tasks/yearly.html' in [template.name for template in response.templates]


@pytest.mark.django_db
def test_add_type_view():
    client = Client()
    user = User.objects.create_user('testuser', 'testuser@example.com', 'password')
    submanager = SubManager.objects.create(name='Test SubManager', user=user)
    client.force_login(user)
    response = client.get(reverse('add_type', args=[submanager.id]))
    assert response.status_code == 200
    assert 'tasks/add_type.html' in [template.name for template in response.templates]

    data = {'name': 'Test Type'}
    response = client.post(reverse('add_type', args=[submanager.id]), data)
    assert response.status_code == 302
    assert TaskType.objects.count() == 1
    assert TaskType.objects.first().name == 'Test Type'


@pytest.mark.django_db
def test_update_type_view():
    client = Client()
    user = User.objects.create_user('testuser', 'testuser@example.com', 'password')
    submanager = SubManager.objects.create(name='Test SubManager', user=user)
    type = TaskType.objects.create(name='Test Type', sub_manager=submanager)
    client.force_login(user)
    response = client.get(reverse('update_type', args=[submanager.id, type.id]))
    assert response.status_code == 200
    assert 'tasks/update_type.html' in [template.name for template in response.templates]

    data = {'name': 'Test Type Updated'}
    response = client.post(reverse('update_type', args=[submanager.id, type.id]), data)
    assert response.status_code == 302
    assert TaskType.objects.count() == 1
    assert TaskType.objects.first().name == 'Test Type Updated'


@pytest.mark.django_db
def test_delete_type_view():
    client = Client()
    user = User.objects.create_user('testuser', 'testuser@example.com', 'password')
    submanager = SubManager.objects.create(name='Test SubManager', user=user)
    type = TaskType.objects.create(name='Test Type', sub_manager=submanager)
    client.force_login(user)
    response = client.get(reverse('delete_type', args=[submanager.id, type.id]))
    assert response.status_code == 302
    assert TaskType.objects.count() == 0


@pytest.mark.django_db
def test_confirm_delete_type_view():
    client = Client()
    user = User.objects.create_user('testuser', 'testuser@example.com', 'password')
    submanager = SubManager.objects.create(name='Test SubManager', user=user)
    type = TaskType.objects.create(name='Test Type', sub_manager=submanager)
    client.force_login(user)
    response = client.get(reverse('confirm_delete_type', args=[submanager.id, type.id]))
    assert response.status_code == 200
    assert 'tasks/confirm_delete_type.html' in [template.name for template in response.templates]


@pytest.mark.django_db
def test_add_ponctual_task_view():
    client = Client()
    user = User.objects.create_user('testuser', 'testuser@example.com', 'password')
    submanager = SubManager.objects.create(name='Test SubManager', user=user)
    client.force_login(user)
    response = client.get(reverse('add_ponctual_task', args=[submanager.id]))
    assert response.status_code == 200
    assert 'tasks/add_ponctual_task.html' in [template.name for template in response.templates]

    data = {'name': 'Test Ponctual Task', 'coins_number': 10}
    response = client.post(reverse('add_ponctual_task', args=[submanager.id]), data)
    assert response.status_code == 302
    assert PonctualTask.objects.count() == 1
    assert PonctualTask.objects.first().name == 'Test Ponctual Task'


@pytest.mark.django_db
def test_activate_submanager_view():
    client = Client()
    user = User.objects.create_user('testuser', 'testuser@example.com', 'password')
    submanager = SubManager.objects.create(name='Test SubManager', user=user, active=False)
    client.force_login(user)
