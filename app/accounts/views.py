from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import translation
from django.http import HttpResponseRedirect
from django.conf import settings

from .forms import SignUpForm


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('tracker:dashboard')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})


def set_language(request):
    language = request.POST.get('language')
    if language and language in dict(settings.LANGUAGES).keys():
        translation.activate(language)
        response = HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language, max_age=settings.LANGUAGE_COOKIE_AGE)
        
        # Save language preference for logged-in users
        if request.user.is_authenticated:
            profile, created = request.user.profile, False
            if not hasattr(request.user, 'profile'):
                from .models import UserProfile
                profile = UserProfile.objects.create(user=request.user)
            profile.preferred_language = language
            profile.save()
        
        return response
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

