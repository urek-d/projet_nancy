from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'admin', AdminViewSet)
router.register(r'produits', views.ProduitViewSet)
router.register(r'boxs', views.BoxViewSet)
router.register(r'commandes', views.CommandeViewSet)
router.register(r'supermarches', views.SupermarcheViewSet)
router.register(r'restaurants', views.RestaurantViewSet)
router.register(r'paniers', views.PanierViewSet)
router.register(r'ligne-paniers', views.LignePanierViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
