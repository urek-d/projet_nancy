from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.models import AbstractUser
from django.contrib.gis.db import models as gis_models
from django.contrib.gis.db.models.functions import Distance
from django_extensions.db.models import TimeStampedModel
from django.contrib.gis.geos import Point

# class CustomUserManager(BaseUserManager):
#     def create_user(self, email, password=None, **extra_fields):
#         if not email:
#             raise ValueError('L\'adresse email est obligatoire.')
#         email = self.normalize_email(email)
#         # Création d'un utilisateur avec l'adresse email et le mot de passe fournis
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save()
#         return user
#
#     def create_superuser(self, email, password=None, **extra_fields):
#         # Création d'un super-utilisateur avec l'adresse email et le mot de passe fournis
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#
#         if extra_fields.get('is_staff') is not True:
#             raise ValueError('Le super-utilisateur doit avoir "is_staff=True".')
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError('Le super-utilisateur doit avoir "is_superuser=True".')
#
#         return self.create_user(email, password, **extra_fields)

class CustomUser(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField()
    mot_de_passe = models.CharField(max_length=100)
    adresse = models.CharField(max_length=255)
    ville = models.CharField(max_length=100)
    date_de_naissance = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # USERNAME_FIELD = 'email'
    # # Associe le CustomUserManager à notre modèle CustomUser
    # objects = CustomUserManager()

    def __str__(self):
        return self.nom

class Lieu(TimeStampedModel):
    nom = models.CharField(max_length=255,default="unkozn")
    # adresse = models.CharField(max_length=255)
    # ville = models.CharField(max_length=100)
    # code_postal = models.CharField(max_length=10)
    # telephone = models.CharField(max_length=20)
    # email = models.EmailField(null=True, blank=True)
    emplacement = gis_models.PointField(geography=True, default=Point(0.0, 0.0))

    def __str__(self):
        return self.nom


class Professionnel(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField(null=True)
    adresse = models.CharField(max_length=255, default='Unknown')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    class Type(models.TextChoices):
        RESTAURANT = 'restaurant'
        SUPERMARCHE = 'supermarché'
        AUTRE = 'autre'
    type = models.CharField(max_length=20, choices=Type.choices, default=Type.AUTRE)
    lieu = models.ForeignKey(Lieu, on_delete=models.CASCADE)

    @property
    def professionnel_type(self):
        if isinstance(self.lieu, Restaurant):
            return self.Type.RESTAURANT
        elif isinstance(self.lieu, Supermarche):
            return self.Type.SUPERMARCHE
        else:
            return self.Type.AUTRE
# class Restaurant(models.Model):
#     nom = models.CharField(max_length=100)
#     ville = models.CharField(max_length=100)
#     adresse = models.CharField(max_length=200)
#     telephone = models.CharField(max_length=20)
#     proprietaire = models.ForeignKey(User, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return f"{self.nom} ({self.ville})"
#
#
# class Supermarche(models.Model):
#     nom = models.CharField(max_length=100)
#     ville = models.CharField(max_length=100)
#     adresse = models.CharField(max_length=200)
#     telephone = models.CharField(max_length=20)
#     proprietaire = models.ForeignKey(User, on_delete=models.CASCADE






# Définition de notre modèle Box
class Box(models.Model):
    nom = models.CharField(max_length=255)
    description = models.TextField()
    prix = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return self.nom




class Produit(models.Model):
    nom = models.CharField(max_length=255)
    description = models.TextField()
    prix = models.DecimalField(max_digits=7, decimal_places=2)
    quantite = models.PositiveIntegerField()
    professionnel = models.ForeignKey(Professionnel, on_delete=models.CASCADE)

    def __str__(self):
        return self.nom

class Panier(models.Model):
    date_creation = models.DateTimeField(auto_now_add=True)
    client = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"Panier {self.id} de {self.client.email}"


# Définition de notre modèle LignePanier
class LignePanier(models.Model):
    quantite = models.PositiveIntegerField()
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    panier = models.ForeignKey(Panier, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.quantite}x {self.produit.nom} dans le panier {self.panier.id}"



class ServiceDeLivraison(models.Model):
    nom = models.CharField(max_length=100)
    adresse = models.CharField(max_length=255)
    frais_livraison = models.DecimalField(max_digits=6, decimal_places=2)
    # ville = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20)
    # email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return self.nom



class Commande(models.Model):
    date_commande = models.DateTimeField(auto_now_add=True)
    quantite = models.PositiveIntegerField()
    total = models.DecimalField(max_digits=7, decimal_places=2)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    client = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    boxes = models.ManyToManyField(Box)
    date_livraison = models.DateTimeField(null=True, blank=True)
    est_livre = models.BooleanField(default=False)
    service_livraison = models.ForeignKey(ServiceDeLivraison, on_delete=models.SET_NULL, null=True, blank=True)
    # supermarche = models.ForeignKey(Supermarche, on_delete=models.CASCADE, null=True)
    # restaurant  = models.ForeignKey( Restaurant, on_delete=models.CASCADE, null=True)
    professionnel = models.ForeignKey(Professionnel, on_delete=models.CASCADE, null=True)

    def calculer_total(self):
        return self.quantite * self.produit.prix

    def __str__(self):
        return f"{self.produit} commandé par {self.client} le {self.date_commande.strftime('%d/%m/%Y')}"

    def annuler(self):
        self.produit.quantite += self.quantite
        self.produit.save()
        self.delete()


class Administrateur(CustomUser):
    professionnels = models.ManyToManyField(Professionnel, related_name='administrateurs')



class Client(CustomUser):
    adresse_livraison =gis_models.PointField(geography=True, default=Point(0.0, 0.0))

    def passer_commande(self, produits):
        if len(produits) == 0 or len(produits) > 4:
            raise ValueError("Le nombre de produits commandé doit être compris entre 1 et 4.")

        commandes = []
        professionnels = set([p.professionnel for p in produits])
        for professionnel in professionnels:
            produits_professionnel = [p for p in produits if p.professionnel == professionnel]
            total_professionnel = sum([p.prix * p.quantite for p in produits_professionnel])

            if isinstance(professionnel, Restaurant):
                commande = CommandeRestaurant.objects.create(
                    produit=produits_professionnel[0],
                    client=self,
                    quantite=len(produits_professionnel),
                    total=total_professionnel
                )
            elif isinstance(professionnel, Supermarche):
                commande = CommandeSupermarche.objects.create(
                    produit=produits_professionnel[0],
                    client=self,
                    quantite=len(produits_professionnel),
                    total=total_professionnel
                )
            else:
                raise ValueError("Le professionnel doit être un restaurant ou un supermarché.")

            commandes.append(commande)

        return commandes



    def voir_restaurants_proches(self):
        restaurants = Professionnel.objects.filter(type=Professionnel.Type.RESTAURANT)
        supermarches = Professionnel.objects.filter(type=Professionnel.Type.SUPERMARCHÉ)
        point_client = Point.from_address(self.adresse_livraison)

# Retourne les restaurants les plus proches de la localisation actuelle du client

# Tri des restaurants et supermarchés par ordre de proximité
        restaurants_proches = restaurants.annotate(distance=Distance('emplacement', point_client)).order_by('distance')
        supermarches_proches = supermarches.annotate(distance=Distance('emplacement', point_client)).order_by('distance')

        return {'restaurants': restaurants_proches, 'supermarchés': supermarches_proches}

    def acceder_localisation_restaurant(self, restaurant):
        distance = Distance(km=2)
        restaurants_proches = Restaurant.objects.filter(emplacement__distance_lte=(restaurant.emplacement, distance)).exclude(id=restaurant.id)
        return restaurants_proches
# Retourne la localisation d'un restaurant


    def passer_commande_multiple(self, restaurants_produits_quantites):
        return commandes
# Permet de passer commande auprès de plusieurs restaurants.
# Le paramètre restaurants_produits_quantites est une liste de tuples (restaurant, produit, quantité)

        commandes = []
        for professionnel, produits_quantites in restaurants_produits_quantites.items():
            if isinstance(professionnel, Restaurant):
                total_produits = sum([p.prix * q for p, q in produits_quantites])
                commande = Commande.objects.create(produit=produits_quantites[0][0], client=self, quantite=len(produits_quantites), total=total_produits)
                commandes.append(commande)
            elif isinstance(professionnel, Supermarche):
                panier = Panier.objects.create(client=self)
                for produit, quantite in produits_quantites:
                    PanierItem.objects.create(panier=panier, produit=produit, quantite=quantite)
                    commande = Commande.objects.create(panier=panier, client=self, total=panier.total())
                    commandes.append(commande)
            else:
                raise ValueError("Le professionnel spécifié doit être soit un restaurant, soit un supermarché.")



    def retirer_soimeme(self):
        self.est_livre = True
        self.save()
# Le client peut retirer sa commande lui-même




    def se_faire_livrer_par_partenaire(self, service_livraison):
        if not self.adresse_livraison:
            raise ValueError("L'adresse de livraison doit être renseignée.")

        # Calculer le montant total de la commande, y compris les frais de livraison
        montant_total = self.calculer_montant_total() + service_livraison.frais_livraison

        # Créer une instance de la classe CommandeLivraison
        commande_livraison = CommandeLivraison.objects.create(
        client=self.client,
        restaurant=self.restaurant,
        produits=self.produits.all(),
        quantites=self.quantites.all(),
        frais_livraison=service_livraison.frais_livraison,
        montant_total=montant_total
        )

    # Envoyer la commande au service de livraison
        service_livraison.envoyer_commande(commande_livraison)

        return commande_livraison













