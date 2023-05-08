from django.contrib import admin

# Register your models here.
from django.contrib import admin
from main.models import Produit, Box, Commande, LignePanier,Professionnel,Lieu,Panier,ServiceDeLivraison,Administrateur,Client


admin.site.register(Produit)
admin.site.register(Box)
admin.site.register(Commande)
admin.site.register(LignePanier)
admin.site.register(Professionnel)
admin.site.register(Lieu)
# admin.site.register(Supermarche)
admin.site.register(Panier)
admin.site.register(ServiceDeLivraison)
admin.site.register(Administrateur)
admin.site.register(Client)
