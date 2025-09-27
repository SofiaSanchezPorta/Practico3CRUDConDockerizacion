from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Oficina
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from django.shortcuts import redirect
from django.db.models.deletion import ProtectedError

# Create your views here.

class OficinaListView(ListView):
    model = Oficina
    template_name = "oficina/lista.html"
    context_object_name = "oficinas"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de oficinas'
        return context
    
class OficinaDetailView(DetailView):
    model = Oficina
    template_name = "oficina/detalle.html"
    context_object_name = "oficinas"
    PAGE_SIZE = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        oficina = self.object

        qs = oficina.personas.all().order_by("apellido")

        page_number = self.request.GET.get("page", 1)
        paginator = Paginator(qs, self.PAGE_SIZE)
        try:
            personas_page = paginator.page(page_number)
        except PageNotAnInteger:
            personas_page = paginator.page(1)
        except EmptyPage:
            personas_page = paginator.page(paginator.num_pages)

        context["personas"] = personas_page
        context["page_obj"] = personas_page
        context["paginator"] = paginator
        context["is_paginated"] = personas_page.has_other_pages()

        context["titulo"] = "Detalle de oficina"
        return context

class OficinaCreateView(LoginRequiredMixin, CreateView):
    model = Oficina
    template_name = "oficina/crear.html"
    fields = ['nombre', 'nombre_corto']
    success_url = reverse_lazy('oficina:lista')
    context_object_name = "oficina" 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear oficina'
        return context
    
class OficinaUpdateView(LoginRequiredMixin, UpdateView):
    model = Oficina
    template_name = "oficina/crear.html"
    fields = ['nombre','nombre_corto']
    success_url = reverse_lazy('oficina:lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar oficina'
        return context
    
class OficinaDeleteView(LoginRequiredMixin, DeleteView):
    model = Oficina
    template_name = "oficina/eliminar.html"
    context_object_name = "oficina"
    success_url = reverse_lazy('oficina:lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'eliminar'
        context['title'] = 'Eliminar oficina'
        return context
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            messages.success(request, "La oficina se eliminó correctamente.")
            return redirect(self.success_url)
        except ProtectedError:
            messages.error(
                request,
                "No se puede eliminar la oficina porque tiene personas asignadas."
            )
            return redirect(self.success_url)
        
    def form_valid(self, form):
            self.object = self.get_object()
            try:
                self.object.delete() 
            except ProtectedError:
                messages.error(
                    self.request,
                    "No se puede eliminar la oficina porque tiene personas asignadas.",
                    extra_tags="eliminar-oficina"
                )
                return redirect(self.success_url)
            else:
                messages.success(self.request, "La oficina se eliminó correctamente.")
                return redirect(self.success_url)
    
class OficinaSearchView(ListView):
    model = Oficina
    template_name = "oficina/buscar.html"
    context_object_name = "oficinas"

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query:
            return Oficina.objects.filter(
                Q(nombre__icontains=query) | Q(nombre_corto__icontains=query)
                )
        return Oficina.objects.none()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Búsqueda de oficinas'
        context['query'] = self.request.GET.get("q", "")

        return context