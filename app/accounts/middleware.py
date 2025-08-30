from django.conf import settings
from django.utils import translation
from django.utils.deprecation import MiddlewareMixin


class UserLanguageMiddleware(MiddlewareMixin):
    """
    Middleware that sets the language for authenticated users based on their preference,
    or falls back to browser language detection for anonymous users.
    """
    
    def process_request(self, request):
        # First, let Django's LocaleMiddleware do its work (browser detection)
        # This sets the language based on cookies, session, or browser headers
        
        # If user is authenticated and has a language preference, use it
        if request.user.is_authenticated:
            try:
                profile = request.user.profile
                if profile.preferred_language:
                    language = profile.preferred_language
                    # Only activate if it's in our supported languages
                    if language in dict(settings.LANGUAGES).keys():
                        translation.activate(language)
                        request.LANGUAGE_CODE = language
            except:
                # If profile doesn't exist or any error, fall back to default behavior
                pass
        
        return None
