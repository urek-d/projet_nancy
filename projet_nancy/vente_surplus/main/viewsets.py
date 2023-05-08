from rest_framework import viewsets
from .models import Produit, Box, Commande, Panier, LignePanier,Professionnel
from .serializers import ProduitSerializer, BoxSerializer, CommandeSerializer,ProfessionnelSerializer, PanierSerializer, LignePanierSerializer, Administrateur


class AdminViewSet(viewsets.ModelViewSet):
    queryset =  Administrateur.objects.all()
    serializer_class = AdminSerializer

class ProduitViewSet(viewsets.ModelViewSet):
    queryset = Produit.objects.all()
    serializer_class = ProduitSerializer

class BoxViewSet(viewsets.ModelViewSet):
    queryset = Box.objects.all()
    serializer_class = BoxSerializer

class CommandeViewSet(viewsets.ModelViewSet):
    queryset = Commande.objects.all()
    serializer_class = CommandeSerializer

# class SupermarcheViewSet(viewsets.ModelViewSet):
#     queryset = Supermarche.objects.all()
#     serializer_class = SupermarcheSerializer
#
# class RestaurantViewSet(viewsets.ModelViewSet):
#     queryset = Restaurant.objects.all()
#     serializer_class = RestaurantSerializer
class ProfessionnelViewSet(viewsets.ModelViewSet):
    queryset = Professionnel.objects.all()

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return ProfessionnelDetailSerializer
        else:
            return ProfessionnelSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(type__in=[Professionnel.Type.RESTAURANT, Professionnel.Type.SUPERMARCHE])
        return queryset


class PanierViewSet(viewsets.ModelViewSet):
    queryset = Panier.objects.all()
    serializer_class = PanierSerializer

class LignePanierViewSet(viewsets.ModelViewSet):
    queryset = LignePanier.objects.all()
    serializer_class = LignePanierSerializer
