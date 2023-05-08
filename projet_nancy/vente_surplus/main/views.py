from django.shortcuts import render, get_object_or_404
from django.views import generic,View
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from .models import Produit, Box, Commande, LignePanier,ServiceDeLivraison,Professionnel


class ProfessionnelListView(generic.ListView):
    model = Professionnel

class ProfessionnelDetailView(generic.DetailView):
    model = Professionnel

class ProfessionnelCreateView(LoginRequiredMixin, generic.CreateView):
    model = Professionnel
    fields = ['nom', 'adresse', 'ville', 'pays', 'type', 'lieu']
    success_url = reverse_lazy('professionnels')

class ProfessionnelUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Professionnel
    fields = ['nom', 'adresse', 'ville', 'pays', 'type', 'lieu']
    success_url = reverse_lazy('professionnels')

class ProfessionnelDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Professionnel
    success_url = reverse_lazy('professionnels')


# class RestaurantListView(generic.ListView):
#     model = Restaurant
#
# class RestaurantDetailView(generic.DetailView):
#     model = Restaurant
#
# class RestaurantCreateView(LoginRequiredMixin, generic.CreateView):
#     model = Restaurant
#     fields = ['nom', 'adresse', 'ville', 'pays']
#     success_url = reverse_lazy('restaurants')
#
# class RestaurantUpdateView(LoginRequiredMixin, generic.UpdateView):
#     model = Restaurant
#     fields = ['nom', 'adresse', 'ville', 'pays']
#     success_url = reverse_lazy('restaurants')
#
# class RestaurantDeleteView(LoginRequiredMixin, generic.DeleteView):
#     model = Restaurant
#     success_url = reverse_lazy('restaurants')
#
# class SupermarcheListView(generic.ListView):
#     model = Supermarche
#
# class SupermarcheDetailView(generic.DetailView):
#     model = Supermarche
#
# class SupermarcheCreateView(LoginRequiredMixin, generic.CreateView):
#     model = Supermarche
#     fields = ['nom', 'adresse', 'ville', 'pays']
#     success_url = reverse_lazy('supermarches')
#
# class SupermarcheUpdateView(LoginRequiredMixin, generic.UpdateView):
#     model = Supermarche
#     fields = ['nom', 'adresse', 'ville', 'pays']
#     success_url = reverse_lazy('supermarches')
#
# class SupermarcheDeleteView(LoginRequiredMixin, generic.DeleteView):
#     model = Supermarche
#     success_url = reverse_lazy('supermarches')

class ServiceLivraisonListView(generic.ListView):
    model = ServiceDeLivraison

class ServiceLivraisonDetailView(generic.DetailView):
    model = ServiceDeLivraison

class ServiceLivraisonCreateView(LoginRequiredMixin, generic.CreateView):
    model = ServiceDeLivraison
    fields = ['nom', 'description']
    success_url = reverse_lazy('services-livraison')

class ServiceLivraisonUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = ServiceDeLivraison
    fields = ['nom', 'description']
    success_url = reverse_lazy('services-livraison')

class ServiceLivraisonDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = ServiceDeLivraison
    success_url = reverse_lazy('services-livraison')

class ProduitListView(generic.ListView):
    model = Produit

class ProduitDetailView(generic.DetailView):
    model = Produit

class BoxListView(generic.ListView):
    model = Box

class BoxDetailView(generic.DetailView):
    model = Box

class CommandeCreateView(LoginRequiredMixin, generic.CreateView):
    model = Commande
    fields = ['quantite', 'produit', 'service_livraison', 'supermarche','restaurant']
    success_url = reverse_lazy('commandes')

    def form_valid(self, form):
        form.instance.client = self.request.user
        form.instance.total = form.instance.calculer_total()
        form.instance.produit.quantite -= form.instance.quantite
        form.instance.produit.save()
        return super().form_valid(form)

class CommandeListView(LoginRequiredMixin, generic.ListView):
    model = Commande
    paginate_by = 20

    def get_queryset(self):
        return self.model.objects.filter(client=self.request.user)

class CommandeDetailView(LoginRequiredMixin, generic.DetailView):
    model = Commande

class CommandeCancelView(LoginRequiredMixin, generic.DeleteView):
    model = Commande
    success_url = reverse_lazy('commandes')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.annuler()
        return super().delete(request, *args, **kwargs)

class LignePanierCreateView(LoginRequiredMixin, generic.CreateView):
    model = LignePanier
    fields = ['quantite', 'produit', 'panier']
    success_url = reverse_lazy('panier')

    def form_valid(self, form):
        form.instance.panier, _ = Panier.objects.get_or_create(client=self.request.user)
        return super().form_valid(form)

class LignePanierUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = LignePanier
    fields = ['quantite']
    success_url = reverse_lazy('panier')

class LignePanierDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = LignePanier
    success_url = reverse_lazy('panier')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.produit.quantite += self.object.quantite
        self.object.produit.save()
        return super().delete(request, *args, **kwargs)

class PanierView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'panier.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        panier, _ = Panier.objects.get_or_create(client=self.request.user)
        context['lignes_panier'] = LignePanier.objects.filter(panier=panier)
        return context

class CheckoutView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'checkout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        panier, _ = Panier.objects.get_or_create(client=self.request.user)
        context['lignes_panier'] = LignePanier.objects.filter(panier=panier)
        context['total'] = sum([ligne.quantite * ligne.produit.prix for ligne in context['lignes_panier']])
        return context

class ConfirmationView(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request, *args, **kwargs):
        try:
            confirmation_code = kwargs['confirmation_code']
            confirmation = Confirmation.objects.get(code=confirmation_code)
            user = confirmation.user
            user.is_active = True
            user.save()
            confirmation.delete()
            messages.success(request, 'Your account has been confirmed!')
        except ObjectDoesNotExist:
            messages.error(request, 'Invalid confirmation code.')
        return redirect('home')
