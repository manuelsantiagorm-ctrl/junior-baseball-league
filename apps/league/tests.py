from datetime import date
from urllib.parse import urlencode

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from .models import Player, Team


class CrudTests(TestCase):
    def setUp(self):
        self.admin = get_user_model().objects.create_superuser(username='admin_test', password='test-password')
        self.client.force_login(self.admin)
        self.team = Team.objects.create(name='Águilas', city='Puebla', category='infantil')
        self.player = Player.objects.create(
            name='Ana', number=7, position='Pitcher',
            birth_date=date(2014, 5, 3), team=self.team,
        )

    def test_pages_and_date_widget(self):
        for name in ['home', 'team_list', 'player_list', 'team_create', 'player_create']:
            with self.subTest(name=name):
                self.assertEqual(self.client.get(reverse(name)).status_code, 200)
        for entity, obj in [('team', self.team), ('player', self.player)]:
            for action in ['detail', 'update', 'delete']:
                with self.subTest(entity=entity, action=action):
                    self.assertEqual(self.client.get(reverse(f'{entity}_{action}', args=[obj.pk])).status_code, 200)
        response = self.client.get(reverse('player_update', args=[self.player.pk]))
        self.assertContains(response, 'value="2014-05-03"')
        response = self.client.get(reverse('player_create'), {'team': self.team.pk})
        self.assertEqual(response.context['form'].initial['team'], self.team)

    def test_create_and_update_team(self):
        response = self.client.post(reverse('team_create'), {'name': 'Toros', 'city': 'León', 'category': 'juvenil'})
        self.assertRedirects(response, reverse('team_list'))
        team = Team.objects.get(name='Toros')
        response = self.client.post(reverse('team_update', args=[team.pk]), {'name': 'Toros Sur', 'city': 'León', 'category': 'infantil'})
        self.assertRedirects(response, reverse('team_list'))
        team.refresh_from_db()
        self.assertEqual(team.name, 'Toros Sur')

    def test_create_and_update_player(self):
        data = {'name': 'Luis', 'number': 12, 'position': 'Catcher', 'birth_date': '2015-02-10', 'team': self.team.pk}
        response = self.client.post(reverse('player_create'), data)
        self.assertRedirects(response, reverse('player_list'))
        player = Player.objects.get(name='Luis')
        other = Team.objects.create(name='Tigres', city='León', category='juvenil')
        data.update(name='Luis Pérez', team=other.pk, number=23)
        response = self.client.post(reverse('player_update', args=[player.pk]), data)
        self.assertRedirects(response, reverse('player_list'))
        player.refresh_from_db()
        self.assertEqual((player.name, player.team_id, player.number), ('Luis Pérez', other.pk, 23))

    def test_invalid_forms_do_not_save(self):
        response = self.client.post(reverse('team_create'), {'name': 'Inválido', 'city': 'Puebla', 'category': 'otra'})
        self.assertTrue(response.context['form'].errors)
        for changes in [{'birth_date': '2999-01-01'}, {'team': 999999}, {'number': -1}]:
            data = {'name': 'Inválido', 'number': 5, 'position': 'Pitcher', 'birth_date': '2015-01-01', 'team': self.team.pk}
            data.update(changes)
            response = self.client.post(reverse('player_create'), data)
            self.assertTrue(response.context['form'].errors)
        self.assertEqual(Player.objects.count(), 1)
        self.assertEqual(Team.objects.count(), 1)

    def test_deletion_requires_post_and_cascades(self):
        url = reverse('team_delete', args=[self.team.pk])
        self.assertContains(self.client.get(url), 'También se eliminarán los 1 jugadores')
        self.assertTrue(Team.objects.filter(pk=self.team.pk).exists())
        response = self.client.post(url)
        self.assertRedirects(response, reverse('team_list'))
        self.assertFalse(Player.objects.exists())
        self.assertFalse(Team.objects.exists())

    def test_delete_player_keeps_team(self):
        url = reverse('player_delete', args=[self.player.pk])
        self.client.get(url)
        self.assertTrue(Player.objects.exists())
        self.assertRedirects(self.client.post(url), reverse('player_list'))
        self.assertTrue(Team.objects.exists())

    def test_csrf_required(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.admin)
        self.assertEqual(client.post(reverse('player_delete', args=[self.player.pk])).status_code, 403)
        self.assertTrue(Player.objects.exists())

    def test_empty_states_and_missing_records(self):
        self.team.delete()
        self.assertContains(self.client.get(reverse('team_list')), 'Todavía no hay equipos')
        self.assertContains(self.client.get(reverse('player_list')), 'Todavía no hay jugadores')
        self.assertContains(self.client.get(reverse('player_create')), 'Primero debes')
        self.assertEqual(self.client.get(reverse('team_detail', args=[999999])).status_code, 404)
        self.assertEqual(self.client.get(reverse('player_update', args=[999999])).status_code, 404)

    def crud_urls(self):
        for entity, obj in [('team', self.team), ('player', self.player)]:
            for action in ['list', 'create', 'detail', 'update', 'delete']:
                yield reverse(f'{entity}_{action}', args=[obj.pk] if action in ['detail', 'update', 'delete'] else [])

    def test_anonymous_cannot_access_any_crud_route(self):
        self.client.logout()
        for url in self.crud_urls():
            for method in ['get', 'post']:
                with self.subTest(url=url, method=method):
                    response = getattr(self.client, method)(url)
                    self.assertRedirects(response, reverse('admin:login') + '?' + urlencode({'next': url}), fetch_redirect_response=False)
        self.assertEqual(Team.objects.count(), 1)
        self.assertEqual(Player.objects.count(), 1)
        self.assertEqual(self.client.get(reverse('home')).status_code, 200)

    def test_non_admin_users_are_forbidden(self):
        for staff in [False, True]:
            user = get_user_model().objects.create_user(username=f'user_{staff}', is_staff=staff)
            self.client.force_login(user)
            for url in self.crud_urls():
                for method in ['get', 'post']:
                    with self.subTest(staff=staff, url=url, method=method):
                        self.assertEqual(getattr(self.client, method)(url).status_code, 403)
        self.assertEqual(Team.objects.count(), 1)
        self.assertEqual(Player.objects.count(), 1)

    def test_admin_login_returns_to_crud_and_logout_blocks_access(self):
        self.client.logout()
        target = reverse('team_list')
        response = self.client.post(reverse('admin:login') + '?' + urlencode({'next': target}), {
            'username': 'admin_test', 'password': 'test-password', 'next': target,
        })
        self.assertRedirects(response, target)
        self.assertRedirects(self.client.post(reverse('league_logout')), reverse('home'))
        self.assertEqual(self.client.get(target).status_code, 302)
