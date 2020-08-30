from django.conf import settings as django_settings


def site_settings(request):
    """Expose specific settings to templates"""
    result = {}
    settings = [
        "BLOG_TITLE_MAX_LENGTH",
        "BLOG_UNIQUE_SLUG_MAX_LENGTH"
    ]
    for attr in settings:
        if (hasattr(django_settings, attr)):
            result[attr] = getattr(django_settings, attr)
    return {
        'settings': result,
    }
