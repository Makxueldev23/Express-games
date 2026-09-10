from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Jogo, Categoria, Plataforma
from .forms import JogoForm


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Só membros da equipe (is_staff) podem cadastrar, editar ou excluir jogos.
    Clientes comuns continuam vendo e comprando normalmente."""

    def test_func(self):
        return self.request.user.is_staff


class JogoListView(ListView):
    model = Jogo
    template_name = 'jogos/jogo_lista.html'
    context_object_name = 'jogos'
    paginate_by = 12

    def get_queryset(self):
        qs = Jogo.objects.all().order_by('nome')
        termo = self.request.GET.get('q')
        categoria_id = self.request.GET.get('categoria')
        plataforma_id = self.request.GET.get('plataforma')

        if termo:
            qs = qs.filter(nome__icontains=termo)
        if categoria_id:
            qs = qs.filter(categorias__id=categoria_id)
        if plataforma_id:
            qs = qs.filter(plataformas__id=plataforma_id)

        return qs.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        context['plataformas'] = Plataforma.objects.all()
        return context


class JogoDetailView(DetailView):
    model = Jogo
    template_name = 'jogos/jogo_detalhe.html'
    context_object_name = 'jogo'


class JogoCreateView(StaffRequiredMixin, CreateView):
    model = Jogo
    form_class = JogoForm
    template_name = 'jogos/jogo_formulario.html'
    success_url = reverse_lazy('jogos:lista')

    def form_valid(self, form):
        messages.success(self.request, 'Jogo cadastrado com sucesso!')
        return super().form_valid(form)


class JogoUpdateView(StaffRequiredMixin, UpdateView):
    model = Jogo
    form_class = JogoForm
    template_name = 'jogos/jogo_formulario.html'
    success_url = reverse_lazy('jogos:lista')

    def form_valid(self, form):
        messages.success(self.request, 'Jogo atualizado com sucesso!')
        return super().form_valid(form)


class JogoDeleteView(StaffRequiredMixin, DeleteView):
    model = Jogo
    template_name = 'jogos/jogo_confirmar_exclusao.html'
    success_url = reverse_lazy('jogos:lista')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Jogo excluído com sucesso!')
        return super().delete(request, *args, **kwargs)