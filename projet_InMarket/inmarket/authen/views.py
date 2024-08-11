from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator, RegexValidator
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from .models import *
from django.contrib.auth.password_validation import validate_password

# Create your views here.

def index(request):
    return render(request, "authen/index.html")

def register_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        # Validation des mots de passe
        if password1 != password2:
            messages.info(request, 'Passwords do not match.')
            return redirect('register_user')
        
        if len(password1) < 5:
            messages.info(request, "password very short")
            return redirect("register_user")
         # Validation du mot de passe avec les règles de Django
        try:
            validate_password(password1)
        except ValidationError as e:
            messages.error(request, f'Erreur de mot de passe : {", ".join(e.messages)}')
            return redirect("register_user")
        
        # Validation du nom d'utilisateur
        if CustomUser.objects.filter(username=username).exists():
            messages.info(request, 'name already exists.')
            return redirect("register_user")
        
        # Validation de l'email
        try:
            EmailValidator()(email)
        except ValidationError:
            messages.error(request, 'Adresse e-mail invalide.')
            return redirect('register_user')
        
        if CustomUser.objects.filter(email=email).exists():
            messages.info(request, 'Email already exists.')
            return redirect('register_user')
        
        # Validation du numéro de téléphone
        phone_number_validator = RegexValidator(r'^\d{9}$', 'Le numéro de téléphone doit contenir exactement 9 chiffres.')
        try:
            phone_number_validator(phone_number)
        except ValidationError:
            messages.error(request, 'Numéro de téléphone invalide.')
            return redirect('register_user')
        
        if CustomUser.objects.filter(phone_number=phone_number).exists():
            messages.info(request, 'phone_number already exists.')
            return redirect('register_user')
        
        #creation de l'utilisateur
        
        user = CustomUser.objects.create_user(
            username = username,
            email = email,
            phone_number = phone_number,
            password = make_password(password1) # `make_password` pour hacher le mot de passe
        )
        user.is_active = False  # Désactive l'utilisateur jusqu'à activation
        user.save()

        messages.success(request, 'Votre compte a été créé avec succès. Veuillez vérifier votre e-mail pour activer votre compte.')
        return redirect("login_user")
    
    return render(request, "authen/inscription.html")
        

def login_user(request):
    if request.method == "POST":
        username_or_email_or_phone = request.POST['username_or_email_or_phone']
        password = request.POST['password']
        
        try:
            if '@' in username_or_email_or_phone:
                user = CustomUser.objects.get(email=username_or_email_or_phone)
            else:
                user = CustomUser.objects.get(phone_number=username_or_email_or_phone)
            
            # Authentifier l'utilisateur
            user = authenticate(username=user.email, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')  # Redirige vers la page d'accueil ou une autre page après connexion
            else:
                messages.error(request, "Identifiant ou mot de passe incorrect.")
                return redirect('login_user')
        
        except CustomUser.DoesNotExist:
            messages.error(request, "Aucun utilisateur trouvé avec ces informations.")
            return redirect('login_user')
        
    return render(request, "authen/connexion.html")

def logout_user(request):
    logout(request)
    messages.success(request, "deconnecter avec succes")
    return redirect("index")
