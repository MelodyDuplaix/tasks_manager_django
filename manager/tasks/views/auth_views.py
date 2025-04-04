from django.contrib import messages  # type: ignore
from django.contrib.auth import login  # type: ignore
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail  # type: ignore
from django.shortcuts import render, redirect  # type: ignore
from django.urls import reverse_lazy

from tasks.forms import CustomUserCreationForm, PasswordResetForm  # type: ignore


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'registration/password_reset.html'
    email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject.txt'
    success_message = "Nous vous avons envoyé par e-mail des instructions pour définir votre mot de passe, " \
                      "si un compte existe avec l'email que vous avez saisi. Vous devriez les recevoir sous peu." \
                      " Si vous ne recevez pas d'e-mail, " \
                      "assurez-vous d'avoir saisi l'adresse avec laquelle vous vous êtes inscrit et vérifiez votre dossier spam."
    success_url = reverse_lazy('login')


def signup(request):
    """
    Display the signup page.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The rendered signup page.
    """

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Inscription reussie')
            return redirect('home')  # Redirige vers la page de connexion après l'inscription
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


def password_reset(request):
    """
    Display the password reset page.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The rendered password reset page.
    """
    # TODO: implémenter un message d'erreur si mot de passe non valide rentrée comme nouveau mot de passe
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            send_mail(
                "Réinitialisation de mot de passe",
                f"Pour réinitiliser votre mot de passe, veuillez accéder à cette page :",
                from_email="melo.surseine@gmail.com",
                fail_silently=False,
                recipient_list=[email],
            )
            messages.success(request, 'Un email vous a ete envoye')
            return redirect('login')
    else:
        form = PasswordResetForm()

    return render(request, 'registration/password_reset.html', {'form': form})

def profile(request):
    """
    Redirect to the home page.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The rendered home page.
    """
    return redirect('home')