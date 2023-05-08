from rest_framework import serializers
from .models import Produit, Box, Commande, Panier, LignePanier, Administrateur,Professionnel


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Administrateur
        fields = '__all__'

class ProduitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produit
        fields = '__all__'

class BoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Box
        fields = '__all__'

class CommandeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commande
        fields = '__all__'

# class SupermarcheSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Supermarche
#         fields = '__all__'
#
# class RestaurantSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Restaurant
#         fields = '__all__'
class ProfessionnelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professionnel
        fields = '__all__'

class PanierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Panier
        fields = '__all__'

class LignePanierSerializer(serializers.ModelSerializer):
    class Meta:
        model = LignePanier
        fields = '__all__'
