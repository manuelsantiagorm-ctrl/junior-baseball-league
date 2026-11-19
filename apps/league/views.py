from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import PlayerForm, TeamForm
from .models import Player, Team


def home(request):
    return render(request, 'league/home.html')


class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = reverse_lazy('admin:login')

    def test_func(self):
        user = self.request.user
        return user.is_active and user.is_staff and user.is_superuser


class TeamList(AdminRequiredMixin, ListView):
    queryset = Team.objects.annotate(player_count=Count('players'))
    template_name = 'league/team_list.html'


class TeamDetail(AdminRequiredMixin, DetailView):
    queryset = Team.objects.prefetch_related('players')
    template_name = 'league/team_detail.html'


class SavedMessageMixin:
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Registro guardado correctamente.')
        return response


class TeamCreate(AdminRequiredMixin, SavedMessageMixin, CreateView):
    model = Team
    form_class = TeamForm
    template_name = 'league/object_form.html'
    success_url = reverse_lazy('team_list')
    extra_context = {'entity': 'equipo', 'list_url': 'team_list'}


class TeamUpdate(AdminRequiredMixin, SavedMessageMixin, UpdateView):
    model = Team
    form_class = TeamForm
    template_name = 'league/object_form.html'
    success_url = reverse_lazy('team_list')
    extra_context = {'entity': 'equipo', 'list_url': 'team_list'}


class DeletedMessageMixin:
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Registro eliminado correctamente.')
        return response


class TeamDelete(AdminRequiredMixin, DeletedMessageMixin, DeleteView):
    model = Team
    template_name = 'league/object_confirm_delete.html'
    success_url = reverse_lazy('team_list')
    extra_context = {'entity': 'equipo', 'list_url': 'team_list', 'is_team': True}


class PlayerList(AdminRequiredMixin, ListView):
    queryset = Player.objects.select_related('team')
    template_name = 'league/player_list.html'


class PlayerDetail(AdminRequiredMixin, DetailView):
    queryset = Player.objects.select_related('team')
    template_name = 'league/player_detail.html'


class PlayerCreate(AdminRequiredMixin, SavedMessageMixin, CreateView):
    model = Player
    form_class = PlayerForm
    template_name = 'league/object_form.html'
    success_url = reverse_lazy('player_list')
    extra_context = {'entity': 'jugador', 'list_url': 'player_list'}

    def get_initial(self):
        initial = super().get_initial()
        team = Team.objects.filter(pk=self.request.GET.get('team')).first() if self.request.GET.get('team', '').isdigit() else None
        if team:
            initial['team'] = team
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['needs_team'] = not Team.objects.exists()
        return context


class PlayerUpdate(AdminRequiredMixin, SavedMessageMixin, UpdateView):
    model = Player
    form_class = PlayerForm
    template_name = 'league/object_form.html'
    success_url = reverse_lazy('player_list')
    extra_context = {'entity': 'jugador', 'list_url': 'player_list'}


class PlayerDelete(AdminRequiredMixin, DeletedMessageMixin, DeleteView):
    model = Player
    template_name = 'league/object_confirm_delete.html'
    success_url = reverse_lazy('player_list')
    extra_context = {'entity': 'jugador', 'list_url': 'player_list'}
