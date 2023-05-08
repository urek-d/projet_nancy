"""vente_surplus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
 """
from django.contrib import admin
# from django.urls import path
#
# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]
from rest_framework_jwt.views import obtain_jwt_token
from django.urls import path,include
from main.views import ProduitListView, ProduitDetailView, BoxListView, BoxDetailView, CommandeCreateView, CommandeListView, CommandeDetailView, CommandeCancelView, LignePanierCreateView, LignePanierUpdateView, LignePanierDeleteView, PanierView, CheckoutView, ConfirmationView, ProfessionnelListView, ProfessionnelCreateView, ProfessionnelUpdateView, ProfessionnelDeleteView, ProfessionnelDetailView

urlpatterns = [
     path('admin/', admin.site.urls),
    path('api/', include(('core.routers', 'core'), namespace='core-api')),
     path('professionnels/', ProfessionnelListView.as_view(), name='professionnels_list'),
    path('professionnels/creer/', ProfessionnelCreateView.as_view(), name='professionnel_create'),
    path('professionnels/<int:pk>/', ProfessionnelDetailView.as_view(), name='professionnel_detail'),
    path('professionnels/<int:pk>/modifier/', ProfessionnelUpdateView.as_view(), name='professionnel_update'),
    path('professionnels/<int:pk>/supprimer/', ProfessionnelDeleteView.as_view(), name='professionnel_delete'),
    path('produits/', ProduitListView.as_view(), name='produits'),
    path('produits/<int:pk>/', ProduitDetailView.as_view(), name='produit-detail'),
    path('boxs/', BoxListView.as_view(), name='boxs'),
    path('boxs/<int:pk>/', BoxDetailView.as_view(), name='box-detail'),
    path('commandes/', CommandeListView.as_view(), name='commandes'),
    path('commandes/<int:pk>/', CommandeDetailView.as_view(), name='commande-detail'),
    path('commandes/creer/', CommandeCreateView.as_view(), name='commande-creer'),
    path('commandes/<int:pk>/annuler/', CommandeCancelView.as_view(), name='commande-annuler'),
    path('panier/', PanierView.as_view(), name='panier'),
    path('panier/ajouter/', LignePanierCreateView.as_view(), name='panier-ajouter'),
    path('panier/modifier/<int:pk>/', LignePanierUpdateView.as_view(), name='panier-modifier'),
    path('panier/supprimer/<int:pk>/', LignePanierDeleteView.as_view(), name='panier-supprimer'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('confirmation/<str:confirmation_code>/', ConfirmationView.as_view(), name='confirmation'),
]
