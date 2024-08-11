from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
#creation du model personnaliser

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length = 30, unique = True, null = True,)
    email = models.EmailField(unique = True)
    
    #identifiant unique de connexion
    USERNAME_FIELD = 'email'
    
    #nouveau champ d'inscription
    REQUIRED_FIELDS = ['username','phone_number']
    
    def __str__(self):
        return self.username
