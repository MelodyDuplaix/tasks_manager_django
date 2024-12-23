from django.test import TestCase
from django.urls import reverse

class TestUrls(TestCase):

    def test_login_url(self):
        url = reverse('login')
        self.assertEqual(url, '/accounts/login/')

    def test_signup_url(self):
        url = reverse('signup')
        self.assertEqual(url, '/accounts/signup/')

    def test_profile_url(self):
        url = reverse('profile')
        self.assertEqual(url, '/accounts/profile/')

    def test_logout_url(self):
        url = reverse('logout')
        self.assertEqual(url, '/accounts/logout/')

    def test_password_reset_url(self):
        url = reverse('password_reset')
        self.assertEqual(url, '/accounts/reset_password/')

    def test_password_reset_confirm_url(self):
        url = reverse('password_reset_confirm', args=['uidb64', 'token'])
        self.assertEqual(url, '/password-reset-confirm/uidb64/token/')

    def test_password_reset_complete_url(self):
        url = reverse('password_reset_complete')
        self.assertEqual(url, '/password-reset-complete/')

    def test_home_url(self):
        url = reverse('home')
        self.assertEqual(url, '/')

    def test_add_submanager_url(self):
        url = reverse('add_submanager')
        self.assertEqual(url, '/add_submanager/')

    def test_delete_submanager_url(self):
        url = reverse('delete_submanager', args=[1])
        self.assertEqual(url, '/delete_submanager/1/')

    def test_submanager_page_url(self):
        url = reverse('submanager_page', args=[1])
        self.assertEqual(url, '/1/')

    def test_task_action_url(self):
        url = reverse('task_action', args=[1])
        self.assertEqual(url, '/action/1/')

    def test_reward_action_url(self):
        url = reverse('reward_action', args=[1])
        self.assertEqual(url, '/reward/1/')

    def test_sub_manager_options_url(self):
        url = reverse('sub_manager_options', args=[1])
        self.assertEqual(url, '/options/1/')

    def test_history_url(self):
        url = reverse('history', args=[1])
        self.assertEqual(url, '/history/1/')

    def test_add_task_url(self):
        url = reverse('add_task', args=[1])
        self.assertEqual(url, '/1/add-task/')

    def test_add_reward_url(self):
        url = reverse('add_reward', args=[1])
        self.assertEqual(url, '/1/add-reward/')

    def test_update_task_url(self):
        url = reverse('update_task', args=[1, 1])
        self.assertEqual(url, '/1/update-task/1/')

    def test_update_reward_url(self):
        url = reverse('update_reward', args=[1, 1])
        self.assertEqual(url, '/1/update-reward/1/')

    def test_delete_task_url(self):
        url = reverse('delete_task', args=[1, 1])
        self.assertEqual(url, '/1/delete-task/1/')

    def test_delete_reward_url(self):
        url = reverse('delete_reward', args=[1, 1])
        self.assertEqual(url, '/1/delete-reward/1/')

    def test_confirm_delete_task_url(self):
        url = reverse('confirm_delete_task', args=[1, 1])
        self.assertEqual(url, '/1/confirm-delete-task/1/')

    def test_confirm_delete_reward_url(self):
        url = reverse('confirm_delete_reward', args=[1, 1])
        self.assertEqual(url, '/1/confirm-delete-reward/1/')

    def test_weekly_url(self):
        url = reverse('weekly')
        self.assertEqual(url, '/weekly/')

    def test_monthly_url(self):
        url = reverse('monthly')
        self.assertEqual(url, '/monthly/')

    def test_yearly_url(self):
        url = reverse('yearly')
        self.assertEqual(url, '/yearly/')

    def test_add_type_url(self):
        url = reverse('add_type', args=[1])
        self.assertEqual(url, '/1/add-type/')

    def test_delete_type_url(self):
        url = reverse('delete_type', args=[1, 1])
        self.assertEqual(url, '/1/delete-type/1/')

    def test_update_type_url(self):
        url = reverse('update_type', args=[1, 1])
        self.assertEqual(url, '/1/update-type/1/')

    def test_confirm_delete_type_url(self):
        url = reverse('confirm_delete_type', args=[1, 1])
        self.assertEqual(url, '/1/confirm-delete-type/1/')

    def test_add_ponctual_task_url(self):
        url = reverse('add_ponctual_task', args=[1])
        self.assertEqual(url, '/1/add-ponctual-task/')

    def test_ponctual_task_action_url(self):
        url = reverse('ponctual_task_action', args=[1])
        self.assertEqual(url, '/ponctual-action/1/')

    def test_update_ponctual_task_url(self):
        url = reverse('update_ponctual_task', args=[1, 1])
        self.assertEqual(url, '/1/update-ponctual-task/1/')

    def test_confirm_delete_ponctual_task_url(self):
        url = reverse('confirm_delete_ponctual_task', args=[1, 1])
        self.assertEqual(url, '/1/confirm-delete-ponctual-task/1/')

    def test_delete_ponctual_task_url(self):
        url = reverse('delete_ponctual_task', args=[1, 1])
        self.assertEqual(url, '/1/delete-ponctual-task/1/')

    def test_activate_submanager_url(self):
        url = reverse('activate_submanager', args=[1])
        self.assertEqual(url, '/activate_submanager/1/')

    def test_desactivate_submanager_url(self):
        url = reverse('desactivate_submanager', args=[1])
        self.assertEqual(url, '/desactivate_submanager/1/')

    def test_delete_action_url(self):
        url = reverse('delete_action', args=[1, 1])
        self.assertEqual(url, '/1/delete-action/1/')

    def test_confirm_delete_action_url(self):
        url = reverse('confirm_delete_action', args=[1, 1])
        self.assertEqual(url, '/1/confirm-delete-action/1/')