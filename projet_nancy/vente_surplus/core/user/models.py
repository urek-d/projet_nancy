from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from main.models import Professionnel, Administrateur


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """
        Cree et retourne un utilisateur avec son mail et son mot de passe
        """
        if not email:
            raise ValueError('L\'adresse email doit être fournie')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_professional(self, email, password, **extra_fields):
        """
       Cree et retourne un utilisateur avec son mail et son mot de passe role=professional.
        """
        extra_fields.setdefault('role', 'professional')
        return self.create_user(email, password, **extra_fields)

    def create_administrator(self, email, password, **extra_fields):
        """
        Cree et retourne un utilisateur avec son mail et son mot de passe role=administrator.
        """
        extra_fields.setdefault('role', 'administrator')
        return self.create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """
        Cree et retourne un utilisateur avec son mail et son mot de passe role=administrator.
        """
        extra_fields.setdefault('role', 'administrator')
        # extra_fields.setdefault('is_staff', True)
        # extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'administrator')
        user = self.create_user(email, password, **extra_fields)
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def get_administrator(self):
        """
        retourne l utilisateur avec le  role=administrator, ou None if s il n existe pas.
        """
        try:
            return self.get(role='administrator')
        except self.model.DoesNotExist:
            return None


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=[('professional', 'Professional'), ('administrator', 'Administrator')], default='professional')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    # Ajout des relations avec les modèles Professionnel et Administrateur
    professionnel = models.ForeignKey(Professionnel, on_delete=models.CASCADE, null=True, blank=True)
    administrateur = models.ForeignKey(Administrateur, on_delete=models.CASCADE, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def is_professional(self):
        return self.role == 'professional'

    def is_administrator(self):
        return self.role == 'administrator'

    # @property
    # def is_superuser(self):
    #     return self.is_administrator()

    @property
    def is_staff(self):
        return self.is_administrator()
