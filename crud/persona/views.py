from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Persona
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

class PersonaListView(ListView):
    model = Persona
    template_name = "persona/lista.html"
    context_object_name = "personas"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de personas'
        return context

class PersonaDetailView(DetailView):
    model = Persona
    template_name = "persona/detalle.html"
    context_object_name = "persona"
    paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Detalle persona'
        return context

class PersonaCreateView(LoginRequiredMixin, CreateView):
    model = Persona
    template_name = "persona/crear.html"
    fields = ['nombre', 'apellido', 'edad', 'oficina']
    success_url = reverse_lazy('persona:lista')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear persona'
        return context

class PersonaUpdateView(LoginRequiredMixin, UpdateView):
    model = Persona
    template_name = "persona/crear.html"
    fields = ['nombre', 'apellido', 'edad', 'oficina']
    success_url = reverse_lazy('persona:lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar persona'
        return context

class PersonaDeleteView(LoginRequiredMixin, DeleteView):
    model = Persona
    template_name = "persona/eliminar.html"
    context_object_name = "persona"    
    success_url = reverse_lazy('persona:lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'eliminar'
        context['title'] = 'Eliminar persona'
        return context

class PersonaSearchView(ListView):
    model = Persona
    template_name = "persona/buscar.html"
    context_object_name = "personas"

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query:
            return Persona.objects.filter(
                Q(nombre__icontains=query) | Q(apellido__icontains=query)
                )
        return Persona.objects.none()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Búsqueda de personas'
        context['query'] = self.request.GET.get("q", "")
    
        #print("Context data:", context)

        return context

def home(request):
    return redirect("persona:lista")
